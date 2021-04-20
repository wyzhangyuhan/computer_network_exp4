from tkinter import *
import time
from socket import * # 导入 socket 模块
from tkinter import filedialog
import pandas as pd
from ttt_client_gui import mainGUI

def main():

    def sendMsg():#发送消息
        client_strMsg = "客户端发送:" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+ '\n'
        txtMsgList.insert(END, client_strMsg, 'greencolor')
        txtMsgList.insert(END, txtMsg.get('1.0', END))
        sendmsg = txtMsg.get('1.0', END)[:-1]
        s.send(sendmsg.encode())
        txtMsg.delete('0.0', END)

        recvmsg = s.recv(1024).decode()
        print('来自服务端的信息: ', recvmsg)
        server_strMsg = "服务器发送:" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+ '\n'
        txtMsgList.insert(END, server_strMsg, 'bluecolor')
        txtMsgList.insert(END, recvmsg+ '\n')
        if 'file-' in sendmsg:
            filename = sendmsg.split('-')[-1]
        if recvmsg == 'bye':
            app.update()
            time.sleep(0.5)
            exit()
        elif recvmsg =='ok':
            file = open(filename, 'wb')
            while True:
                r = s.recv(1024*128)
                if len(r)==0:
                    file.close()
                    break
                if r == 'EOF':
                    file.close()
                    break
                print('接收到 ', len(r), ' 字节的数据')
                txtMsgList.insert(END, f'接收到{len(r)}字节的数据\n')
                file.write(r)
                if len(r) < 1024*128:
                    file.close()
                    break
            print('接收完成')
            txtMsgList.insert(END, '接收完成')
        

    def cancelMsg():#取消信息
        txtMsg.delete('0.0', END)

    def sendMsgEvent(event):#发送消息事件
        if event.keysym =='Up':
            sendMsg()

    def openfile():
        sfname = filedialog.askopenfilename(title='选择要传输的文件', filetypes=[('All Files', '*')])
        file_text = sfname.split('/')[-1]
        if file_text != '':
            file_text = 'file-' + file_text
        txtMsg.insert(END,file_text)

    def playgame():
        ttt = mainGUI()
        ttt.main()


    #服务器连接通信
    host = 'localhost'
    port = 8712
    s = socket(AF_INET, SOCK_STREAM) # 创建 socket 对象
    s.connect((host, port))
    print(s.recv(1024).decode(encoding='utf8'))
    s.send("连接了".encode('utf8'))
    print(s.recv(1024).decode(encoding='utf8'))
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
    lblImage.grid()
    txtMsgList.grid()
    txtMsg.grid()

    #主事件循环
    app.mainloop()

if  __name__ == "__main__":
    main()