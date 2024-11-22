import matplotlib.pyplot as plt
import numpy as np

# Simulating a dataset
# load the data
# file_path = 'MagneticFieldWire/results/scalar_data.dat'
file_path = 'results/scalar_data.dat'
with open(file_path, 'r') as file:
    lines = file.readlines()

data = np.array([list(map(float, line.split())) for line in lines])
current_A = data[:, 0]

# Compute time_ns based on index * 1e-9
time_ns = np.arange(len(current_A)) * 1e-9

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(time_ns, current_A, label='Current (A)', color='b')
plt.xlabel('Time (ns)')
plt.ylabel('Current (A)')
plt.title('Current vs Time')
plt.grid(True)
plt.legend()
plt.show()
