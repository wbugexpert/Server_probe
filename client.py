#! /bin/python3
import os
import sys
print(__file__)
def check():
    try:
        import psutil
    except:
        os.system('pip install psutil')
        os.execv(__file__, sys.argv)
    try:
        import socket
    except:
        os.system('pip install socket')
        os.execv(__file__, sys.argv)
    try:
        import re
    except:
        os.system('pip install re')
        os.execv(__file__, sys.argv)
    try:
        import time
    except:
        os.system('pip install time')
        os.execv(__file__, sys.argv)
    try:
        import json
    except:
        os.system('pip install json')
        os.execv(__file__, sys.argv)

check()
import json
import psutil
import socket
import re
import time


server_address=""
pwd=""
server_port=""
def get_opt():
    try:
        global server_address,pwd,server_port
        for i in range(1,len(sys.argv)):
            if sys.argv[i].find("-a=",0,3)!=-1:
                server_address=sys.argv[i][3:len(sys.argv[i])]
            elif sys.argv[i].find("-p=",0,3)!=-1:
                pwd=sys.argv[i][3:len(sys.argv[i])]
            elif sys.argv[i].find("-m=",0,3)!=-1:
                server_port=sys.argv[i][3:len(sys.argv[i])]
    finally:
        if server_port=="":
            server_port="8000"
        if server_address == "" or pwd == "":
            print(sys.argv[0]+" -p=<password> -a=<sever_address> -m=<server_port(=8000)>")
            print("Please note that there is no space between the equal sign and the parameter")
            sys.exit()


def get_network_ip(ipv4,ipv6):
    try:
        tmp=os.popen("ifconfig | grep inet6 | awk '{print $2}'").read()
        for line in tmp.splitlines():
            if line.find("fe",0,2)==-1 and line!="::1":
                ipv6.append(line)
    finally:
        if len(ipv6)==0:
            ipv6.append("error")
    try:
        tmp=os.popen("ifconfig | grep inet | awk '{print $2}'").read()
        for line in tmp.splitlines():
            if line not in ipv6 and line.find("fe",0,2)==-1 and line!="::1" and line!="127.0.0.1":
                ipv4.append(line)
    finally:
        if len(ipv4)==0:
            ipv4.append("error")
    return  0

def str_cnt(str1,str2):
    pos=0
    cnt=-1
    while(pos != -1):
        pos=str1.find(str2,pos+1,len(str1))
        cnt+=1
    return cnt

def get_tcp_connection(tcp,tcp_stat):
    tmp=os.popen('netstat -nat').read()
    for i in range (0,len(tcp_stat)):
        tcp.append(str_cnt(tmp,tcp_stat[i]))
def get_udp_connection():
    tmp=os.popen('netstat -nau').read()
    udp=str_cnt(tmp,"udp")
    return udp


