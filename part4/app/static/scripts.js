/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
	const loginForm = document.getElementById('login-form');
	if (loginForm){
		loginForm.addEventListener('submit', (e) => {
			e.preventDefault();
			const loginData = new FormData(loginForm);
			body = {
				email:`${loginData.get('email')}`,
				password:`${loginData.get('password')}`
			};
			fetch('api/v1/auth/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(body),
			}).then((response) => {
				if (response.ok) {
					return response.json();
				}
				alert("Login Failed: " + response.statusText);
				throw new Error('Login Failed')
			}).then((credentials) => {
				document.cookie = `token=${credentials.access_token}; path=/`;
				location.href = '/';
			}).catch(()=>{});
		});
	}
  });
