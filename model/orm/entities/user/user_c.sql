CREATE TABLE IF NOT EXISTS user_c (
    admin INTEGER NOT NULL,
    cat   VARCHAR(15) NOT NULL,
    id    INTEGER NOT NULL,
    FOREIGN KEY(id) REFERENCES user(id),
    FOREIGN KEY(admin) REFERENCES administrator(id),
    PRIMARY KEY(admin, cat, id));
