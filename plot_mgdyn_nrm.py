import matplotlib.pyplot as plt
import re

# File paths
file_serial = "elmersolver.log"  # Current directory
file_parallel = "../single_core_simdata/elmersolver.log"  # Backup directory

# Function to extract NRM values from a file
def extract_nrm_values(file_path):
    nrm_values = []
    pattern = r"NRM,RELC\): \(\s*([\d.E+-]+)"
    with open(file_path, "r") as file:
        for line in file:
            if ":: mgdynamics" in line:
                match = re.search(pattern, line)
                if match:
                    nrm_value = float(match.group(1))
                    nrm_values.append(nrm_value)
    return nrm_values

# Extract NRM values from both files
nrm_serial = extract_nrm_values(file_serial)
nrm_parallel = extract_nrm_values(file_parallel)

# Plot the NRM values
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(nrm_serial) + 1), nrm_serial, marker="o", linestyle="-", label="Parallel")
plt.plot(range(1, len(nrm_parallel) + 1), nrm_parallel, marker="x", linestyle="--", label="Serial")

# Customize the plot
plt.xlabel("Line Index")
plt.ylabel("NRM Value")
plt.title("Comparison of NRM Values (Serial vs Parallel)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
