document.addEventListener('DOMContentLoaded', function () {
    const loginSection = document.getElementById('login-section');
    const registerSection = document.getElementById('register-section');
    const welcomeSection = document.getElementById('welcome-section');
    const showLoginLink = document.getElementById('show-login');
    const showRegisterLink = document.getElementById('show-register');
    const logoutBtn = document.getElementById('logout-btn');
    const welcomeMessage = document.getElementById('welcome-message');

    // Mostrar la pantalla de inicio de sesión
    showLoginLink.addEventListener('click', function () {
        loginSection.classList.add('active');
        registerSection.classList.remove('active');
        welcomeSection.classList.remove('active');
    });

    // Mostrar la pantalla de registro
    showRegisterLink.addEventListener('click', function () {
        registerSection.classList.add('active');
        loginSection.classList.remove('active');
        welcomeSection.classList.remove('active');
    });

    // Manejar el cierre de sesión
    logoutBtn.addEventListener('click', function () {
        fetch('/logout', {
            method: 'POST',
            credentials: 'same-origin'  // Asegura que se envíen las cookies de sesión
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al cerrar sesión.');
            }
        })
        .then(data => {
            alert(data.message);  // Mostrar el mensaje de éxito
            // Volver a la sección de inicio de sesión
            welcomeSection.classList.remove('active');
            loginSection.classList.add('active');
        })
        .catch(error => console.error('Error:', error));
    });

    // Comprobar si el usuario está autenticado 
    fetch('/dashboard', {
        method: 'GET',
        credentials: 'same-origin'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('No autenticado');
        }
    })
    .then(data => {
        welcomeMessage.textContent = data.message;
        welcomeSection.classList.add('active');
        loginSection.classList.remove('active');
        registerSection.classList.remove('active');
    })
    .catch(error => {
        console.log(error.message);
    });
});
