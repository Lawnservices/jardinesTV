document.addEventListener("DOMContentLoaded",()=>{


const videos=document.querySelectorAll(".short-video");



const observer=new IntersectionObserver((entries)=>{


entries.forEach(entry=>{


const video=entry.target;



if(entry.isIntersecting){


videos.forEach(v=>{


if(v !== video){

v.pause();

}


});



video.play();



}else{


video.pause();


}


});


},{

threshold:0.80

});



videos.forEach(video=>{


observer.observe(video);



video.addEventListener("click",()=>{


if(video.paused){

video.play();

}else{

video.pause();

}


});


});


});