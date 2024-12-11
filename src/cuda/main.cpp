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
        
    args.add_argument("--frameWidth")
        .help("")
        .default_value("");
        
    args.add_argument("--frameHeight")
        .help("")
        .default_value("");
        
    args.add_argument("--frameAmount")
        .help("")
        .default_value("");
        
    args.add_argument("--iteration_per_frame")
        .help("")
        .default_value("");
        
    args.add_argument("--deltaTime")
        .help("")
        .default_value("");
        
    args.add_argument("--kernel_type")
        .help("")
        .default_value("");
        
    args.add_argument("--kernel_radius")
        .help("")
        .default_value("");
        
    args.add_argument("--kernel_alpha")
        .help("")
        .default_value("");
        
    args.add_argument("--kernel_peak_heights")
        .help("")
        .default_value("");
        
    args.add_argument("--growth_type")
        .help("")
        .default_value("");

    args.add_argument("--growth_mhu")
        .help("")
        .default_value("");
        
    args.add_argument("--growth_sigma")
        .help("")
        .default_value("");
        
    args.add_argument("--blocks_x")
        .help("")
        .default_value("");
        
    args.add_argument("--blocks_y")
        .help("")
        .default_value("");
        
    args.add_argument("--threads_x")
        .help("")
        .default_value("");
        
    args.add_argument("--threads_y")
        .help("")
        .default_value("");

    args.add_argument("--seed")
        .help("")
        .default_value("");

    args.add_argument("--rand_threshold")
        .help("")
        .default_value("");


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
    int kernelType;
    int kernelRadius;
    float kernelAlpha;
    std::vector<float> kernelPeakHeights;
    int growthType;
    float growthMhu;
    float growthSigma;

    int blocks_x;
    int blocks_y;
    int threads_x;
    int threads_y;

    int seed;
    float rand_threshold;

    nlohmann::json config;
    if (args.get<std::string>("--input") != "") {
        std::ifstream file(args.get<std::string>("--input"));
        if (!file.is_open()) {
            std::cerr << "Error opening config file" << std::endl; 
            return 1;
        }
        file >> config;
    }
    else {
        config["frameWidth"] = std::stoi(args.get<std::string>("--frameWidth"));
        config["frameHeight"] = std::stoi(args.get<std::string>("--frameHeight"));
        config["frameAmount"] = std::stoi(args.get<std::string>("--frameAmount"));

        config["iteration_per_frame"] = std::stoi(args.get<std::string>("--iteration_per_frame"));

        config["deltaTime"] = std::stof(args.get<std::string>("--deltaTime"));
        config["kernel_type"] = std::stoi(args.get<std::string>("--kernel_type"));
        config["kernel_radius"] = std::stoi(args.get<std::string>("--kernel_radius"));
        config["kernel_alpha"] = std::stof(args.get<std::string>("--kernel_alpha"));

        std::string peaksStr = args.get<std::string>("--kernel_peak_heights");
        std::istringstream peaksStream(peaksStr);
        std::string peak;
        std::vector<float> kernelPeaks;
        while (std::getline(peaksStream, peak, ',')) {
            kernelPeaks.push_back(std::stof(peak));
        }
        config["kernel_peak_heights"] = kernelPeaks;

        config["growth_type"] = std::stof(args.get<std::string>("--growth_type"));
        config["growth_mhu"] = std::stof(args.get<std::string>("--growth_mhu"));
        config["growth_sigma"] = std::stof(args.get<std::string>("--growth_sigma"));

        config["blocks_x"] = std::stoi(args.get<std::string>("--blocks_x"));
        config["blocks_y"] = std::stoi(args.get<std::string>("--blocks_y"));
        config["threads_x"] = std::stoi(args.get<std::string>("--threads_x"));
        config["threads_y"] = std::stoi(args.get<std::string>("--threads_y"));

        config["seed"] = std::stoi(args.get<std::string>("--seed"));
        config["rand_threshold"] = std::stof(args.get<std::string>("--rand_threshold"));
    }

    
    frameWidth = config["frameWidth"].get<int>();
    frameHeight = config["frameHeight"].get<int>();
    frameAmount = config["frameAmount"].get<int>();

    iterationPerFrame = config["iteration_per_frame"].get<int>();

    deltaTime = config["deltaTime"].get<float>();
    kernelType = config["kernel_type"].get<int>();
    kernelRadius = config["kernel_radius"].get<int>();
    kernelAlpha = config["kernel_alpha"].get<float>(); 
    kernelPeakHeights = config["kernel_peak_heights"].get<std::vector<float>>();
    growthType = config["growth_type"].get<int>();
    growthMhu = config["growth_mhu"].get<float>();
    growthSigma = config["growth_sigma"].get<float>();

    blocks_x = config["blocks_x"].get<int>();
    blocks_y = config["blocks_y"].get<int>();
    threads_x = config["threads_x"].get<int>();
    threads_y = config["threads_y"].get<int>();

    seed = config["seed"].get<int>();
    rand_threshold = config["rand_threshold"].get<float>();

    LeniaData data(
        frameWidth, frameHeight, frameAmount, iterationPerFrame,
        deltaTime,
        kernelType, kernelRadius, kernelAlpha, kernelPeakHeights,
        growthType, growthMhu, growthSigma,
        blocks_x, blocks_y, threads_x, threads_y,
        seed, rand_threshold
    );

    leniaRun(data, args.get<std::string>("--output"), args.get<bool>("--verbose"));
    return 0;
}
