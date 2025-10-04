# HBNB - RESTful API Project (Part 2)

## Overview

This project is part of the Holberton School curriculum, focusing on building a RESTful API for an Airbnb clone. The application manages resources such as users, amenities, places, and reviews. Each resource supports CRUD operations and is designed to handle edge cases and error responses.

## Folder Structure

Here is an overview of the folder structure inside the `part2/hbnb` directory:

```
hbnb
├── app
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models
│   │   ├── amenity.py
│   │   ├── BaseModels.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence
│   │   └── repository.py
│   └── services
│       └── facade.py
├── config.py
├── README.md
├── requirements.txt
├── run.py
└── test
    ├── test_amenity_facade.py
    ├── test_aminity_endpoints.py
    ├── test_places_endpoints.py
    ├── test_Places_facade.py
    ├── test_user_endpoint.py
    └── test_user.py
```

### Description of Key Folders and Files

- **app/**  
  The main application package containing all backend logic.

  - **api/**  
    Contains API route definitions.
    - **v1/**  
      Version 1 of the API with separate modules for amenities, places, reviews, and users. Each file defines endpoints and handlers for its resource.

  - **models/**  
    Defines the data models for each resource (Amenity, Place, Review, User) and a base model for shared logic.

  - **persistence/**  
    Manages data persistence and repository logic, abstracting storage operations.

  - **services/**  
    Contains service layer logic, such as the `facade.py`, which coordinates operations between models and persistence.

- **config.py**  
  Configuration file for environment variables or app settings.

- **requirements.txt**  
  Lists required Python packages for the project.

- **run.py**  
  Script to start the application/server.

- **test/**  
  Contains automated test scripts for various API endpoints and service layers, ensuring that the application behaves as expected.

- **README.md**  
  Documentation and instructions for the project.



This structure separates concerns between API endpoints, models, persistence, and services, making the project easier to maintain and extend.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AboFawaz305/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part2/hbnb
   ```
2. **Install dependencies:**
   - Ensure you have Python 3.x installed.
   - Install required packages using pip (if a requirements file is present):
     ```bash
     pip install -r requirements.txt
     ```

## Running the Application

To start the API server, run:
```bash
python3 main.py
```
Replace `main.py` with the actual entry point if different.

## Usage

The API exposes endpoints for:
- **User:** Create, read, update, and list users.
- **Amenity:** Manage amenities.
- **Place:** Manage places (with owner relationships).
- **Review:** Manage reviews for places.

Refer to the source code for details on each endpoint.

## Testing Process

The following tests have been performed:

### User
- Creation with empty fields
- Creation with invalid email
- Getting all users with/without stored users
- Updating a user
- Retrieving user by ID

#### Issues Encountered
- [x] Accepted empty first_name and last_name during creation
- [x] Wrong output for getting all users when repo is empty
- [ ] Error when updating a user
- [ ] Getting user by ID does not work

### Amenity
- Get all amenities
- Create amenity
- Get amenity by ID
- Update amenity
- Get all amenities with two stored amenities

#### Issues Encountered
- [x] Wrong output when getting all amenities and repo is empty

### Place
- Get all places
- Create with non-existing/existing owner ID
- Get place by invalid ID
- Update place

#### Issues Encountered
- [ ] Wrong output when trying to get a non-existing place

### Review
- Get all reviews with empty repo
- Create review with invalid user/place ID
- Create valid review
- Get reviews for place without reviews

#### Issues Encountered
- [ ] Internal server error when creating a valid review

## Contributing

Contributions are welcome! Please open issues for bugs or feature requests.

## License

See the LICENSE file for details.
