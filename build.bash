#!/bin/bash -l
#SBATCH --account=lp_h_pds_iiw
#SBATCH --cluster=wice
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=1
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --time=00:05:00
#SBATCH --error="%x.e%A"
#SBATCH --output="%x.o%A"

module purge
module load cluster/wice/gpu_a100
module load CUDA/11.7.0
module load GCC/10.3.0

echo "NVCC version:"
nvcc --version 2>&1

echo "GCC version:"
gcc --version 2>&1

nvcc -ccbin=g++ ./cuda/main.cpp ./cuda/lenia.cpp ./cuda/lenia.cu -o ./lenia --std=c++17