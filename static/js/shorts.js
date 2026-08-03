document.addEventListener("DOMContentLoaded",()=>{

const videos=document.querySelectorAll(".short-video");
const isMobile=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

const observer=new IntersectionObserver((entries)=>{

entries.forEach(entry=>{

const video=entry.target;

if(entry.isIntersecting){

videos.forEach(v=>{
if(v!==video){
v.pause();
}
});

if(isMobile){

video.muted=false;
video.volume=1;

video.play().catch(()=>{
video.muted=true;
video.play();
});

}else{

video.muted=false;
video.volume=1;
video.play();

}

}else{

video.pause();

}

});

},{threshold:0.75});


videos.forEach(video=>{

observer.observe(video);

video.addEventListener("click",()=>{

video.muted=false;
video.volume=1;

if(video.paused){
video.play();
}

});

});

});



// document.addEventListener("DOMContentLoaded", () => {


//   const videos = document.querySelectorAll(".short-video");


//   // Cuando el video aparece en pantalla
//   const observer = new IntersectionObserver((entries) => {


//     entries.forEach(entry => {


//       const video = entry.target;


//       if (entry.isIntersecting) {


//         // Pausar todos los demás videos
//         videos.forEach(v => {

//           if (v !== video) {

//             v.pause();

//             v.currentTime = 0;

//           }

//         });


//         // Truco TikTok:
//         // empieza mudo para permitir autoplay
//         video.muted = true;


//         video.play().catch(() => { });


//       } else {


//         video.pause();

//       }



//     });


//   }, {

//     threshold: 0.80

//   });




//   // Activar observador

//   videos.forEach(video => {


//     observer.observe(video);



//     /*
//      Primer toque:
//      - activa sonido
//      - mantiene reproducción
//     */

//     video.addEventListener("click", () => {


//       if (video.paused) {


//         video.play();


//       } else {


//         // si está reproduciendo,
//         // toca para activar/desactivar audio

//         video.muted = !video.muted;


//       }



//     });



//   });



// });