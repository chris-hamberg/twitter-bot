CREATE TABLE temp (
    admin                               INTEGER NOT NULL,
    type_lambda_delta                   DATETIME DEFAULT CURRENT_TIMESTAMP,
    type_epsilon_subcycle_delta         DATETIME DEFAULT CURRENT_TIMESTAMP,
    follower_delta                      DATETIME DEFAULT CURRENT_TIMESTAMP,
    following_delta                     DATETIME DEFAULT CURRENT_TIMESTAMP,
    type_alpha_delta                    DATETIME DEFAULT CURRENT_TIMESTAMP,

    playlist_delta                      DATETIME DEFAULT CURRENT_TIMESTAMP,
    ystream_delta                       DATETIME DEFAULT CURRENT_TIMESTAMP,
    blog_delta                          DATETIME DEFAULT CURRENT_TIMESTAMP,

    destroyer_delta                     DATETIME DEFAULT CURRENT_TIMESTAMP,
    inactive_delta                      DATETIME DEFAULT CURRENT_TIMESTAMP,

    unfriend_delta                      DATETIME DEFAULT CURRENT_TIMESTAMP,
    friend_delta                        DATETIME DEFAULT CURRENT_TIMESTAMP,
    type_gamma_delta                    DATETIME DEFAULT CURRENT_TIMESTAMP,
    mention_delta                       DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_delta                         DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply_type1_delta                   DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply_type2_delta                   DATETIME DEFAULT CURRENT_TIMESTAMP,

    type_epsilon_supercycle_index       INTEGER DEFAULT 0,
    type_epsilon_subcycle_index         INTEGER DEFAULT 0,
    tweetAI_subcycle_index              INTEGER DEFAULT 0,
    unfriend_subcycle_index             INTEGER DEFAULT 0,
    friend_subcycle_index               INTEGER DEFAULT 0,
    playlist_subcycle_index             INTEGER DEFAULT 0,
    ystream_subcycle_index              INTEGER DEFAULT 0,

    tweetHardcoded_index                INTEGER DEFAULT 0,
    tweetMeme_index                     INTEGER DEFAULT 0,
    type_lambda_index                   INTEGER DEFAULT 0,
    playlist_index                      INTEGER DEFAULT 0,
    ystream_index                       INTEGER DEFAULT 0,
    blog_index                          INTEGER DEFAULT 0,
    type_alpha_index                    INTEGER DEFAULT 0,
    inactive_index                      INTEGER DEFAULT 0,
    destroyer_index                     INTEGER DEFAULT 0,
    tfilter_index                       INTEGER DEFAULT 0,

    tweetAI_injection_state             BOOLEAN DEFAULT FALSE,
    follower_pagination                 VARCHAR(255),
    following_pagination                VARCHAR(255),

    follower_count                      INTEGER DEFAULT 0,
    following_count                     INTEGER DEFAULT 0,
    unfriendQ_count                     INTEGER DEFAULT 0,
    unfriend_count                      INTEGER DEFAULT 0,
    friendQ_count                       INTEGER DEFAULT 0,
    friend_count                        INTEGER DEFAULT 0,

    type_alpha_count                    INTEGER DEFAULT 0,

    like_subcycle_count                 INTEGER DEFAULT 0,
    retweet_reply_count                 INTEGER DEFAULT 0,
    tweet_count                         INTEGER DEFAULT 0,
    reply_count                         INTEGER DEFAULT 0,
    like_count                          INTEGER DEFAULT 0,

    follower_complete                   BOOLEAN DEFAULT FALSE,
    following_complete                  BOOLEAN DEFAULT FALSE,

    like_probability                    REAL DEFAULT 0.0,
    reply_probability                   REAL DEFAULT 0.0,
    retweet_probability                 REAL DEFAULT 0.0,
    reply_probability_type2             REAL DEFAULT 0.0,

    tweetAI_prompt_index                INTEGER DEFAULT 0,

    FOREIGN KEY(admin) REFERENCES administrator(id),
    PRIMARY KEY(admin));
