document.addEventListener("DOMContentLoaded",()=>{


const videos = document.querySelectorAll(".short-video");


const observer = new IntersectionObserver((entries)=>{


entries.forEach(entry=>{


const video = entry.target;


if(entry.isIntersecting){

    video.play()
    .catch(()=>{});


}else{

    video.pause();
    video.currentTime = 0;

}


});


},{

threshold:0.75

});



videos.forEach(video=>{

observer.observe(video);


});



});