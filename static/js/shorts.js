document.addEventListener("DOMContentLoaded",()=>{

const videos=document.querySelectorAll(".short-video");
const isMobile=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

let soundEnabled=false;


const observer=new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

const video=entry.target;


if(entry.isIntersecting){


videos.forEach(v=>{
if(v!==video){
v.pause();
}
});


if(soundEnabled){

video.muted=false;
video.volume=1;

}else{

video.muted=true;

}


video.play().catch(()=>{});


}else{

video.pause();

}


});

},{threshold:0.75});



videos.forEach(video=>{


observer.observe(video);


video.addEventListener("click",()=>{


soundEnabled=true;


videos.forEach(v=>{

if(v!==video){
v.pause();
v.muted=true;
}

});


video.muted=false;
video.volume=1;


video.play().catch(()=>{});


});


});


});