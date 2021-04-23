import socket
import threading as th
import logging
import time
from typing import *

import hashlib
import mysql.connector as sql
import json

PORT = 5001
MTU  = 32*1024

class UDPChatServer: 
    def __init__(self):
        """
        Server Initialization
        """

        # ip address and port
        # hostname = socket.gethostname()
        # ip = socket.gethostbyname(hostname)
        self.addr = ("", PORT)
        
        # connection pool
        self.userlist = {}

        # the first element in connection pool is server itself
        self.userlist[self.addr] = "admin"
        self.onlinelist = []
        
        # start socket server connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.addr)
        
        # database support
        self.db = sql.connect(host="localhost", 
                              user="webchatTest", 
                              passwd="webchatroom",
                              database="webchatroom")
        self.db_cursor = self.db.cursor()

    def _txt_send(self, addr: Tuple[str, int], data: str, tolist: List):
        """
        Send the normal text to other users
        @data: the data to send
        @tolist: indicating who to send. tolist=[] if send to all.
        @addr: (IP, port) of user
        """

        nickname = self.userlist[addr]
        print(f"...\n{addr} send: {data}\n[server@udp]>> ", end="")

        # the response data: [<data_type>, <who_send>, <data>]
        json_data = json.dumps(["txt", nickname, data, [] ])
        
        # if $tolist is empty list, then send to all.
        if tolist == []:
            # send data to all user
            for each_addr in self.userlist:
                if each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)
        else:
            # send data to user in tolist
            for each_addr, name in self.userlist.items():
                if name in tolist and each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)

    def _fle_send(self, addr: Tuple[str, int], filename: str, data: str, tolist: List):
        """
        
        """
        nickname = self.userlist[addr]
        print(f"...\n{addr} send: {data}\n[server@udp]>> ", end="")

        # the response data: [<data_type>, <who_send>, <data>]
        json_data = json.dumps(["fle", nickname, filename, data])
        
        # if $tolist is empty list, then send to all.
        if tolist == []:
            # send data to all user
            for each_addr in self.userlist:
                if each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)
        else:
            # send data to user in tolist
            for each_addr, name in self.userlist.items():
                if name in tolist and each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)


    def _ctl_onlinelist(self, method: str, obj: str):
        if method not in ["<+>", "<->"]:
            print("...\nUnknown online list control method.\n[server@udp]>> ", end="")
            return
        jdata = json.dumps(["ctl", "admin", method, obj])

        # send to each online user
        for each_addr in self.userlist:
            if each_addr != self.addr:
                self.server.sendto(jdata.encode("utf-8"), each_addr)

    def _ctl_exit(self, addr: Tuple[str, int]):
        """
        Handle the exiting client
        @addr: (IP, port) of exiting user
        """

        # log information
        print(f"...\n<Control-Exit> from {addr} \n[server@udp]>> ", end="")
        nickname = self.userlist[addr]

        # pop out this guy
        self.userlist.pop(addr)
        self.onlinelist.remove(nickname)
        
        # send exiting confirmation
        exit_cmd = json.dumps(["ctl", "admin", "\x1b\x1b\x1b\x1b", [] ])
        self.server.sendto(exit_cmd.encode("utf-8"), addr) # exitng signal

        # brodcast to other user that someone has left
        self._ctl_onlinelist("<->", nickname)

    def _ctl_auth(self, addr: Tuple[str, int], name: str, passwd: str):
        """
        Authentication for user
        @name: username of user
        @passwd: the password
        @addr: (IP, port) of user
        """
        print(f"...\n{addr} send: {name}<sep><password>\n[server@udp]>> ", end="")
        try:
            # this account has been online
            if name in self.onlinelist:
                auth_data = json.dumps(["ctl", "admin", "\x02\x02\x02\x02", [] ]) # fail to auth
                self.server.sendto(auth_data.encode("utf-8"), addr)
            # authentication with database
            # and send authentication info to the requesting user
            user_id = self.__user_id(name, passwd)
            if user_id is None:
                auth_data = json.dumps(["ctl", "admin", "\x00\x00\x00\x00", [] ]) # fail to auth
                self.server.sendto(auth_data.encode("utf-8"), addr)
            else:
                auth_data = json.dumps(["ctl", "admin", "\x01\x01\x01\x01", self.onlinelist]) # success
                self._ctl_onlinelist("<+>", name) # broadcast to others that someone comes
                self.server.sendto(auth_data.encode("utf-8"), addr)
                self.userlist[addr] = name
                self.onlinelist.append(name)
            
        except Exception as e:
            # exception handling
            # send failure signal to the requesting user
            print(f"...\n{e}\n[server@udp]>> ", end="")
            auth_data = json.dumps(["ctl", "admin", "\x01\x01\x01\x01", [] ])
            self.server.sendto(auth_data.encode("utf-8"), addr) # fail
    
    def _emj_builtin(self, addr: Tuple[str, int], emjcode: int, tolist: List):
        nickname = self.userlist[addr]
        print(f"...\n{addr} send: <emjcode:{emjcode}>\n[server@udp]>> ", end="")

        # the response data: [<data_type>, <who_send>, <data>, <appendix>]
        json_data = json.dumps(["emj", nickname, emjcode, [] ])
        
        # if $tolist is empty list, then send to all.
        if tolist == []:
            # send data to all user
            for each_addr in self.userlist:
                if each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)
        else:
            # send data to user in tolist
            for each_addr, name in self.userlist.items():
                if name in tolist and each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)

    def _emj_diypic(self, addr: Tuple[str, int], filename: str, data: str, tolist: List):
        """
        
        """
        nickname = self.userlist[addr]
        print(f"...\n{addr} send: {data}\n[server@udp]>> ", end="")

        # the response data: [<data_type>, <who_send>, <data>, <appendix>]
        emjcode = int(hashlib.md5((nickname + filename).encode("utf-8")).hexdigest()[:7], base=16)
        emjcode = abs(emjcode) + 4
        json_data = json.dumps(["emj", nickname, emjcode, data])
        
        # if $tolist is empty list, then send to all.
        if tolist == []:
            # send data to all user
            for each_addr in self.userlist:
                if each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)
        else:
            # send data to user in tolist
            for each_addr, name in self.userlist.items():
                if name in tolist and each_addr != addr and each_addr != self.addr:
                    self.server.sendto(json_data.encode("utf-8"), each_addr)

    def parse_execute(self, addr: Tuple[str, int], byte_data: bytes):
        """
        Parse the data from clients.
        @data: received byte data, which is in form of json:
               [<data_type>, {data_pars}, <data>]
               where <data_type> can be 'txt', 'emj', 'fle', 'ctl' (or others for future)
        """
        try:
            # get data_type, parameters, data from json data
            data_type, data_pars, data = json.loads(byte_data)

            # plain text data
            if data_type == "txt":
                tolist = data_pars["tolist"]
                self._txt_send(addr, data, tolist)
            # emoji data
            # including built-in emoji, and DIY image.
            elif data_type == "emj":
                tolist = data_pars["tolist"]
                emj_t  = data_pars["type"]
                if emj_t == "bti":
                    self._emj_builtin(addr, data, tolist)
                elif emj_t == "diy":
                    fname = data_pars["fname"]
                    self._emj_diypic(addr, fname, data, tolist)
                else:
                    logging.warning("Undefined emoji format.")
            # controling data
            # i.e. exit, auth
            elif data_type == "ctl":
                ctl_t = data_pars["type"]
                if ctl_t == "auth":
                    usrname = data_pars["name"]
                    passwd  = data_pars["pass"]
                    self._ctl_auth(addr, usrname, passwd)
                elif ctl_t == "exit":
                    self._ctl_exit(addr)
                else:
                    logging.warning("Undefined control command")
            # file data
            # binary encoding transforming.
            elif data_type == "fle":
                tolist = data_pars["tolist"]
                fname  = data_pars["fname"]
                self._fle_send(addr, fname, data, tolist)
            
        except Exception as e:
            print(e)
            print(byte_data)
            logging.warning("Invalid data format!")

    def _message_handler(self):
        """
        Handling message from clinets
        """
        while True:
            try:
                # obtain json data and address
                data, addr = self.server.recvfrom(MTU)

                # if the data is from a fresh user
                self.parse_execute(addr, data)

            # exception of connection error
            except Exception as e:
                print("...")
                logging.warning(f'{e}\n[server@udp]>> ')

    def __message_handler_old(self):
        """
        Abandoned
        """
        while True:
            try:
                # obtain data
                data, addr = self.server.recvfrom(MTU)
                data = data.decode("utf-8")

                # if the data is from a fresh user
                # first do authentication
                # then register the new user into connection pool
                if not addr in self.userlist:
                    # authentication
                    # query SQL database to check the validation of username-password pair
                    try:
                        name, passwd = data.split("|@@|")
                        print(f"...\n{addr} send: {name}<sep><password>\n[server@udp]>> ", end="")
                        user_id = self.user_id(name, passwd)
                        if user_id is None:
                            self.server.sendto(b"\000\000\000\000", addr) # fail to auth
                            continue
                        else:
                            self.server.sendto(b"\001\001\001\001", addr) # success
                    except:
                        print("...")
                        logging.warning("Invalid user-password pair")
                        print("[server@udp]>> ", end="")
                        self.server.sendto(b"\000\000\000\000", addr) # fail
                        continue
                    
                    # broadcast this new guy coming
                    for each_addr in self.userlist:
                        self.server.sendto(f"<Notice>: {name} enter chatroom.".encode("utf-8"), each_addr)
                    self.userlist[addr] = name

                # if the data is special commands
                elif data[0] == '-':
                    udp_args = data.split("-")
                    nickname = self.userlist[addr]
                    print(f"...\n{addr} send: {data}\n[server@udp]>> ", end="")

                    # if the command is "-exit", then pop out the user
                    # and brodcast his exiting to others
                    if len(udp_args) == 2 and udp_args[1] == "exit":
                        self.userlist.pop(addr)
                        self.server.sendto(b"\033\033\033", addr) # exitng signal
                        for each_addr in self.userlist:
                            self.server.sendto(f"<Notice>: {nickname} exit chatroom.".encode("utf-8"), each_addr)

                    # if the command is "-sendto-[username]-[msg]",
                    # then only send this msg to that user
                    elif len(udp_args) == 4 and udp_args[1] == "sendto":
                        for each_addr, name in self.userlist.items():
                            if name == udp_args[2]:
                                self.server.sendto(f"<Only you msg> {nickname}: {udp_args[3]}".encode("utf-8"), each_addr)
                                break
                    else:
                        self.server.sendto("Invalid command.".encode("utf-8"), each_addr)

                # otherwise, normal information
                # brodcast the information to others
                else:
                    nickname = self.userlist[addr]
                    print(f"...\n{addr} send: {data}\n[server@udp]>> ", end="")
                    for each_addr in self.userlist:
                        if each_addr != addr:
                            self.server.sendto(f"{nickname}: {data}".encode("utf-8"), each_addr)

            # exception of connection error
            except ConnectionResetError:
                print("...")
                logging.warning('Connection exception.\n')
                print("[server@udp]>> ", end="")

    def __user_id(self, name: str, passwd: str):
        """
        User identification
        @name: username
        @passwd: password
        """
        # query the entry of the user-password pair
        passwd_hash = hashlib.md5(passwd.encode("utf-8")).hexdigest()
        sql_query = f"SELECT `id` FROM `user` WHERE `password_hash`='{passwd_hash}' AND `username`='{name}'"
        self.db_cursor.execute(sql_query)
        result = self.db_cursor.fetchall()

        if len(result) > 0:
            return result
        else:
            return None

    def server_run(self):
        """
        Run the UDP server
        """
        print("==== UDP Chatroom Server ====")
        print("Server starting...")
        print("Start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f"Server IP: {self.addr[0]}:{self.addr[1]}")
        print("==== UDP Chatroom Server ====")

        thread = th.Thread(target=self._message_handler)
        thread.setDaemon(True)
        thread.start()

        while True:
            cmd = input("[server@udp]>> ")
            if cmd == "num-online":
                print("online:", len(self.userlist))
            elif cmd == "who-online":
                print("online user list:")
                for addr, name in self.userlist.items():
                    print(addr, name)
            elif cmd == "exit":
                break

        print("==== UDP Chatroom Server ====")
        print("Server exiting...")
        print("==== UDP Chatroom Server ====")            

if __name__ == "__main__":
    server = UDPChatServer()
    server.server_run()