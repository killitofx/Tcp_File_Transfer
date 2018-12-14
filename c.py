from socket import *
import sys
import json
import time

# 初始化
local_ip = (gethostbyname(getfqdn(gethostname())))
ipa = input("请输入服务器的机器号")
ip = (gethostbyname(getfqdn(gethostname())))
HOST = ip.split(".")[0] + '.' + ip.split(".")[1] + '.' + ip.split(".")[2] + '.' + ipa
print("ip:",HOST)





# HOST = '127.0.0.1'
PORT = 9001
ADDR =(HOST,PORT)
BUFSIZE = 1024


temp = -1



def send_data(data):
     data = json.dumps(data)
     data = data.encode('utf-8')
     return data

def receive_data(data):
     data = data.decode('utf-8')
     # data = data.loads(data)
     return data



sock = socket()
# try:
sock.connect(ADDR)
print('have connected with server')

# 服务初始化
a1 = {'method':'0001','ip':local_ip}
sock.sendall(send_data(a1))
r_data =  sock.recv(BUFSIZE)
data = receive_data(r_data)
print("初始化完成")
# print(data)



# 获取客户端列表
a2 = {'method':'0002','ip':local_ip}
sock.sendall(send_data(a2))
r_data =  sock.recv(BUFSIZE)
data = receive_data(r_data)
print("获取用户列表")
print(data)

# 聊天 暂时废弃
# a10 = {'method':'0005','from_ip':local_ip,'to_ip':'192.168.10.1','text':"hello"}
# sock.sendall(send_data(a10))
# r_data =  sock.recv(BUFSIZE)
# data = receive_data(r_data)
# print(data)

# 获取服务器文件列表
print("获取文件列表")
a3 = {'method':'0003','ip':local_ip}
sock.sendall(send_data(a3))
r_data =  sock.recv(BUFSIZE)
data = receive_data(r_data)
print(data)
data = json.loads(data)


print("select a file start from 0,q to exit")
# 选择文件
choose = input("> ")
if choose != 'q':
     choose = int(choose)
     print("准备接受%s"%data[choose])
     file_name = data[choose]

     # 发送准备接受的文件名
     a4 = {'method':'0004','ip':local_ip,"file":data[choose]}
     # print(a4)
     sock.sendall(send_data(a4))
     r_data =  sock.recv(BUFSIZE)
     data = receive_data(r_data)
     data = json.loads(data)
     print(data)
     # 获取文件大小
     file_total_size = data['file_size']
     received_size = 0
     f = open(time.strftime("%H_%M_%S_", time.localtime()) + file_name  ,"wb")
     while received_size < file_total_size:
          data = sock.recv(BUFSIZE)
          f.write(data)
          received_size += len(data)
          # print("已接收:",received_size)
          fns = int(received_size / file_total_size*10)
          
          if not temp == fns:
               temp = fns
               print("已完成 %d%%" %int(fns*10))
          


sock.close()
sys.exit()
