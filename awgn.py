import numpy as np
from modulate import Modulate


class AWGN:
    """
    AWGN信道
    """

    def __init__(self, modulate: Modulate, SNR: float, received_signal: np.ndarray):
        self.modulate = modulate
        self.SNR = SNR
        self.N0 = 1 / (2 * self.modulate.Rb * self.SNR)  # AWGN噪声功率, N0 = 1 / (2 * Rb * SNR)
        self.n = np.random.normal(0, np.sqrt(self.N0 / 2), self.modulate.N)
        self.received_signal = received_signal
        self.y = self.received_signal + self.n

    def noise(self) -> np.ndarray:
        """
        生成高斯白噪声
        """
        return self.n

    def output(self) -> np.ndarray:
        """
        生成AWGN信道输出
        """
        return self.y

