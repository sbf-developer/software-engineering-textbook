#include <algorithm>
#include <iostream>
#include <stdexcept>
#include <vector>

int percentile_approx(std::vector<int> samples, double p) {
    if (samples.empty() || p < 0.0 || p > 1.0) {
        throw std::invalid_argument("invalid percentile request");
    }
    std::sort(samples.begin(), samples.end());
    const auto index = static_cast<std::size_t>(p * static_cast<double>(samples.size() - 1));
    return samples[index];
}

int main() {
    const std::vector<int> samples{20, 40, 50, 80, 120, 180, 300};
    std::cout << "p95=" << percentile_approx(samples, 0.95) << "\n";
}
