const videos = document.querySelectorAll(".video");


const observer = new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

let video = entry.target;


if(entry.isIntersecting){

video.play();

}else{

video.pause();

}


});


},{
threshold:0.8
});


videos.forEach(video=>{
observer.observe(video);
});