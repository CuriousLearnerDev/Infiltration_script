import requests
import urllib3
urllib3.disable_warnings()  # 忽略https证书告警
import json
import time


# host = "https://192.168.0.119:3443/api/v1/scans?l=2"
# Api_Key="1986ad8c0a5b3df4d7028d5f3c06e936cf2dbc5df8ab94feda5e55423fd6f4fdc"
#
# headers = {
#     "X-Auth": Api_Key,
#     "Content-type": "application/json;charset=utf8"
# }
#
#
# response = requests.get(url=host, headers=headers, verify=False)
# response = response.json()
# processing=0
# failed=0
# completed=0
# print(response)
# for i in response['scans']:
#     print(i['current_session']['status'])
#     if i['current_session']['status']=="processing":
#         processing+=1
#     elif i['current_session']['status'] == "failed":
#         failed+=1
#     elif i['current_session']['status'] == "completed":
#         completed+= 1
# print(f"在扫描中：{processing}个")
# print(f"一共扫描失败：{failed}个")
# print(f"一共扫描成功：{completed}个")
#

# http = "https://192.168.0.119:3443/api/v1/targets/372550b5-fa3b-4a2e-b44e-3c97839db26b/configuration"
# Api_Key="1986ad8c0a5b3df4d7028d5f3c06e936cf2dbc5df8ab94feda5e55423fd6f4fdc"
# headers = {"X-Auth": Api_Key,
#            "Content-type": "application/json;charset=utf8"}
# datas = json.dumps({"proxy":{"enabled":True,"protocol":"http","address":"192.168.0.174","port":8080}})
# response = requests.patch(url=http, headers=headers, data=datas, verify=False)

# print(response)



