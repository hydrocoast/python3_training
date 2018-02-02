import os
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime

def AxesFormats(axes):
    # ticks
    xticks = np.arange(0., 360.1, 60. )
    xticklabels = np.append(np.arange(0, 181, 60), np.arange(-120, 1, 60))
    yticks = np.arange(-90., 90.1, 30.)
    # formats
    axes.axis('scaled')
    axes.set_xlim(0., 360.)
    axes.set_ylim(-90., 90.)
    axes.set_xticks(xticks)
    axes.set_xticklabels(xticklabels)
    axes.set_yticks(yticks)
    axes.set_xlabel('Longitude')
    axes.set_ylabel('Latitude')

def CBFormats(fig, PC):
    # colorbar formats
    PC.set_clim(0.,15.)
    cbar = fig.colorbar(PC, ticks=np.linspace(0.,15.,7))
    cbar.ax.set_ylabel('wind speed [m/s]')

def update_pcolor(it, axes, X, Y, pcdata, time_in_datetime):
    PC = axes.pcolor(X, Y, pcdata[it,:,:], cmap='jet')
    PC.set_clim(0.,15.)
    axes.set_title(time_in_datetime[it].strftime('%Y/%m'))
    print(it, '/', pcdata.shape[0])

def getncfile(url, destination):
    import wget
    wget.download(url)
    filename = os.path.basename(url)
    os.rename(filename, destination)

def main():
    # read netCDF file
    ncfile = './data/wspd.mon.mean.nc'
    # if not exist
    if not (os.path.isfile(ncfile)):
        url='http://database.rish.kyoto-u.ac.jp/arch/ncep/data/ncep.reanalysis.derived/surface/wspd.mon.mean.nc'
        getncfile(url, ncfile)
    ncdata = netCDF4.Dataset(ncfile, 'r', format='NETCDF4')
    # get variables
    time = ncdata.variables['time'][:]
    wspd = ncdata.variables['wspd'][:]
    lon, lat =  ncdata.variables['lon'][:],  ncdata.variables['lat'][:]
    # get data size and resion
    nt = wspd.shape[0]
    lon, lat = np.meshgrid(lon,lat)
    # arrange time lines
    days_1800to1900 = 36524
    thours = [datetime.timedelta(hours=time[k]-(days_1800to1900)*24.) for k in np.arange(0, nt, 1) ]
    time_arranged = [datetime.datetime(1900,1,1) + thours[k] for k in np.arange(0, nt, 1)]
    # draw figure
    fig = plt.figure(figsize=(8,4))
    ax = fig.add_subplot(111)
    PC = ax.pcolor(lon, lat, wspd[0,:,:], cmap='jet')
    # setting into specific formats
    AxesFormats(ax)
    CBFormats(fig, PC)
    # make and save movie
    #ani = animation.FuncAnimation(fig, update_pcolor, fargs=(ax, lon, lat, wspd, time_arranged), interval=100, frames = nt)
    ani = animation.FuncAnimation(fig, update_pcolor, fargs=(ax, lon, lat, wspd, time_arranged), interval=400, frames = 24)
    ani.save("wspd.gif", writer='imagemagick')

if __name__ == '__main__':
    main()

