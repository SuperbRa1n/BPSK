import numpy as np
from modulate import Modulate
import matplotlib.pyplot as plt

Rb = 50 # 比特速率50 bps
M = 2 # 二进制BPSK
Rs = Rb * np.log2(M) # 码元速率50 bps * log2(2) = 50 bps * 1 = 50 bps
fc = 5e3 # 载波频率5 kHz
fs = 10e3 # 采样频率100 kHz
sps = fs / Rs # 每个码元采样点数100 kHz / 50 bps = 2000
x = [0b1, 0b0, 0b0, 0b0, 0b1, 0b1, 0b1, 0b0, 0b1, 0b1, 0b1, 0b0] # 输入二进制数据
Symbols = len(x) # 二进制数据长度
N = int(Symbols * sps) # 采样点数
t = np.arange(0, N) / fs # 时间序列

def main():
    # 实例化调制器
    mod = Modulate(Rb, M, fc, fs, x, invert=False)
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
    plt.plot(t, np.repeat(x, sps))
    plt.figure(3)
    plt.plot(mod.baseband_shaping_filter())
    plt.figure(4)
    plt.plot(mod.rcosdesign(span=10, sps=sps, rolloff=0.5))
    plt.show()
if __name__ == '__main__':
    main()