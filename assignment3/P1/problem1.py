import numpy as np
import matplotlib.pyplot as plt


def SRW(N):
    """
    SRW(N) = Sn = X1 + .. + XN
    """
    x = [1, -1]
    Sn = np.sum([np.random.choice(x) for i in range(N)])
    return Sn


def SRW_normal(N):
    return SRW(N) / np.sqrt(N)


def histogram_plot_data(N, M):
    Sn_norm_values = [SRW_normal(N) for i in range(M)]
    return Sn_norm_values


plt.hist(histogram_plot_data(1000, 50), bins="auto")
plt.show()
