# web_server
### 基于python3编写的一个服务器探针

服务器端配置：调用的库函数：socket,json,time,os,sys,psutil,http.server,threading,eventlet，需自行配置

客户端已编写代码自动配置，需有os库和sys库，以及pip

网页端查看：ip地址:端口/?密码


## 服务端参数


-p：password（预设的密码）  -w：web_port（供访问的网页端口，默认为8001，默认8001） -m:message_port（接收客户端上报信息的端口，默认为8000）

.eg： server.py -p=password -w=8001 -m=8000





## 客户端参数：


-p=password(预设的密码) -a=server_address(请求的服务端地址) -m=server_port(服务端接收信息端口，默认为8000)

.eg: client.py -p=password -a=1.1.1.1 -m=8000


## 请注意：dash.html文件必须与server.py放在同一目录下

