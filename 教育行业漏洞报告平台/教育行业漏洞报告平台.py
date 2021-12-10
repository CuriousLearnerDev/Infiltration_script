import  requests
from lxml import etree
import base64
import time

print("--------------------------------------------------")
print("+\t\t _____    ____     ____  \t\t+")
print("+\t\t|__  /   / ___|   / ___| \t\t+")
print("+\t\t  / /    \___ \   \___ \ \t\t+")
print("+\t\t / /_     ___) |   ___) |\t\t+")
print("+\t\t/____|___|____/___|____/ \t\t+")
print("+\t\t    |_____|  |_____|     \t\t")
print("")
print("\t*在教育行业漏洞报告平台提取名在搜索引擎提取相关URL")
print("\t*AWVS进行自动化漏洞扫描")
print("\t*提取出来的会保存当前目录下的学校名.txt")
print("---------------------------------------------------")



headers = {  # 定义User-Agent请求头，用键值对的方式
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",

        }


save=open("学校.txt","w")

url = "https://src.sjtu.edu.cn/rank/firm/?page="
try:
    for i in range(1,197):


        html = requests.get(url+str(i), headers=headers)

        html=etree.HTML(html.text)

        divs=html.xpath(r'//td/a/text()') # 语法


        for address_save in divs:
            print("正在提取："+address_save)
            print("只提取就一页：提取会等待4秒进行发送请求以防被屏蔽IP")
            time.sleep(4)
            coding = base64.b64encode(address_save.encode('utf-8')).decode("utf-8")
            html = requests.get("https://fofa.so/result?qbase64=" + str(coding), headers)
            html = etree.HTML(html.text)
            divs = html.xpath(r'//span/a/@href')  # 语法
            for i in divs:
                print("可能的地址"+i)

            save.write(address_save +"可能的地址"+str(divs)+"\n")
    save.close()

except Exception as bc:
    print("出差了："+str(bc))