#include <cmath>    

float gaussian_bump(double value, double alpha) {
    if (value <= 0 || value >= 1) return 0.0;
    if (alpha <= 0) return 0.0;
    
    return 2 * std::exp(alpha * (1 - (1 / (4 * value * (1 - value)))));
}

float step(double value, double mhu, double sigma) {
    return (std::abs(value - mhu) <= sigma) ? 1 : -1;
}