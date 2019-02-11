-- a) izlistati koliko zapisa pripada svakom od žanrova
select COUNT(*)
from album_genre
group by genre;

-- b) izlistati koliko zapisa pripada svakom od stilova
select COUNT(*)
from album_style
group by style;

-- c) prikazati rang listu prvih 10 albuma koji imaju najveći broj izdatih verzija (više albuma
--   može deliti jedno mesto na rang listi, pa konačan broj albuma na listi može biti i veći od 10)
select album_name
from album
order by versions asc
LIMIT 10;

-- d) prikazati prvih 50 osoba koje imaju:
--    * najveći generalni rejting u pesmama (Credits)
select art.artist_name, avg(alb.rating)
from artist art, album alb
where alb.artist_id = art.id and
alb.rating != 0 and alb.rating is not null
group by art.artist_name
order by avg(alb.rating) desc
limit 50;

--    * najviše učešća kao vokal (Vocals)
select art.artist_name, count(vocal.album_id)
from artist art, album_vocals vocal
where art.id = vocal.artist_id
group by vocal.artist_id
order by count(vocal.album_id) desc
limit 50;
--    * najviše napisanih pesama (Writing & Arrangement)


-- e) prikazati prvih 100 pesama koje se nalaze na najviše albuma, i osim broja albuma
--   (COUNT), uz svaku pesmu napisati podatke o tim albumima (Format, Country,
--   Year/Relased, Genre, Style)
select track_name
from track_list
group by track_name
order by count(album_id)
limit 100

