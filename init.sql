-- Reset the database
DROP TABLE IF EXISTS x_docs;
DROP TABLE IF EXISTS un_docs;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS rel_x_topics;
DROP TABLE IF EXISTS rel_un_topics;

-- Store tweets
CREATE TABLE x_docs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255),             -- The username of the tweet author
    date_created DATE,                  -- The date the tweet was created
    text_content VARCHAR(255),          -- The actual content of the tweet
    hashtags VARCHAR(255)              -- In the format "hashtag1, hashtag2, hashtag3"
);

-- Store UN position papers
CREATE TABLE un_docs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255),               -- The country the news is from
    year_created INT,                   -- The year the news was created
    text_content VARCHAR(255)          -- The actual content of the news
);

-- Model topics for indexing and searching
CREATE TABLE topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_name VARCHAR(255)            -- The name of the topic
);

-- Model many-to-many relationships between tweets and topics
CREATE TABLE rel_x_topics (
    x_id INT,                           -- The id of the tweet
    topic_id INT,                       -- The id of the topic
    relevancy FLOAT,                    -- The relevancy score between the tweet and the topic, between 0 and 1 (1 indicating high relevancy, 0 indicating low relevancy)
    PRIMARY KEY (x_id, topic_id)
);

-- Model many-to-many relationships between UN position papers and topics
CREATE TABLE rel_un_topics (
    un_id INT,                          -- The id of the news
    topic_id INT,                       -- The id of the topic
    relevancy FLOAT,                    -- The relevancy score between the news and the topic, between 0 and 1 (1 indicating high relevancy, 0 indicating low relevancy)
    PRIMARY KEY (un_id, topic_id)
);

-- Setup foreign keys
ALTER TABLE rel_x_topics ADD FOREIGN KEY (x_id) REFERENCES x_docs(id);
ALTER TABLE rel_x_topics ADD FOREIGN KEY (topic_id) REFERENCES topics(id);
ALTER TABLE rel_un_topics ADD FOREIGN KEY (un_id) REFERENCES un_docs(id);
ALTER TABLE rel_un_topics ADD FOREIGN KEY (topic_id) REFERENCES topics(id);

-- TODO: Insert all necessary INSERT statements below to populate the `x_docs` and `un_docs` tables with initial data from all our datasets

INSERT INTO x_docs (user_name, date_created, text_content, hashtags) VALUES ('@exampleuser', '2020-01-01', 'This is a tweet about the UN', 'UN');
INSERT INTO un_docs (country, year_created, text_content) VALUES ('USA', 2020, 'This is an example UN position paper from the USA');
