CREATE TABLE IF NOT EXISTS youtube (
    type            VARCHAR(10),
    admin           INTEGER NOT NULL,
    channel_id      VARCHAR(255),
    playlist_id     VARCHAR(255),
    video_id        VARCHAR(255),
    title           VARCHAR(255),
    url             VARCHAR(255),
    emojis          VARCHAR(255),
    flags           VARCHAR(255),
    posted          BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (admin, video_id),
    FOREIGN KEY (admin) REFERENCES administrator (id));
