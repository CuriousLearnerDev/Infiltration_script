import requests
import urllib3
urllib3.disable_warnings()  # 忽略https证书告警
import json
import time
def awvs():
    http = "https://192.168.0.119:3443/api/v1/targets"
    Api_Key="1986ad8c0a5b3df4d7028d5f3c06e936cf2dbc5df8ab94feda5e55423fd6f4fdc"

    headers = {
        "X-Auth": Api_Key,
        "Content-type": "application/json;charset=utf8"
    }
    r = requests.get(url=http, headers=headers, verify=False)
    response=r.json()

    high=0 # 记录高危漏洞
    medium=0 # 记录中危漏洞
    low=0 # 记录低危漏洞
    info=0 # 信息性泄露漏洞
    for i in response['targets']: # 记录扫描漏洞
        high += i['severity_counts']['high']
        medium += i['severity_counts']['medium']
        low += i['severity_counts']['low']
        info += i['severity_counts']['info']


    print(f"高危漏洞：{high}个\n中危漏洞：{medium}个\n低危漏洞：{low}\n泄露漏洞：{info}")

    leak = f"""
---------------
高危漏洞：{high}个

中危漏洞：{medium}个

低危漏洞：{low}个

泄露漏洞：{info}个

"""
    push_dingding_group(leak)
    time.sleep(1300)  # 暂停10秒
def push_dingding_group(content):
    headers = {"Content-Type": "application/json"}
    # 消息类型和数据格式参照钉钉开发文档
    data = {"msgtype": "markdown", "markdown": {"title": "xray 发现了新漏洞"}}
    data['markdown']['text'] = content

    r = requests.post("https://oapi.dingtalk.com/robot/send?access_token=3afda4969edf03f8195ed8a93345c974b5d979dcd4f8f2294199bdba02c8ad41", data=json.dumps(data),
                      headers=headers)
    print(r.text)
if __name__ == '__main__':
    while True:
        awvs()