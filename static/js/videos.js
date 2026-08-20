document.addEventListener("DOMContentLoaded", () => {

    const items = document.querySelectorAll(".video-item");

    items.forEach(item => {

        const video = item.querySelector("video");

        video.addEventListener("click", (event) => {

            event.stopPropagation();

            const yaActivo = item.classList.contains("active");

            /* ================================
               QUITAR ACTIVE DE LOS DEMÁS
            ================================= */

            items.forEach(otherItem => {

                if (otherItem !== item) {

                    otherItem.classList.remove("active");

                    const otherVideo =
                        otherItem.querySelector("video");

                    if (otherVideo) {
                        otherVideo.pause();
                    }

                }

            });

            /* ================================
               ACTIVAR VIDEO
            ================================= */

            if (!yaActivo) {

                item.classList.add("active");

                /* ================================
                   SCROLL HACIA ARRIBA
                ================================= */

                document.querySelector(".content").scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            } else {

                /* Si vuelve a hacer click,
                   quitar active */

                item.classList.remove("active");

            }

        });

    });

});