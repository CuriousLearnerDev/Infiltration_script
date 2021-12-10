import requests
import os

print("--------------------------------------------------")
print("+\t\t _____    ____     ____  \t\t+")
print("+\t\t|__  /   / ___|   / ___| \t\t+")
print("+\t\t  / /    \___ \   \___ \ \t\t+")
print("+\t\t / /_     ___) |   ___) |\t\t+")
print("+\t\t/____|___|____/___|____/ \t\t+")
print("+\t\t    |_____|  |_____|     \t\t")
print("")
print("\t*自己用的信息收集子域名探测工具")
print("---------------------------------------------------")
domain = input("请输入要探测的域名：")

headers = {  # 定义User-Agent请求头，用键值对的方式
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
try:
    # 判断文件是否存在
    if os.path.exists('dns.txt'):
        save = open('dns.txt','r')
    else:
        print("不存在dns.txt字典文件！")

    content = save.read()
    subdomains = content.splitlines()

    for i in subdomains:
        url = f'http://{i}.{domain}'
        try:
            requests.get(url,headers=headers)
        except requests.ConnectionError:
            pass
        else:
            print("发现了:",url)
except Exception as bc:
    print("出差了："+str(bc))