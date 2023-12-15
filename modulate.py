import numpy as np
import scipy as sp

class Modulate:
    """
    调制器
    """
    def __init__(self, Rb, M, fc, fs, x, invert):
        self.Rb = Rb
        self.M = M
        self.Rs = Rb * np.log2(M)
        self.fc = fc
        self.fs = fs
        self.sps = fs / self.Rs
        self.x = x
        self.Symbols = len(x)
        self.N = self.Symbols * self.sps
        self.t = np.arange(0, self.N) / fs
        self.invert = invert
        
    def rcosdesign(self, span, sps, rolloff):
        """
        生成升余弦滤波器，防止分母为0
        :param span: 滤波器长度
        :param sps: 每个符号的采样点数
        :param rolloff: 滚降系数
        """
        if rolloff == 0:
            return np.ones(span)
        elif rolloff > 0 and rolloff < 1:
            t = np.arange(-span / 2, span / 2 + 1) / sps
            x = np.zeros(len(t))
            for i in range(len(t)):
                if t[i] == 0:
                    x[i] = 1
                elif t[i] == rolloff / (2 * sps) or t[i] == -rolloff / (2 * sps):
                    x[i] = np.pi / 4
                else:
                    x[i] = np.sin(np.pi * t[i] * (1 - rolloff) / sps) + 4 * rolloff * t[i] / sps * np.cos(np.pi * t[i] * (1 + rolloff) / sps) / (np.pi * t[i] * (1 - 4 * rolloff ** 2 * t[i] ** 2 / sps ** 2))
            return x
        else:
            print('Rolloff must be between 0 and 1')
            return None
        
    def baseband_shaping_filter(self):
        """
        生成基带滤波器
        """
        # 生成升余弦滤波器
        h = self.rcosdesign(span=10, sps=self.sps, rolloff=0.5)
        x = np.repeat(self.x, self.sps)
        # 生成基带滤波器
        x = np.convolve(x, h)
        return x

    def BPSK(self):
        # 基带成型滤波
        x = self.baseband_shaping_filter()
        x = x[0:int(self.N)]
        # 生成载波
        carrier = np.cos(2 * np.pi * self.fc * self.t + x * np.pi)
        # 相位选择开关 
        carrier = carrier if self.invert == False else -carrier
        # BPSK调制
        y = carrier
        return y
        
        