 

const videos = document.querySelectorAll(".short-video");


const observer = new IntersectionObserver((entries)=>{


entries.forEach(entry=>{


let video = entry.target;


if(entry.isIntersecting){


videos.forEach(v=>{

if(v !== video){

v.pause();

}

});


video.play().catch(()=>{});


}else{


video.pause();


}


});


},{

threshold:0.75

});



videos.forEach(video=>{


observer.observe(video);



video.addEventListener("click",()=>{


if(video.paused){

videos.forEach(v=>v.pause());

video.play();


}else{

video.pause();

}


});


});


 