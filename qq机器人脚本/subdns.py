# -- coding:UTF-8 --
from lxml import etree
from urllib.parse import urlparse  # urlparse提取url的dns
import requests
from bs4 import BeautifulSoup
import urllib3
import re
import base64
from urllib.parse import quote

urllib3.disable_warnings()  # 忽略https证书告警

def Bing_DNS_Interface(DNS): #使用bing进行探测
    keywords = "site:" + DNS
    # keywords = keywords.replace(' ', '+') # 空格用+来代替
    # keywords=quote(keywords, 'utf-8') # 进行url编码
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }
    print(keywords)
    amount = 3  # 默认页数
    Dns_List = []
    for i in range(0, int(amount)):
        url = f"https://cn.bing.com/search?q={keywords}&PC=U316&first={i}0&FORM=PERE"
        try:
            html = requests.get(url=url, headers=headers, verify=False, timeout=5)
            # //div[@id="search"]//div//div//div//div//div//div/a[@data-ved]/@href
            html = etree.HTML(html.text)
            divs = html.xpath(r'//div/h2/a/@href')  # 语法

            # print(divs2)
            for i in divs:
                if DNS in i:
                    DNS_Res = urlparse(i).netloc  # 获得url里面的域名
                    if not (DNS_Res in Dns_List):  # 取反如果Dns_List列表里面有就不添加
                        Dns_List.append(DNS_Res)
        except Exception as bc:
            print("有错误！错误提示" + str(bc))

    return Dns_List
def Climb_Google(DNS):

    keywords = "site:" + DNS
    # keywords = keywords.replace(' ', '+') # 空格用+来代替
    # keywords=quote(keywords, 'utf-8') # 进行url编码

    Headers = {
        'Host': 'www.google.com.hk',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.google.com.hk',
        'sec-ch-ua-platform': "Linux",
        'sec-ch-ua-arch': "x86",
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'empty',
    }
    Dns_List = []

    for i in range(0, 3): # 探测3页
        url = f"https://www.google.com.hk/search?q={keywords}&hl=zh-CN&start={str(i)}0"
        print(url)
        try:
            html = requests.get(url=url, headers=Headers, verify=False)
            html = etree.HTML(html.text)
            divs = html.xpath('//div[@id="search"]//div//div//div//div//div//div/a[@data-ved]/@href')  # 语法
            for DNS in divs:
                DNS_Res = urlparse(DNS).netloc  # 获得url里面的域名
                if not (DNS_Res in Dns_List):  # 取反如果Dns_List列表里面有就不添加
                    Dns_List.append(DNS_Res)

        except IndexError:
            print("Google出现问题")
    return Dns_List

def Censys_DNS_Climb_censys(DNS): # 证书探测Censys

    try:
        amount = 4  # 默认页数

        Dns_List = []
        headers={
            'Host': 'search.censys.io',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'close',
            'Referer': 'https://search.censys.io',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        for i in range(int(amount)):
            url=f"https://search.censys.io/certificates/_search?q={DNS}&page={i}"
            html=requests.get(url=url,headers=headers,verify=False)
            soup = BeautifulSoup(html.text, 'lxml')
            dns_ = soup.find_all(text=re.compile(rf"{DNS}"))
            for i in dns_: # 临时发挥写的现在我也懵看不太懂
                a=re.sub('\*=', '', i)
                a=a.split(',')[0]
                a = a.split('=')
                if len(a)==2:
                    if not (a in Dns_List):  # 取反如果Dns_List列表里面有就不添加
                        Dns_List.append(a[1])

        #Dns_List=numpy.unique(Dns_List)
        return Dns_List

    except Exception as bc:
        print("有错误！错误提示" + str(bc))


def Crt_DNS_Climb_Crt(DNS): #Crt证书探测

    headers = {
        'Host': 'crt.sh',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    try:
        Dns_List=[]
        html = requests.get(f"https://crt.sh/?q={DNS}",headers=headers,verify=False)
        soup = BeautifulSoup(html.text, 'lxml')
        dns_=soup.find_all(text=re.compile(fr".{DNS}"))

        for i in range(2,len(dns_)):
            if not (dns_[i] in Dns_List):  # 取反如果Dns_List列表里面有就不添加
                Dns_List.append(dns_[i])
        #print(Dns_List)
        return Dns_List
    except Exception as bc:
        print("有错误！错误提示" + str(bc))


# 目前用不了
def Fofa_Dns_Request(DNS):
    try:
        DNS = f'domain="{DNS}"'
        DNS = base64.b64encode(DNS.encode('utf-8')).decode("utf-8")


        Dns_List = []
        headers = {
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }
        # 请求
        html=requests.get("https://fofa.info/result?qbase64="+str(DNS),headers=headers)
        html = etree.HTML(html.text)
        divs = html.xpath(r'//span[@class="aSpan"]//@href')  # 探测IP


        for DNS in divs:
            DNS_Res = urlparse(DNS).netloc  # 获得url里面的域名
            if not (DNS_Res in Dns_List):  # 取反如果Dns_List列表里面有就不添加
                Dns_List.append(DNS_Res)
        return Dns_List

    except Exception as bc:
        print("有错误！错误提示" + str(bc))


from nonebot import on_command

from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

ND = on_command("子域名查询", priority=2)


@ND.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("Name", args)  # 如果用户发送了参数则直接赋值


@ND.got("Name", prompt="用法：子域名查询 域名")
async def handle_city(Name: Message = Arg(), sname: str = ArgPlainText("Name")):

    try:
        Dns_List = []  # 统计
#---------------bing探测------------------------------
        await ND.send("正在用搜索引擎进行探测DNS")
        Bing = Bing_DNS_Interface(sname)
        Dns_List+=Bing # 统计
        for i in Bing:
            print('bing输出：'+i)
            await ND.send(i)
#------------------------------------------------------

# ---------------Google探测------------------------------
        Google = Climb_Google(sname)
        diff_list = list(set(Google) - set(Dns_List))  # 用于检查没有出来的域名进行输出
        for i in diff_list:
            print('Google输出：' + i)
            await ND.send(i)
        Dns_List += Google  # 统计
# ------------------------------------------------------


# ---------------Censys探测------------------------------
        await ND.send("正在用证书进行探测DNS")
        censys=Censys_DNS_Climb_censys(sname)
        diff_list = list(set(censys) - set(Dns_List)) # 用于检查没有出来的域名进行输出
        for i in diff_list:
            print('Censys输出：'+i)
            await ND.send(i)
        Dns_List += censys # 统计
# ------------------------------------------------------

# ---------------crt探测------------------------------
        crt = Crt_DNS_Climb_Crt(sname) # crt证书探测
        diff_list = list(set(crt) - set(Dns_List)) # 用于检查没有出来的域名进行输出
        for i in diff_list:
            print('crt输出：'+i)
            await ND.send(i)
        Dns_List += censys # 统计
# ------------------------------------------------------

    except Exception as e:
        await ND.send("出现问题请联系赛赛")