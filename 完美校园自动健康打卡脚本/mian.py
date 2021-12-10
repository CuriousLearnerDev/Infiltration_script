import uiautomator2 as u2
import time
import random


d = u2.connect('192.168.0.102:5555')  #需要adb打开手机的端口


print(d.info) # check connection
print("远程连接手机成功")
def ydk():
    d.click(0.547, 0.684)
    print("正在打字")
    d.click(0.515, 0.961)
    d.click(0.547, 0.684)
    d.click(0.291, 0.758)
    d.click(0.786, 0.762)
    d.click(0.103, 0.633)
    print("打字完成")
    time.sleep(2)
    print("发信息")
    d.click(0.899, 0.533)

    print("发送成功")
    print("正在关闭屏幕")
    d.screen_off()
    print("成功关闭屏幕")

def douyin():

    #
    time.sleep(2)
    d.screen_on()# 打开屏幕
    d.swipe(313,1370,313,110)
    print("准备打开屏幕")
    time.sleep(2)
    print("正在手机解锁")
    d.click(0.504, 0.511)

    d.click(0.498, 0.754)

    d.click(0.498, 0.754)
    d.click(0.504, 0.511)
    d.click(0.227, 0.521)

    d.click(0.504, 0.511)
    d.click(0.775, 0.51)

    d.click(0.498, 0.754)
    time.sleep(2)
    print("准备完美校园")
    d(text="完美校园").click()
    d.click(0.372, 0.328)
    time.sleep(2)
    time.sleep(2)
    print("正在屏幕滑动")
    d.swipe(313,1370,313,110)

    print("正在屏幕滑动")
    d.swipe(313,1370,313,110)

    print("正在屏幕滑动")
    d.swipe(313,1370,313,110)
    print("正在屏幕滑动")
    d.swipe(313,1370,313,110)

    print("正在屏幕滑动")
    d.swipe(313,1370,313,110)
    print("正在屏幕滑动")
    d.swipe(313, 1370, 313, 110)
    print("正在屏幕滑动")
    d.swipe(313, 1370, 313, 110)
    print("点击提交")
    d.click(0.478, 0.931)

    print("确定提交")
    d.click(0.708, 0.777)

    print("返回主页")
    d.press("home")

    print("找寻QQ")
    d.click(0.449, 0.787)
    print("打开QQ")
    d(text="QQ").click()
    time.sleep(5)
    print("找寻打卡群")
    d.click(0.394, 0.34)
    ydk()

if __name__=='__main__':
    douyin()