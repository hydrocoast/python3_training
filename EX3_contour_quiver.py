import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from EX1_peaks_surf import peaks
#import seaborn as sns

def setlabels(axes, FS):
    axes.set_xlabel('X-axis',fontsize=FS)
    axes.set_ylabel('Y-axis',fontsize=FS)
    axes.axis('scaled')

def main():
    # parameters
    nlen = 25
    nContour = 14
    # appearances
    FS = 14
    cmin, cmax = -6., 8.
    # makegrid
    (X,Y,Z) = peaks(nlen)
    # gradient
    Fy,Fx = np.gradient(Z)
    Fxy,Fxx = np.gradient(Fx)
    Fyy,Fyx = np.gradient(Fy)
    
    # figure contour & quiver
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    CS1 = ax1.contour(X,Y,Z,nContour, cmap='jet')
    #ax1.clabel(CS1, np.arange(cmin, cmax, 2))
    Q = ax1.quiver(X,Y,-Fx,-Fy, angles='xy')
    ax1.quiverkey(Q,0.5,.93,1,'1.0',labelpos='E',coordinates='figure')
    setlabels(ax1, FS)
    
    # figure contourf
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    CS2 = ax2.contourf(X,Y,Z,np.linspace(cmin,cmax,nContour+1), extend='both', cmap='jet')
    Q = ax2.quiver(X,Y,Fxx,Fyy, angles='xy')
    ax2.quiverkey(Q,0.5,.93,1,'1.0',labelpos='E',coordinates='figure')
    setlabels(ax2, FS)
    cbar = fig2.colorbar(CS2)
    cbar.ax.set_xlabel('Z')

    # save figure
    #fig1.savefig('contourf_test.png',format='png',dpi=600)
    #fig1.savefig('contourf_test.eps',format='eps',dpi=600)
    fig1.savefig('contourf_test.svg',format='svg')
 
if __name__ == '__main__':
    main()
    plt.show()

