from common.db.dizcoz_db_driver import DiscozDBDriver

db = DiscozDBDriver()
db.custom_query("select count(*) from album")
albums_in_db = db.get_next_result()

query_map = {
    "genre": "select genre from album_genre",
    "style": "select genre from album_style",
    "year" : "select relesed from album"
}

"select c1,c2,c3 from t1, t2, t3 where common_cond " join?

transcode_genre_map = {}

transcode_style_map = {}