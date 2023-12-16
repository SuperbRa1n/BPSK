import numpy as np


def text2bit(file_name: str) -> list:
    """
    读取文本文件, 将文本转换为二进制比特流
    """
    with open(file_name, 'r') as f:
        text = f.read()
    return list(map(int, ''.join([bin(ord(item))[2:].zfill(8) for item in text])))


def bit2text(bit: list) -> str:
    """
    将二进制比特流转换为文本
    """
    return ''.join([chr(int(''.join(map(str, bit[i:i + 8])), 2)) for i in range(0, len(bit), 8)])


