let lastScrollTop = 0;
const navbar = document.getElementById('navbar');
const navbarToggle = document.getElementById('navbar-toggle');
const navbarMenu = document.getElementById('navbar-menu');

navbarToggle.addEventListener('click', () => {
    navbarMenu.classList.toggle('active');
});

window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        // Scrolling down
        navbar.classList.add('hidden');
    } else {
        // Scrolling up
        navbar.classList.remove('hidden');
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
});

// script.js

document.getElementById('op').addEventListener('click', function() {
    window.location.href = 'templates/signup.html'; 
});

document.getElementById('open').addEventListener('click', function() {
    window.location.href = 'cat.html'; 
});

document.getElementById('ope').addEventListener('click', function() {
    window.location.href = 'templates/login.html'; 
});

document.getElementById('vie').addEventListener('click', function() {
    window.location.href = 'cat.html'; 
});

document.getElementById('com').addEventListener('click', function() {
    window.location.href = 'templates/ethical_threads.html'; 
});

document.getElementById('sus').addEventListener('click', function() {
    window.location.href = 'sus.html'; 
});





