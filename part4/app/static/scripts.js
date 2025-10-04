// --- Utility: Get Place ID from Add Review URL ---
function getPlaceIdFromAddReviewURL() {
    // For URL like /place/123/add-review, get the place ID (second-to-last part)
    const parts = window.location.pathname.split('/');
    return parts[parts.length - 2]; // Gets '123' from ['', 'place', '123', 'add-review']
}


// --- Utility: Token, Authentication ---
function getAccessToken() {
    const token_cookie = document.cookie
        .split('; ')
        .find(cookie => cookie.startsWith('token='));
    return token_cookie && token_cookie.split('=').length > 1 ? token_cookie.split('=')[1] : undefined;
}

// --- Utility: Get Place ID ---
function getPlaceIdFromURL() {
    const parts = window.location.pathname.split('/');
    return parts[parts.length - 1];
}

// --- Utility: Display error/messages ---
function displayMessage(sectionId, message) {
    const section = document.getElementById(sectionId);
    if (section) section.innerHTML = `<p>${message}</p>`;
}

// --- Reviews Renderer ---
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviews || !reviews.length) {
        reviewsSection.innerHTML = "<p>No reviews yet.</p>";
        return;
    }
    reviewsSection.innerHTML = reviews.map(review => `
        <div class="review-card">
            <h3>${review.reviewer ?? "Anonymous"}</h3>
            <p>${review.text}</p>
            <p>
                Rating: ${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}
            </p>
        </div>
    `).join('');
}

// --- Review Form Renderer & Handler ---
function displayReviewForm(placeId) {
    const access_token = getAccessToken(); // Re-get token
    const is_loggedin = Boolean(access_token);
    
    const formSection = document.getElementById('add-review');
    if (!formSection) return;
    
    if (!is_loggedin) {
        formSection.innerHTML = "";
        return;
    }
    
    formSection.innerHTML = `
        <h2>Add a Review</h2>
        <form id="review-form">
            <label for="review-text">Review:</label>
            <textarea id="review-text" required></textarea>
            <label for="rating">Rating:
                <input type="number" id="rating" min="1" max="5" required>
            </label>
            <button type="submit">Submit</button>
        </form>
        <div id="review-message"></div>
    `;
    
    document.getElementById('review-form').onsubmit = async function(event) {
        event.preventDefault();
        const text = document.getElementById('review-text').value;
        const rating = parseInt(document.getElementById('rating').value, 10);
        try {
            const response = await fetch('/api/v1/reviews', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${access_token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ place_id: placeId, text, rating })
            });
            if (response.ok) {
                document.getElementById('review-message').textContent = "Review submitted!";
                fetchPlaceDetails(); // Reload everything after review
            } else {
                const err = await response.json();
                document.getElementById('review-message').textContent = "Error: " + (err.error || "Failed");
            }
        } catch (e) {
            document.getElementById('review-message').textContent = "Error submitting review.";
        }
    };
}

// --- Place Details Renderer ---
function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    detailsSection.innerHTML = `
        <div class="place-info">
            <h2>${place.title}</h2>
            <dl>
                <dt>Host</dt>
                <dd>${place.owner?.first_name ?? ""} ${place.owner?.last_name ?? ""}</dd>
                <dt>Price Per Night</dt>
                <dd>$${place.price}</dd>
                <dt>Description</dt>
                <dd>${place.description}</dd>
                <dt>Amenities</dt>
                <dd>
                    <ul class="amenities-lists">
                        ${(place.amenities ?? []).map(amenity => `<li>${amenity.name}</li>`).join('')}
                    </ul>
                </dd>
            </dl>
        </div>
    `;
    displayReviews(place.reviews);
    displayReviewForm(place.id);
}

// --- Place Details Loader ---
async function fetchPlaceDetails() {
    const access_token = getAccessToken(); // Re-get token
    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        displayMessage('place-details', 'No Place ID provided!');
        return;
    }
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            headers: access_token ? { 'Authorization': `Bearer ${access_token}` } : {}
        });
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            displayMessage('place-details', 'Failed to fetch details');
        }
    } catch (e) {
        displayMessage('place-details', 'Error loading place details.');
    }
}

// --- Places List Renderer ---
function renderPlaces(places) {
    const places_list = document.getElementById('places-list');
    if (!places || !places.length) {
        places_list.innerHTML = "<p>No places found.</p>";
        return;
    }
    places_list.innerHTML = places.map(place => `
        <div class="place-card">
            <h2>${place.title}</h2>
            <p>Price Per Night: $${place.price}</p>
            <a href="/place/${place.id}" class="details-button">View Details</a>
        </div>
    `).join('');
}

// --- Load and Render Places ---
async function loadPlaces() {
    const access_token = getAccessToken(); // Re-get token
    const is_loggedin = Boolean(access_token);
    const places_list = document.getElementById('places-list');
    const price_filter = document.getElementById('price-filter');
    
    if (!is_loggedin) {
        places_list.innerHTML = `<p>Please log in to view places.</p>`;
        return;
    }
    try {
        const response = await fetch('/api/v1/places', {
            headers: { 'Authorization': `Bearer ${access_token}` }
        });
        if (response.ok) {
            const places = await response.json();
            renderPlaces(places);

            // Build price filter dropdown
            const priceOptions = [10, 50, 100, 250, 500];
            price_filter.innerHTML = `<option value="all">All</option>` +
                priceOptions.map(p => `<option value="${p}">Up to $${p}</option>`).join('');
            price_filter.addEventListener('change', () => {
                const val = price_filter.value;
                let filtered = places;
                if (val !== 'all') {
                    filtered = places.filter(place => place.price <= parseFloat(val));
                }
                renderPlaces(filtered);
            });
        } else {
            places_list.innerHTML = `<p>Error loading places.</p>`;
        }
    } catch (e) {
        places_list.innerHTML = `<p>Error loading places.</p>`;
    }
}

// --- DOM Ready Handler ---
document.addEventListener('DOMContentLoaded', () => {
    const access_token = getAccessToken();
    const is_loggedin = Boolean(access_token);
    
    // --- Login Button Control everywhere
    const login_link = document.getElementById('login-link');
    if (login_link) {
        if (!is_loggedin) login_link.style.display = 'block';
        else login_link.style.display = 'none';
    }

    // --- Login Form Logic
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = new FormData(loginForm);
            const body = {
                email: data.get('email'),
                password: data.get('password')
            };
            try {
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body)
                });
                if (response.ok) {
                    const result = await response.json();
                    document.cookie = `token=${result.access_token}; path=/`;
                    window.location.href = '/';
                } else {
                    const err = await response.json();
                    alert('Login Failed: ' + (err.error || response.statusText));
                }
            } catch (error) {
                alert('Login Failed - Network error');
            }
        });
        return;
    }

    // --- Index Page: List of Places
    if (document.getElementById('places-list')) {
        loadPlaces();
        return;
    }

    // --- Place Details Page
    if (window.location.pathname.startsWith('/place/')) {
        fetchPlaceDetails();
        return;
    
    }
    if (window.location.pathname.includes('/add-review')) {
        const placeId = getPlaceIdFromAddReviewURL();
        displayReviewForm(placeId);
        return;
    }
  }
);
