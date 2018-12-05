DROP TABLE artist_profile;
DROP TABLE track_list;
DROP TABLE artist;

CREATE TABLE artist
(
	id INT PRIMARY KEY AUTO_INCREMENT,
    artist_name VARCHAR(60)
);


CREATE TABLE artist_profile
(
	id INT AUTO_INCREMENT PRIMARY KEY,
    artist_id INT NOT NULL,
    header VARCHAR(30),
    content VARCHAR(30),
    FOREIGN KEY fk_id(artist_id)
    REFERENCES artist(id),
    unique(artist_id, header)
);


CREATE TABLE track_list
(
	id INT AUTO_INCREMENT PRIMARY KEY,
    artist_id INT NOT NULL,
    track_name VARCHAR(60),
    FOREIGN KEY fk_id(artist_id)
    REFERENCES artist(id),
    unique(artist_id, track_name)
);



