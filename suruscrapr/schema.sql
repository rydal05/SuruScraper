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
	id TEXT PRIMARY KEY, -- usa and jp sites can have items with same ID but the information can be different depending on the site
	url TEXT UNIQUE NOT NULL, --the URL is the true unique identifier
	name TEXT NOT NULL,
	price INTEGER NOT NULL DEFAULT 0,
	dateLastSeen TEXT NOT NULL DEFAULT "N/A",
	timeLastSeen TEXT NOT NULL DEFAULT "N/A",
	cleaned BOOLEAN NOT NULL DEFAULT 0 CHECK (cleaned IN (0, 1))
	visible BOOLEAN NOT NULL DEFAULT 0 CHECK (visible IN (0, 1))
);

CREATE TABLE history_wishlist {
	id TEXT PRIMARY KEY,
	wishlist_id INTEGER NOT NULL,
	price TEXT NOT NULL,
	seen_datetime TEXT NOT NULL,
	FOREIGN KEY (wishlist_id) REFERENCES wishlist (id)
}

CREATE TABLE stats_wishlist {
	id TEXT PRIMARY KEY,
	wishlist_id INTEGER NOT NULL,
	iteration_count INTEGER NOT NULL DEFAULT 0,
	price_history TEXT NOT NULL DEFAULT "",
	FOREIGN KEY (wishlist_id) references wishlist (id)
}