document.addEventListener("DOMContentLoaded",()=>{

const videos=document.querySelectorAll(".short-video");

let soundEnabled=false;
let currentVideo=null;


const observer=new IntersectionObserver((entries)=>{


entries.forEach(entry=>{


const video=entry.target;


if(entry.isIntersecting){


if(currentVideo && currentVideo!==video){

currentVideo.pause();

}


currentVideo=video;



if(soundEnabled){

video.muted=false;
video.volume=1;

}else{

video.muted=true;

}



video.play().catch(()=>{

video.muted=true;
video.play();

});



}else{


if(currentVideo!==video){

video.pause();

}


}



});


},{threshold:0.75});




videos.forEach(video=>{


observer.observe(video);



video.addEventListener("click",()=>{


soundEnabled=true;



if(currentVideo && currentVideo!==video){

currentVideo.pause();

}


currentVideo=video;



video.muted=false;
video.volume=1;


video.play().catch(()=>{});


});



});


});