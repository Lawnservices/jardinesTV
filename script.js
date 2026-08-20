document.addEventListener("DOMContentLoaded", () => {

  const videos = document.querySelectorAll(".short-video");

  const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {
      const video = entry.target;

      if (entry.isIntersecting) {

        // Pausar otros videos
        videos.forEach(v => {
          if (v !== video) {
            v.pause();
            v.muted = true;
          }
        });

        // Autoplay permitido: empieza mudo
        video.muted = true;
        video.play().catch(() => { });

        // Activar sonido SOLO cuando el usuario hizo scroll
        // En móviles se necesita un pequeño delay
        requestAnimationFrame(() => {
          setTimeout(() => {
            if (!video.paused) {
              video.muted = false;
            }
          }, 250); // 🔥 delay necesario para móviles
        });

      } else {
        video.pause();
        video.muted = true;
      }
    });

  }, { threshold: 0.70 });

  videos.forEach(video => observer.observe(video));

});
