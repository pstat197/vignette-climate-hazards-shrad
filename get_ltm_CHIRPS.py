
# coding: utf-8

# This script analyzes CHIRTS for quality control, missing data etc.

# In[ ]:


from __future__ import division
import pandas as pd
import numpy as np
from Shrad_modules import read_nc_files, MAKEDIR
import calendar
from matplotlib import pyplot as plt
import matplotlib as mpl
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import time
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import xarray as xr


# In[ ]:


# IMERG Directories and infile template
CHIRPS_infile = '/home/GPM/IMERG/v05/daily/CHIRPS_on_Imerg_grid/chirps-v2.0.*'


# In[ ]:
CHIRPS = xr.open_mfdataset(CHIRPS_infile, autoclose=True, chunks={'lat':1000, 'lon':1000})
print ("Finished reading files")

COND1 = (((CHIRPS.coords['time.year']==2014) & (CHIRPS.coords['time.month']==3) & (CHIRPS.coords['time.day']>=12)) | ((CHIRPS.coords['time.year']==2014) & (CHIRPS.coords['time.month']>3)) | ((CHIRPS.coords['time.year']>=2015) & (CHIRPS.coords['time.year']<2018)) | ((CHIRPS.coords['time.year']==2018) & (CHIRPS.coords['time.month']<=2)))

CHIRPS_FINAL_PRECIP = CHIRPS.precip.sel(time=COND1)

print (CHIRPS_FINAL_PRECIP.coords['time'])

print ("Starting to calculate the first mean")
MEAN = CHIRPS_FINAL_PRECIP.chunk({'lat':300, 'lon':600}).mean(dim='time')
OUTFILE = '/home/GPM/IMERG/v05/daily/final/LTM_CHIRPS.20140312-20180228.nc'
print ("Computing")
r = MEAN.compute()
print ("Now writing {}".format(OUTFILE))
r.to_netcdf(OUTFILE)
