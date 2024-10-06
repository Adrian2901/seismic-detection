import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

def filter(file_st):
    # Copy the original stream to avoid modifying the original data
    st_threshold  = file_st.copy()
    trace = st_threshold.traces[0]
    
    velocities = trace.data

    # Create a DataFrame with time and velocity data
    df = pd.DataFrame({
        'velocity(m/s)': velocities
    })

    df['abs_velocity(m/s)'] = np.abs(df['velocity(m/s)'])

    # Calculate the threshold based on the 20 percent of the max velocity
    threshold = 0.2 * np.max(df['abs_velocity(m/s)'])

    # Filter out rows where velocity is below a certain threshold
    # threshold = 2e-9
    default_value = 0  # You can change this to any other value, such as a small constant

    # Filter out rows where absolute velocity is below a certain threshold
    # Replace velocities below the threshold with the default value
    filtered_velocities = np.where(df['abs_velocity(m/s)'] >= threshold, df['abs_velocity(m/s)'], default_value)

    # Use a sliding window to get the widest range of continuous data
    longest_start = longest_end = current_start = 0
    max_length = 0
    current_length = 0
    current_zeroes = 0
    max_number_of_zeroes = 50000
    
    for i in range(len(filtered_velocities)):
        if filtered_velocities[i] > default_value:
            if current_length == 0:
                current_start = i # Start a new sequence
            current_length += 1
            
            if current_length > max_length:
                max_length = current_length
                longest_start = current_start
                longest_end = i
        else:
            current_zeroes += 1
            if (current_zeroes > max_number_of_zeroes):
                current_zeroes = 0
                current_length = 0
                
    
    # Prepare the result array with original size
    result_velocities = np.full_like(filtered_velocities, default_value, dtype=float)
    
    # Fill up the data
    if max_length:
        result_velocities[longest_start:longest_end+1] = filtered_velocities[longest_start:longest_end+1]

    return result_velocities
