CREATE TABLE IF NOT EXISTS type_alpha (
    admin     INTEGER NOT NULL,
    id        INTEGER NOT NULL,
    resource    INTEGER,
    following BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(admin) REFERENCES administrator(id),
    FOREIGN KEY(id) REFERENCES user(id),
    FOREIGN KEY(admin, resource) REFERENCES resource(admin, id),
    PRIMARY KEY(admin, id));
