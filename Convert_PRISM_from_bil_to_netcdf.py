import xarray as xr
import rasterio
import rioxarray as rx
import glob
import pandas as pd
import numpy as np
# Define the .hdr file that contains the metadata for the .bil file

for i, hdr_file in enumerate(np.sort(glob.glob('/home/chc-shrad/DATA/Atmopheric_forcings/PRISM/Monthly/ppt/bil/PRISM_ppt_stable_4kmM3_*_bil.bil'))):
    # Read the metadata using rasterio
    with rasterio.open(hdr_file) as src:
        # Create an xarray DataArray from the rasterio dataset
        da = rx.open_rasterio(src)
        da=da.where(da!=-9999.0)
    # Create a dataset from the DataArray
    ds = da.to_dataset(name='precip')

    ## Adding time values
    date_str = hdr_file.split('/')[-1].split('_')[-2]
    outputfile = '/home/chc-shrad/DATA/Atmopheric_forcings/PRISM/Monthly/ppt/netcdf/PRISM_ppt_stable_4kmM3_{}.nc'.format(date_str)


    date_str = str(date_str) + "15"  # Add day = 15 to the string representation
    date_obj = pd.to_datetime(date_str, format='%Y%m%d')
    ds = ds.isel(band=0).assign_coords(time=date_obj).expand_dims('time')
    ds = ds.rename({'x':'longitude', 'y':'latitude'})
    ds = ds.drop(['band', 'spatial_ref'])
    if i==0:
        lats, lons = ds.coords['latitude'], ds.coords['longitude']
    else:
        ds.coords['latitude'], ds.coords['longitude'] = lats, lons
        
    print ("Writing {}".format(outputfile))
    # Save the dataset as a netCDF file
    ds.to_netcdf(outputfile)