class awvs():

    # 钉钉推送
    def push_dingding_group(self,content):
        headers = {"Content-Type": "application/json"}
        # 消息类型和数据格式参照钉钉开发文档
        data = {"msgtype": "markdown", "markdown": {"title": "awvs 添加新的扫描"}}
        data['markdown']['text'] = content

        r = requests.post(
            "https://oapi.dingtalk.com/robot/send?access_token=3afda4969edf03f8195ed8a93345c974b5d979dcd4f8f2294199bdba02c8ad41",
            data=json.dumps(data),
            headers=headers)
        #print(r.text)

    # 设置代理
    def AWVS_Broker(self,target_id,Broker_Host,Broker_Port):
        Broker_url_api=self.host + f"/api/v1/targets/{target_id}/configuration"
        datas = json.dumps({"proxy": {"enabled": True, "protocol": "http", "address": Broker_Host, "port": int(Broker_Port)}})
        response = requests.patch(url=Broker_url_api, headers=self.headers, data=datas, verify=False)
        if str(response) == "<Response [204]>":
            return "- 设置代理成功！"
        else:
            return "- 设置代理失败！"


    # 设置扫描速度
    def AWVS_Velocity(self,target_id):
        speed_url_api = self.host + f'/api/v1/targets/{target_id}/configuration'
        datas = json.dumps({"scan_speed": "moderate"}) # slow(慢)、moderate(中)、fasts(快)
        response = requests.patch(url=speed_url_api, headers=self.headers, data=datas, verify=False)
        #print(target_id)
        if str(response) == "<Response [204]>":
            return "- 扫描速度设置成功！"
        else:
            return "- 扫描速度设置失败！"



    # # 获取目标的target_id
    # def AWVS_targets(self):
    #     r = requests.get(url=self.host+"/api/v1/targets", headers=self.headers, verify=False)
    #     target_id = r.json()
    #     for i in target_id["targets"]:
    #         self.AWVS_Velocity(i.get("target_id"))

    # 添加扫描目标
    def AWVS_New(self):
        datas = json.dumps({'address': self.targeted,  # address：需要扫描的url；以http或https开头
                            'description': '扫描备注',  # description：扫描备注
                            'criticality': '10'})  # criticality：危险程度;范围:[30,20,10,0];默认为10

        response = requests.post(url=self.host+"/api/v1/targets", headers=self.headers, data=datas, verify=False)

        ifresponse = response
        response = response.json()
        if str(ifresponse)=="<Response [201]>":
            print(self.targeted+"：添加目标成功!")
            print(response["target_id"])
            return response["target_id"]  # 返回添加目标的target_id
        else:
            print(self.targeted+"添加目标失败!")

    # 启动扫描
    def AWVS_scans(self,target_id):

        datas = json.dumps(
            {'profile_id': '11111111-1111-1111-1111-111111111111',  # 扫描类型
             'schedule': {'disable': False,  # 扫描时间设置 (默认即时)
                          'start_date': None,
                          'time_sensitive': False},
             'target_id': target_id}
        )
        response = requests.post(url=self.host+"/api/v1/scans", headers=self.headers, data=datas, verify=False)
        if str(response)=="<Response [201]>":
            return  "- 扫描启动成功！"
        else:
            return  "- 扫描启动失败！"

    # 记录扫描漏洞
    def leak(self):
        r = requests.get(url=self.host+"/api/v1/targets", headers=self.headers, verify=False)
        response = r.json()
        high = 0  # 记录高危漏洞
        medium = 0  # 记录中危漏洞
        low = 0  # 记录低危漏洞
        info = 0  # 信息性泄露漏洞
        for i in response['targets']:  # 记录扫描漏洞
            try:
                high += i['severity_counts']['high']
            except :
                high +=0
            try:
                medium += i['severity_counts']['medium']
            except:
                medium +=0
            try:
                low += i['severity_counts']['low']
            except:
                low +=0
            try:
                info += i['severity_counts']['info']
            except:
                info += 0

        leak = f"""
---------------
高危漏洞：{high}个

中危漏洞：{medium}个

低危漏洞：{low}个

泄露漏洞：{info}个"""
        return leak
    # 扫描状态
    def Scan_status(self):
        r = requests.get(url=self.host+"/api/v1/targets", headers=self.headers, verify=False)
        response = r.json()
        Scan_the_target = []  # 记录扫描目标
        processing = 0  # 记录在扫描中
        failed = 0  # 记录扫描失败的
        completed = 0  # 记录扫描成功
        #print(response['targets'])
        for i in response['targets']:
            Scan_the_target.append(i['address'])
            if i['last_scan_session_status'] == "processing":
                processing += 1
            elif i['last_scan_session_status'] == "failed":
                failed += 1
            elif i['last_scan_session_status'] == "completed":
                completed += 1
        scan=f"""
---------------
在扫描中：{processing}个

一共扫描失败：{failed}个

一共扫描成功：{completed}个"""

        status={"Scanstatus":scan,
                "processing":processing}
        return  status # 扫描状态和在扫描中的

    def main(self,host,Api_Key,targeted,remark,Broker_Host,Broker_Port):
        self.host=host # awvs地址
        self.remark=remark # 扫描备注
        self.targeted=targeted # 扫描目标
        self.Api_Key=Api_Key # awvs的api
        self.headers = {"X-Auth": Api_Key,"Content-type": "application/json;charset=utf8"}
        #self.AWVS_New()

        status=self.Scan_status() # 返回扫描状态和在扫描中的

        target_id = self.AWVS_New()  # 添加扫描目标 返回添加目标的target_id

        leak=self.leak()  # 扫描漏洞信息
        Velocity=self.AWVS_Velocity(target_id)  # 设置扫描速度  返回成功失败
        Broker=self.AWVS_Broker(target_id,Broker_Host,Broker_Port)  # 设置扫描速度  返回成功失败
        scans=self.AWVS_scans(target_id)  # 启动扫描 返回成功失败
        print(scans)
        print(Broker)
        print(Velocity)
        status = self.Scan_status()  # 10秒查看描状态和在扫描中的
        Scanstatus = status['Scanstatus']  # 扫描状态信息
        dingtalk = f"""
AWVS 扫描：

--------------

- 添加目标：{targeted}

{Velocity}

{Broker}

{scans}

{Scanstatus}

{leak}"""
        print(dingtalk)
        self.push_dingding_group(dingtalk)
        time.sleep(500)  # 暂停10秒

if __name__ == '__main__':
    host = "https://192.168.5.241:3443" # awvs地址
    Api_Key="1986ad8c0a5b3df4d7028d5f3c06e936c1c858707f5714c26ad168cc818063c1c" # api
    remark="测试" # 备注
    Broker_Host="127.0.0.1" # 代理
    Broker_Port=1081 # 代理
    awvs=awvs()
    for targeted  in open("url.txt"):
        print(targeted)
        targeted=targeted.strip()
        awvs.main(host,Api_Key,targeted,remark,Broker_Host,Broker_Port)