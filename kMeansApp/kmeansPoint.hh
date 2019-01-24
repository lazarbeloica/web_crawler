#pragma once

#include "kmeansCommon.hh"

#include <array>
#include <iostream>

namespace kmeans
{

struct Point
{
    std::array<double, COORDINATES_NUM> coordinates;
    int meta;

    Point& operator+=(const Point&);
    Point& operator/=(const int);

    Point():meta(K) {}
};

double operator-(const Point&, const Point&);
std::ostream& operator<<(std::ostream&, const Point&);

} // namespace kmeans