# Shrad
# Tue Mar  7 04:44:22 PST 2023

from __future__ import division
import glob
import numpy as np
import pandas as pd
import xarray as xr
import rioxarray as rx
from dask.diagnostics import ProgressBar

def read_tiff_data(file_list):
    """Read raster data from a list of file paths."""
    data = []
    for file_path in file_list:
        with rx.open_rasterio(glob.glob(file_path)[0]) as file:
            data.append(file.isel(band=0).values)
            lats, lons = file.y.values, file.x.values
    return np.stack(data), lats, lons

## stacking chirps3 tiff files
file_list = np.sort(glob.glob('/home/chc-data-out/experimental/CHIRP-n-CHIRPS_v3_beta/CHIRPS/beta/monthly/global/beta.chirps*'))
#chirps3_ar, lats, lons = read_tiff_data(file_list)
print ("Done stacking chirps3")

## reading chirps2 netcdf to borrow time-dimension this can be done in many other ways just wanted to make sure to have the same time dimension as chirps3, makes the comparison between both datasets much easier
chirps2 = xr.open_dataset('/home/chc-data-out/products/CHIRPS-2.0/global_monthly/netcdf/chirps-v2.0.monthly.nc')

#date_ts = chirps2.coords['time'][chirps2.coords['time.year']<2023].values # same as chirps2
#print ("Converting chirps3 array to xarray dataa rray")
#chirps3 = xr.DataArray(chirps3_ar, dims=['time', 'latitude', 'longitude'], coords=[date_ts, lats, lons])
#chirps3 = chirps3.to_dataset(name='precip')
outfile = '/home/chc-shrad/DATA/Precipitation_Global/CHIRPS/v3.0/monthly/beta.chirps-v3.0.monthly.nc'

#with ProgressBar():
 #   print ("Writing {}".format(outfile))
  #  chirps3.where(chirps3['precip']>=0).to_netcdf(outfile)

chirps3 = xr.open_dataset(outfile)
sel_chirps3 = chirps3.sel(latitude=slice(49.98, -49.98), 
                                                    longitude=slice(chirps2.longitude.values.min(), chirps2.longitude.values.max()))
sel_chirps3 = sel_chirps3.reindex(latitude=sel_chirps3.latitude[::-1])
sel_chirps3.coords['latitude'], sel_chirps3.coords['longitude'] = chirps2.coords['latitude'], chirps2.coords['longitude']
sel_chirps3.to_netcdf('/home/chc-shrad/DATA/Precipitation_Global/CHIRPS/v3.0/monthly/beta.chirps_2_compatiable_chirps-v3.0.monthly.nc')
