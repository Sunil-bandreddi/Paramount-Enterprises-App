function openGallery(type){


    document
    .getElementById("galleryContent")
    .style.display="grid";


}





function showLightbox(card){


    let img =
    card.querySelector("img").src;


    document
    .getElementById("lightboxImg")
    .src=img;



    document
    .getElementById("lightbox")
    .style.display="flex";


}




function closeLightbox(){


    document
    .getElementById("lightbox")
    .style.display="none";


}