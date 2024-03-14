let html = document.querySelector("html");
var navbar = document.querySelector(".home__navigation-wrapper");

window.addEventListener("scroll", function () {
  if (window.scrollY > 100) {
    navbar.classList.add("navbar-scrolled");
  } else {
    navbar.classList.remove("navbar-scrolled");
  }
});

var descriptionElement = document.querySelector(".last_p");
if (descriptionElement) {
  var description = descriptionElement.innerHTML;
  var truncatedDescription = truncate(description, 14);
  descriptionElement.innerHTML = truncatedDescription;
}

function truncate(text, limit) {
  var words = text.split(" ");
  if (words.length > limit) {
    return words.slice(0, limit).join(" ") + "...";
  } else {
    return text;
  }
}

let lightButton = document.querySelector(".home__navigation .fa-sun");
let nightButton = document.querySelector(".home__navigation .fa-moon");

lightButton.addEventListener("click", () => {
  html.classList.remove("dark");
  navbar.classList.add("navbar-scrolled-light");
});
nightButton.addEventListener("click", () => {
  html.classList.add("dark");
  navbar.classList.remove("navbar-scrolled-light");
});
