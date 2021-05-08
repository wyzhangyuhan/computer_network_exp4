import struct
import binascii

def endian_check():
    var = 0x12345678
    pk = struct.pack('i', var)
    if pk[0] == 0x12:
        return "BE"
    elif pk[0] == 0x78:
        return "LE"

def utf32_encode(data: str):
    endian = endian_check()
    if   endian == "LE":
        return data.encode("utf-32le")
    elif endian == "BE":
        return data.encode("utf-32be")

def utf32_decode(data: bytes):
    endian = endian_check()
    if   endian == "LE":
        return data.decode("utf-32le")
    elif endian == "BE":
        return data.decode("utf-32be")

def endian_change(data):
    return binascii.hexlify(binascii.unhexlify(data)[::-1])