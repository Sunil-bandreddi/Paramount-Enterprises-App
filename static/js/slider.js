let slides =
document.querySelectorAll(".hero-slider img");


let current = 0;



function changeSlide(){


    slides[current].classList.remove("active");


    current =
    (current + 1) % slides.length;


    slides[current].classList.add("active");


}



setInterval(changeSlide,6000);