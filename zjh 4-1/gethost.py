'''
Author: your name
Date: 2021-04-07 08:33:02
LastEditTime: 2021-04-09 21:12:48
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \4-1\gethost.py
'''

import socket

def getMyHost():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return (hostname, ip)

def getHostByName(hostname: str):
    (name, aliases, addr) = socket.gethostbyname_ex(hostname)
    return (name, aliases, addr)

def printnslook(hostname: str):
    (name, aliases, addr) = getHostByName(hostname)
    print("Name: ", name)
    print("Aliases: ", aliases)
    print("IP: ", addr, end="\n\n")

if __name__ == "__main__":
    print("Current name and IP of my PC:", end=" ")
    print(getMyHost(), end="\n\n")
    printnslook("baidu.com")
    printnslook("csdn.net")
    printnslook("google.com")