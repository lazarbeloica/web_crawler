from common.db.dizcoz_db_driver import DiscozDBDriver
from datetime import datetime
import csv
import os
import kMeansApp.plotter

query_base = "select {} from relevant_data {};"
suported_coordinates = ["year_released", "genre", "style", "rating", "versions", "country", "album_name"]

def get_help():
    help = "Available input data options are:\n"
    for coordinate in suported_coordinates:
        help = help + "* " + coordinate + "\n"
    return help

def trasncode_style(style):
    code = ["Baroque", "Renaissance", "Classical", "Neo-Classical", "Modern Classical", "Indian Classical", "Thai Classical", "Impressionist",
            "Medieval", "Religious", "Opera", "Post-Modern", "Fado", "Samba", "Schlager", "Chanson", "Folk", "African", "Afro-Cuban", "Celtic",
            "Cha-Cha", "Country", "Western Swing", "Salsa", "Schranz", "Volksmusik", "Mambo", "Nordic", "Rumba", "Romani", "Gospel", "Latin", "Neofolk",
            "Tango", "Cubano", "Flamenco",  "Canzone Napoletana", "Italodance", "Trap", "Nu-Disco", "Italo-Disco" ,
            "Euro-Disco", "Disco", "Breakbeat", "Dub", "Drum n Bass", "Dubstep", "Psychedelic", "Progressive Trance", "Trance", "Psy-Trance", "Goa Trance",
            "Tech Trance", "Neo Trance", "Techno", "Dub Techno", "Deep Techno", "Minimal Techno", "Hard Techno", "Electro", "Eurobeat", "Eurodance",
            "Broken Beat", "Power Electronics", "Ghettotech", "Happy Hardcore", "Progressive Breaks", "Technical", "New Beat", "Cut-up/DJ", "Breakcore",
            "Space-Age", "Dancehall", "DJ Battle Tool", "Big Beat", "Bass Music", "Hardstyle", "Electroclash", "Electro House", "Progressive House",
            "House", "Deep House", "Tech House", "Euro House", "Tropical House", "Acid House", "Garage House", "Witch House", "Ghetto House", "Hip-House",
            "Hard House", "Tribal House", "Hip Hop", "Trip Hop", "Jazzy Hip-Hop", "Hardcore Hip-Hop", "Ragga HipHop", "Freestyle", "Pop Rap", "Thug Rap",
            "Ghetto", "Gangsta", "Europop", "Synth-pop", "Dance-pop", "Indie Pop", "Power Pop", "Reggae-Pop", "Brit Pop", "Ethno-pop", "Dream Pop",
            "Pop Punk", "Ska", "Punk", "Psychobilly", "Post-Punk", "Melodic Hardcore", "Black Metal", "Heavy Metal", "Death Metal", "Doom Metal",
            "Nu Metal", "Power Metal", "Progressive Metal", "Speed Metal", "Melodic Death Metal", "Sludge Metal", "Gothic Metal", "Folk Metal",
            "Funeral Doom Metal", "Funk Metal", "Viking Metal", "Grindcore", "Horrorcore", "Grime", "Power Violence", "Metalcore", "Hardcore" ,
            "Post-Hardcore", "Deathcore", "Speedcore", "Goregrind" , "Pornogrind", "Thrash", "Reggae", "Reggaeton", "Roots Reggae", "Reggae Gospel",
            "Ragtime", "Pipe & Drum", "Ragga", "Afrobeat", "RnB/Swing", "Swing", "Rhythm & Blues", "Contemporary R&B", "Electric Blues", "Country Blues",
            "Harmonica Blues", "Chicago Blues", "Bluegrass", "Modern Electric Blues", "Boogie Woogie", "Delta Blues", "Piano Blues", "Jump Blues",
            "Texas Blues", "Rockabilly", "Rocksteady", "Emo", "Glam", "Pop Rock", "Blues Rock", "Alternative Rock", "Indie Rock", "Hard Rock",
            "Folk Rock", "Garage Rock", "Psychedelic Rock", "Post Rock", "Prog Rock", "Art Rock", "Goth Rock", "Stoner Rock", "Country Rock",
            "Soft Rock", "Symphonic Rock", "Krautrock", "Math Rock", "Southern Rock", "Pub Rock", "Arena Rock", "Space Rock", "Acid Rock",
            "Classic Rock", "Deathrock", "Jazz-Rock", "Rock & Roll", "Grunge", "UK Garage", "Funk", "Favela Funk", "G-Funk", "Free Funk", "UK Funky",
            "Dixieland", "Jazz-Funk", "Gypsy Jazz", "Contemporary Jazz", "Smooth Jazz", "Avant-garde Jazz", "Future Jazz", "Latin Jazz", "Free Jazz",
            "Acid Jazz", "Cool Jazz", "Soul-Jazz", "Hard Bop", "Boogie", "Doo Wop", "Jazzdance", "Boom Bap", "Soul", "Overtone Singing" , "Vocal" ,
            "Ambient" , "Acoustic" , "Dark Ambient" , "Downtempo", "Sound Art" , "Romantic" , "Ballad" , "Neo-Romantic",
            "Exp erimental", "Noise", "Industrial", "Abstract", "Minimal", "Drone", "New Wave", "Lo-Fi", "Conscious", "IDM", "Harsh Noise Wall",
            "EBM", "Avantgarde", "Parody", "Brass Band", "Rhythmic Noise", "Leftfield", "Fusion", "Instrumental", "Glitch", "Easy Listening",
            "Contemporary", "Nursery Rhymes", "Shoegaze", "Acid", "Field Recording", "Oi", "Breaks", "Free Improvisation", "Darkwave", "Surf",
            "Jungle", "New Age", "Soundtrack", "Spoken Word", "Poetry", "Tribal", "Crust", "Chiptune", "Modern", "Ethereal", "Radioplay", "Speech",
            "Audiobook", "Crunk", "Educational", "Comedy", "Big Band", "Score", "No Wave", "Story", "AOR", "Synthwave", "Theme", "Bossa Nova",
            "Vaporwave", "Illbient", "Musical", "Novelty", "Bubblegum", "Chillwave", "Lounge", "Monolog", "Mouth Music", "Rebetiko",
            "Special Effects", "Turntablism", "Bassline", "Beat", "Bossanova", "Light Music", "Screw", "Sound Collage", "Sound Poetry", "Therapy",
            "Beatdown", "Bounce", "Coldwave", "Early", "Education", "Hi NRG", "Political", "Promotional", "Public Broadcast", "Cumbia", "Hiplife", "Juke"]

    for i in range(0, len(code)):
        if code[i].lower() == style.lower():
            return i

    raise Exception("Style not suported")

