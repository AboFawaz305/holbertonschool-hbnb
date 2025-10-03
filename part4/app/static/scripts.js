/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

const token_cookie = document.cookie
  .split('; ')
  .find((cookie) => cookie.startsWith('token='));
const access_token = token_cookie && token_cookie.split('=').length > 1 ? token_cookie.split('=')[1] : undefined;
const is_loggedin = Boolean(access_token);
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const loginData = new FormData(loginForm);
      body = {
        email: `${loginData.get('email')}`,
        password: `${loginData.get('password')}`
      };
      fetch('api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      }).then((response) => {
        if (response.ok) {
          return response.json();
        }
        alert('Login Failed: ' + response.statusText);
        throw new Error('Login Failed');
      }).then((credentials) => {
        document.cookie = `token=${credentials.access_token}; path=/`;
        location.href = '/';
      }).catch(() => {});
    });
  }
  const login_link = document.getElementById('login-link');
  if (!is_loggedin && login_link) {
    login_link.style.display = 'block';
  } else if(is_loggedin && login_link) {
	  login_link.style.display = 'none';
  }
  const price_filter = document.getElementById('price-filter');
  const places_list = document.getElementById('places-list');
  const render_places = (places) => {
    places_template = places.map((place) => {
		const place_title = document.createElement('h2');
		place_title.innerText = place.title;
		const place_price = document.createElement('p')
		place_price.innerText = `Price Per Night ${place.price}`;
		const place_details_link = document.createElement('a')
		place_details_link.innerText = 'View Details'
		place_details_link.setAttribute('href', `/place/${place.id}`)
		const place_card = document.createElement('div');
		place_card.appendChild(place_title);
		place_card.appendChild(place_price);
		place_card.appendChild(place_details_link);
		return place_card;
	});
    places_list.replaceChildren(...places_template)
  };
  if (is_loggedin && price_filter && places_list) {
    fetch('api/v1/places', {
      headers: {
        Authentication: `Bearer ${access_token}`
      }
    }).then((response) => {
      if (response.ok) {
        return response.json();
      }
      alert('Failed to fetch places');
      throw new Error('Failed to fetch places');
    }).then((places) => {
      const prices = places.map((place) => place.price);
      const prices_options = prices.map((price) => {
		  const option = document.createElement('option');
		  option.setAttribute('value', price);
		  option.innerText = price;
		  return option;
	  });
      price_filter.replaceChildren(...prices_options);
      price_filter.addEventListener('change', (e) => {
        render_places(places.filter(
			(place) => place.price <= price_filter.value
        ));
      });
        render_places(places.filter(
			(place) => place.price <= price_filter.value
        ));
    }).catch((e) => {
      console.log(e);
    });
  }
});
