import socket # 导入 socket 模块
from threading import Thread
import time
import os
  
ADDRESS = ('127.0.0.1', 8712) # 绑定地址
  
g_socket_server = None # 负责监听的socket
  
g_conn_pool = [] # 连接池

def init():
    """
    初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建 socket 对象
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(10) # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("服务端已启动，等待客户端连接...")

def accept_client():
    """
    接收新连接
    """
    while True:
        client, _ = g_socket_server.accept() # 阻塞，等待客户端连接
        # 加入连接池
        g_conn_pool.append(client)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=message_handle, args=(client,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()
  
  
def message_handle(client):
    """
    消息处理
    """
    client.send("连接服务器成功!".encode(encoding='utf8'))
    while True:
        bytes = client.recv(1024)
        recvmsg =  bytes.decode(encoding='utf8')
        # print("客户端消息:", bytes.decode(encoding='utf8'))
        if recvmsg=='':
            continue
        print('服务端收到信息: ', recvmsg)
        if recvmsg=='time':
            ret = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            
            client.send(ret.encode(encoding='utf8'))
        elif 'file-' in recvmsg:
            print('服务端发送信息: ', 'downloading files')
            cfiles = str([d for d in os.listdir('.')])
            filename = recvmsg.split('-')[-1]

            try:
                file = open(filename, 'rb+')
                print('服务端信息: ', filename)
                client.send('ok'.encode(encoding='utf8'))
            except:
                print('服务端信息: ', '目标文件不存在')
                client.send('404 Not Found'.encode(encoding='utf8'))
                continue
            while True:
                r = file.read(1024*128)
                if len(r)==0:
                    file.close()
                    break
                print('发送 ', len(r), ' 字节的数据')
                client.send(r)
                if len(r) < 1024*128:
                    file.close()
                    break
            client.send('EOF'.encode(encoding='utf8'))
            
        elif recvmsg == 'ls':
            cfiles = str([d for d in os.listdir('.')])
            client.send(cfiles.encode(encoding='utf8'))
        elif recvmsg=='exit':
            client.send('bye'.encode(encoding='utf8'))
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
            print("有一个客户端下线了。")
            break
        else:
           
            client.send('无效命令'.encode(encoding='utf8'))

if __name__ == '__main__':
    init()
    # 新开一个线程，用于接收新连接
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:
        cmd = input("""--------------------------
        输入1:查看当前在线人数
        输入2:关闭服务端
        """)
        if cmd == '1':
            print("--------------------------")
            print("当前在线人数：", len(g_conn_pool))
        elif cmd == '2':
            exit()
            