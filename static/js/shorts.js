const videos = document.querySelectorAll(".video");

const observer = new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

const video = entry.target;

if(entry.isIntersecting){

video.play();

}else{

video.pause();

}

});

},{
threshold:0.7
});


videos.forEach(video=>{
observer.observe(video);
});