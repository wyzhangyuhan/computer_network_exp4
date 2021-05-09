from tkinter import *
import time
from socket import * # 导入 socket 模块
from tkinter import filedialog
import pandas as pd
from ttt_client_gui import mainGUI
from baidutrans import BaiduTranslate
from translate import Translate
from endianHandler import *

# import myglobal
KBYTE = 1024

def main():
    def sendMsg():#发送消息
        client_strMsg = "客户端发送:" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+ '\n'
        txtMsgList.insert(END, client_strMsg, 'greencolor')
        txtMsgList.insert(END, txtMsg.get('1.0', END))
        sendmsg = txtMsg.get('1.0', END)[:-1] #获取GUI信息框中的信息
        print(sendmsg)
        if (sendmsg.strip() == ""):
            print("Warning: dont send empty!!!!!!!!!!")
            return
        s.send(sendmsg.encode()) #对信息编码后发送
        txtMsg.delete('0.0', END)

        recvmsg = s.recv(KBYTE).decode() #接收来自服务器的消息
        print('来自服务端的信息: ', recvmsg)
        server_strMsg = "服务器发送:" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+ '\n'
        txtMsgList.insert(END, server_strMsg, 'bluecolor')
        txtMsgList.insert(END, recvmsg+ '\n')

        if 'file:' in sendmsg:
            # 分析 file 命令的输入
            argvs = sendmsg.split(':')
            if len(argvs) == 2:
                filename = "dup-" + argvs[1]
            elif len(argvs) == 3:
                filename = argvs[2]
            else:
                print("invalid input")
        
        if 'Bye' in recvmsg:
            app.update()
            sendmsg = 'fin (4th wave)'
            txtMsgList.insert(END, client_strMsg, 'greencolor')
            txtMsgList.insert(END, sendmsg)
            s.send(sendmsg.encode()) #对信息编码后发送
            app.update()
            time.sleep(1)
            s.close()
            exit()
        elif 'ok' in recvmsg:
            file_size = int(recvmsg.split(':')[-1])
            file = open("Download/" + filename, 'wb')
            recv_size=0
            while recv_size < file_size:
                r = s.recv(KBYTE*128)
                print('接收到 ', len(r), ' 字节的数据')
                txtMsgList.insert(END, f'接收到{len(r)}字节的数据\n')
                file.write(r)
                recv_size = recv_size + len(r)
            print('接收完成\n')
            txtMsgList.insert(END, '接收完成\n')
        

    def cancelMsg():#取消信息
        txtMsg.delete('0.0', END)

    def sendMsgEvent(event: Event):#发送消息事件
        if event.keysym =='Up':
            sendMsg()

    def openfile():
        sfname = filedialog.askopenfilename(title='选择要传输的文件', filetypes=[('All Files', '*')])
        file_text = sfname.split('/')[-1]
        if file_text != '':
            file_text = 'file:' + file_text
        txtMsg.insert(END,file_text)

    def translate():
        tmp_t = Translate()
        tmp_t.main()

    def playgame():
        ttt = mainGUI()
        ttt.main()


    #与服务器连接通信
    host = '172.26.128.21'
    port = 8712
    s = socket(AF_INET, SOCK_STREAM) # 创建 socket 对象
    s.connect((host, port))
    print(s.recv(KBYTE).decode(encoding='utf8'))
    s.send("连接了".encode('utf8'))
    print(s.recv(KBYTE).decode(encoding='utf8'))
    print('连接到 ', host, ':', port)
    print('-----------------------------------')

    #创建窗口
    app = Tk()
    app.title('与服务器通信')

    #创建frame容器
    frmLT = Frame(width = 500, height = 320, bg = 'white')
    frmLC = Frame(width = 500, height = 150, bg = 'white')
    frmLB = Frame(width = 500, height = 30)
    frmRT = Frame(width = 200, height = 500)

    #创建控件
    txtMsgList = Text(frmLT)
    txtMsgList.tag_config('greencolor',foreground = '#008C00')#创建tag
    txtMsgList.tag_config('bluecolor',foreground = '#0087D2')#创建tag
    txtMsg = Text(frmLC)
    txtMsg.bind("<KeyPress-Up>", sendMsgEvent)
    btnSend = Button(frmLB, text = '发送', width = 8, command = sendMsg)
    btnCancel = Button(frmLB, text = '取消', width = 8, command = cancelMsg)
    btnselect = Button(frmLB, text = '选择文件', width = 8, command = openfile)
    btngame = Button(frmLB, text = '游戏时间', width = 8, command = playgame)
    btntrans = Button(frmLB, text = '翻译文字', width = 8, command = translate)
    imgInfo = PhotoImage(file = "13.gif")
    lblImage = Label(frmRT, image = imgInfo)
    lblImage.image = imgInfo

    #窗口布局
    frmLT.grid(row = 0, column = 0, columnspan = 2, padx = 1, pady = 3)
    frmLC.grid(row = 1, column = 0, columnspan = 2, padx = 1, pady = 3)
    frmLB.grid(row = 2, column = 0, columnspan = 2)
    frmRT.grid(row = 0, column = 2, rowspan = 3, padx =2, pady = 3)

    #固定大小
    frmLT.grid_propagate(0)
    frmLC.grid_propagate(0)
    frmLB.grid_propagate(0)
    frmRT.grid_propagate(0)

    btnSend.grid(row = 2, column = 0)
    btnCancel.grid(row = 2, column = 1)
    btnselect.grid(row = 2, column = 2) 
    btngame.grid(row = 2, column = 3) 
    btntrans.grid(row = 2, column = 4) 
    lblImage.grid()
    txtMsgList.grid()
    txtMsg.grid()

    #主事件循环
    app.mainloop()

if  __name__ == "__main__":
    main()