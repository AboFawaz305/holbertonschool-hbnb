# User
## Tested
- user creation with empty fields
- user creation with invalid email
- get all users with a single saved user
- get all users without any stored user
- update a user
- get a user by id
## Issues encountered
- [x] user creation accepted empty first\_name and last\_name
- [x] wrong output when accessing get all users with an empty user repo
- [ ] got an error when trying to update a user
- [ ] get user by id dont work
# Amenity
- get all amenities
- create amenity
- get amenity by id
- update amenity
- get all amenities with 2 stored amenities
## Issues encountered
- wrong output when get all and empty amenity repo
# Place
## Tested
- get all places
- create a place with a non-existing owner id
- create a place with an existing owner id
- get a place by an invalid id
- update a place
## Issues encountered
- [ ] got a wrong output when tried to get a non existing place
# Review
## Tested
- get all reviews with empty review repo
- create a review with invalid user id
- create a review with invalid place id
- create a valid review
- get reviews with place id for a place without reviews
## Issues encountered
- [ ] internal server error when creating a valid review
