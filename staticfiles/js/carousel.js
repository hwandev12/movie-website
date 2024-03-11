let carouselContainer = document.querySelector(".home__carousel");
let carouselItem = document.querySelectorAll(".carousel__item");
let leftSliderButton = document.querySelector(
  ".home__carousel .fa-chevron-left"
);
let rightSliderButton = document.querySelector(
  ".home__carousel .fa-chevron-right"
);

let counterCarousel = 0;

var circleContainer = document.querySelectorAll(".circle");
var circleContainerWrapper = document.querySelector(".circle_container");
// Create circle elements dynamically
function createCircles() {
  circleContainerWrapper.innerHTML = ""; // Clear existing circles
  for (var i = 0; i < carouselItem.length; i++) {
    var circle = document.createElement("span");
    circle.classList.add("circle");
    circle.dataset.index = i;
    circleContainerWrapper.appendChild(circle);
  }
}

// Initial creation of circles
createCircles();

function updateCircles() {
  var circleContainer = document.querySelectorAll(".circle");
  circleContainer.forEach((circle, index) => {
    if (index == counterCarousel) {
      circle.classList.add("circle_full");
    } else {
      circle.classList.remove("circle_full");
    }
  });
}

// Initial update of circles
updateCircles();

circleContainerWrapper.addEventListener("click", (event) => {
  if (event.target.classList.contains("circle")) {
    counterCarousel = parseInt(event.target.dataset.index);
    changeImage();
  }
});

leftSliderButton.addEventListener("click", () => {
  counterCarousel -= 1;
  clearInterval(animationCarousel)
  animationCarousel = setInterval(nextImage, 5000)
  changeImage();
});

rightSliderButton.addEventListener("click", () => {
  counterCarousel += 1;
  clearInterval(animationCarousel)
  animationCarousel = setInterval(nextImage, 5000)
  changeImage();
});

function nextImage() {
  counterCarousel += 1
  changeImage()
}

const changeImage = () => {
  if (counterCarousel > carouselItem.length - 1) {
    counterCarousel = 0;
  } else if (counterCarousel < 0) {
    counterCarousel = carouselItem.length - 1;
  }
  carouselItem.forEach((a, b) => {
    a.style.transform = `translateX(-${counterCarousel * 100}%)`;
    let p = a.querySelectorAll("p");
    let h1 = a.querySelector("h1");
    let dv = a.querySelector(".a_wrapper");
    let dvr = a.querySelector(".carousel__item-right");
    let elements = [h1, dv, dvr];
    if (b == counterCarousel) {
      h1.classList.add("active");
      dv.classList.add("active");
      dvr.classList.add("activeC");
      p.forEach((l) => {
        l.classList.add("active");
      });
    } else {
      h1.classList.remove("active");
      dv.classList.remove("active");
      dvr.classList.remove("activeC");
      p.forEach((l) => {
        l.classList.remove("active");
      });
    }
  });
  updateCircles();
};

let animationCarousel = setInterval(() => {
  counterCarousel += 1
  changeImage();
}, 5000);
