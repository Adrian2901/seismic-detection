import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

# Get the catalogue to find the actual arrival time
cat_directory = './space_apps_2024_seismic_detection/data/lunar/training/catalogs/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
cat = pd.read_csv(cat_file)
print(cat)

# row = cat.iloc[6]
row = cat.iloc[9]
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')

# Read the mseed file
test_filename = row.filename
data_directory = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'
mseed_file = f'{data_directory}{test_filename}.mseed'
st = read(mseed_file)

# Copy the original stream to avoid modifying the original data
st_threshold  = st.copy()
trace = st_threshold.traces[0]
sampling_rate = trace.stats.sampling_rate
starttime = trace.stats.starttime

# Get the velocity data
npts = trace.stats.npts
times = trace.times('timestamp')
velocities = trace.data
print('Velocities')
print(velocities)

# Create a DataFrame with time and velocity data
df = pd.DataFrame({
    'time_abs': pd.to_datetime(times, unit='s', origin=pd.Timestamp(starttime.datetime)),
    'velocity(m/s)': velocities
})

df['abs_velocity(m/s)'] = np.abs(df['velocity(m/s)'])

# Filter out rows where velocity is below a certain threshold
threshold = 2e-9
default_value = 0  # You can change this to any other value, such as a small constant
filtered_df = df[df['abs_velocity(m/s)'] >= threshold]

# Replace velocities below the threshold with the default value
df['filtered_velocity(m/s)'] = np.where(df['abs_velocity(m/s)'] >= threshold, df['velocity(m/s)'], default_value)

# Filter out rows where absolute velocity is below a certain threshold
# filtered_df = df['velocity(m/s)']
# filtered_df = df[(df['velocity(m/s)'] >= threshold) | (df['velocity(m/s)'] <= -threshold)]
# filtered_df = df[(df['velocity(m/s)'] <= threshold) & (df['velocity(m/s)'] >= -threshold)]

print('Filtered Velocities')
print(filtered_df)

# Create a figure with two subplots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # Adjust size as needed

# Plot original velocities in the first subplot
ax1.plot(df['time_abs'], df['velocity(m/s)'], label='Original Velocity', color='blue', alpha=0.7)
ax1.set_title('Original Velocity Over Time')
ax1.set_xlabel('Time')
ax1.set_ylabel('Velocity (m/s)')
ax1.legend()

# Plot filtered velocities in the second subplot
# Plot filtered velocities (with default values) in the second subplot
ax2.plot(df['time_abs'], df['filtered_velocity(m/s)'], label='Filtered Velocity with Defaults', color='red', linewidth=2)
ax2.set_title(f'Filtered Velocity with Default Values (Threshold: {threshold})')
ax2.set_xlabel('Time')
ax2.set_ylabel('Velocity (m/s)')
ax2.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()

plt.show()
