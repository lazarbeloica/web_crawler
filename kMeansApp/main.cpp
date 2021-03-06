

#include <algorithm>
#include <random>
#include <array>
#include <limits>
#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <sstream>

double fuzzyLimit = 0.00002;

struct Point
{
    std::array<double, COORDINATES_NUMBER> coordinates;
    int meta;

    Point& operator+=(const Point& rhs) {
        std::transform(coordinates.begin(), coordinates.end(), rhs.coordinates.begin(), coordinates.begin(), [](auto x, auto y) {
            return x + y;
        });
    };

    Point& operator/=(const int denominator) {
        std::for_each(coordinates.begin(), coordinates.end(), [&](auto& x) {
            x /= denominator;
        });
    };

    Point():meta(K) {}
};

double operator-(const Point& a, const Point& b) {
    std::array<double, COORDINATES_NUMBER> sum;
    std::transform(a.coordinates.begin(), a.coordinates.end(), b.coordinates.begin(), sum.begin(), [&](auto x, auto y) {
        return std::pow(x - y, 2);
    });

    return std::sqrt(std::accumulate(sum.begin(), sum.end(), 0));
}

bool operator==(const Point& a, const Point& b) {
    return a.coordinates == b.coordinates;
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
    std::copy(p.coordinates.begin(), p.coordinates.end(), std::ostream_iterator<double>(os, ","));
    os << p.meta;
    os <<"\n";
    return os;
}

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

    std::minstd_rand0 g(32323521313535);
    std::uniform_int_distribution <int> uf(0, data.size() - 1);

    std::ifstream infile(argv[1]);
    std::string line;

    std::for_each(data.begin(), data.end(), [&](Point& p) {
        std::getline(infile,line);
        std::vector<std::string> tmp = tokenize( line, ',');
        for(int i = 0; i < COORDINATES_NUMBER; i++) {
            p.coordinates[i] = std::stoi(tmp[i]);
        }
    });

    for(int i = 0; i < kar.size(); i++) {
        auto tmp = data[uf(g)];
        for (int j = 0; j < i; j++) {
            if (tmp == kar[j]) {
                auto tmp = data[uf(g)];
                j = 0; // restart the loop
            }
        }
        kar[i] = tmp;
    }

    std::ofstream startCenters("frames/center0.csv");

    std::copy(kar.begin(), kar.end(), std::ostream_iterator<Point>(startCenters));

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
        std::ofstream pointsColours("frames/pointColour" + std::to_string(i) + ".csv");

        std::copy(kar.begin(), kar.end(), std::ostream_iterator<Point>(centers));
        std::for_each(data.begin(), data.end(), [&] (const Point p) {
            pointsColours << p.meta << '\n';
        });

    } while(!fuzzyEquals(kar, old_kar) && i < 10000);

    return 0;
}
