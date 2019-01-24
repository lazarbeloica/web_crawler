
#include "kmeansPoint.hh"

#include <algorithm>
#include <random>
#include <array>
#include <limits>
#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <sstream>

using namespace kmeans;

double fuzzyLimit = 0.00002;

template<class T>
bool fuzzyEquals(const T& a1, const T& a2) {

    for(auto i = 0; i < a1.size(); i++) {
        for(auto j = 0; j < a1[i].coordinates.size(); j++){
            if ( fuzzyLimit < a1[i].coordinates[j] - a2[i].coordinates[j] ||
                    a1[i].coordinates[j] - a2[i].coordinates[j] < fuzzyLimit * (-1))
                return false;
        }
    }
    return true;
}

std::vector<std::string> tokenize(std::string const &str, const char delim)
{
	// construct a stream from the string
	std::stringstream ss(str);

	std::string s;
    std::vector<std::string> out;
	while (std::getline(ss, s, delim)) {
		out.push_back(s);
	}
    return out;
}

int main(int argc, char *argv[]) {

    if(argc != 2) {
        return 0;
    }

    std::array<Point, INPUT_DATA_SET_SIZE> data;
    std::array<Point, K> kar;

    std::minstd_rand0 g(12345573);
    std::uniform_int_distribution <int> uf(0, data.size() - 1);

    std::ifstream infile(argv[1]);
    std::string line;

    std::for_each(data.begin(), data.end(), [&](Point& p) {
        std::getline(infile,line);
        std::vector<std::string> tmp = tokenize( line, ',');
        for(int i = 0; i < COORDINATES_NUM; i++) {
            p.coordinates[i] = std::stoi(tmp[i]);
        }
    });

    for(int i = 0; i < kar.size(); i++) {
        kar[i] = data[i];
    }

    std::ofstream startCenters("frames/center0.csv");
    std::ofstream startPoints("frames/point0.csv");

    std::copy(kar.begin(), kar.end(), std::ostream_iterator<Point>(startCenters));
    std::copy(data.begin(), data.end(), std::ostream_iterator<Point>(startPoints));

    auto old_kar = kar;

    size_t i = 0;

    do {
        old_kar = kar;
        ++i;

        std::for_each(kar.begin(), kar.end(),[](Point& k) {k.meta = 0;});

        std::for_each(data.begin(), data.end(), [&](Point& p) {
            double min = std::numeric_limits<double>::max();
            for (int i = 0; i < kar.size(); i++) {
                double tmp = kar[i] - p;
                if (tmp < min) {
                    min = tmp;
                    p.meta = i;
                }
            }

            kar[p.meta].meta++;
        });

        std::for_each(kar.begin(), kar.end(),[](Point& k) {k.coordinates.fill(0.0);});

        std::for_each(data.begin(), data.end(), [&] (const Point& p){
            kar[p.meta] += p;
        });

        std::for_each(kar.begin(), kar.end(), [&](Point& k) {
            k /= k.meta;
        });

        std::ofstream centers("frames/center" + std::to_string(i) + ".csv");
        std::ofstream points("frames/point" + std::to_string(i) + ".csv");

        std::copy(kar.begin(), kar.end(), std::ostream_iterator<Point>(centers));
        std::copy(data.begin(), data.end(), std::ostream_iterator<Point>(points));

    } while(!fuzzyEquals(kar, old_kar) && i < 10000);

    return 0;
}
