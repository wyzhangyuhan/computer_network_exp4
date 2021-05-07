import binascii

def endian_change(data):
    return binascii.hexlify(binascii.unhexlify(data)[::-1])

if __name__ == '__main__':
    test = b'12345678'
    res = endian_change(test)
    print(f'原输入数据：{test}')
    print(f'大小端转换后数据：{res}')
    res2 = endian_change(res)
    print(f'原输入数据：{res}')
    print(f'大小端转换后数据：{res2}')