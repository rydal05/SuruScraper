DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wishlist_item_history;
DROP TABLE IF EXISTS wishlist_item_stats;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE wishlist (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	url TEXT UNIQUE NOT NULL,
	name TEXT NOT NULL,
	price TEXT NOT NULL DEFAULT "N/A",
	lastSeenDateTime TEXT NOT NULL DEFAULT "N/A",
	cleaned BOOLEAN NOT NULL DEFAULT 0 CHECK (cleaned IN (0, 1))
	visible BOOLEAN NOT NULL DEFAULT 0 CHECK (visible IN (0, 1))
);

CREATE TABLE wishlist_item_history {
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	wishlist_id INTEGER NOT NULL,
	price TEXT NOT NULL,
	seen_datetime TEXT NOT NULL,
	FOREIGN KEY (wishlist_id) REFERENCES wishlist (id)
}

CREATE TABLE wishlist_item_stats {
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	wishlist_id INTEGER NOT NULL,
	iteration_count INTEGER NOT NULL DEFAULT 0,
	price_history TEXT NOT NULL DEFAULT "",
	FOREIGN KEY (wishlist_id) references wishlist (id)
}