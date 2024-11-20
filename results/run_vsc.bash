#!/bin/bash
#SBATCH --account=lp_h_pds_iiw
#SBATCH --cluster=wice
#SBATCH --partition=gpu_a100
#SBATCH --gpus-per-node=1
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=23:00:00
#SBATCH --error="%x.e%A"
#SBATCH --output="%x.o%A"

output_file="lenia_results.csv"
> $output_file # Clear the file if it exists

# Write the CSV header
echo "blocks_x,blocks_y,time" > $output_file

# Fixed arguments
frame_width=4096
frame_height=32
frame_amount=2000
iteration_per_frame=10
delta_time=0.001
kernel_radius=18
kernel_alpha=4
kernel_peak_heights=1.0
growth_mhu=0.14
growth_sigma=0.015
threads_x=32
threads_y=32
blocks_y=1

# Loop over blocks_x from 1 to 128
for blocks_x in {1..128}; do
  echo "Running with blocks_x=$blocks_x, blocks_y=$blocks_y"
  
  # Run the program with the current configuration
  result=$(./lenia \
    --frameWidth $frame_width \
    --frameHeight $frame_height \
    --frameAmount $frame_amount \
    --iteration_per_frame $iteration_per_frame \
    --deltaTime $delta_time \
    --kernel_radius $kernel_radius \
    --kernel_alpha $kernel_alpha \
    --kernel_peak_heights $kernel_peak_heights \
    --growth_mhu $growth_mhu \
    --growth_sigma $growth_sigma \
    --blocks_x $blocks_x \
    --blocks_y $blocks_y \
    --threads_x $threads_x \
    --threads_y $threads_y)
  
  # Extract the parallel execution time
  time=$(echo "$result" | grep -oP '(?<=Lenia completed in )[0-9.]+(?= ms)')
  
  # Log the results to the file in CSV format
  echo "$blocks_x,$blocks_y,$time" >> $output_file
done

echo "Results written to $output_file in CSV format."
