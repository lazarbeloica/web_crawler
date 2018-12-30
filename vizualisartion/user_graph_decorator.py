from vizualisartion.graph_decorator import RegisterDecorator
import pandas as pnd
import common.utils.utils as utils
import itertools


'''
Brief: In this file are located user-defined graph decoratros
'''

#class ExampleDecorator(RegisterDecorator):
#
#     def get_brief(self):
#         return 'Example graph decorator 1'
#
#     def get_dataframe(self):
#         return pnd.DataFrame({'a':[1, 1], 'b':[2, 2]})
#
#
#
#class AlbumNumberDecorator(RegisterDecorator):
#
#    def get_brief(self):
#        return 'Number of albums by decades'
#
#    def get_dataframe(self):
#        query_base = """select count(*) from album where released between '{0}' and '{1}';"""
#        query0 = query_base.format(utils.convert_to_date('1.1.1950.'), utils.convert_to_date('31.12.1950.'))
#        query1 = query_base.format(utils.convert_to_date('1.1.1960.'), utils.convert_to_date('31.12.1969.'))
#        query2 = query_base.format(utils.convert_to_date('1.1.1970.'), utils.convert_to_date('31.12.1979.'))
#        query3 = query_base.format(utils.convert_to_date('1.1.1980.'), utils.convert_to_date('31.12.1989.'))
#        query4 = query_base.format(utils.convert_to_date('1.1.1990.'), utils.convert_to_date('31.12.1999.'))
#        query5 = query_base.format(utils.convert_to_date('1.1.2000.'), utils.convert_to_date('31.12.2009.'))
#        query6 = query_base.format(utils.convert_to_date('1.1.2010.'), utils.convert_to_date('31.12.2018.'))
#
#        self.db.custom_query(query0)
#        res0 = self.db.get_next_result()[0]
#
#        self.db.custom_query(query1)
#        res1 = self.db.get_next_result()[0]
#
#        self.db.custom_query(query2)
#        res2 = self.db.get_next_result()[0]
#
#        self.db.custom_query(query3)
#        res3 = self.db.get_next_result()[0]
#
#        self.db.custom_query(query4)
#        res4 = self.db.get_next_result()[0]
#
#        self.db.custom_query(query5)
#        res5 = self.db.get_next_result()[0]
#
#        self.db.custom_query(query6)
#        res6 = self.db.get_next_result()[0]
#
#        return pnd.DataFrame({'1950-1959':[res0], '1960-1969':[res1],
#                            '1970-1979':[res2], '1980-1989':[res3],
#                            '1990-1999':[res4], '2000-2009':[res5],
#                            '2010-2018':[res6]})
#
#
#class MostCommonGenresDecorator(RegisterDecorator):
#
#    def get_brief(self):
#        return 'Six most common genres'
#
#
#    def get_dataframe(self):
#
#        query_base = """select genre, count(genre) from album_genre group by genre order by count(genre) limit 6;"""
#        self.db.custom_query(query_base)
#        data = {}
#        for row in self.db.get_all_results():
#            data[row[0]] = [row[1]]
#
#        return pnd.DataFrame(data)


#c) Broj pesama prema trajanju (do 90 sekundi, 91-180, 181-240, 241-300, 301-360, 361
#sekunda i više)
#

