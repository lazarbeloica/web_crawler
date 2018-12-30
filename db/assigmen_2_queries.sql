--a) izlistati koliko zapisa pripada svakom od žanrova
select COUNT(*)
from album_genre
group by genre;

--b) izlistati koliko zapisa pripada svakom od stilova
select COUNT(*)
from album_style
group by style;

--c) prikazati rang listu prvih 10 albuma koji imaju najveći broj izdatih verzija (više albuma
--   može deliti jedno mesto na rang listi, pa konačan broj albuma na listi može biti i veći od 10)
select album_name
from album
group by versions asc
LIMIT 10;

--d) prikazati prvih 50 osoba koje imaju:
--    * najveći generalni rejting u pesmama (Credits)
--    * najviše učešća kao vokal (Vocals)
--    * najviše napisanih pesama (Writing & Arrangement)
-------------- not implemented --------------

--e) prikazati prvih 100 pesama koje se nalaze na najviše albuma, i osim broja albuma
--   (COUNT), uz svaku pesmu napisati podatke o tim albumima (Format, Country,
--   Year/Relased, Genre, Style)
select track_name
from track_list
group by track_name, count(album_id)
limit 100

