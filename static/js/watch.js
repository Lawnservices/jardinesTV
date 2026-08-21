document.addEventListener("DOMContentLoaded", () => {

    const feed = document.querySelector(".video-feed");
    const videos = document.querySelectorAll(".short-video");

    if (!feed || !videos.length) return;

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            const video = entry.target;

            if (entry.isIntersecting && entry.intersectionRatio >= 0.7) {

                videos.forEach(otherVideo => {

                    if (otherVideo !== video) {
                        otherVideo.pause();
                    }

                });

                video.play().catch(() => {});

            } else {

                video.pause();

            }

        });

    }, {
        threshold: [0.7]
    });

    videos.forEach(video => {
        observer.observe(video);
    });

});