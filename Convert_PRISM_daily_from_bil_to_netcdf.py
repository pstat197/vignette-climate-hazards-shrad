import rasterio
import rioxarray as rx
import glob
import pandas as pd
import numpy as np
# Define the .hdr file that contains the metadata for the .bil file

for var in ['ppt', 'tmin']:
    infile = '/home/chc-shrad/DATA/Atmopheric_forcings/PRISM/Daily/{}/bil/PRISM_*.bil'.format(var)
    for i, hdr_file in enumerate(np.sort(glob.glob(infile))):
        # Read the metadata using rasterio
        with rasterio.open(hdr_file) as src:
            # Create an xarray DataArray from the rasterio dataset
            da = rx.open_rasterio(src)
            da=da.where(da!=-9999.0)
        # Create a dataset from the DataArray
        ds = da.to_dataset(name=var)

        ## Adding time values
        date_str = hdr_file.split('/')[-1].split('_')[-2]
        data_flag = hdr_file.split('/')[-1].split('_')[2]
        outputfile = '/home/chc-shrad/DATA/Atmopheric_forcings/PRISM/Daily/{}/netcdf/PRISM_{}_{}_4kmM3_{}.nc'.format(var, var, data_flag, date_str)
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
