import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from obspy.signal.invsim import cosine_taper
from obspy.signal.filter import highpass
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset


data_directory = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'

# cat_directory = './space_apps_2024_seismic_detection/data/lunar/training/catalogs/'
# cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
# cat = pd.read_csv(cat_file)

#iterate through files in directory
filename = 'xa.s12.00.mhz.1973-03-01HR00_evid00093'
# guide = 'xa.s12.00.mhz.1970-06-26HR00_evid00009'
# noisy = 'xa.s12.00.mhz.1970-01-19HR00_evid00002'
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

####################################### LTA and STA ########################################
from obspy.signal.trigger import classic_sta_lta

# Initialize figure 2
#fig_2,ax_2 = plt.subplots(1,1,figsize=(10,3))
# Sampling frequency of our trace
df = tr.stats.sampling_rate

# How long should the short-term and long-term window be, in seconds?
sta_len = 1000
lta_len = 10000


# Plot characteristic function
# ax_2.plot(tr_times,cft)
# ax_2.set_xlim([min(tr_times),max(tr_times)])
# ax_2.set_xlabel('Time (s)')
# ax_2.set_ylabel('Characteristic function')

####################################### LTA and STA ########################################

####################################### BANDPASS ########################################
# Set the minimum and maximum frequency for the bandpass filter
minfreq = 0.5
maxfreq = 1.0

# Make a copy of the original stream for filtering
st_filt = st.copy()

# Apply the bandpass filter to each trace within the stream
st_filt.filter('bandpass', freqmin=minfreq, freqmax=maxfreq, corners=4, zerophase=True)
tr_filt = st_filt[0]  # Access the first trace after filtering
tr_times_filt = tr_filt.times()
tr_data_filt = tr_filt.data

# Run Obspy's STA/LTA to obtain a characteristic function
# This function basically calculates the ratio of amplitude between the short-term 
# and long-term windows, moving consecutively in time across the data
cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))

# Play around with the on and off triggers, based on values in the characteristic function
thr_on = 4
thr_off = 1.5
on_off = np.array(trigger_onset(cft, thr_on, thr_off))
# The first column contains the indices where the trigger is turned "on".

for i in np.arange(0,len(on_off)):
    triggers = on_off[i]
    ax.axvline(x = tr_times[triggers[0]], color='red', label='Trig. On')
    ax.axvline(x = tr_times[triggers[1]], color='purple', label='Trig. Off')

# # To better visualize the frequency components, we will use a spectrogram
# from scipy import signal
# from matplotlib import cm

# # Create the spectrogram
# f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)

# # Plot the time series and spectrogram
# fig_3 = plt.figure(figsize=(10, 10))

# # Plot filtered trace
# ax_3 = plt.subplot(2, 1, 1)
# ax_3.plot(tr_times_filt, tr_data_filt)

# # Mark detection (you should define 'arrival' beforehand)
# # arrival = some_value  # Define the correct arrival time
# # ax_3.axvline(x=arrival, color='red', label='Detection')  # This line will fail if 'arrival' is undefined
# ax_3.legend(loc='upper left')

# # Make the plot pretty
# ax_3.set_xlim([min(tr_times_filt), max(tr_times_filt)])
# ax_3.set_ylabel('Velocity (m/s)')
# ax_3.set_xlabel('Time (s)')

# # Plot spectrogram
# ax2 = plt.subplot(2, 1, 2)
# vals = ax2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=5e-17)
# ax2.set_xlim([min(tr_times_filt), max(tr_times_filt)])
# ax2.set_xlabel('Time (Day Hour:Minute)', fontweight='bold')
# ax2.set_ylabel('Frequency (Hz)', fontweight='bold')

# # Mark detection on the spectrogram (optional)
# # ax2.axvline(x=arrival, color='red')

# # Add colorbar for the spectrogram
# cbar = plt.colorbar(vals, orientation='horizontal')
# cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')
####################################### BANDPASS ########################################

plt.show()


