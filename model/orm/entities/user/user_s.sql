CREATE TABLE IF NOT EXISTS user_s (
    admin            INTEGER NOT NULL,
    id               INTEGER NOT NULL,
    unfollowed_count INTEGER DEFAULT 0,
    priority         INTEGER DEFAULT 0,
    delta            DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(admin) REFERENCES administrator(id),
    FOREIGN KEY(id) REFERENCES user(id),
    PRIMARY KEY(admin, id));
