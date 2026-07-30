  const API = "https://www.creantunegocio.com/api/videos";

        function obtenerLikes() {
            const id = document.getElementById("videoId").value;

            fetch(`${API}/${id}/likess`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById("likesBox").innerText = "Likes: " + data.likes;
                });
        }

        function darLike() {
            const id = document.getElementById("videoId").value;

            fetch(`${API}/${id}/likesone`, { method: "POST" })
                .then(res => res.json())
                .then(data => {
                    alert(data.mensaje);
                    obtenerLikes();
                });
        }