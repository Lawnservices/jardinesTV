document.addEventListener("DOMContentLoaded", () => {

  const videos = document.querySelectorAll(".short-video");

  // Observador para detectar cuando el video está visible
  const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {
      const video = entry.target;

      if (entry.isIntersecting) {

        // Pausar todos los demás videos
        videos.forEach(v => {
          if (v !== video) {
            v.pause();
            v.muted = true;
          }
        });

        // Autoplay permitido: empieza mudo
        video.muted = true;
        video.play().catch(() => {});

        // Activar sonido cuando el usuario hizo scroll
        setTimeout(() => {
          video.muted = false;
        }, 150); // pequeño delay para evitar bloqueo del navegador

      } else {
        video.pause();
        video.muted = true;
      }
    });

  }, { threshold: 0.75 });

  // Activar observador
  videos.forEach(video => observer.observe(video));

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