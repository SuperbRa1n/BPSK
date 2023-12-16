import numpy as np
from modulate import Modulate
import matplotlib.pyplot as plt
from awgn import AWGN
from demodulate import Demodulate

Rb = 50  # 比特速率50 bps
M = 2  # 二进制BPSK
Rs = Rb * np.log2(M)  # 码元速率50 bps * log2(2) = 50 bps * 1 = 50 bps
fc = 5e3  # 载波频率5 kHz
fs = 100e3  # 采样频率100 kHz
sps = fs / Rs  # 每个码元采样点数100 kHz / 50 bps = 2000
x = [0b1, 0b0, 0b0, 0b0, 0b1, 0b1, 0b1, 0b0, 0b1, 0b1, 0b1, 0b0]  # 输入二进制数据
Symbols = len(x)  # 二进制数据长度
N = int(Symbols * sps)  # 采样点数
t = np.arange(0, N) / fs  # 时间序列
SNR = 10 * np.log10(1 / 0.01)  # 信噪比10 dB


def main():
    # 实例化调制器
    mod = Modulate(Rb, M, fc, fs, x)
    # BPSK调制
    y = mod.BPSK()
    # 绘制调制后的波形
    plt.figure(1)
    plt.plot(t, y)
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title('BPSK Modulation')
    # 绘制信号的时域波形
    plt.figure(2)
    plt.plot(t, mod.baseband_shaping_filter())
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title('Baseband Shaping Filter')
    # 通过AWGN信道
    awgn = AWGN(mod, SNR, y)
    y = awgn.output()
    # 绘制通过AWGN信道后的波形
    plt.figure(3)
    plt.plot(t, y)
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title('BPSK Modulation Through AWGN Channel')
    # 解调
    demod = Demodulate(y, mod, awgn)
    y = demod.integrator()
    # 绘制解调后的波形
    plt.figure(4)
    plt.plot(y)
    plt.xlabel('Time(s)')
    plt.ylabel('Amplitude')
    plt.title('BPSK Demodulation')
    # 输出解调结果
    print(demod.output())
    plt.show()


if __name__ == '__main__':
    main()
