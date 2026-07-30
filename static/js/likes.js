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

 async function darLike(id){

    const res = await fetch(
        `https://www.creantunegocio.com/api/videos/${id}/like`,
        {
            method:"POST"
        }
    );

    if(res.ok){

        cargarLikes(id);

    }

}


async function cargarLikes(id){

    const res = await fetch(
        `https://www.creantunegocio.com/api/videos/${id}/likess`
    );

    const data = await res.json();

    document.getElementById(`likes-${id}`).textContent = data.likes;

}

// Cargar likes al entrar
cargarLikes(12);