CREATE TABLE IF NOT EXISTS blog (
    admin           INTEGER NOT NULL,
    feed_title      VARCHAR(255),
    feed_url        VARCHAR(255),
    article_url     VARCHAR(255),
    article_title   VARCHAR(255),
    article_author  VARCHAR(255),
    article_summary VARCHAR(255),
    posted          BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (admin, article_url),
    FOREIGN KEY (admin) REFERENCES administrator (id));
