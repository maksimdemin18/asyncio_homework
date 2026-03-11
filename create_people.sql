CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY,
    birth_year VARCHAR(32),
    eye_color VARCHAR(64),
    gender VARCHAR(32),
    hair_color VARCHAR(128),
    homeworld TEXT,
    mass VARCHAR(32),
    name VARCHAR(255) NOT NULL,
    skin_color VARCHAR(128)
);
