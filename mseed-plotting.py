import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os


data_directory = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'

# cat_directory = './space_apps_2024_seismic_detection/data/lunar/training/catalogs/'
# cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
# cat = pd.read_csv(cat_file)


#iterate through files in directory
filename = 'xa.s12.00.mhz.1970-06-26HR00_evid00009'
mseed_file = f'{data_directory}{filename}.mseed'
st = read(mseed_file)

# This is how you get the data and the time, which is in seconds
tr = st.traces[0].copy()
tr_times = tr.times()
tr_data = tr.data

# Initialize figure
fig,ax = plt.subplots(1,1,figsize=(10,3))

# Plot trace
ax.plot(tr_times,tr_data)

# Make the plot pretty
ax.set_xlim([min(tr_times),max(tr_times)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')
ax.set_title(f'{filename}')

# LTA and STA
from obspy.signal.trigger import classic_sta_lta

# Initialize figure 2
fig_2,ax_2 = plt.subplots(1,1,figsize=(10,3))
# Sampling frequency of our trace
df = tr.stats.sampling_rate

# How long should the short-term and long-term window be, in seconds?
sta_len = 120
lta_len = 600

# Run Obspy's STA/LTA to obtain a characteristic function
# This function basically calculates the ratio of amplitude between the short-term 
# and long-term windows, moving consecutively in time across the data
cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))

# Plot characteristic function
ax_2.plot(tr_times,cft)
ax_2.set_xlim([min(tr_times),max(tr_times)])
ax_2.set_xlabel('Time (s)')
ax_2.set_ylabel('Characteristic function')

plt.show()