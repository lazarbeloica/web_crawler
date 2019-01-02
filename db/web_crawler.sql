	DROP TABLE track_list;
    DROP TABLE album_genre;
    DROP TABLE album_style;
    DROP TABLE album_misc_content;
    DROP TABLE album_format;
	DROP TABLE album;
	DROP TABLE artist;

	CREATE TABLE artist
	(
		id INT PRIMARY KEY AUTO_INCREMENT,
		artist_name national VARCHAR(60)
	);

	create table album
	(
		id int auto_increment primary key,
		artist_id int not null,
		album_name national varchar(60) not null,
		versions int not null,
		released DATE default null,
		country national VARCHAR(60),
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

	CREATE TABLE album_format
	(
		id INT AUTO_INCREMENT PRIMARY KEY,
		album_id INT NOT NULL,
		album_format VARCHAR(40),
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
		unique(album_id, album_format)
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
		track_name national varchar(60),
        duration int,
		FOREIGN KEY fk_id(album_id)
		REFERENCES album(id),
		unique(album_id, track_name)
	);

