#include <cuda.h>
#include <vector>
#include <iostream>
#include "lenia.h"

__device__ float growth_function(float input, float growth_center, float growth_width) {
    return 2 * exp(-pow(input - growth_center, 2) / (2 * pow(growth_width, 2))) - 1; // Gaussian function [0, 1] -> [-1, 1]
}

__device__ float convolution(int centerx, int centery, float* frame, int frame_width, int frame_height, float* kernel, int kernel_radius) {
    float value = 0.0f;
    int kernel_size = kernel_radius * 2 + 1;

    for (int conv_x = 0; conv_x < kernel_size; ++conv_x) {
        for (int conv_y = 0; conv_y < kernel_size; ++conv_y) {
            int imagex = (centerx + (conv_x - kernel_radius));
            int imagey = (centery + (conv_y - kernel_radius));

            // % (modulo) does not work -_- (figured it out after 5 hours...)
            // if (imagex < 0) imagex += frame_width;
            // if (imagex >= frame_width) imagex -= frame_width;
            // if (imagey < 0) imagey += frame_height;
            // if (imagey >= frame_width) imagey -= frame_height;
            
            if (imagex < 0 || imagex >= frame_width || imagey < 0 || imagey >= frame_height) {
                continue;
            }

            value += frame[imagex + imagey * frame_width] * kernel[conv_x + conv_y * kernel_size];
        }
    }

    return value;
}

__global__ void cudaLenia(float *frames, float* lastFrame, int frameWidth, int frameHeight, int frameIndex, float* kernel, int kernalRadius, float growthCenter, float growthWidth, float deltaTime, int blockx, int blocky, bool saveFrame) {
    for (int imagex = blockIdx.x * blockDim.x + threadIdx.x; imagex < frameWidth; imagex += blockDim.x * blockx) {
        for (int imagey = blockIdx.y * blockDim.y + threadIdx.y; imagey < frameHeight; imagey += blockDim.y * blocky) {
            if (imagex >= frameWidth || imagey >= frameHeight)
                return;

            float value = lastFrame[imagex + imagey * frameWidth];
            float convolutionValue = convolution(imagex, imagey, &frames[frameWidth * frameHeight * (frameIndex - 1)], frameWidth, frameHeight, kernel, kernalRadius);
            float growthValue = growth_function(convolutionValue, growthCenter, growthWidth);
            float newValue = value + growthValue * deltaTime;
            newValue = fmaxf(0, fminf(newValue, 1));
            lastFrame[imagex + imagey * frameWidth] = newValue;
            if (saveFrame) frames[(imagex + imagey * frameWidth) + (frameHeight * frameWidth * frameIndex)] = newValue;
        }
    }
}

LeniaResult leniaRunCuda(LeniaData data, std::vector<float> input, KernelData kernel) {
    float* frames_cu;
    float* lastFrame_cu;
    float* kernal_cu;

	cudaMalloc((void**)&frames_cu, data.FrameWidth * data.FrameHeight * sizeof(float) * data.FrameAmount);
	cudaMalloc((void**)&lastFrame_cu, data.FrameWidth * data.FrameHeight * sizeof(float));
	cudaMalloc((void**)&kernal_cu, kernel.Kernel.size() * sizeof(float));

    cudaMemcpy(frames_cu, input.data(), data.FrameWidth * data.FrameHeight * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(lastFrame_cu, input.data(), data.FrameWidth * data.FrameHeight * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(kernal_cu, kernel.Kernel.data(), kernel.Kernel.size() * sizeof(float), cudaMemcpyHostToDevice);

	cudaEvent_t startEvt, stopEvt; 
	cudaEventCreate(&startEvt);
	cudaEventCreate(&stopEvt);

	cudaEventRecord(startEvt);
    for (int frameIndex = 1; frameIndex < data.FrameAmount; ++frameIndex) {
        for (int i = 0; i < data.IterationPerFrame; ++i) {
            cudaLenia<<<dim3(data.Blocks_x, data.Blocks_y), dim3(data.Threads_x, data.Threads_y)>>>(
                frames_cu, lastFrame_cu, 
                data.FrameWidth, data.FrameHeight, 
                frameIndex, 
                kernal_cu, kernel.Radius, 
                data.GrowthCenter, data.GrowthWidth, data.DeltaTime,
                data.Blocks_x, data.Blocks_y,
                i == data.IterationPerFrame - 1
            );
        }
    }
	cudaError_t error = cudaGetLastError();
	cudaEventRecord(stopEvt);
	
    std::vector<float> output(data.FrameWidth * data.FrameHeight * data.FrameAmount);
	cudaMemcpy(output.data(), frames_cu, data.FrameWidth * data.FrameHeight * sizeof(float) * data.FrameAmount, cudaMemcpyDeviceToHost);

	float elapsedTime;
	cudaEventElapsedTime(&elapsedTime, startEvt, stopEvt);

	cudaEventDestroy(startEvt);
	cudaEventDestroy(stopEvt);
    cudaFree(frames_cu);
    cudaFree(lastFrame_cu);
    cudaFree(kernal_cu);

    return LeniaResult(elapsedTime, cudaGetErrorString(error), output);
}