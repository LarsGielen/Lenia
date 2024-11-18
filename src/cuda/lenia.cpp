#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <random>

#include "lenia.h"
#include "commandLineUtils.h"
#include "leniaFunctions.h"

LeniaResult leniaRunCuda(LeniaData data, std::vector<float> input, KernelData kernel);

void leniaRun(LeniaData data, std::string output_name, bool verbose) {
	std::vector<float> input(data.FrameWidth * data.FrameHeight);
    KernelData kernel = createKernel(data.KernelRadius, data.KernelPeakHeights, data.KernelAlpha);

    for (size_t i = 0; i < input.size(); ++i) {
        input[i] = (float)rand() / RAND_MAX;
        // if ((float)rand() / RAND_MAX < 0.1) input[i] = 1.0;
    }

    if (verbose)
        std::cout << "Starting Lenia with:" << std::endl 
            << " -" << "Frame Width: " << data.FrameWidth << " Height: " << data.FrameHeight << std::endl
            << " -" << "Frame Amount: " << data.FrameAmount << " Iterations per Frame: " << data.IterationPerFrame << std::endl
            << " -" << "Delta Time: " << data.DeltaTime << std::endl
            << " -" << "Kernel Radius: " << data.KernelRadius << " Kernel Alpha: " << data.KernelAlpha << std::endl
            << " -" << "Growth Center: " << data.GrowthCenter << " Growth Width: " << data.GrowthWidth << std::endl
            << " -" << "Blocks X: " << data.Blocks_x << " Y: " << data.Blocks_y << std::endl
            << " -" << "Threads X: " << data.Threads_x << " Y: " << data.Threads_y << std::endl;

    LeniaResult result = leniaRunCuda(data, input, kernel);

    std::cout << "Cuda error: " << result.CudaError << std::endl;
    std::cout << "Lenia completed in " << result.ElapsedTime << " ms" << std::endl;

    if (!output_name.empty()) {
        writeDataToBinFile(data.FrameWidth, data.FrameHeight, data.FrameAmount, result.Frames, std::string(output_name + ".bin"), verbose);
        // writeDataToFile(kernel.Size, kernel.Size, 1, kernel.Kernel, std::string(output_name + "_kernel1.txt"), verbose);
    }
}

float kernelFunction(float value, const std::vector<float>& peak_heights, float alpha) {
    float sum = 0.0;
    int peak_amount = peak_heights.size();

    for (int i = 0; i < peak_amount; ++i) {
        if ((i / (float)peak_amount <= value) && (value <= (i + 1) / (float)peak_amount)) 
            sum += peak_heights[i] * std::abs(gaussian_bump(peak_amount * value - i, alpha));
    }
    return sum;
}

KernelData createKernel(int radius, std::vector<float> peaks, float alpha) {
    int size = radius * 2 + 1;
    float total_sum = 0.0f;
    std::vector<float> kernel(size * size);

    for  (size_t x = 0; x < size; ++x) {
        for (size_t y = 0; y < size; ++y) {
            int kernel_x = x - radius;
            int kernel_y = y - radius;
            float radial_distance = std::sqrt(kernel_x * kernel_x + kernel_y * kernel_y);
            float radial_distance_percentage = radial_distance / radius;

            float value = kernelFunction(radial_distance_percentage, peaks, alpha);

            kernel[x + y * size] = value;
            total_sum += value;
        }
    }

    for (float& value : kernel) 
        value /= total_sum;

    return KernelData(radius, alpha, peaks, kernel);
}

void writeDataToTxtFile(size_t width, size_t height, size_t frame_amount, const std::vector<float>& frames, std::string output_name, bool verbose) {
    std::ofstream output_file(output_name);
    if (!output_file) 
        throw std::runtime_error("Unable to open file for writing.");

    output_file.open(output_name);
    output_file << "width:" << width << " height:" << height << " frames:" << frame_amount << std::endl;
    for (int frame_index = 0; frame_index < frame_amount; ++frame_index) {
        for (int i = 0; i < width * height; ++i) {
            output_file << std::to_string(frames[i + (width * height * frame_index)]) << "; ";
        }
        output_file << std::endl;
        if (verbose) print_progress_bar("Creating file " + output_name, frame_index + 1, frame_amount);
    }
    output_file.close();
}

void writeDataToBinFile(size_t width, size_t height, size_t frame_amount, const std::vector<float>& frames, const std::string& output_name, bool verbose) {
    std::ofstream output_file(output_name, std::ios::binary);
    if (!output_file) 
        throw std::runtime_error("Unable to open file for writing.");
    
    if (verbose) print_progress_bar("Creating file " + output_name, 1, 5);
    output_file.write(reinterpret_cast<const char*>(&width), sizeof(width));
    if (verbose) print_progress_bar("Creating file " + output_name, 2, 5);
    output_file.write(reinterpret_cast<const char*>(&height), sizeof(height));
    if (verbose) print_progress_bar("Creating file " + output_name, 3, 5);
    output_file.write(reinterpret_cast<const char*>(&frame_amount), sizeof(frame_amount));
    if (verbose) print_progress_bar("Creating file " + output_name, 4, 5);
    output_file.write(reinterpret_cast<const char*>(frames.data()), frames.size() * sizeof(float));
    if (verbose) print_progress_bar("Creating file " + output_name, 5, 5);

    output_file.close();
}