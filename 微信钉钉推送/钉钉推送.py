from flask import Flask, request
import requests
import datetime
import logging
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def xray_webhook():
    vuln = request.json
    #print(vuln)
    content = f"""
    xray 发现了新漏洞
    ---------------
    插件: {vuln['data']["plugin"]}
    漏洞类型: {vuln["type"]}
    漏洞地址: {vuln['data']["target"]["url"]}
    发现时间: {str(datetime.datetime.fromtimestamp(vuln["data"]["create_time"] / 1000))}
    ---------------
    请及时查看和处理
    """

    try:
        push_dingding_group(content)
    except Exception as e:
        logging.exception(e)
    print(content)
    return 'ok'


def push_dingding_group(content):
    headers = {"Content-Type": "application/json"}
    # 消息类型和数据格式参照钉钉开发文档
    data = {"msgtype": "markdown", "markdown": {"title": "xray 发现了新漏洞"}}
    data['markdown']['text'] = content


    # 钉钉api
    r = requests.post("xx", data=json.dumps(data),
                      headers=headers)
    print(r.text)

if __name__ == '__main__':
    app.run()