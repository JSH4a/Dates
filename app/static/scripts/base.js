// base.js

window.addEventListener('load', function () {
    document.querySelector('.title').classList.add('fade-in');
});

// JavaScript code for handling "Continue" button click event
document.getElementById("continue-btn").addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("login-container").classList.remove('hidden');
    document.getElementById("cta-container").classList.add('hidden');
});

document.getElementById("begin-btn").addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("sign-up-container").classList.remove('hidden');
    document.getElementById("cta-container").classList.add('hidden');
});

document.getElementById("go-back-login").addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("login-container").classList.add('hidden');
    document.getElementById("cta-container").classList.remove('hidden');
});

document.getElementById("go-back-sign-up").addEventListener("click", function (event) {
    event.preventDefault();
    document.getElementById("sign-up-container").classList.add('hidden');
    document.getElementById("cta-container").classList.remove('hidden');
});