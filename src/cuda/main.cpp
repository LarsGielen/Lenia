#include <iostream>
#include <fstream>
#include <vector>
#include "vendor/argparse.hpp"
#include "vendor/json.hpp"

#include "lenia.h"

int main(int argc, char* argv[]) {
    argparse::ArgumentParser args("example_program");

    args.add_argument("-o", "--output")
        .help("output file name")
        .default_value("");
    args.add_argument("-i", "--input")
        .help("input config file name")
        .default_value("");
    args.add_argument("-v", "--verbose")
        .help("Enable verbose output")
        .default_value(false)
        .implicit_value(true);

    try {
        args.parse_args(argc, argv);
    } catch (const std::runtime_error& err) {
        std::cerr << err.what() << std::endl; return 1;
    }

    int frameWidth;
    int frameHeight;
    int frameAmount;

    int iterationPerFrame;

    float deltaTime;
    int kernelRadius;
    float kernelAlpha;
    std::vector<float> kernelPeakHeights;
    float growthMhu;
    float growthSigma;

    int blocks_x;
    int blocks_y;
    int threads_x;
    int threads_y;

    if (args.get<std::string>("--input") != "") {
        std::ifstream file(args.get<std::string>("--input"));
        if (!file.is_open()) {
            std::cerr << "Error opening config file" << std::endl; 
            return 1;
        }
        
        nlohmann::json config;
        file >> config;
        frameWidth = config["frameWidth"].get<int>();
        frameHeight = config["frameHeight"].get<int>();
        frameAmount = config["frameAmount"].get<int>();

        iterationPerFrame = config["iteration_per_frame"].get<int>();

        deltaTime = config["deltaTime"].get<float>();
        kernelRadius = config["kernel_radius"].get<int>();
        kernelAlpha = config["kernel_alpha"].get<float>(); 
        kernelPeakHeights = config["kernel_peak_heights"].get<std::vector<float>>();
        growthMhu = config["growth_mhu"].get<float>();
        growthSigma = config["growth_sigma"].get<float>();

        blocks_x = config["blocks_x"].get<int>();
        blocks_y = config["blocks_y"].get<int>();
        threads_x = config["threads_x"].get<int>();
        threads_y = config["threads_y"].get<int>();
    }
    else {
        std::cerr << "No input file given." << std::endl; 
        return 1;
    }

    LeniaData data(
        frameWidth, frameHeight, frameAmount, iterationPerFrame,
        deltaTime,
        kernelRadius, kernelAlpha, kernelPeakHeights,
        growthMhu, growthSigma,
        blocks_x, blocks_y, threads_x, threads_y
    );

    leniaRun(data, args.get<std::string>("--output"), args.get<bool>("--verbose"));
    return 0;
}
