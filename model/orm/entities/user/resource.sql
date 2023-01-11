CREATE TABLE IF NOT EXISTS resource (
    admin      INTEGER NOT NULL,
    id         INTEGER NOT NULL,
    complete   BOOLEAN DEFAULT FALSE,
    pagination VARCHAR(255),
    FOREIGN KEY(admin) REFERENCES administrator(id),
    FOREIGN KEY(id) REFERENCES user(id),
    PRIMARY KEY(admin, id));
