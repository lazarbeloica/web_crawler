from common.db.dizcoz_db_driver import DiscozDBDriver
from datetime import datetime
import csv

query_base = "select {} from relevant_data {};"
suported_coordinates = ["year_released", "genre", "style", "rating", "versions", "country", "album_name"]

def get_help():
    help = "Available input data options are:\n"
    for coordinate in suported_coordinates:
        help = help + "* " + coordinate + "\n"
    return help

def trasncode_style(style):
    code = ["Folk", "Progressive House", "Vocal", "Europop", "Techno", "Electro", "Experimental", "Pop Rock", "Ballad", "Progressive Trance", "Trance", "Punk", "Psy-Trance",
            "House", "Alternative Rock", "Noise", "Ambient", "Black Metal", "Deep House", "Tech House", "Industrial", "Hardcore", "Indie Rock", "Funk", "Acoustic", "Abstract",
            "Minimal", "Heavy Metal", "Thrash", "Hard Rock", "Disco", "Death Metal", "Drone", "Dark Ambient", "Downtempo", "Folk Rock", "Rock & Roll", "Classic Rock",
            "Dub Techno", "Goa Trance", "Blues Rock", "Synth-pop", "Euro House", "New Wave", "Lo-Fi", "Garage Rock", "Pop Rap", "Psychedelic Rock", "Grindcore", "Post Rock",
            "Conscious", "IDM", "Prog Rock", "Art Rock", "Doom Metal", "Schlager", "Hip Hop", "Emo", "Drum n Bass", "Harsh Noise Wall", "Grunge", "EBM", "Breakbeat", "Dub",
            "Post-Punk", "Nu-Disco", "Dance-pop", "Avantgarde", "Nu Metal", "Romani", "Musique Concrète", "Jazz-Rock", "Indie Pop", "Trap", "Reggae", "Goth Rock", "Parody",
            "Stoner Rock", "Brass Band", "Dubstep", "Gangsta", "Rhythmic Noise", "Thug Rap", "Power Metal", "Trip Hop", "Eurobeat", "Eurodance", "Leftfield", "Country Rock",
            "Chanson", "Metalcore", "Soft Rock", "Fusion", "Instrumental", "Power Pop", "RnB/Swing", "Glitch", "Gypsy Jazz", "Easy Listening", "Rhythm & Blues",
            "Contemporary", "Nursery Rhymes", "Power Electronics", "Shoegaze", "Acid", "Field Recording", "Oi", "Symphonic Rock", "Breaks", "Classical", "Contemporary Jazz",
            "Deep Techno", "Free Improvisation", "Neo-Classical", "Darkwave", "Progressive Metal", "Ska", "Jazz-Funk", "Speed Metal", "Surf", "Reggaeton", "Soul",
            "Electro House", "Jungle", "New Age", "Smooth Jazz", "Soundtrack", "Spoken Word", "Electric Blues", "Religious", "Krautrock", "Melodic Death Metal",
            "Poetry", "Tech Trance", "Avant-garde Jazz", "Hardcore Hip-Hop", "Swing", "Rockabilly", "Roots Reggae", "Jazzy Hip-Hop", "Post-Modern", "Tribal",
            "Melodic Hardcore", "Bass Music", "Crust", "Reggae-Pop", "Afrobeat", "Chiptune", "Modern", "Sludge Metal", "Country", "Ethereal", "Math Rock", "Neofolk",
            "Radioplay", "Southern Rock", "Modern Classical", "Romantic", "Speech", "Audiobook", "Country Blues", "Crunk", "Educational", "Future Jazz", "Népzene",
            "Pop Punk", "Salsa", "Comedy", "Latin Jazz", "Ragga HipHop", "Big Band", "Brit Pop", "Gothic Metal", "Medieval", "Minimal Techno", "Rumba", "Breakcore",
            "Ethno-pop", "Free Jazz", "Laïkó", "Post-Hardcore", "Score", "Tropical House", "Acid House", "Big Beat", "Boom Bap", "Grime", "No Wave", "Space-Age",
            "Story", "AOR", "Acid Jazz", "Baroque", "Cool Jazz", "Cut-up/DJ", "Dancehall", "Garage House", "Harmonica Blues", "Latin", "Rocksteady", "Soul-Jazz",
            "Synthwave", "Theme", "Boogie", "Bossa Nova", "Broken Beat", "Chicago Blues", "Dixieland", "Favela Funk", "Glam", "Progressive Breaks", "Pub Rock",
            "Ragga", "UK Garage", "Vaporwave", "Volksmusik", "Arena Rock", "Folk Metal", "Funk Metal", "G-Funk", "Illbient", "Jazzdance", "Modern Electric Blues",
            "Musical", "Novelty", "Renaissance", "Space Rock", "Bubblegum", "Chillwave", "Delta Blues", "Freestyle", "Gospel", "Italo-Disco", "Lounge", "Monolog",
            "Mouth Music", "Psychobilly", "Rebetiko", "Special Effects", "Tango", "Turntablism", "Witch House", "Bassline", "Beat", "Bossanova", "Contemporary R&B",
            "Euro-Disco", "Ghetto House", "Ghettotech", "Hip-House", "Horrorcore", "Light Music", "Neo-Romantic", "Opera", "Screw", "Sound Collage", "Sound Poetry",
            "Speedcore", "Therapy", "Acid Rock", "Beatdown", "Bounce", "Coldwave", "Cubano", "Deathcore", "Early", "Education", "Fado", "Flamenco", "Ghetto",
            "Hard House", "Hi NRG", "Italodance", "Neo Trance", "Piano Blues", "Pipe & Drum", "Political", "Promotional", "Psychedelic", "Public Broadcast",
            "Ragtime", "Éntekhno", "African", "Afro-Cuban", "Bluegrass", "Boogie Woogie", "Canzone Napoletana", "Celtic", "Cha-Cha", "Cumbia", "DJ Battle Tool",
            "Deathrock", "Doo Wop", "Dream Pop", "Electroclash", "Free Funk", "Funeral Doom Metal", "Goregrind", "Happy Hardcore", "Hard Bop", "Hard Techno",
            "Hardstyle", "Hiplife", "Impressionist", "Indian Classical", "Juke", "Jump Blues", "Mambo", "New Beat", "Nordic", "Overtone Singing", "Pornogrind",
            "Power Violence", "Reggae Gospel", "Samba", "Schranz", "Sound Art", "Technical", "Texas Blues", "Thai Classical", "Tribal House", "UK Funky",
            "Viking Metal", "Western Swing"]
    for i in range(0, len(code)):
        if code[i].lower() == style.lower():
            return i

    raise Exception("Style not suported")

def trasncode_genre(genre):
    code = {
        "Folk" : 1,
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
        "Country" : 15,
        "Brass & Military" : 16,
        "Brass" : 17,
        "Military" : 18,
        "Children's" : 19
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

input = ["versions", "rating"]
query = build_query(input)
print(query)
print(transcode_coordinate_tuple(input, ged_data_from_db(query)[0]))
print_to_csv(transcode_coordinate_data(input, ged_data_from_db(query)), "file.csv")
