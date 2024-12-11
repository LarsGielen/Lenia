#pragma once
#include <vector>
#include <string>

struct KernelData {
    int Radius;
    int Size;
    float Alpha;
    std::vector<float> PeakHeights;
    std::vector<float> Kernel;

    KernelData(int radius, float alpha, std::vector<float> peakHeights, std::vector<float> kernel)
        : Radius(radius), Size(radius * 2 + 1), Alpha(alpha), PeakHeights(std::move(peakHeights)), Kernel(std::move(kernel)) {}
};

struct LeniaData {
    int FrameWidth;
    int FrameHeight;
    int FrameAmount;
    int IterationPerFrame;

    float DeltaTime;

    int KernelType;
    int KernelRadius;
    float KernelAlpha;
    std::vector<float> KernelPeakHeights;

    int GrowthType;
    float GrowthCenter;
    float GrowthWidth;

    int Blocks_x;
    int Blocks_y;
    int Threads_x;
    int Threads_y;

    int Seed;
    float Rand_threshold;

    LeniaData(
        int frameWidth,
        int frameHeight,
        int frameAmount,

        int iterationPerFrame,

        float deltaTime,

        int kernelType,
        int kernelRadius,
        float kernelAlpha,
        std::vector<float> kernelPeakHeights,

        int growthType,
        float growthCenter,
        float growthWidth,

        int blocks_x,
        int blocks_y,
        int threads_x,
        int threads_y,

        int seed,
        float rand_threshold
    ): 
    FrameWidth(frameWidth),
    FrameHeight(frameHeight),
    FrameAmount(frameAmount),
    IterationPerFrame(iterationPerFrame),

    DeltaTime(deltaTime),

    KernelType(kernelType),
    KernelRadius(kernelRadius),
    KernelAlpha(kernelAlpha),
    KernelPeakHeights(std::move(kernelPeakHeights)),

    GrowthType(growthType),
    GrowthCenter(growthCenter),
    GrowthWidth(growthWidth),

    Blocks_x(blocks_x),
    Blocks_y(blocks_y),
    Threads_x(threads_x),
    Threads_y(threads_y),
    
    Seed(seed),
    Rand_threshold(rand_threshold) {}
};

struct LeniaResult {
    float ElapsedTime;
    std::string CudaError;
    std::vector<float> Frames;

    LeniaResult(float elapsedTime, std::string cudaError, std::vector<float> frames)
        : ElapsedTime(elapsedTime), CudaError(std::move(cudaError)), Frames(std::move(frames)) {}
};

void leniaRun(LeniaData data, std::string outputName, bool verbose);
KernelData createKernel(int radius, std::vector<float> peaks, float alpha, int kernel_type);
void writeDataToFile(size_t width, size_t height, size_t frameAmount, const std::vector<float>& frames, std::string outputName, bool verbose);
void writeDataToBinFile(size_t width, size_t height, size_t frame_amount, const std::vector<float>& frames, const std::string& output_name, bool verbose);