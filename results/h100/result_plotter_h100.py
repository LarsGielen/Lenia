import pandas as pd
import matplotlib.pyplot as plt

# Input file containing the CSV data
input_file = "results/h100/lenia_results_h100.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(input_file)

# Extract the time for blocks_x = 1 (serial time)
serial_time = data[data['blocks_x'] == 1]['time'].values[0]

# Calculate speedup for each configuration
data['speedup'] = serial_time / data['time']

# Create a figure with 2 rows and 2 columns
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Parallel execution time (linear scale)
axes[0, 0].plot(data['blocks_x'], data['time'], marker="o", label="Execution Time (ms)")
axes[0, 0].set_title("Parallel Execution Time (Linear Scale)")
axes[0, 0].set_xlabel("Blocks_x")
axes[0, 0].set_ylabel("Time (ms)")
axes[0, 0].grid(True)
axes[0, 0].legend()

# Plot 2: Parallel execution time (log scale)
axes[0, 1].plot(data['blocks_x'], data['time'], marker="o", label="Execution Time (ms)")
axes[0, 1].set_title("Parallel Execution Time (Log Scale)")
axes[0, 1].set_xlabel("Blocks_x")
axes[0, 1].set_ylabel("Time (ms)")
axes[0, 1].set_yscale("log")
axes[0, 1].grid(True)
axes[0, 1].legend()

# Plot 3: Speedup (linear scale)
axes[1, 0].plot(data['blocks_x'], data['speedup'], marker="o", color="green", label="Speedup")
axes[1, 0].set_title("Speedup (Linear Scale)")
axes[1, 0].set_xlabel("Blocks_x")
axes[1, 0].set_ylabel("Speedup (x)")
axes[1, 0].grid(True)
axes[1, 0].legend()

# Plot 4: Speedup (log scale)
axes[1, 1].plot(data['blocks_x'], data['speedup'], marker="o", color="green", label="Speedup")
axes[1, 1].set_title("Speedup (Log Scale)")
axes[1, 1].set_xlabel("Blocks_x")
axes[1, 1].set_ylabel("Speedup (x)")
axes[1, 1].set_yscale("log")
axes[1, 1].grid(True)
axes[1, 1].legend()

# Adjust layout
plt.tight_layout()
plt.savefig("results_h100.png")
print("Combined plots saved as 'combined_parallel_time_speedup_plots.png'.")
