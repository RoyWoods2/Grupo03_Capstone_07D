window.onscroll = function() {
    var navbar = document.getElementById("cd-main-nav");
    var sticky = navbar.offsetTop;

    if (window.pageYOffset > sticky) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky");
    }
};

