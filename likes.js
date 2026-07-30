async function darLike(id){

    const respuesta = await fetch(
        `/api/videos/${id}/like`,
        {
            method:"POST"
        }
    );

    const datos = await respuesta.json();

    alert(datos.mensaje);

}