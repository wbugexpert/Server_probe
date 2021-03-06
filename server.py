#! /bin/python3
import socket
import time
import os
import json
import sys
import psutil
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import eventlet

pwd=""
msg_port=""
web_port=""
def get_opt():
    try:
        global pwd,msg_port,web_port
        for i in range(1,len(sys.argv)):
            if sys.argv[i].find("-w=",0,3)!=-1:
                web_port=sys.argv[i][3:len(sys.argv[i])]
            elif sys.argv[i].find("-m=",0,3)!=-1:
                msg_port=sys.argv[i][3:len(sys.argv[i])]
            elif sys.argv[i].find("-p=",0,3)!=-1:
                pwd=sys.argv[i][3:len(sys.argv[i])]
    finally:
        if web_port == "" :
            web_port="8001"
        if msg_port=="":
            msg_port="8000"
        if pwd == "":
            print(sys.argv[0]+" -p=<password> -w=<web_port(=8001)> -m=<message_port(=8000)>")
            print("Please note that there is no space between the equal sign and the parameter")
            sys.exit()
    return

data_list=[]

class Resquest(BaseHTTPRequestHandler):
  
    def do_GET(self):
        full_path = os.path.split(os.path.realpath(__file__))[0] + "/dash.html"
        #self.send_header("Access-Control-Allow-Origin", "*")
        if self.path!='/status.json?'+pwd:
            page=open(full_path,"rb").read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
        else:
            page = self.create_page()
            self.send_content(page.encode())
    
    Page = '''\
        {content}
    '''
    def create_page(self):
        global data_list
        now_time=time.time()
        tmp_list=[]
        for i in range(0,len(data_list)):
            sent_time=(int)(data_list[i]['sys_time'])
            if now_time-sent_time>=1800:
                data_list[i]['status']="offline"
                continue
            elif now_time-sent_time>10:
                data_list[i]['status']="offline"
            else:
                data_list[i]['status']="online"
            tmp_list.append(data_list[i])
        data_list=tmp_list[:]
        string=json.dumps(data_list)
        values = {'content':string}
        page = self.Page.format(**values)
        return page
    def send_content(self, page):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

def check_hostname(list,ipv4_list,ipv6_list,hostname):
    for i in range(0,len(list)):
        if ipv4_list == list[i]['ipv4'] and ipv6_list == list[i]['ipv6'] and hostname==list[i]['hostname']:
            return i
    return -1

def web_server():
    server = HTTPServer(('',int(web_port)), Resquest)
    server.serve_forever()

def recv_msg(connection):
    with eventlet.Timeout(1, False):
        try:
            buf = connection.recv(1024).decode()
            while buf[len(buf)-1]!="}":
                buf+=connection.recv(1024).decode()
            if not buf:
                connection.close()
                return
            data=json.loads(buf)
            #print(data)
            if(data['password'] != pwd):
                print("password wrong")
                connection.close()
                return
            del data['password']
            if check_hostname(data_list,data['ipv4'],data['ipv6'],data['hostname']) == -1:
                data_list.append(data)
            else:
                data_list[check_hostname(data_list,data['ipv4'],data['ipv6'],data['hostname'])]=data
            data_list.sort(key=lambda ele:ele['hostname'].lower())
        except:
            pass
    connection.close()
    return

if __name__=="__main__":
    get_opt()
    print("???????????????",web_port,"?????????????????????",msg_port)
    print("?????????",pwd)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #???????????????   
        sock.bind(('0.0.0.0', int(msg_port)))  #??????soket?????????IP??????????????????  
        sock.listen(128) #??????????????????????????????????????????server???????????????FIFO??????
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    except:
        print("????????????????????????????????????????????????"+msg_port+"??????????????????")
        sys.exit()
    try:    
        threading.Thread(target=web_server).start() 
    except:
        print("??????????????????????????????????????????"+web_port+"??????????????????")
        sys.exit()
    print("????????????????????????")
    eventlet.monkey_patch()
    while True:
        while threading.active_count()>6:
            time.sleep(1)
        connection,address = sock.accept()
        try: 
            threading.Thread(target=recv_msg,args=(connection,)).start()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print("????????????:%s??????????????????..."%e)
            time.sleep(3)
