import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

# Function to load and plot the data
def plot_real_time_data(file_path, update_interval=1):
    plt.ion()  # Turn on interactive mode for live updating plots
    
    # Create a figure with two subplots (one for current, one for voltage)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Loop until the figure is closed
    try:
        while plt.fignum_exists(fig.number):  # Check if the figure is still open
            # Load the data
            with open(file_path, 'r') as file:
                lines = file.readlines()

            data = np.array([list(map(float, line.split())) for line in lines])
            current_1 = -data[:, 2]
            voltage_1 = data[:, 3] - data[:, 7]  
            if coupled_inductors:
                if negative_coupling:
                    current_2 = -data[:, 10]
                    voltage_2 = data[:, 11] - data[:, 15]
                else:
                    current_2 = data[:, 10]
                    voltage_2 = data[:, 11] - data[:, 15]

            # Compute time_us based on index * 1e-6 (converted to microseconds for x-axis)
            time_us = np.arange(len(current_1))

            # Clear the previous plots
            ax1.clear()
            ax2.clear()

            # Plotting the updated current data on the first subplot
            ax1.plot(time_us, current_1, label='Current 1 (A)', color='b')
            if coupled_inductors:
                ax1.plot(time_us, current_2, label='Current 2 (A)', color='g')
            ax1.set_xlabel('Time (µs)')
            ax1.set_ylabel('Current (A)')
            ax1.set_title('Current vs Time')
            ax1.grid(True)
            ax1.legend()

            # Plotting the updated voltage data on the second subplot
            ax2.plot(time_us, voltage_1, label='Inductor Voltage 1 (V)', color='r')
            if coupled_inductors:
                ax2.plot(time_us, voltage_2, label='Inductor Voltage 2 (V)', color='y')
            ax2.set_xlabel('Time (µs)')
            ax2.set_ylabel('Voltage (V)')
            ax2.set_title('Voltage vs Time')
            ax2.grid(True)
            ax2.legend()

            # Draw the updated plots
            plt.draw()
            plt.pause(10)  # Short pause to update the plot

            # Wait for the specified update interval before reading the file again
            time.sleep(update_interval)
    except KeyboardInterrupt:
        print("Plotting interrupted manually.")
    finally:
        plt.ioff()  # Turn off interactive mode
        plt.show()  # Display the last plot before exiting

# Define file path and call the function
file_path = 'results/scalar_data.dat'

coupled_inductors = True

negative_coupling = True


plot_real_time_data(file_path, update_interval=1)  # Update every 1 second
