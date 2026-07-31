import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { 
    getStorage,
    ref,
    uploadBytes,
    getDownloadURL
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-storage.js";


const firebaseConfig = {
    apiKey: "AIzaSyBEfiq790QMhU64qIuIhabh2Rq_Ll4Dgtk",
    authDomain: "jardines-4e1db.firebaseapp.com",
    projectId: "jardines-4e1db",
    storageBucket: "jardines-4e1db.firebasestorage.app",
    messagingSenderId: "226365823853",
    appId: "1:226365823853:web:1634bdc66bc2cc12b91864"
};


const app = initializeApp(firebaseConfig);

const storage = getStorage(app);


const formulario = document.querySelector("form");


formulario.addEventListener("submit", async (e) => {

    e.preventDefault();

    const boton = formulario.querySelector("button");

    // bloquear botón
    boton.disabled = true;
    boton.innerHTML = "⏳ Subiendo video...";


    const titulo = document.getElementById("titulo").value;
    const descripcion = document.getElementById("descripcion").value;
    const archivo = document.getElementById("video").files[0];


    // verificar archivo
    if (!archivo) {

        alert("Selecciona un video");

        boton.disabled = false;
        boton.innerHTML = "🚀 Publicar video";

        return;
    }


    try {

        // crear nombre único
        const nombreArchivo = Date.now() + "_" + archivo.name;


        // ubicación en Firebase Storage
        const referencia = ref(
            storage,
            "videos/" + nombreArchivo
        );


        // subir video a Firebase
        await uploadBytes(referencia, archivo);


        // obtener URL del video
        const urlVideo = await getDownloadURL(referencia);


        // enviar datos a Flask
        const datos = new FormData();

        datos.append("titulo", titulo);
        datos.append("descripcion", descripcion);
        datos.append("url_video", urlVideo);
        datos.append("thumbnail", urlThumbnail);

        const respuesta = await fetch(
            "https://www.creantunegocio.com/api/videos",
            {
                method: "POST",
                body: datos
            }
        );


        const resultado = await respuesta.json();


        if (!respuesta.ok) {
            throw new Error(resultado.error || "Error guardando video");
        }


        alert("✅ Video publicado correctamente");


        // limpiar formulario
        formulario.reset();


    } catch(error) {

        console.error("Error:", error);

        alert("❌ Error subiendo video");


    } finally {

        // siempre desbloquear botón
        boton.disabled = false;
        boton.innerHTML = "🚀 Publicar video";

    }

});