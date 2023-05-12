import xarray as xr
import pandas as pd
import numpy as np
import geopandas as gpd
import salem
from Shrad_modules import *

basin_shp = gpd.read_file("/home/chc-shrad/DATA/GRDC/USA/subregions.north_america.shp")


def basin_avg_rf(data, shdf):
    t2_sub = data.salem.subset(shape=shdf, margin=0)
    sel_data = t2_sub.salem.roi(shape=shdf)
    sel_data_ts = calc_spatial_integral(sel_data['precip']/1000)
    sel_data_ts = sel_data_ts.resample(time='A-Sep').sum()
    ann_rf = float(sel_data_ts.sel(time=slice('2001-09-30', '2021-09-30')).mean().values)*(8.1071319378991E-10)
    return ann_rf


columns = ['FID', 'chirps2', 'chirps3', 'prism', 'gridmet']
df = pd.DataFrame(columns=columns)

for i, fid in enumerate(basin_shp['FID']):
    shdf = basin_shp[basin_shp['FID']==fid]
    print (fid)
    #chirps2
    data = xr.open_dataset('/home/chc-data-out/products/CHIRPS-2.0/global_monthly/netcdf/chirps-v2.0.monthly.nc')
    ann_rf_c2 = basin_avg_rf(data, shdf)
    del data
    
    #chirps3
    data = xr.open_dataset('/home/chc-shrad/DATA/Precipitation_Global/CHIRPS/v3.0/monthly/beta.chirps-v3.0.monthly.nc')
    ann_rf_c3 = basin_avg_rf(data, shdf)
    del data
    
    # prism
    data = xr.open_mfdataset('/home/chc-shrad/DATA/Atmopheric_forcings/PRISM/Monthly/ppt/netcdf/PRISM_ppt_stable_4kmM3_*', concat_dim='time', combine='nested')
    ann_rf_p = basin_avg_rf(data, shdf)
    del data
    
    # gridmet
    data = xr.open_mfdataset('/home/chc-shrad/DATA/Atmopheric_forcings/GridMET/Daily/pr_*', concat_dim='day', combine='nested')
    data = data.rename({'precipitation_amount':'precip', 'lat':'latitude', 'lon':'longitude', 'day':'time'})
    ann_rf_g = basin_avg_rf(data, shdf)
    del data
    
    # Writing output in dataframe
    df.loc[i] = {'FID': fid,
                 'chirps2': ann_rf_c2,
                 'chirps3': ann_rf_c3,
                 'prism': ann_rf_p,
                 'gridmet': ann_rf_g}
df.to_csv('/home/chc-shrad/DATA/Precipitation_Global/CHIRPS/v3.0/monthly/compare_conus_subregion_average_total_rainfall.csv')