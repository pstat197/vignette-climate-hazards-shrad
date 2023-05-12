import xarray as xr
import numpy as np
import pandas as pd
import os.path as op
import rioxarray as rx

INDIR = '/home/CHIRP/pentads'
OUTDIR = '/home/chg-shrad/DATA/Precipitation_Global/CHIRP/v3.0/Daily'
INFILE_template = '/home/CHIRP/v3.0/daily/{:04d}/chirp-v3.{:04d}.{:02d}.{:02d}.tif'
OUTFILE_template = '{}/chirp-v3.{:04d}{:02d}{:02d}.nc'

DATE_TS = pd.date_range('2001-01-01', '2021-12-31', freq='1D')

for c, tstep in enumerate(DATE_TS):
    Daily_PRECIP = np.zeros([2400, 7200])
    INFILE = INFILE_template.format(tstep.year, tstep.year, tstep.month, tstep.day)
    print ("Reading {}".format(INFILE))
    Daily_PRECIP = rx.open_rasterio(INFILE).isel(band=0)
    Daily_PRECIP_XR = xr.DataArray(Daily_PRECIP, coords=[Daily_PRECIP.y, Daily_PRECIP.x], dims=['latitude', 'longitude'])
    Daily_PRECIP_XR = Daily_PRECIP_XR.assign_coords(time=tstep)
    Daily_PRECIP_XR = Daily_PRECIP_XR.expand_dims('time')
    Daily_PRECIP_XR.attrs['units'] = 'mm/day'
    MASKED_Daily_PRECIP_XR = Daily_PRECIP_XR.where(Daily_PRECIP_XR>=0)
    OUTFILE = OUTFILE_template.format(OUTDIR, tstep.year, tstep.month, tstep.day)
    print ("Writing {}".format(OUTFILE))
    MASKED_Daily_PRECIP_XR.to_dataset(name='precip').to_netcdf(OUTFILE)

    