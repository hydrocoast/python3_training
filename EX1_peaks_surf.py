"""
Question 1
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# import seaborn as sns


def peaks(n=49):
    """ 
    input
    -----------------
    n : int
        meshsize
    """
    x = np.linspace(-3., 3., n)
    y = np.linspace(-3., 3., n)
    xx, yy = np.meshgrid(x, y)
    zz = 3. * (1. - xx) ** 2. * np.exp(-(xx ** 2.) - (yy + 1.) ** 2.) \
         -10. * (xx / 5. - xx ** 3. - yy ** 5.) * np.exp(-xx ** 2. - yy ** 2.) \
         -1. / 3. * np.exp(-(xx + 1.) ** 2. - yy ** 2.)
    return xx, yy, zz


def main():
    # parameters
    NLEN = 25
    MIN_XY, MAX_XY = -3.0, 3.0
    DELTA = (MAX_XY - MIN_XY) / (NLEN - 1)
    DH = DELTA / 2.
    NCONTOUR = 10
    EL, AZ = 20., -130.

    # makegrid and elevation
    xx, yy, zz = peaks(NLEN)

    # get max/min values and their locations
    maxval = np.max(zz)
    minval = np.min(zz)
    maxi, maxj = [np.argmax(zz) // NLEN], [np.argmax(zz) % NLEN]
    mini, minj = [np.argmin(zz) // NLEN], [np.argmin(zz) % NLEN]

    # figure 3D
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.plot(xx[maxi, maxj], yy[maxi, maxj] + DH, maxval, "o",
             color="#ffff00", ms=10, mec="k", mew=1.0)
    ax1.plot(xx[mini, minj], yy[mini, minj] + DH, minval, "o",
             color="#00ffff", ms=10, mec="k", mew=1.0)
    ax1.plot_surface(xx, yy, zz, rstride=1, cstride=1, cmap='jet')
    ax1.view_init(elev=EL, azim=AZ)

    # figure 2D
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    plt.contour(xx, yy, zz, NCONTOUR, cmap='jet')
    ax2.plot(xx[maxi, maxj], yy[maxi, maxj] + DH, "o",
             mfc="#ffff00", ms=10, mec="k", mew=1.0)
    ax2.plot(xx[mini, minj], yy[mini, minj] + DH, "o",
             mfc="#00ffff", ms=10, mec="k", mew=1.0)
    ax2.axis("image")

    # show figures
    plt.show()
    plt.close()

if __name__ == '__main__':
    main()
