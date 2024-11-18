#include <string.h>
#include <iostream>

void print_progress_bar(std::string title, size_t current, size_t total) {
    if ((float)(current - 1) / total * 100.0f >= (int)((float)current / total * 100.0f))
        return;

    const int bar_width = 50;
    float progress = (float)current / total;
    int pos = bar_width * progress;

    std::cout << title + ": " << "[";
    for (int i = 0; i < bar_width; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] " << int(progress * 100.0) << "%\r";
    if (current == total) std::cout << std::endl;
    std::cout.flush();
}