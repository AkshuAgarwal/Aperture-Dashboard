var hamburger = document.getElementById("nav-right");
var mainPage = document.getElementById("main");
var dropdown = document.getElementById("nav-dropdown");
var dropdownButton = document.getElementById("dropdown-button");

function hamburgerActivate() {
    hamburger.classList.toggle('hamburger-activated');
    mainPage.classList.toggle('hamburger-activated');
}

function dropdownActive() {
    dropdown.classList.toggle("dropdown-active");
}

document.addEventListener("click", function(event) {
    if (event.target != dropdownButton && event.target != dropdown) {
        dropdown.classList.remove("dropdown-active");
    }
}, false);