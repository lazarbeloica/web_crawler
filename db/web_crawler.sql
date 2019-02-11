	DROP VIEW relevant_data ;
	DROP TABLE album_vocals;
    DROP TABLE album_writers;
    DROP TABLE album_aragments;
	DROP TABLE track_list;
    DROP TABLE album_genre;
    DROP TABLE album_style;
    DROP TABLE album_misc_content;
	DROP TABLE album;
	DROP TABLE artist;

	CREATE TABLE artist
	(
		id INT PRIMARY KEY AUTO_INCREMENT,
		artist_name national VARCHAR(90),
		unique(artist_name)
	);

	create table album
	(
		id int auto_increment primary key,
		artist_id int not null,
		album_name national varchar(90) not null,
		versions int not null,
		released DATE default null,
		country national VARCHAR(60),
        rating float default NULL,
		foreign key fk_id(artist_id)
		references artist(id)
	);

	CREATE TABLE album_style
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		album_id INT NOT NULL,
		style national VARCHAR(40),
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
		unique(album_id, style)
	);

	CREATE TABLE album_genre
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		album_id INT NOT NULL,
		genre national VARCHAR(40),
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
		unique(album_id, genre)
	);

	CREATE TABLE album_misc_content
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		album_id INT NOT NULL,
		header VARCHAR(30),
		content national VARCHAR(90),
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
		unique(album_id, header)
	);

	CREATE TABLE track_list
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		album_id INT NOT NULL,
		track_name national varchar(90),
        duration int,
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
		unique(album_id, track_name)
	);

	CREATE TABLE album_vocals
	(
		album_id INT NOT NULL,
		artist_id INT NOT NULL,
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
        FOREIGN KEY fk_id(artist_id)
		REFERENCES artist(id),
		primary key(album_id, artist_id)
	);

    CREATE TABLE album_writers
	(
		album_id INT NOT NULL,
		artist_id INT NOT NULL,
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
        FOREIGN KEY fk_id(artist_id)
		REFERENCES artist(id),
		primary key(album_id, artist_id)
	);

    CREATE TABLE album_aragments
	(
		album_id INT NOT NULL,
		artist_id INT NOT NULL,
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
        FOREIGN KEY fk_id(artist_id)
		REFERENCES artist(id),
		primary key(album_id, artist_id)
	);

    CREATE VIEW relevant_data (album_name, versions, year_released, country, rating, genre, style)
    AS
    select al.album_name, al.versions, al.released, al.country, al.rating, alge.genre, alst.style
    from album al left join album_genre alge on al.id = alge.album_id left join album_style alst on alge.album_id = alst.album_id;
