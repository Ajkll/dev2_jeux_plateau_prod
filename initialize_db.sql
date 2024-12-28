CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    pseudo VARCHAR(255) NOT NULL,
    score_total INTEGER NOT NULL,
    date_partie TIMESTAMP NOT NULL
);
