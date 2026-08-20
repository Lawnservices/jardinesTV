document.addEventListener("DOMContentLoaded", () => {

    const videos = document.querySelectorAll(".video-item");

    videos.forEach(item => {

        const video = item.querySelector("video");

        video.addEventListener("click", (event) => {

            event.stopPropagation();

            videos.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove("active");

                    const otherVideo = otherItem.querySelector("video");

                    if (otherVideo) {
                        otherVideo.pause();
                    }
                }
            });

            item.classList.toggle("active");

        });

    });

});