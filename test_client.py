from socket import * # 导入 socket 模块
from tkinter import *



host = 'localhost'
port = 8712
s = socket(AF_INET, SOCK_STREAM) # 创建 socket 对象
s.connect((host, port))
print(s.recv(1024).decode(encoding='utf8'))
s.send("连接了".encode('utf8'))
print(s.recv(1024).decode(encoding='utf8'))
print('连接到 ', host, ':', port)
print('-----------------------------------')

while True:
    sendmsg = input('请输入发送的信息:  ')
    filename = ''
    s.send(sendmsg.encode())
    recvmsg = s.recv(1024).decode()
    print('来自服务端的信息: ', recvmsg)
    if 'file-' in sendmsg:
        filename = sendmsg.split('-')[-1]
    if recvmsg=='bye':
        break
    elif recvmsg =='ok':
        file = open(filename, 'wb')
        while True:
            r = s.recv(1024*128)
            if len(r)==0:
                file.close()
                break
            print('接收到 ', len(r), ' 字节的数据')
            file.write(r)
            if len(r) < 1024*128:
                file.close()
                break
        print('接收完成')

s.close()

