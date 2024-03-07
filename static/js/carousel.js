let carouselContainer = document.querySelector(".home__carousel")
let carouselItem = document.querySelectorAll(".carousel__item")
let leftSliderButton = document.querySelector(".home__carousel .fa-chevron-left")
let rightSliderButton = document.querySelector(".home__carousel .fa-chevron-right")

let counterCarousel = 0

leftSliderButton.addEventListener("click", () => {
    counterCarousel -= 1
    changeImage()
})

rightSliderButton.addEventListener("click", () => {
    counterCarousel += 1
    changeImage()
})

const changeImage = () => {
    if(counterCarousel > carouselItem.length-1) {
        counterCarousel = 0
    }else if(counterCarousel < 0) {
        counterCarousel = carouselItem.length-1
    }
    carouselItem.forEach((a,b) => {
        a.style.transform = `translateX(-${counterCarousel * 100}%)`
        let p = a.querySelectorAll("p")
        let h1 = a.querySelector("h1")
        let dv = a.querySelector(".a_wrapper")
        let elements = [h1, dv]
        if(b == counterCarousel) {
            h1.classList.add("active") 
            dv.classList.add("active")
            p.forEach((l) => {
                l.classList.add("active")
            })
        }else {
            h1.classList.remove("active")
            dv.classList.remove("active")
            p.forEach((l) => {
                l.classList.remove("active")
            })
        }
    })
}