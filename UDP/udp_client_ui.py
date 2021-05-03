import sys
import os
import socket
import json
import logging
import time
import threading as th
import typing
import base64 as b64
import hashlib

# PYQT
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import Ui_login
import Ui_main

# Baidu Translation API
import baidutrans as tran

# TTT
import ttt_client_gui as ttt

MTU = 32*1024

class UDPChatDesktop():
    def __init__(self, dialog: QDialog, mainwin: QMainWindow, host: str, port: int):
        # UDP Socket initialization
        self.selfaddr = socket.gethostbyname(socket.gethostname())
        self.server_addr = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.nickname = "none"
        self._connection = True
        self.sendtolist = []
        self.onlinelist = []
        self.chatlist = []
        self.ollm = QtCore.QStringListModel()
        self.trans_cursor = -1
        self.bdtrans = tran.BaiduTranslate("auto", "zh")

        # setup login UI
        self._set_login(dialog)
        self._set_main(mainwin)

        self.listener = self.UpdateChat(socket_=self.socket)

    def run_client(self):
        self._login_show_ui()

    @staticmethod
    def exefile(url: QtCore.QUrl):
        os.chdir("Download")
        _, filename = os.path.split(url.toString())
        os.startfile(filename)
        os.chdir(os.pardir)

    def _set_main(self, mainwin: QMainWindow):
        self.mainw = mainwin
        self.mainw.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.mui = Ui_main.Ui_MainWindow()
        self.mui.setupUi(self.mainw)
        self.mui.txtSubmitBtn.clicked.connect(self._main_submit_chat)
        self.mui.txtClearBtn.clicked.connect(self._main_clear_input)
        self.mui.exitButton.clicked.connect(self._main_exit)
        self.mui.onlineList.clicked.connect(self._main_select_sendto)
        self.mui.fileButton.clicked.connect(self._main_file_transfer)
        self.mui.searchBtn.clicked.connect(self._main_search_history)
        self.mui.picButton.clicked.connect(self._main_send_diy_emoji)
        self.mui.tttButton.clicked.connect(self._main_play_ttt)

        self.mui.transButton.clicked.connect(self._main_trans_msg)
        self.mui.transUpButton.clicked.connect(lambda: self._main_move_cursor(-1))
        self.mui.transDownButton.clicked.connect(lambda: self._main_move_cursor(1))

        self.mui.tickleButton.clicked.connect(self._main_tickle)

        # set the notice of input box
        self.mui.userInput.setPlaceholderText("Input your message!")
        self.mui.searchBox.setPlaceholderText("Search what?")

        # set the link to files, and use 
        self.mui.chatHistory.setOpenExternalLinks(False)
        self.mui.chatHistory.setOpenLinks(False)
        self.mui.chatHistory.anchorClicked.connect(UDPChatDesktop.exefile)

        # builtin emoji setup
        # this is a shit mountain
        self.mui.emojiBtn.clicked.connect(self._main_show_builtin_emoji)
        self.mui.emj_bBtn_1.clicked.connect(lambda: self._main_send_builtin_emoji(0))
        self.mui.emj_bBtn_2.clicked.connect(lambda: self._main_send_builtin_emoji(1))
        self.mui.emj_bBtn_3.clicked.connect(lambda: self._main_send_builtin_emoji(2))
        self.mui.emj_bBtn_4.clicked.connect(lambda: self._main_send_builtin_emoji(3))
        self.mui.emj_bBtn_1.hide()
        self.mui.emj_bBtn_2.hide()
        self.mui.emj_bBtn_3.hide()
        self.mui.emj_bBtn_4.hide()

    def _set_login(self, dialog: QDialog):
        # UI initialization
        self.dialog = dialog
        self.lui = Ui_login.Ui_Dialog()
        self.lui.setupUi(self.dialog)
        self.lui.submitButton.clicked.connect(self._login_submit_auth)
        self.lui.exitButton.clicked.connect(self._login_exit)
    
    #
    #  ====== login window ======
    #
    def _login_show_ui(self):
        self.dialog.show()

    def _login_exit(self):
        self.dialog.close()
       
    def _login_submit_auth(self):
        nickname = self.lui.nameInput.text()
        passwd = self.lui.passInput.text()
        # nickname = "AppleZhang"
        # passwd = "apple123"
        
        # username-password pair
        auth_data = json.dumps(["ctl",  # data_type
                                {"type": "auth", "name": nickname, "pass": passwd}, # data parameters
                                ""])    # data

        # send authentication
        self.socket.sendto(auth_data.encode("utf-8"), self.server_addr)
        result = self.socket.recv(MTU)

        _, _, data, appdix = json.loads(result)

        # check the 4byte data from server
        if data == "\x00\x00\x00\x00":
            print("Wrong username or password.")
            self.lui.nameInput.clear()
            self.lui.noticeLabel.setText("Wrong username or password.\nPlease retry.")

            # set red color to notice wrong auth
            plt = QtGui.QPalette()
            color = QtGui.QColor(255, 10, 10, 255)
            plt.setColor(QtGui.QPalette.Foreground, color)
            self.lui.noticeLabel.setPalette(plt)
        elif data == "\x01\x01\x01\x01":
            print("Authentication success.")
            self.nickname = nickname
            
            # switch to main window
            self._login_exit()
            self.onlinelist.append(self.nickname)
            self.onlinelist.extend(appdix)
            self._main_show_ui()
            pass # TODO
        elif data == "\x02\x02\x02\x02":
            print(f"{nickname} has been online.")
            self.lui.noticeLabel.setText(f"{nickname} has been online.\nYou cannot loggin by this account.")

            # set red color to notice wrong auth
            plt = QtGui.QPalette()
            color = QtGui.QColor(255, 10, 10, 255)
            plt.setColor(QtGui.QPalette.Foreground, color)
            self.lui.noticeLabel.setPalette(plt)
        else:
            logging.warning(f"Undefined data flag {data[0]}")

    #
    #  ====== chatroom main window ======
    #
    def _main_show_ui(self):
        self.mainw.setWindowTitle(f"Chatroom -- {self.nickname} --")
        self.mainw.show()
        self.mui.addressLabel.setText(f"Your address: {self.selfaddr}")
        self.listener.update_sig.connect(self._message_handler)
        recv_th = th.Thread(target=self.listener._recv_routine)
        recv_th.setDaemon(True)
        recv_th.start()
        self.__update_chat_txt("admin", f"{self.nickname}, welcome to chatroom!")
        self._main_disp_online()

    def _main_exit(self):
        data = json.dumps(["ctl", {"type": "exit"}, ""])
        self.socket.sendto(data.encode("utf-8"), self.server_addr)
        self._connection = False
        self.mainw.close()

    def _main_select_sendto(self, model_id: QtCore.QModelIndex):
        self.sendtolist = []
        model_ids = self.mui.onlineList.selectedIndexes()
        for each in model_ids:
            self.sendtolist.append(self.onlinelist[each.row()])
        # debug
        # print(self.sendtolist)

    def _main_show_builtin_emoji(self):
        self.mui.emj_bBtn_1.show()
        self.mui.emj_bBtn_2.show()
        self.mui.emj_bBtn_3.show()
        self.mui.emj_bBtn_4.show()
        # debug

    def _main_send_builtin_emoji(self, emjcode: int):
        jdata = json.dumps(["emj", {"type": "bti", "tolist": self.sendtolist}, emjcode])
        self.socket.sendto(jdata.encode("utf-8"), self.server_addr)
        self.mui.emj_bBtn_1.hide()
        self.mui.emj_bBtn_2.hide()
        self.mui.emj_bBtn_3.hide()
        self.mui.emj_bBtn_4.hide()
        self.__update_chat_emj("@myself@", emjcode, "")

    def _main_send_diy_emoji(self):
        fname = QFileDialog.getOpenFileName(self.mainw,
                                            "Select a file for transfermission.", os.curdir,
                                            "Portable Network Graphics (*.png);; Joint Photographic Experts Group (*jpeg)")
        # debug
        # print(fname)
        if fname[0] != '' and fname[1] != '':
            with open(fname[0], "rb") as f:
                _, file_name = os.path.split(fname[0])
                file_data = b64.b64encode(f.read()).decode()
                jdata = json.dumps(["emj", {"type": "diy", "tolist": self.sendtolist, "fname": file_name}, file_data])
                self.socket.sendto(jdata.encode("utf-8"), self.server_addr)

                emjcode = int(hashlib.md5((self.nickname + file_name).encode()).hexdigest()[:7], base=16)
                emjcode = abs(emjcode) + 4
                self.__update_chat_emj("@myself@", emjcode, file_data)

    def _main_disp_online(self):
        self.ollm.setStringList(self.onlinelist)
        self.mui.onlineList.setModel(self.ollm)

    def _main_submit_chat(self):
        msg = self.mui.userInput.toPlainText()
        if msg == "":
            print("Cannot send empty message.")
            return
        
        self.__update_chat_txt("@myself@", msg)
        self.mui.userInput.clear()

        data = json.dumps(["txt", {"tolist": self.sendtolist}, msg])
        self.socket.sendto(data.encode("utf-8"), self.server_addr)

    def _main_clear_input(self):
        self.mui.userInput.clear()

    def _main_file_transfer(self):
        fname = QFileDialog.getOpenFileName(self.mainw, "Select a file for transfermission.")
        # debug
        # print(fname)
        if fname[0] != '' and fname[1] != '':
            with open(fname[0], "rb") as f:
                _, file_name = os.path.split(fname[0])
                file_data = b64.b64encode(f.read()).decode()
                jdata = json.dumps(["fle", {"tolist": self.sendtolist, "fname": file_name}, file_data])
                self.socket.sendto(jdata.encode("utf-8"), self.server_addr)
                self.__update_chat_fle("@myself@", file_name, file_data)

    def _main_search_history(self):
        pattern = self.mui.searchBox.text()
        if pattern != "":
            self.mui.chatHistory.clear()
            for each in self.chatlist:
                if each[2] == "txt":
                    msg = each[3].replace(pattern, f"<strong style='background:yellow'>{pattern}</strong>")
                else:
                    msg = each[3]
                msg = f"<font color='{each[4]}'>{each[0]}<br>{each[1]}: {msg}</font><br>"
                self.mui.chatHistory.append(msg)
        else:
            self.mui.chatHistory.clear()
            for each in self.chatlist:
                msg = f"<font color='{each[4]}'>{each[0]}<br>{each[1]}: {each[3]}</font><br>"
                self.mui.chatHistory.append(msg)

    def _main_play_ttt(self):
        ttt_main = ttt.mainGUI()
        ttt_main.main()
        pass

    def _main_trans_msg(self):
        chat = self.chatlist[self.trans_cursor]
        
        # if is not txt, then return error
        if chat[2] != "txt":
            print("You can only translate 'txt' chat entry.")
            return
        
        msg = chat[3]
        
        # translating
        # trans_msg = "This is a test..."
        isok, trans_msg = self.bdtrans.BdTrans(msg)

        # error, early return
        if not isok:
            print("Error in translating.")
            return

        # update chat history
        self.mui.chatHistory.clear()
        curs = self.mui.chatHistory.textCursor()

        for ii in range(len(self.chatlist)):
            each = self.chatlist[ii]
            if ii == self.trans_cursor:
                chatmsg = f"<font color='{each[4]}'>{each[0]}<br>{each[1]}: {trans_msg} 👈</font><br>"
                pos = len(self.mui.chatHistory.toPlainText())
            else:
                chatmsg = f"<font color='{each[4]}'>{each[0]}<br>{each[1]}: {each[3]}</font><br>"
            self.mui.chatHistory.append(chatmsg)
        
        curs.setPosition(pos)
        self.mui.chatHistory.setTextCursor(curs)

    def _main_move_cursor(self, direction: int):
        index = self.trans_cursor
        if index < 0:
            # initialize
            index = 0
        else:
            # otherwise, move it
            if direction > 0:
                # if current cursor is the last one, early return
                if index < len(self.chatlist)-1:
                    index += 1
                else: return
            else:
                # if current cursor is the first one, early return
                if index > 0:
                    index -= 1
                else: return

        # set the cursor
        self.trans_cursor = index
        self.mui.chatHistory.clear()
        curs = self.mui.chatHistory.textCursor()

        for ii in range(len(self.chatlist)):
            each = self.chatlist[ii]
            if ii == self.trans_cursor:
                chatmsg = f"<font color='{each[4]}'>{each[0]}<br>{each[1]}: {each[3]} 👈</font><br>"
                pos = len(self.mui.chatHistory.toPlainText())
            else:
                chatmsg = f"<font color='{each[4]}'>{each[0]}<br>{each[1]}: {each[3]}</font><br>"
            self.mui.chatHistory.append(chatmsg)
        
        curs.setPosition(pos)
        self.mui.chatHistory.setTextCursor(curs)

    def _main_tickle(self):
        # just for funny.
        # tickle someone haha
        
        # select chat
        chat = self.chatlist[self.trans_cursor]

        tick_who = chat[1]
        if tick_who == self.nickname:
            tick_who = "myself"
        msg = f"<b>I tickled {tick_who} and say: GOOD!</b>"

        # send the message
        self.__update_chat_txt("@myself@", msg)
        data = json.dumps(["txt", {"tolist": self.sendtolist}, msg])
        self.socket.sendto(data.encode("utf-8"), self.server_addr)


    def __update_chat_txt(self, name: str, msg: str):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        
        # determine the message color
        if name == "admin":
            color = "red"
        elif name == "@myself@":
            color = "blue"
            name = self.nickname
        else:
            color = "green"

        self.chatlist.append(
            (now_time, name, "txt", msg, color)
        )

        # display
        color_msg = f"<font color='{color}'>{now_time}<br>{name}: {msg}</font><br>"
        self.mui.chatHistory.append(color_msg)
        # print(self.chatlist)

    def __update_chat_fle(self, name: str, fname: str, data: str):
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # determine the message color
        if name == "admin":
            color = "red"
        elif name == "@myself@":
            color = "blue"
            name = self.nickname
        else:
            color = "green"

        # save the file
        msg_path = f"./Download/{name}_{fname}"
        with open(msg_path, "wb+") as f:
            binary_data = b64.b64decode(data)
            f.write(binary_data)
        msg = f"<a href='{msg_path}'>{fname}"

        self.chatlist.append(
            (now_time, name, "fle", msg, color)
        )
        
        color_msg = f"<font color='{color}'>{now_time}<br>{name}: {msg}</font><br>"
        self.mui.chatHistory.append(color_msg)

    def __update_chat_emj(self, name: str, emjcode: int, appdix: str):
        emojis = ["concerned", "facepalm", "smart", "smirk"]
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # determine the message color
        if name == "admin":
            color = "red"
        elif name == "@myself@":
            color = "blue"
            name = self.nickname
        else:
            color = "green"
        
        # see the emjcode
        # determine the sticker
        if 0 <= emjcode <= 3:
            sticker = f"<br><img src='./Resources/emoji_pics/{emojis[emjcode]}.png'>"
        elif emjcode > 3:
            with open(f"./Download/{name}_{emjcode}.sticker", "wb+") as f:
                binary_data = b64.b64decode(appdix)
                f.write(binary_data)
            sticker = f"<br><img src='./Download/{name}_{emjcode}.sticker'>"
        elif emjcode < 0:
            print("Undefined emjcode!")
            pass

        self.chatlist.append(
            (now_time, name, "emj", sticker, color)
        )
        
        # display
        color_msg = f"<font color='{color}'>{now_time}<br>{name}: {sticker}</font><br>"
        self.mui.chatHistory.append(color_msg)
        # print(self.chatlist)

    def __update_onlinelist(self, method: str, who: str):
        if method == "<+>":
            self.onlinelist.append(who)
            self.__update_chat_txt("admin", f"{who} enters chatroom.")
        elif method == "<->":
            self.onlinelist.remove(who)
            self.__update_chat_txt("admin", f"{who} leaves chatroom.")
        else:
            print("Undefined method.")

    def _message_handler(self, jsondata: bytes):
        data_type, from_who, data, appdix = json.loads(jsondata)
        if data_type == "txt":
            print(f"<Plain> {from_who}: {data}")
            self.__update_chat_txt(from_who, data)
        elif data_type == "emj":
            print(f"<Emoji> {from_who}: <emjcode:{data}>")
            self.__update_chat_emj(from_who, data, appdix)
        elif data_type == "ctl":
            print(f"<Control> {from_who}: {data} {appdix}")
            self.__update_onlinelist(data, appdix)
            self._main_disp_online()
        elif data_type == "fle":
            print(f"<File> {from_who}: {data}.")
            self.__update_chat_fle(from_who, data, appdix)

    # Listener for thread receiving data
    # 
    class UpdateChat(QtCore.QObject):
        update_sig = QtCore.pyqtSignal(bytes)
        def __init__(self, socket_: socket.socket) -> None:
            super().__init__()
            self.socket = socket_
            self._connection = True

        def _recv_routine(self):
            while True:
                try:
                    jdata = self.socket.recv(MTU)
                except:
                    print("Stop receving data.")
                    break

                data_type, from_who, data, _ = json.loads(jdata)

                # the exiting flag
                if data_type == "ctl" and from_who == "admin" and data == "\x1b\x1b\x1b\x1b":
                    break
                
                # send signal to main thread
                self.update_sig.emit(jdata)
            # close the socket connection
            self.socket.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = "localhost"
    
    print(host)
    port = 5001

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    dialog = QDialog()
    mainw  = QMainWindow()
    desktop = UDPChatDesktop(dialog, mainw, host, port)
    desktop.run_client()

    sys.exit(app.exec_())