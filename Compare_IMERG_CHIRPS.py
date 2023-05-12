
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
IMERG_final_infile = '/home/GPM/IMERG/v05/daily/final/3B-DAY.MS.MRG.3IMERG.*.V05.nc4'
IMERG_late_infile = '/home/chg-shrad/DATA/Precipitation_Global/IMERG/GPM/Reordered_files/3B-DAY-L.MS.MRG.3IMERG.*.nc4'


# In[ ]:


IMERG_Final = xr.open_mfdataset(IMERG_final_infile, concat_dim='time', autoclose=True, chunks={'lat':200, 'lon':400})
IMERG_Late = xr.open_mfdataset(IMERG_late_infile, concat_dim='time', autoclose=True, chunks={'lat':200, 'lon':400})


# In[ ]:


IMERG_Final.coords['time'] = pd.date_range('20140312', '20180228', freq='D')
COND1 = (((IMERG_Final.coords['time.year']>=2014) & (IMERG_Final.coords['time.year']<2018)) | ((IMERG_Final.coords['time.year']==2018) & (IMERG_Final.coords['time.month']<=2)))
IMERG_FINAL_PRECIP = IMERG_Final.precipitationCal.transpose().sel(time=COND1)


# In[ ]:


IMERG_Late.coords['time'] = pd.date_range('20140312', '20180329', freq='D')
COND2 = (((IMERG_Late.coords['time.year']>=2014) & (IMERG_Late.coords['time.year']<2018)) | ((IMERG_Late.coords['time.year']==2018) & (IMERG_Late.coords['time.month']<=2)))
IMERG_LATE_PRECIP = IMERG_Late.precipitationCal.sel(time=COND2)


# In[ ]:


DIFF_1 = (IMERG_FINAL_PRECIP-IMERG_LATE_PRECIP).mean(dim='time')


# In[ ]:


OUTFILE = '/home/GPM/IMERG/v05/daily/final/Mean_3B-DAY.MS.MRG.3IMERG.20140312-20180228.V05.nc4'
print ("Now writing {}".format(OUTFILE))
DIFF_1.to_netcdf(OUTFILE)

