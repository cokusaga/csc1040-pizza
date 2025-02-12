// static/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    // Example of a simple effect when the page loads
    console.log("Welcome to Papa's Pizzeria!");
});

function toggleMenu() {
    var x = document.getElementById("navLinks");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}
