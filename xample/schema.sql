DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS technology;
DROP TABLE IF EXISTS difficulty;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE technology (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL
);

CREATE TABLE difficulty (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL
);

CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	likes INTEGER NOT NULL DEFAULT 0,
	author_id INTEGER NOT NULL,
	title TEXT NOT NULL,
	body TEXT NULL,
	link TEXT NOT NULL,
	technology INTEGER NOT NULL,
	difficulty INTEGER NOT NULL,
	-- filled asynchronously
	link_accessible BOOLEAN NULL,
	project_name TEXT NULL,
	project_author TEXT NULL,

	CHECK(length("title") <= 100),
	CHECK (link_accessible IN (NULL, 0, 1)),

	FOREIGN KEY (author_id) REFERENCES user (id),
	FOREIGN KEY (technology) REFERENCES technology (id),
	FOREIGN KEY (difficulty) REFERENCES technology (id)
);
