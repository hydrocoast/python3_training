import os
import numpy as np
import matplotlib.pyplot as plt
from  scipy import fftpack, io

def load_matfile(matname):
    matdata = io.loadmat(matname, squeeze_me=True)
    nt, nz = matdata["nt"], matdata["nz"]
    dt = matdata["dt"]
    z, u = matdata["z"], matdata["u"]
    return (nt, nz, dt, z, u)

def read_txtfile(txtfilename):
    with open(txtfilename, 'r') as f:
        header1 = f.readline()
        header2 = f.readline()
        header3 = f.readline()
    nt, nz = [ int(x) for x in header1.split()]
    dt = float(header2)
    z = np.array(header3.split())
    u = np.loadtxt(txtfilename, skiprows=3)
    return (nt, nz, dt, z, u)

def remove_noise(nt, dt, dataorg):
    # Fourier tranform
    F0 = fftpack.fft(dataorg)
    freq = fftpack.fftfreq(nt, d=dt)
    power = np.abs(F0/(nt/2.))
    # frequency cut off
    #fc = 1./dt
    fc = 0.10
    F0[(freq > fc)] = 0.
    F0[(freq < 0.)] = 0.
    # Inverse Fourier transform
    data = np.real(fftpack.ifft(F0))
    return (freq, power, data)

def drawfig(nt, dt, data1, data2, freq, power):
    tline = np.linspace(0,(nt-1)*dt,nt)
    # figure1: 1st layer of u
    fig1 = plt.figure(figsize=(18,6))
    ax1 = fig1.add_subplot(111)
    ax1.plot(tline, data1,'b-')
    ax1.plot(tline, data2, 'r-', lw=2.5)
    ax1.axis('tight')
    ax1.grid(which='major',color=[0.2,0.2,0.2],linestyle='-')
    ax1.set_xlabel('time [s]',fontsize=18)
    ax1.set_ylabel('wind speed [m/s] ',fontsize=18)

    # figure2: power spectrum density
    fig2 = plt.figure(figsize=(12,6))
    ax2 = fig2.add_subplot(111)
    ax2.loglog(freq[(freq>0.)], power[(freq>0.)],'b-')
    ax2.grid(which='major',color=[0.2,0.2,0.2],linestyle='-')
    ax2.grid(which='minor',color=[.75,.75,.75],linestyle='-',axis='x')
    ax2.set_xlabel('Frequency f [Hz]',fontsize=18)
    ax2.set_ylabel('P(f) [$\mathsf{m^2/s^2}$]',fontsize=18)
    ax2.set_ylim(1.0E-5,1.0E+01)

def main(form):
    fdir = "./data"
    if form == 'mat':
        fname = "crf_wind.mat"
        nt, nz, dt, z, u = load_matfile(os.path.join(fdir,fname))
    elif form == 'txt':
        fname = "crf_wind.dat"
        nt, nz, dt, z, u = read_txtfile(os.path.join(fdir,fname))
    freq, power, umod = remove_noise(nt, dt, u[0,:])
    drawfig(nt, dt, u[0,:], umod, freq, power)

if __name__ == "__main__":
    #main("txt")
    main("mat")
    plt.show()
