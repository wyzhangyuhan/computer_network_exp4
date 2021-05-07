import socket # 导入 socket 模块
from threading import Thread
import time
import os
import pandas as pd
from baidutrans import BaiduTranslate
  
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
  

# AppleZhang 在这里加了个 client 的类型，方便 vscode 做代码补全
def message_handle(client: socket.socket):
    """
    消息处理
    """
    stu_name = ['张钰涵','张峻弘','庄宝开','杨松佳']
    stu_id = ['2018192008', '2018151014','2018152008', '2018151020']
    stu_sex = ['男', '男', '大奶子', '女']
    data = []
    data.append(stu_name)
    data.append(stu_id)
    data.append(stu_sex)
    data = list(map(list, zip(*data)))
    student_info = pd.DataFrame(
        data = data,
        columns = ['名字', '学号', '性别'] 
    )

    client.send("连接服务器成功!".encode(encoding='utf8'))
    while True:
        bytes = client.recv(1024)
        recvmsg =  bytes.decode(encoding='utf8')
        # print("客户端消息:", bytes.decode(encoding='utf8'))
        print('服务端收到信息: ', recvmsg)
        if recvmsg=='time':
            ret = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            
            client.send(ret.encode(encoding='utf8'))
        elif 'file:' in recvmsg:
            print('服务端发送信息: ', 'downloading files')
            cfiles = str([d for d in os.listdir('.')])
            filename = recvmsg.split(':')[1]

            try:
                file = open(filename, 'rb+')
                print('服务端信息: ', filename)
                tmpstr = 'ok:' + filename
                client.send(tmpstr.encode(encoding='utf8'))
            except:
                print('服务端信息: ', f'目标文件{filename}不存在')
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
        
        elif 'trans:' in recvmsg:
            tmpt = recvmsg.split(':')
            BaiduTranslate_test = BaiduTranslate(tmpt[0],tmpt[1])
            Results = BaiduTranslate_test.BdTrans(tmpt[2])#要翻译的词组
            client.send(Results.encode(encoding='utf8'))

        elif recvmsg == 'ls':
            cfiles = str([d for d in os.listdir('.')])
            client.send(cfiles.encode(encoding='utf8'))
            
        elif 'exit' in recvmsg:
            # for i in range(0,2):
            client.send('Bye (server send closed)\nBye (server will closed)'.encode(encoding='utf8'))
            
        elif 'fin' in recvmsg:
            # client.send('Bye (recieved 4th wave)'.encode(encoding='utf8'))
            client.close()
            # 删除连接
            g_conn_pool.remove(client)
            print("有一个客户端下线了。")
            break
        elif str.isdigit(recvmsg):
            if recvmsg in student_info.values:
                a = student_info[(student_info.学号 == recvmsg)].index.tolist() #return index
                info_str = str(student_info.iloc[a])
                client.send(info_str.encode(encoding='utf8'))
            else:
                client.send('学号不存在'.encode(encoding='utf8'))
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
        elif cmd == '3':
            print(g_conn_pool)
            