const videos = document.querySelectorAll(".video-item video");
const videoModal = document.getElementById("videoModal");
const modalVideo = document.getElementById("modalVideo");
const closeVideo = document.getElementById("closeVideo");

videos.forEach(video => {

    video.addEventListener("click", function () {

        const source = video.querySelector("source");

        if (!source) {
            return;
        }

        modalVideo.src = source.src;

        videoModal.classList.add("active");

        modalVideo.play();

    });

});

closeVideo.addEventListener("click", function () {

    modalVideo.pause();

    modalVideo.src = "";

    videoModal.classList.remove("active");

});

videoModal.addEventListener("click", function (event) {

    if (event.target === videoModal) {

        modalVideo.pause();

        modalVideo.src = "";

        videoModal.classList.remove("active");

    }

});

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        modalVideo.pause();

        modalVideo.src = "";

        videoModal.classList.remove("active");

    }

});