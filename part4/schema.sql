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
    '$2b$12$w..guslDWHol6eh/jIr8f.5p.HCg9Ff/giaKAM2Sctu4tH2zXLOiS',
    TRUE
);

INSERT INTO users (
    id, email, first_name, last_name, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2',
    'user@hbnb.io',
    'user',
    'HBnB',
    '$2b$12$w..guslDWHol6eh/jIr8f.5p.HCg9Ff/giaKAM2Sctu4tH2zXLOiS',
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

-- Add two more users for sufficient reviewers
INSERT INTO users (id, email, first_name, last_name, password, is_admin) VALUES
('2a0b1e82-43e1-4b21-907f-1e55e1f77aa1', 'reviewer1@hbnb.io', 'Alice', 'Blue', '$2b$12$w..guslDWHol6eh/jIr8f.5p.HCg9Ff/giaKAM2Sctu4tH2zXLOiS', FALSE),
('5e77cc37-c9a2-49d7-bdab-667a3b30827e', 'reviewer2@hbnb.io', 'Eli', 'Green', '$2b$12$w..guslDWHol6eh/jIr8f.5p.HCg9Ff/giaKAM2Sctu4tH2zXLOiS', FALSE);

-- Insert 3 places (one for admin, one for user, one for reviewer1)
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('01e29960-c48b-4963-b2c8-9ad3aa35da63', 'Luxury Loft', 'Spacious loft in downtown', 150.00, 24.50, 46.70, '36c9050e-ddd3-4c3b-9731-9f487208bbc1'), -- admin owns
('d71240e9-0873-43e9-ac12-22117f7a974f', 'Cozy Studio', 'Perfect for solo travelers', 90.50, 24.60, 46.80, '36c9050e-ddd3-4c3b-9731-9f487208bbc2'), -- user owns
('de4bcc28-f90e-4c52-aca3-70c1ecc31a2f', 'Beach House', 'Amazing sea views', 250.00, 24.70, 46.90, '2a0b1e82-43e1-4b21-907f-1e55e1f77aa1'); -- reviewer1 owns

-- Add 4 reviews for each place (exclude the owner as reviewer)
