// async function darLike(id){

//     const respuesta = await fetch(
//         `https://www.creantunegocio.com/api/videos/${id}/like`,
//         {
//             method:"POST"
//         }
//     );

//     const datos = await respuesta.json();

//     alert(datos.mensaje);

// }

async function darLike(id) {

    const res = await fetch(
        `https://www.creantunegocio.com/api/videos/${id}/like`,
        {
            method: "POST"
        }
    );

    const data = await res.json();


    const btn = document.getElementById("btnLike");


    if (res.ok) {

        btn.textContent = "❤️ Gracias";
        btn.classList.add("disabled");
        btn.disabled = true;

    }


    cargarLikes(id);
}



async function cargarLikes(id) {

    const res = await fetch(
        `https://www.creantunegocio.com/api/videos/${id}/likess`
    );


    const data = await res.json();


    document.getElementById("totalLikes").textContent = data.likes;

}

// Cargar likes al entrar
cargarLikes(12);