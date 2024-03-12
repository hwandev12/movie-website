window.addEventListener("scroll", function () {
  var navbar = document.querySelector(".home__navigation-wrapper");
  if (window.scrollY > 100) {
    navbar.classList.add("navbar-scrolled");
  } else {
    navbar.classList.remove("navbar-scrolled");
  }
});

var descriptionElement = document.querySelector(".last_p");
console.log(descriptionElement);
var description = descriptionElement.innerHTML;
var truncatedDescription = truncate(description, 14);
descriptionElement.innerHTML = truncatedDescription;

function truncate(text, limit) {
  var words = text.split(" ");
  console.log(words);
  if (words.length > limit) {
    return words.slice(0, limit).join(" ") + "...";
  } else {
    return text;
  }
}
