document.addEventListener("DOMContentLoaded", () => {

    const items = document.querySelectorAll(".video-item");

    items.forEach(item => {

        const video = item.querySelector("video");

        video.addEventListener("click", (event) => {

            event.stopPropagation();

            const yaActivo = item.classList.contains("active");

            items.forEach(otherItem => {

                otherItem.classList.remove("active");

                if (otherItem !== item) {

                    const otherVideo =
                        otherItem.querySelector("video");

                    if (otherVideo) {
                        otherVideo.pause();
                    }

                }

            });

            if (!yaActivo) {
                item.classList.add("active");
            }

        });

    });

});