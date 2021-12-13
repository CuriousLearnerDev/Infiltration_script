import  requests
import time
from lxml import etree
import  re

#添加请求头
def headers_():
    headers = {  # 定义User-Agent请求头，用键值对的方式
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",

    }
    return headers

def verify(proxies):
    headers = headers_()
    print(proxies['http'])
    try:
        html = requests.get('http://httpbin.org/get', proxies=proxies,timeout=2)

        print(html)
        # html = etree.HTML(html.text)
        #
        # IP = html.xpath(r'//th/div[@id="tab0_ip"]/text()')  # 提取ip
        # address=html.xpath(r'//th/div[@id="tab0_address"]/text()')  # 地址
        # print("可以用的：IP"+IP+"地址:"+address)
        IP=re.findall(r'\d+\.\d+\.\d+\.\d+', html.text)[0]
        print("这个IP可以用:"+IP)
    except Exception:
        print("这个代理不可用")
# 判断代理方式
def judge(ip,PORT,protocol):
    print("正在验证")
    if protocol=='HTTP':
        proxies = {"http": ('http://'+ip+':'+PORT)}
        verify(proxies)
    elif protocol=='SOCKS5':
        proxies = {"http": ('socks5://'+ip+':'+protocol)}
        verify(proxies)

# 提取代理服务器地址和端口地方
def collection(url,speed):
    headers = headers_()

    html=requests.get(url,headers=headers)
    html = etree.HTML(html.text)

    IP = html.xpath(r'//tr/td[@data-title="IP"]/text()')  # 提取ip
    PORT = html.xpath(r'//tr/td[@data-title="PORT"]/text()')  # 提取端口
    anonymous = html.xpath(r'//tr/td[@data-title="匿名度"]/text()')  # 提取匿名程度
    protocol = html.xpath(r'//tr/td[@data-title="类型"]/text()')  # 提取协议
    Location = html.xpath(r'//tr/td[@data-title="位置"]/text()')  # 提取协议
    for i in range(len(IP)):
        time.sleep(speed)
        print("ip地址是："+IP[i]+"|端口是"+str(PORT[i])+"\n匿名程度："+anonymous[i]+"|用的协议"+str(protocol[i])+"|位置在:"+Location[i])
        judge(IP[i],str(PORT[i]),protocol[i])



if __name__ == '__main__':
    print('''
     ___ ____          _ _           _   _             
    |_ _|  _ \    ___ | | | ___  ___| |_(_) ___  _ __  
     | || |_) |  / _ \| | |/ _ \/ __| __| |/ _ \| '_ \ 
     | ||  __/  | (_) | | |  __/ (__| |_| | (_) | | | |
    |___|_|      \___/|_|_|\___|\___|\__|_|\___/|_| |_|
    
                                                * 博客地址：www.zssnp.top
                                                * 作者：赵赛赛
    ''')
    speed=int(input("请输入采集速度："))

    url='https://www.kuaidaili.com/free/'
    collection(url,speed)
