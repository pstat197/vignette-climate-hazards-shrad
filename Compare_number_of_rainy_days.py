
# coding: utf-8

# This script analyzes CHIRTS for quality control, missing data etc.

# In[ ]:


from __future__ import division
import pandas as pd
import numpy as np
from Shrad_modules import read_nc_files, MAKEDIR
import calendar
from matplotlib import pyplot as plt
import time
import xarray as xr


CHIRPS = xr.open_mfdataset()
