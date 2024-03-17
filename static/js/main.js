let html = document.querySelector("html");
var navbar = document.querySelector(".home__navigation-wrapper");
let episodeSwitcher = document.querySelectorAll(".serie__episodes-top a")

window.addEventListener('load', function () {
  // Hide the loader
  document.querySelector('.loader_wrapper').style.display = 'none';
  // Show the website content
  document.getElementById('main__website').style.display = 'block';
});


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
let spanLatestMovies = document.querySelector(".text_title span")

function switchToLightMode() {
  html.classList.remove("dark");
  if(spanLatestMovies) {
    spanLatestMovies.style.color = "#222"
  }
  navbar.classList.add("navbar-scrolled-light");
  // Store the user's preference for light mode in localStorage
  localStorage.setItem("theme", "light");
}

// Function to handle switching to dark mode
function switchToDarkMode() {
  html.classList.add("dark");
  if(spanLatestMovies) {
    spanLatestMovies.style.color = "inherit"
  }
  navbar.classList.remove("navbar-scrolled-light");
  // Store the user's preference for dark mode in localStorage
  localStorage.setItem("theme", "dark");
}

lightButton.addEventListener("click", switchToLightMode);
nightButton.addEventListener("click", switchToDarkMode);

const storedTheme = localStorage.getItem("theme");

// Apply the stored theme preference when the page loads
if (storedTheme === 'light') {
  switchToLightMode();
} else {
  switchToDarkMode(); // Default to dark mode if no preference is stored
}

const handleClick = (event) => {
  episodeSwitcher.forEach(item => {
    item.classList.remove("bg-primary")
  })
  event.target.classList.add("bg-primary")
}

// to add class to buttons
episodeSwitcher.forEach((item, index) => {
  item.addEventListener("click", handleClick)
})