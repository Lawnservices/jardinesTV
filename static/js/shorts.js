// const videos = document.querySelectorAll(".video-player");


// const observer = new IntersectionObserver((entries)=>{

// entries.forEach(entry=>{

// const video = entry.target;


// if(entry.isIntersecting){

//     video.play();

// }else{

//     video.pause();
//     video.currentTime = 0;

// }

// });


// },{
// threshold:0.8
// });


// videos.forEach(video=>{

// observer.observe(video);

// });
const videos = document.querySelectorAll("video");

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const video = entry.target;

    if (entry.isIntersecting) {
      video.play();     // el video visible se reproduce
    } else {
      video.pause();    // el video que sale de pantalla se pausa
    }
  });
}, {
  threshold: 0.6   // el video debe estar 60% visible para reproducirse
});

videos.forEach(video => observer.observe(video));
