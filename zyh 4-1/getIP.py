import socket

## 获取本地机名称和IP地址
def getlocal_info():
    hostname = socket.gethostname() # 获取本机计算机名称
    ip = socket.gethostbyname(hostname) # 获取本机ip
    str = '本地机名称为：' + hostname + '\n本机IP为：' + ip; 
    print(str)


##获取网站的所有IP地址
def getweb_info(url):
    ip_list = [] #保存所有ip的list
    try: #异常检测
        addr = socket.getaddrinfo(url,None)
        for i in addr:
            if i[4][0] not in ip_list:
                ip_list.append(i[4][0])
    except Exception as exc:
        print(exc)
    
    print(f'当前网站 "{url}" 所含的所有IP地址为: ')

    for i in range(len(ip_list)):
        info = str(i) + ': ' + ip_list[i]
        print(info)


if __name__ == '__main__':
    getlocal_info() #获取本机
    url = 'www.baidu.com'   
    getweb_info(url)
    url = 'www.csdn.net'
    getweb_info(url)
    url = 'www.google.com'
    getweb_info(url)
    