#class CirilicVsLatinicNamesNumberDecorator(RegisterDecorator):
#
#    def get_brief(self):
#        return 'Gets number (and procentige) of Cirilc and Latinic album titles '
#
#
#    def get_dataframe(self):
#
#        cyrlic_query = """select count(*) FROM album WHERE album_name REGEXP '[А-Ша-ш]+';"""
#        latinic_query = """select count(*) FROM album WHERE album_name REGEXP '[A-Za-z]+';"""
#
#        self.db.custom_query(cyrlic_query)
#        cirlic = self.db.get_next_result()[0]
#
#        self.db.custom_query(latinic_query)
#        latinic = self.db.get_next_result()[0]
#
#        return pnd.DataFrame({"Cirilic titles":[cirlic],
#                            "Latin titles":[latinic]})
#
#
#
#class CirilicVsLatinicNamesPercentDecorator(RegisterDecorator):
#
#    def get_brief(self):
#        return 'Gets procentige of Cirilc and Latinic album titles '
#
#
#    def get_dataframe(self):
#
#        cyrlic_query = """select count(*) FROM album WHERE album_name REGEXP '[А-Ша-ш]+';"""
#        latinic_query = """select count(*) FROM album WHERE album_name REGEXP '[A-Za-z]+';"""
#        all_titles_query = """select count(*) FROM album;"""
#
#        self.db.custom_query(cyrlic_query)
#        cirlic = self.db.get_next_result()[0]
#
#        self.db.custom_query(latinic_query)
#        latinic = self.db.get_next_result()[0]
#
#        self.db.custom_query(all_titles_query)
#        all_titles = self.db.get_next_result()[0]
#
#        cirlic_percent = cirlic / all_titles * 100
#        latinic_percent = latinic / all_titles * 100
#
#        return pnd.DataFrame({"Cirilic titles (%)":[cirlic_percent],
#                            "Latin titles(%)":[latinic_percent]})
#


class GenresPerAlbumDecorator(RegisterDecorator):

    def get_brief(self):
        return 'Gets number of genres per album '


    def get_dataframe(self):

        base_query = """ SELECT COUNT(*) FROM (SELECT COUNT(ag.album_id) AS cnt FROM album_genre ag GROUP BY ag.album_id HAVING cnt = {0}) x; """
        one_genre_query = base_query.format(1)
        two_genre_query = base_query.format(2)
        three_genre_query = base_query.format(3)
        more_genre_query = """ SELECT COUNT(*) FROM (SELECT COUNT(ag.album_id) AS cnt FROM album_genre ag GROUP BY ag.album_id HAVING cnt > 3) x; """

        self.db.custom_query(one_genre_query)
        one_genre = self.db.get_next_result()[0]

        self.db.custom_query(two_genre_query)
        two_genre = self.db.get_next_result()[0]

        self.db.custom_query(three_genre_query)
        three_genre = self.db.get_next_result()[0]

        self.db.custom_query(more_genre_query)
        more_genre = self.db.get_next_result()[0]

        return pnd.DataFrame({"One genre":[one_genre],
                            "Two genres":[two_genre],
                            "Three genres":[three_genre],
                            "Four and more genres":[more_genre]})


class GenresPerAlbumPercentegDecorator(RegisterDecorator):

    def get_brief(self):
        return 'Gets percentige of genres per album '


    def get_dataframe(self):

        base_query = """ SELECT COUNT(*) FROM (SELECT COUNT(ag.album_id) AS cnt FROM album_genre ag GROUP BY ag.album_id HAVING cnt = {0}) x; """
        one_genre_query = base_query.format(1)
        two_genre_query = base_query.format(2)
        three_genre_query = base_query.format(3)
        more_genre_query = """ SELECT COUNT(*) FROM (SELECT COUNT(ag.album_id) AS cnt FROM album_genre ag GROUP BY ag.album_id HAVING cnt > 3) x; """
        number_of_albums_query = """ select count(id) from album;"""


        self.db.custom_query(one_genre_query)
        one_genre = self.db.get_next_result()[0]

        self.db.custom_query(two_genre_query)
        two_genre = self.db.get_next_result()[0]

        self.db.custom_query(three_genre_query)
        three_genre = self.db.get_next_result()[0]

        self.db.custom_query(more_genre_query)
        more_genre = self.db.get_next_result()[0]

        self.db.custom_query(number_of_albums_query)
        all_albums = self.db.get_next_result()[0]

        return pnd.DataFrame({"One genre":[one_genre / all_albums * 100],
                            "Two genres":[two_genre / all_albums * 100],
                            "Three genres":[three_genre / all_albums * 100],
                            "Four and more genres":[more_genre / all_albums * 100]})