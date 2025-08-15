Sequence Diagrams

This section describes the sequence of interactions between the different layers of the HBnB application for four core API calls: User Registration, Place Creation, Review Submission, and Fetching a List of Places.

These diagrams illustrate how the Presentation Layer (UI/API), Business Logic Layer (service managers), and Persistence Layer (data access components) communicate to fulfill each request, using the App Facade as the entry point for the presentation layer.

User Registration

When a user signs up for a new account, the UI calls the AppFacade.userRegistration() method.
The facade validates the request by invoking the Logic Layer to perform verification and business rules checks.
If the user does not already exist, the logic layer requests the Persistence Layer to create a new user.
The persistence layer stores the new record and returns success to the logic layer, which then returns the newly created user information to the UI via the facade.
If the user already exists, the logic layer returns an appropriate error message through the facade.

Place Creation

When a user creates a new place listing, the UI calls the AppFacade.placeCreation() method.
The facade delegates to the Logic Layer to validate the listing and enforce creation rules.
If validation passes, the logic layer requests the Persistence Layer to store the new place data.
Upon success, the persistence layer returns the newly created place details to the logic layer, which sends the result back to the UI through the facade.

Review Submission

When a user submits a review for a place, the UI calls the AppFacade.createReview() method.
The Logic Layer validates the review content, ensures the user and place exist, and then calls the Persistence Layer to store the review.
If successful, the persistence layer returns the new review details to the logic layer, which relays them to the UI via the facade.

Fetching a List of Places

When a user searches for places based on specific criteria, the UI calls the AppFacade.showPlaces() method.
The Logic Layer processes the criteria and requests the Persistence Layer to retrieve matching place records.
The persistence layer returns the relevant place data to the logic layer, which sends it back to the UI through the facade for display.

Purpose of the Sequence Diagrams

These sequence diagrams ensure that:

Layer separation is respected — each layer only communicates through its designated interface.

The App Facade pattern is consistently applied, serving as the single entry point from the presentation layer to the business logic layer.

Data flow is clearly visualized — including validations, persistence operations, and returned results.

By maintaining this interaction structure, HBnB achieves a clean separation of concerns, making the system easier to maintain, extend, and test.