def trasncode_genre(genre):
    code = {
        "Electronic" : 2,
        "Stage & Screen" : 3,
        "Hip Hop" : 4,
        "World" : 5,
        "Rock" : 6,
        "Pop" : 7,
        "Classical" : 8,
        "Latin" : 9,
        "Jazz" : 10,
        "Blues" : 11,
        "Funk / Soul" : 12,
        "Reggae" : 13,
        "Non-Music" : 14,
        "Folk" : 15,
        "Country" : 16,
        "Brass & Military" : 17,
        "Brass" : 18,
        "Military" : 19,
        "Children's" : 20
    }
    try:
        return code[genre]
    except:
        msg = "Album genre {} not supporetd".format(genre)
        raise Exception(msg)

def trasncode_year(year):
    return datetime(year).year

def trasncode_rating(rating):
    return int(rating)

def trasncode_versions(ver):
    return int(float(ver))

def trasncode_coutntry(country):
    code = {
        "serbia" : 1,
        "yugoslavia" : 2
    }
    return code[country.lower()]

def build_query(data):
    condition_map = {
        "year_released" : "released is not NULL",
        "genre" : "genre != ''",
        "style" : "style != ''",
        "rating" : "rating  != 0"
    }

    tables = ""
    conditions = ""

    for el in data:
        if tables != "":
            tables = tables + ", "
        tables = tables + el

        if el in condition_map:
            if conditions != "":
                conditions = conditions + " AND "
            else:
                conditions = " where "
            conditions = conditions + condition_map[el]

    return query_base.format(tables, conditions)

def ged_data_from_db(query):
    db = DiscozDBDriver()
    db._connect()
    db.custom_query(query)
    return db.get_all_results()

transcode_map = {
        "year_released" : trasncode_year,
        "genre" : trasncode_genre,
        "style" : trasncode_style,
        "rating" : trasncode_rating,
        "versions" : trasncode_versions,
        "country" : trasncode_year
    }

def transcode_coordinate_tuple(coordinates, data_tuple):

    result = []
    for i in range (0, len(coordinates)):
        result.append(transcode_map[coordinates[i]](data_tuple[i]))
    return result

def transcode_coordinate_data(coordinates, data):
    transcoded_matrix = []
    for data_tuple in data:
        transcoded_matrix.append(transcode_coordinate_tuple(coordinates, data_tuple))
    return transcoded_matrix

def print_to_csv(transcoded_matrix, filename):
    lines = []
    for row in transcoded_matrix:
        line = ""
        for el in row:
            if line != "":
                line = line + ", "
            line = line + "{}".format(el)
        line = line + "\n"
        lines.append(line)

    with open(filename, 'w') as output:
        output.writelines(lines)

    return len(lines)

def run_compilation(K, data_set_size, num_of_coordinates, output_file):
    cmd = "g++ -std=c++14 kMeansApp/main.cpp -DINPUT_DATA_SET_SIZE={} -DK={} -DCOORDINATES_NUMBER={} -o kMeansApp/{}".format(data_set_size, K, num_of_coordinates, output_file)
    print(cmd)
    os.system(cmd)

def run_kmeans_prog(program_name, data_file):
    cmd = "cd kMeansApp; ./{} {}".format(program_name, data_file)
    print(cmd)
    os.system(cmd)

def check_coordinates(coordinates):
    for coordinate in coordinates:
        if coordinate not in suported_coordinates:
            print("Coordinate {} not supported".format(coordinate))
            print(get_help())
            return False
    return True

def run(coordinates, K):
    if len(coordinates) == 0:
        print("No data to process")
        print(get_help())
        return True

    if check_coordinates(coordinates) != True:
        return False
    if K < 1:
        print("K must be positive integer!")

    data_file = "kMeansApp/points.csv"
    program_name = "kmeansAlg"
    query = build_query(coordinates)
    print("Sending query to db: " + query)
    data = ged_data_from_db(query)
    print_to_csv(transcode_coordinate_data(coordinates, data), data_file)
    run_compilation(K, len(data), len(coordinates), program_name)
    run_kmeans_prog(program_name, "points.csv")
    return True

