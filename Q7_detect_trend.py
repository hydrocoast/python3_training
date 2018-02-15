import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy import signal, interpolate
from dateutil.parser import parse

def read_csv(filename):
    # read csvdata
    with open(filename,'r') as f:
        header = f.readline()
        dataorg = [k for k in csv.reader(f)]
    dataorg = np.array(dataorg)
    timestr = dataorg[:,0]
    val = dataorg[:,1]
    # str2date
    timep = [parse(k) for k in timestr]
    return(timep,val)

def interpval(timep,val):
    # total days from the first date in data
    dt_days = [((timep[k]-timep[0]).total_seconds())/86400.0 \
                 for k in range(0,len(timep))]
    # interpolation
    dt_days_i = np.arange(dt_days[0],dt_days[-1],1)
    timeinterp = [timep[0]+datetime.timedelta(days=k) \
                  for k in range(0,len(dt_days_i))] 
    Fv = interpolate.interp1d(dt_days,val)
    valinterp = Fv(dt_days_i)
    # polyfit and polyval
    coef = np.polyfit(dt_days_i, valinterp, 1)
    valreg = np.polyval(coef,dt_days_i)
    return(timeinterp, valinterp, coef, valreg)

def getPSD(xdate,yval,dt=1.):
    # pwelch
    n = yval.size
    fs = 1./dt
    freq, PD = signal.welch(yval, fs, nperseg=700)
    return (freq, PD)

def draw_lines(axes, xdate, yval, yval2):
    # data plot
    axes.plot(xdate,yval,'r-')
    axes.plot(xdate,yval2,'b--')
    # formats
    axes.grid(which='major',color=[.5,.5,.5],linestyle='-')
    axes.set_xlabel('year', fontsize=18)
    axes.set_ylim(62,71)
    axes.set_xlim(datetime.datetime(2011,1,1),datetime.datetime(2017,1,1))

def draw_PSD(axes, freq, PD):
    # PSD
    ind_over0 = np.where(freq > 0)
    per = 1./freq[ind_over0]
    axes.semilogx(per, PD[ind_over0], "c", label="PSD")
    
    # periods
    ind_rmax = signal.argrelmax(PD,order=1)[0][0:2]
    nper = 1./freq[ind_rmax]
    axes.semilogx(nper, PD[ind_rmax], "ro", ms=8., label="Period(s)")
    
    # formats
    axes.legend(loc="upper left", fontsize=14)
    axes.grid(which='major', color=[.3,.3,.3], linestyle='-')
    axes.grid(which='minor', color=[.5,.5,.5], linestyle='--')
    axes.set_xlim(1,1e4)
    axes.set_xlabel("cycle [days]", fontsize=18)
    axes.set_ylabel("Power spectral density", fontsize=18)

def main():
    plt.close('all')
    # basic setup
    fdir = './data'
    fname = 'dat_climate.csv'

    # get key parameters
    timep, val = read_csv(os.path.join(fdir,fname))
    timeinterp, valinterp, _, valreg = interpval(timep,val)
    freq, PSD = getPSD(timeinterp, valinterp)

    # figures
    fig =  plt.figure(figsize=(12,16))
    draw_lines(fig.add_subplot(211), timeinterp, valinterp, valreg)
    draw_PSD(fig.add_subplot(212), freq, PSD)
    plt.show()

if __name__ == "__main__":
    main()
