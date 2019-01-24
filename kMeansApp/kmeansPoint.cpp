#include "kmeansPoint.hh"

#include <cmath>
#include <algorithm>
#include <iterator>

namespace kmeans
{

Point& Point::operator+=(const Point& rhs){
    std::transform(coordinates.begin(), coordinates.end(), rhs.coordinates.begin(), coordinates.begin(), [](auto x, auto y) {
        return x + y;
    });
}

Point& Point::operator/=(const int denominator){
    std::for_each(coordinates.begin(), coordinates.end(), [&](auto& x) {
        x /= denominator;
    });
}

double operator-(const Point& a, const Point& b) {
    std::array<double, COORDINATES_NUMBER> sum;
    std::transform(a.coordinates.begin(), a.coordinates.end(), b.coordinates.begin(), sum.begin(), [&](auto x, auto y) {
        return std::pow(x - y, 2);
    });

    return std::sqrt(std::accumulate(sum.begin(), sum.end(), 0));
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
    std::copy(p.coordinates.begin(), p.coordinates.end(), std::ostream_iterator<double>(os, ","));
    os << p.meta;
    os <<"\n";
    return os;
}

} // namespace kmeans
