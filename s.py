from socketserver import BaseRequestHandler,ThreadingTCPServer
import threading
import json
import os
from socket import *

BUF_SIZE=1024
u=[]
talk = {}
# files=[]

def translate_dict(data):
    data = data.decode('utf-8')
    data = json.loads(data)
    return data

def send_method0():
    data = {'method':'0000'}
    data = json.dumps(data)
    data = data.encode() 
    return data

def send_list(data):
    data = json.dumps(data)
    data = data.encode() 
    return data

def get_all_file():
    files=[]
    allfilelist=os.listdir(os.getcwd())
    for f in allfilelist:
        if not os.path.isdir(f):
            files.append(f)
    return files
    # files.remove("cilent.py")
    # files.remove("server.py")
    


class Handler(BaseRequestHandler):
    def handle(self):
        address,pid = self.client_address
        print('%s connected!'%address)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data)>0:
                data = translate_dict(data)
                if data["method"] == "0001":
                    ip = data["ip"]
                    if ip not in u:
                        u.append(ip)
                    print("%s is connect"%ip)
                    self.request.sendall(send_method0())
                if data["method"] == "0002":
                    ip = data["ip"]
                    print("%s get cilent list "%ip)
                    self.request.sendall(send_list(u))
                if data["method"] == "0003":
                    ip = data["ip"]
                    print("%s get file list "%ip)
                    files = get_all_file()
                    self.request.sendall(send_list(files))
                if data["method"] == "0005":
                    from_ip = data["from_ip"]
                    to_ip = data["to_ip"]
                    text = data["text"]
                    talk[str(to_ip)] =  {from_ip:text}
                    print(talk)
                # if data["method"] == "0006":
                #     ip = str(data["ip"])
                #     if ip in talk:
                #         print(talk[ip])
                #         from_ip = talk[ip]
                #         talk.pop(ip)
                #         data = {'method':'0006','from':}

                if data["method"] == "0004":
                    ip = data["ip"]
                    file_name = data["file"]
                    print("%s downing %s "%(ip,file_name))
                    if os.path.exists(file_name):
                        filesize = int(os.path.getsize(file_name))
                        data = {'method':"0004","file_size":filesize}
                        self.request.sendall(send_list(data))
                        print("文件大小为：",filesize)
                        # self.request.sendall(filesize.encode())
                        # data = self.request.recv(BUF_SIZE)   #挂起服务器发送，确保客户端单独收到文件大小数据，避免粘包
                        print("开始发送")
                        f = open(file_name, "rb")
                        for line in f:
                            self.request.sendall(line)
                        print("发送结束")
                        
                    else:
                        data = {'method':"0011"}
                        self.request.sendall(send_list(data))
                    

                
            else:
                print('close')
                break

if __name__ == '__main__':
    HOST = ''
    PORT = 9001
    ADDR = (HOST,PORT)

    ip = (gethostbyname(getfqdn(gethostname())))
    ipl = ip.split(".")[-1]
    print("当前地址为",ip)
    print("当前机器号为",ipl)

    server = ThreadingTCPServer(ADDR,Handler)  #参数为监听地址和已建立连接的处理类
    print('服务已运行，正在监听端口')
    server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理
    print(server)