import text2bit
import numpy as np
from modulate import Modulate
from awgn import AWGN
from demodulate import Demodulate

Rb = 50  # 比特速率50 bps
M = 2  # 二进制BPSK
Rs = Rb * np.log2(M)  # 码元速率50 bps * log2(2) = 50 bps * 1 = 50 bps
fc = 5e3  # 载波频率5 kHz
fs = 100e3  # 采样频率100 kHz
sps = fs / Rs  # 每个码元采样点数100 kHz / 50 bps = 2000
x = text2bit.text2bit('text.txt')  # 输入二进制数据
Symbols = len(x)  # 二进制数据长度
N = int(Symbols * sps)  # 采样点数
t = np.arange(0, N) / fs  # 时间序列
SNR = [-55, -45, -35, -25, -15, -5, 0, 5, 15]  # 信噪比分别为-5 dB, 0 dB, 5 dB, 15 dB


def main():
    # 实例化调制器
    mod = Modulate(Rb, M, fc, fs, x)
    # BPSK调制
    transmit = mod.BPSK()
    # 通过AWGN信道
    for snr in SNR:
        awgn = AWGN(mod, snr, transmit)
        y = awgn.output()
        # 解调
        demod = Demodulate(y, mod, awgn)
        y = demod.output()
        # 输出解调结果
        output = text2bit.bit2text(y)
        print(f'当信噪比为{snr}dB时，输出为:\n{output}\n误码率为{demod.error_rate()}\n')


if __name__ == '__main__':
    main()
