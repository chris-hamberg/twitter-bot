CREATE TABLE IF NOT EXISTS user (
    id        INTEGER PRIMARY KEY NOT NULL,
    name      VARCHAR(255),
    username  VARCHAR(255));

CREATE UNIQUE INDEX uidx ON user(id);
