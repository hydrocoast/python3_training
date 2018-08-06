import os, sys
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from numpy import genfromtxt

def main():
    # parameters
    fdir = './data'
    fname = 'windspeed.dat'
    extend_years = np.linspace(2001.,2100.,100)
    # load data
    if not os.path.isfile(os.path.join(fdir,fname)):
        print("Not exist, FILE:"+os.path.join(fdir,fname))
        sys.exit()
    #dat = np.loadtxt(os.path.join(fdir,fname), delimiter=' ', skiprows=0, dtype='float')
    dat = genfromtxt(os.path.join(fdir,fname), delimiter=' ', skip_header=0, dtype='float')
    # arrange
    years, avg_w, std_w = dat[:,0], dat[:,1], dat[:,2]
    # regression
    pl = np.polyfit(years,avg_w,1)
    pq = np.polyfit(years,avg_w,2)

    # figure plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    hd1 = ax.plot(years, avg_w,'o', mec='b', mfc='none', mew=2., ms=8.)
    hd2 = ax.plot(years, np.polyval(pl,years),'-', c='g', lw=2.)
    hd3 = ax.plot(years, np.polyval(pq,years),'-', c='#ff4500', lw=2.)
    ax.plot(extend_years, np.polyval(pl,extend_years), '--', c='g', lw=2.)
    ax.plot(extend_years, np.polyval(pq,extend_years), '--', c='#ff4500', lw=2.)
    ax.grid(which='major', color='#808080', linestyle='--')
    ax.set_xlabel('year', fontsize=14, fontdict={"name":"serif"})
    ax.set_ylabel('wind speed [m/s]', fontsize=15, fontname='serif')
    ax.legend(['raw data','linear','quadratic'], loc=3)
    #fig.savefig('regressions.svg',format='svg')
 
if __name__ == '__main__':
    main()  
    plt.show()
