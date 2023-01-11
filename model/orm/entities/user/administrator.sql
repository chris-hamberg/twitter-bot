CREATE TABLE IF NOT EXISTS administrator (
    id          INTEGER PRIMARY KEY NOT NULL,
    auth        BLOB,
    bearer      VARCHAR(255),
    youtube_api VARCHAR(255),
    FOREIGN KEY(id) REFERENCES user(id));