def calbyte(num):
    unit=['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    cnt=0
    while num >= 1024:
        num/=1024
        cnt+=1
    return [round(num,2),unit[cnt]]

def caltime(sys_time,boot_time):
    tmp=sys_time-boot_time
    day=int(tmp/60/60/24)
    tmp-=60*60*24*day
    hr=int(tmp/60/60)
    tmp-=60*60*hr
    min=int(tmp/60)
    sec=int(tmp)-60*min
    time_list=[day,hr,min,sec]
    if time_list[0]!=0:
        return str(time_list[0])+"天"+str(time_list[1])+"时"
    elif time_list[1]!=0:
        return str(time_list[1])+"时"+str(time_list[2])+"分"
    elif time_list[2]!=0:
        return str(time_list[2])+"分"+str(time_list[3])+"秒"
    else:
        return str(time_list[3])+"秒" 

def func():
    data={}
    hostname=socket.gethostname()
    data['hostname']=hostname
    boot_time=psutil.boot_time()
    sys_time=time.time()
    run_time=caltime(sys_time,boot_time)
    data['run_time']=run_time
    data['sys_time']=sys_time
    cpu_percent=psutil.cpu_percent(interval=0.1,percpu=False)
    cpu_cnt=psutil.cpu_count(logical=True)
    cpu_logical_percent_list=psutil.cpu_percent(interval=0.1,percpu=True)
    data['cpu_percent']=str(cpu_percent)
    data['cpu_cnt']=str(cpu_cnt)
    data['cpu_logical_percent_list']=cpu_logical_percent_list
    vir_memory_list=psutil.virtual_memory()
    vir_total=vir_memory_list[0]
    vir_used=vir_memory_list[0]-vir_memory_list[1]
    data['memory_total']=str(calbyte(vir_total)[0])+calbyte(vir_total)[1]
    data['memory_used']=str(calbyte(vir_used)[0])+calbyte(vir_used)[1]
    try:
        data['memory_percent']=str(round(vir_used/vir_total*100,2))
    except:
        data['memory_percent']="error"
    swap_memory_list=psutil.swap_memory()
    swap_total=swap_memory_list[0]
    swap_used=swap_memory_list[1]
    data['swap_total']=str(calbyte(swap_total)[0])+calbyte(swap_total)[1]
    data['swap_used']=str(calbyte(swap_used)[0])+calbyte(swap_used)[1]
    try:
        data['swap_percent']=str(round(swap_used/swap_total*100,2))
    except:
        data['swap_percent']="error"
    disk_usage_list=psutil.disk_usage('/')
    disk_total=disk_usage_list[0]
    disk_used=disk_usage_list[1]
    data['disk_total']=str(calbyte(disk_total)[0])+calbyte(disk_total)[1]
    data['disk_used']=str(calbyte(disk_used)[0])+calbyte(disk_used)[1]
    try:    
        data['disk_percent']=str(round(disk_used/disk_total*100,2))
    except:
        data['disk_percent']="error"
    net_pre_list=psutil.net_io_counters()
    time.sleep(1)
    net_list=psutil.net_io_counters()
    net_pre_sent=net_pre_list[0]
    net_pre_recv=net_pre_list[1]
    net_sent=net_list[0]
    net_recv=net_list[1]
    net_sent_speed=(net_sent-net_pre_sent)
    net_recv_speed=(net_recv-net_pre_recv)
    data['net_sent_speed']=str(calbyte(net_sent_speed)[0])+calbyte(net_sent_speed)[1]+"/s"
    data['net_recv_speed']=str(calbyte(net_recv_speed)[0])+calbyte(net_recv_speed)[1]+"/s"
    data['net_sent']=str(calbyte(net_sent)[0])+calbyte(net_sent)[1]
    data['net_recv']=str(calbyte(net_recv)[0])+calbyte(net_recv)[1]
    ipv4=[]
    ipv6=[]
    get_network_ip(ipv4,ipv6)
    data['ipv4']=ipv4
    data['ipv6']=ipv6
    tcp=[]
    tcp_stat=["tcp","LISTEN","SYN_SENT","SYN_RECEIVED","ESTABLISHED","FIN_WAIT_1","CLOSE_WAIT","CLOSING","LAST_ACK","TIME_WAIT","CLOSED"]
    get_tcp_connection(tcp,tcp_stat)
    data['tcp_total']=str(tcp[0])
    tcp_dict={}
    for i in range(1,len(tcp)):
        tcp_dict[tcp_stat[i]]=tcp[i]
    data['tcp_stat']=tcp_dict
    udp=get_udp_connection()
    data['udp_total']=str(udp)
    data['mac']=os.popen("ifconfig|grep ether|awk '{print $2}'").readline()
    return data


if __name__=="__main__": 
    get_opt()
    print("客户端开始工作")
    print("服务器地址：",server_address,"服务器端口:",server_port)
    print("密码：",pwd)
    while True:
        try:
            src_data=func()
            src_data['password']=pwd
            data=json.dumps(src_data)
            if not data:
                continue
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_address, int(server_port)))
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            sock.send(data.encode()) 
            print ('send to server with value: ',data)
            sock.close()
        except KeyboardInterrupt:
            raise
        except socket.error:
            print("数据发送不成功...")
            time.sleep(3)
        except Exception as e:
            print("Caught Exception:", e)
