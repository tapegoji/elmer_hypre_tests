import matplotlib.pyplot as plt
import numpy as np

# Simulating a dataset
# load the data
# file_path = 'MagneticFieldWire/results/scalar_data.dat'
file_path_case = 'results_case/scalar_data.dat'
file_path_direct = 'results_direct/scalar_data.dat'
file_path_hypre= 'results_hypre/scalar_data.dat'
with open(file_path_case, 'r') as file:
    lines = file.readlines()
with open(file_path_direct, 'r') as file:
    lines_direct = file.readlines()
with open(file_path_hypre, 'r') as file:
    lines_hypre = file.readlines()

data = np.array([list(map(float, line.split())) for line in lines])
data_direct = np.array([list(map(float, line.split())) for line in lines_direct])
data_hypre = np.array([list(map(float, line.split())) for line in lines_hypre])

current_A = data[:, 0]
current_A_direct = data_direct[:, 0]
current_A_hypre = data_hypre[:, 0]

# Compute time_ns based on index * 1e-9
time_ns = np.arange(len(current_A)) * 1e-9

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(time_ns, current_A, label='elmer solver iterative')
plt.plot(time_ns, current_A_direct, label='elmer solver direct')
plt.plot(time_ns, current_A_hypre, label='Hypre')

plt.xlabel('Time (ns)')
plt.ylabel('Current (A)')
plt.title('Current vs Time')
plt.grid(True)
plt.legend()
plt.show()
