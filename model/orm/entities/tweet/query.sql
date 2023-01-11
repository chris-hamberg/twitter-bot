CREATE TABLE IF NOT EXISTS query (
    rowid       INTEGER PRIMARY KEY AUTOINCREMENT,
    admin       INTEGER NOT NULL,
    query       VARCHAR(255) UNIQUE,
    type        VARCHAR(15) NOT NULL,
    pagination  VARCHAR(255) DEFAULT NULL,
    polling     VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY(admin) REFERENCES administrator(id));
