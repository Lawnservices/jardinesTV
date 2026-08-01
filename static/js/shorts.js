const videos = document.querySelectorAll(".video-player");


const observer = new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

const video = entry.target;


if(entry.isIntersecting){

    video.play();

}else{

    video.pause();
    video.currentTime = 0;

}

});


},{
threshold:0.8
});


videos.forEach(video=>{

observer.observe(video);

});