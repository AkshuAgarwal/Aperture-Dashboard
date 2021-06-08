const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const navLink = document.querySelectorAll(".nav-link");
const mainPage = document.querySelector(".main-page");

const topScrollBtn = document.querySelector(".top-scroll-btn");

window.onscroll = function() {scrollFunction()};

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
    mainPage.classList.toggle("active");
}

navLink.forEach(n => n.addEventListener("click", closeMenu));

function closeMenu() {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    mainPage.classList.remove("active");
}

function scrollFunction() {
    if (document.body.scrollTop > 360 || document.documentElement.scrollTop > 360) {
        topScrollBtn.classList.add("btn-show");
    }
    else {
        topScrollBtn.classList.remove("btn-show");
    }
}

function topFunction() {
    document.body.scrollTo({
        top: 0,
        behavior: "smooth"
    })
    document.documentElement.scrollTo({
        top: 0,
        behavior: "smooth"
    })
}