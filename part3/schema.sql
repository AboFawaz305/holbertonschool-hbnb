CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    "password" VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(256),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    "text" TEXT,
    rating INT,
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (place_id) REFERENCES places (id)
);


CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,
    "name" VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    FOREIGN KEY (place_id) REFERENCES places (id),
    FOREIGN KEY (amenity_id) REFERENCES amenities (id)
);

INSERT INTO users (
    id, email, first_name, last_name, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2a$12$A3kuCT9lRXqbQdsF6xrH8uvJLa9gr1izMzZpxkwf7DgGkCzUtEMD6',
    TRUE
);

INSERT INTO amenities (
    id, name
) VALUES (
    'b9016afb-6548-4929-96dd-8a5857a57926',
    'WIFI'
),
(
    'c9d7dd1d-9c01-4ede-a08e-5ddf3cf3d830',
    'Swimming Pool'
),
(
    'f6033ad4-7dec-4b31-a6e3-fcb81c59062c',
    'Air Conditioning'
);
