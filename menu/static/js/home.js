function mostrarLoginForm() {
    var blurBackground = document.getElementById("blur-background");
    var loginForm = document.getElementById("login-form");
    var closeButton = document.getElementById("close-button");
    blurBackground.style.display = "block";
    loginForm.style.display = "block";
    closeButton.style.display = "block";
}

function cerrarLoginForm() {
    var blurBackground = document.getElementById("blur-background");
    var loginForm = document.getElementById("login-form");
    var closeButton = document.getElementById("close-button");
    blurBackground.style.display = "none";
    loginForm.style.display = "none";
    closeButton.style.display = "none";
}


document.addEventListener('DOMContentLoaded', function() {
    var successMessage = document.getElementById('login-success-message');
    if (successMessage) {
        setTimeout(function() {
            successMessage.style.display = 'none';
        }, 3000); // 3000 ms = 3 segundos
    }
});