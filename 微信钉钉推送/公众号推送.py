import requests
import json


class SendMessage():  # 定义发送消息的类
    def __init__(self):
        self.appID = ''  # appid 注册时有
        self.appsecret = ''  # appsecret 同上
        self.template_id = ''  # 模板id
        self.access_token = self.get_access_token()  # 获取 access token
        self.opend_ids = self.get_openid()  # 获取关注用户的openid

    def get_access_token(self):
        """
        获取access_token
        通过查阅微信公众号的开发说明就清晰明了了
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'. \
            format(self.appID, self.appsecret)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        return access_token

    def get_openid(self):
        """
        获取所有用户的openid
        微信公众号开发文档中可以查阅获取openid的方法
        """
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (
        self.access_token, next_openid)
        ans = requests.get(url_openid)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    def sendmsg(self):
        """
        给所有用户发送消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=o8ayp6L5TMlPo-hv3DElQT81JZo4".format(self.access_token)

        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                    "touser": open_id,
                    "template_id": self.template_id,
                    "url": "https://www.baidu.com/",
                    "topcolor": "#FF0000",
                    # 对应模板中的数据模板
                    "data": {
                        "frist": {
                            "value": self.dataJson.get("frist"),
                            "color": "#FF99CC"  # 文字颜色
                        },
                        "body": {
                            "value": self.dataJson.get("body"),
                            "color": "#EA0000"
                        },
                        "weather": {
                            "value": self.dataJson.get("weather"),
                            "color": "#00EC00"
                        },
                        "date": {
                            "value": self.dataJson.get("date"),
                            "color": "#6F00D2"
                        },
                        "last": {
                            "value": self.dataJson.get("last"),
                            "color": "#66CCFF"
                        }
                    }
                }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))  # 将数据编码json并转换为bytes型
                response = requests.post(url, data=data)
                result = response.json()  # 将返回信息json解码
                print(result)  # 根据response查看是否广播成功
        else:
            print("当前没有用户关注该公众号！")
if __name__ == "__main__":
    sends = SendMessage()
    sends.sendmsg()
