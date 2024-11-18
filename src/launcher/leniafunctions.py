import numpy as np

def create_kernel_2d(radius, peak_heights, alpha):
    size = radius * 2 + 1
    kernel = np.zeros((size, size))
    total_sum = 0.0

    for x in range(size):
        for y in range(size):
            kernel_x = x - radius
            kernel_y = y - radius
            radial_distance = np.sqrt(kernel_x**2 + kernel_y**2)
            radial_distance_percentage = radial_distance / radius
            value = kernel_function(radial_distance_percentage, peak_heights, alpha)

            kernel[x, y] = value
            total_sum += value

    kernel /= total_sum
    return kernel

def kernel_function(value, peak_heights, alpha,):
    sum = 0.0
    peak_amount = len(peak_heights)

    for i in range(peak_amount):
        if ((i / peak_amount) <= value and value <= (i + 1) / peak_amount): sum += peak_heights[i] * np.abs(gaussian_bump(peak_amount * value - i, alpha))

    return sum

def growth_function(value, growth_center, growth_width): 
    return gaussian(value, growth_center, growth_width)

def gaussian(value, mhu, sigma):
    if sigma == 0: sigma = 1e-6
    return 2 * np.exp(-pow(value - mhu, 2) / (2 * pow(sigma, 2))) - 1

def gaussian_bump(value, alpha):
    if value == 0 or value == 1: return 0
    if alpha == 0: return 0
    return 2 * np.exp(alpha * (1 - (1 / (4 * value * (1 - value))))) 