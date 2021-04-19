from socket import *
import sys
import time

port = 888
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(114514)

conn, addr = serverSocket.accept()
print('-----------------------------------')
print('接收到新连接: ')
print('客户端地址: ', addr, ':')

filename = conn.recv(1024).decode()

try:
    file = open(filename, 'rb+')
    print('客户端请求文件: ', filename)
    print('服务端发送信息: ', 'ok')
    conn.send('ok'.encode())
except:
    print('服务端发送信息: ', '目标文件不存在')
    conn.send('目标文件不存在'.encode())
    conn.close()
    exit()

while True:
    r = file.read(1024*128)
    if len(r)==0:
        break
    print('发送 ', len(r), ' 字节的数据')
    conn.send(r)

conn.close()
print('发送完成')
