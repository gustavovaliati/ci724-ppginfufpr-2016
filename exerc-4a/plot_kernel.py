import numpy as np
import datetime
import scipy.stats as st
import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt

def gkern(kernlen=21, nsig=5):

    interval = (2*nsig+1.)/(kernlen)
    x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()
    return kernel

plt.plot(gkern(21))
plt.savefig("./kernel{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")))
