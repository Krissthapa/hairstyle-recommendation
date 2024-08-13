document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&email=${encodeURIComponent(email)}`
    })
    .then(response => {
        if (response.ok) {
            alert('Registration successful! Redirecting to main page.');
            window.location.href = '/main';  // Redirect to the main page
        } else {
            return response.json().then(data => {
                alert('Error: ' + data.error);
            });
        }
    })
    .catch(error => console.error('Error:', error));
});
