import urllib
import getweather
import numpy as np
import matplotlib.pyplot as pp
pp.rc('text', usetex=True)

urllib.request.urlretrieve('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt', 'readme.txt')
urllib.request.urlretrieve('https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt', 'stations.txt')

stations = np.genfromtxt('stations.txt', delimiter=[11,9,10,7,3,31,4,4,6],
                                         names=['id','latitude','longitude','elevation','state','name','gsn','hcn','wmo'],
                                         dtype=['U11','d','d','d','U3','U31','U4','U4','U6'],
                                         autostrip=True)

# pp.show(pp.plot(stations['longitude'], stations['latitude'], '.', markersize=1))

def fillnans(array):            # handling the missing data
    x = np.arange(len(array))
    good = ~np.isnan(array)     # ~ takes the array as binary and flips all bits to obtain the complement, performing logical negation on each bit
    return np.interp(x, x[good], array[good])

# Data smoothing - enhancing signal over noise (without biasing the information)
# Here we use a so-called "box filter": mask with positive entries that sum up to 1
# This replaces  each value with an average of its neighborhood

def smooth(array, window=10, mode='valid'):     # window = lenght of the smoothing mask for cross-correlation
    return np.correlate(array, np.ones(window)/window, mode)

def plotsmooth(station, year):
    station_data = getweather.getyear(station, ['TMIN','TMAX'], year)

    for obs in ['TMIN','TMAX']:
        station_data[obs] = fillnans(station_data[obs])
        pp.plot(station_data[obs], '.', ms=1)
        pp.plot(range(10,356), smooth(station_data[obs], 20), label=f'{obs} in {station} ({year})')
        # pp.title(f'{station}, {year}')

        # We used a window of 20 days, so the range can just be from day 10 to day 356 of the year

    pp.axis(xmin=1, xmax=365, ymin=-5, ymax=40)
    pp.xlabel(r'$\textit{days}$')
    pp.ylabel(r'$^\circ C$')
    # pp.legend(loc='lower center', ncol=3, frameon=False, prop={'size': 8})

for k in range(3):
    plotsmooth('ROMA CIAMPINO', 1960+(20*k))

pp.figure(figsize=(12,9))

for i, city in enumerate(['NEW ORLEANS','NEW YORK','SAN DIEGO','MINNEAPOLIS']):
    pp.subplot(2,2,i+1)
    plotsmooth(city,2019)
    pp.legend(loc='lower center', frameon=False, prop={'size': 7})

pp.show()
