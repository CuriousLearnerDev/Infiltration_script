import nmap
import threading
import time
import queue



# 提取出来的结果保存起来
def Searchresults(results_IP):
    Searchresults_document = open("存活的主机.txt", 'a', encoding='utf-8')  # 打开文件写的方式
    Searchresults_document.write((results_IP+'\n'))  # 写入
    Searchresults_document.close()  # 关闭文件


def scan(IP_range):

    while not IP_range.empty():
        ip=IP_range.get()
        print(f"当前正在探测：{ip}")
        nm = nmap.PortScanner()
        nm.scan(hosts=ip,arguments = '-sP')

        hosts_list=[(x,nm[x]['status']['state']) for x in nm.all_hosts()]

        for host,status in hosts_list:

            print(f"{host}---{status}")

            Searchresults(host)

def cs(IP_range):
    print(IP_range)
    time.sleep(1)  # 暂停 1 秒

def Thread(IP_range):
    threadpool = []
    for _ in range(int(10)):
        Threads = threading.Thread(target=scan, args=(IP_range,))
        threadpool.append(Threads)
    for th in threadpool:
        th.start()
    for th in threadpool:
        threading.Thread.join(th)

if __name__ == '__main__':
    IP_192_range=['']
    IP_172_range=['']
    IP_10_2_range=['']
    IP_10_1_range=['']
    for i1 in range(77,256):
        #print(f"192.168.{i1}.0")

        IP_192_range.append(f"192.168.{i1}.1/24")
        #print(f"172.17.{i1}.0")
        IP_172_range.append(f"172.17.{i1}.1/24")
        #print(f"10.2.{i1}.0")
        IP_10_2_range.append(f"10.2.{i1}.1/24")
        #print(f"10.1.{i1}.0")
        IP_10_1_range.append(f"10.1.{i1}.1/24")
    ip = queue.Queue()
    for i in IP_10_2_range:
        ip.put(i)
    IP_range =ip
    Thread(IP_range)
    # for i2  in IP_range:
    #     scan(i)