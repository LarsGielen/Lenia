#!/bin/bash
nvcc ./src/cuda/main.cpp ./src/cuda/lenia.cpp ./src/cuda/lenia.cu -o ./build/lenia