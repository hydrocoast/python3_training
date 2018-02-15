import numpy as np

def peaks(N=49):
    """ 
    generate DEMO data
    """
    x = np.linspace(-3., 3., N)
    y = np.linspace(-3., 3., N)
    X, Y = np.meshgrid(x, y)
    Z = 3.*(1.-X)**2.*np.exp(-(X**2.)-(Y+1.)**2.) \
       -10.*(X/5.-X**3.-Y**5.)*np.exp(-X**2.-Y**2.) \
       -1./3.*np.exp(-(X+1.)**2.-Y**2.)
    return X, Y, Z

def main():
    # parameters
    nlen = 25
    minXY, maxXY = -3.0, 3.0
    delta = (maxXY - minXY)/float(nlen-1)
    dh = delta/2.
    nContour = 10
    el, az = 20., -130.
    
    # makegrid
    X,Y,Z = peaks(nlen)
    
    # get val
    maxval = np.max(Z)
    minval = np.min(Z)
    maxi, maxj = np.where(Z == np.max(Z))
    mini, minj = np.where(Z == np.min(Z))
    
    # figure 3D
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.plot(X[maxi,maxj], Y[maxi,maxj]+dh, maxval,"o", color="#ffff00", ms=10, mec="k", mew=1.0)
    ax1.plot(X[mini,minj], Y[mini,minj]+dh, minval,"o", color="#00ffff", ms=10, mec="k", mew=1.0)
    ax1.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap='jet')
    ax1.view_init(elev=el,azim=az)
    
    # figure 2D
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    CS = plt.contour(X,Y,Z,nContour, cmap='jet')
    ax2.plot(X[maxi,maxj], Y[maxi,maxj]+dh,"o", mfc="#ffff00", ms=10, mec="k", mew=1.0)
    ax2.plot(X[mini,minj], Y[mini,minj]+dh,"o", mfc="#00ffff", ms=10, mec="k", mew=1.0)
    ax2.axis("image")
    # show figures
    plt.show()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    #import seaborn as sns
    main() 
