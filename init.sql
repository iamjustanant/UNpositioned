DROP TABLE IF EXISTS rel_un_topics;
DROP TABLE IF EXISTS rel_x_topics;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS un_docs;
DROP TABLE IF EXISTS x_docs;
DROP TABLE IF EXISTS rep_docs;

CREATE TABLE IF NOT EXISTS un_docs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sess INT,
    country VARCHAR(255),               -- The country the news is from
    year_created INT,                   -- The year the news was created
    text_content TEXT         -- The actual content of the news
);

CREATE TABLE IF NOT EXISTS x_docs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name TEXT,             -- The username of the tweet author
    location TEXT,
    followers FLOAT,
    verified BOOL,
    date_created DATE,                  -- The date the tweet was created
    text_content TEXT,          -- The actual content of the tweet
    hashtags TEXT              -- In the format "hashtag1, hashtag2, hashtag3"
);

CREATE TABLE IF NOT EXISTS rep_docs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    media_source VARCHAR(255),
    author TEXT,
    text_content TEXT,
    audience VARCHAR(255),
    audience_conf FLOAT,
    bias VARCHAR(255),
    bias_conf FLOAT,
    message VARCHAR(255),
    message_conf FLOAT,
    trusted_judgments INT
);