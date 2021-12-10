import  requests
from lxml import etree
import base64
import time



# 如果搜索结果多执行
def Multiple(Judge_page,coding,headers,Cookie,speed):
    print("搜索结果有" + Judge_page + "页")
    for all in range(1,int(Judge_page)):
        time.sleep(speed)
        print("现在提取是第"+str(all)+"页")
        html = requests.get('https://fofa.so/result?qbase64=' + coding+"&page="+str(all), headers=headers,cookies=Cookie)
        html = etree.HTML(html.text)
        divs = html.xpath(r'//span/a/@href')  # 语法
        for i in divs:
            print(i)


def interface():##界面
    print("---------------------------------------------------")
    print("\t _________ ____     __        __        \t\t")
    print("\t|__  / ___/ ___|   / _| ___  / _| __ _  \t\t")
    print("\t  / /\___ \___ \  | |_ / _ \| |_ / _` | \t\t")
    print("\t / /_ ___) |__) | |  _| (_) |  _| (_| | \t\t")
    print("\t/____|____/____/  |_|  \___/|_|  \__,_| \t\t\n\n")
    print("*fofa信息收集探测工具")
    print("*扫描速度快对方可能会屏蔽IP的")
    print("---------------------------------------------------")  

interface()##界面

Cookie=input("Fofa登录后的值Cookie的fofa_token值：")
speed=int(input("请输入扫描速度："))
#base64编码
z=input("请输入要搜索的关键字：")
coding=base64.b64encode(z.encode('utf-8')).decode("utf-8")


Cookie= {'fofa_token': Cookie}
headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

print("你输入的是"+z)
html=requests.get("https://fofa.so/result?qbase64="+str(coding),headers)
html=etree.HTML(html.text)
try:

    Judge_page=divs=html.xpath(r'//ul[@class="el-pager"]/li[last()]/text()')  # 查看是否有页数


    if Judge_page: # 如果搜索结果多进行循环一个一个页面的读取
        Multiple(Judge_page[0],coding,headers,Cookie,speed)
    else:
        print("搜索结果就一页！")
        divs = html.xpath(r'//span[@class="aSpan"]//@href')  # 探测IP
        service = html.xpath(r'//p[@class="listSpanCont"]/a/text()')  # 用的服务器软件


        order=0
        for i in divs:
            print("服务器IP地址是" + str(i)+"服务器软件"+service[order])
            order += 1

except Exception as bc:

    print("出差了："+str(bc))
