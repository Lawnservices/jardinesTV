document.addEventListener("DOMContentLoaded",()=>{


const videos=document.querySelectorAll(".short-video");



const observer=new IntersectionObserver((entries)=>{


entries.forEach(entry=>{


const video=entry.target;



if(entry.isIntersecting){


    // detener todos los demás

    videos.forEach(v=>{

        if(v!==video){

            v.pause();

            v.currentTime=0;

        }

    });



    // autoplay permitido en teléfono

    video.muted=true;

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



/*
 TOQUE EN PANTALLA:
 activa sonido y pausa/play
*/

video.addEventListener("click",()=>{


    if(video.muted){

        video.muted=false;

        video.volume=1;

        video.play();


    }else{


        if(video.paused){

            video.play();

        }else{

            video.pause();

        }


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