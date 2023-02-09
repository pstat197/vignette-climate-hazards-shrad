__author__ = "Enbo Zhou"

import xarray as xr
import matplotlib.pyplot as plt

#%% read in climatology
chirps_data_dir  = './chirps-v2.0.2018.days_p05.nc'
prism_data_dir  = './PRISM_annual_daily_ppt_4km_2018.nc'

chirps_data = xr.open_dataset(chirps_data_dir)
prism_data = xr.open_dataset(prism_data_dir)

# Get the 121 day's precipitation
prism_first_day = prism_data.ppt[121, :, :]
chirps_first_day = chirps_data.precip[121, :, :]
print(prism_first_day)
print(chirps_first_day)

# interpolate chirps to prism
chirps_interpolated = chirps_first_day.interp_like(prism_first_day)
# Get the difference
diff = chirps_interpolated - prism_first_day
# Difference visualization 
diff.plot.pcolormesh()

plt.show()