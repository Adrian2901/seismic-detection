import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Step 1: Load the data
df = pd.read_csv('./space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/xa.s12.00.mhz.1970-01-19HR00_evid00002.csv')

# Convert 'time_abs' to datetime format for better plotting
df['time_abs'] = pd.to_datetime(df['time_abs(%Y-%m-%dT%H:%M:%S.%f)'])

def power_iteration(A, num_iterations: int):
    # Ideally choose a random vector
    # To decrease the chance that our vector
    # Is orthogonal to the eigenvector
    b_k = np.random.rand(A.shape[0])

    for _ in range(num_iterations):
        # calculate the matrix-by-vector product Ab
        b_k1 = np.dot(A, b_k)       

        # calculate the norm
        b_k1_norm = np.linalg.norm(b_k1)

        # re normalize the vector
        b_k = b_k1 / b_k1_norm

    return b_k

ksdjfhjkdsf = power_iteration(df['velocity(m/s)'].to_numpy(), 10)
print(ksdjfhjkdsf)

# Step 3: Detect Peaks
# Nd sequence of minimum and maximum prominence values
prominence = (8.596065098208513e-11, None)  # Adjust the prominence threshold as needed

peaks, properties = find_peaks(df['velocity(m/s)'], width=5, prominence=25.596065098208513e-10, distance=10)

# # Find the highest peak
# highest_peak = df['velocity(m/s)'].iloc[peaks].max()
# highest_peak_time_abs = df['time_abs'].iloc[df['velocity(m/s)'].iloc[peaks].idxmax()]


# Step 4: Extract Peak Information
peak_times_abs = df['time_abs'].iloc[peaks]
peak_velocities = df['velocity(m/s)'].iloc[peaks]
print(peak_times_abs)

# Find the highest peak
highest_peak = peak_velocities.max()
highest_peak_time_abs = peak_times_abs[peak_velocities.idxmax()]

# Step 5: Plot Velocity over Time with Peaks

plt.figure(figsize=(10, 6))

# Plot the original velocity
plt.plot(df['time_abs'], df['velocity(m/s)'], label='Original Velocity', color='blue', alpha=0.5)


# Mark the peaks
plt.plot(peak_times_abs, peak_velocities, 'ro', label='Peaks')

# Highlight the highest peak
plt.plot(highest_peak_time_abs, highest_peak, 'go', label='Highest Peak', markersize=10)

# Add labels and title
plt.xlabel('Time (Absolute)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity Over Time with Detected Peaks')

# Show legend
plt.legend()

# Display the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()       # Adjust layout for better display
plt.show()
