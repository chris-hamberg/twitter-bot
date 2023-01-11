CREATE TABLE IF NOT EXISTS message (
    rowid       INTEGER PRIMARY KEY AUTOINCREMENT,
    admin       INTEGER NOT NULL,
    admin_name  VARCHAR(255),
    data        VARCHAR(255),
    process     VARCHAR(255),
    delta       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin) REFERENCES administrator(id),
    FOREIGN KEY (admin_name) REFERENCES administrator(name));
