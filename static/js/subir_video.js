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


    const titulo = document.getElementById("titulo").value;
    const descripcion = document.getElementById("descripcion").value;
    const archivo = document.getElementById("video").files[0];


    if (!archivo) {
        alert("Selecciona un video");
        return;
    }


    try {

        // nombre único del video
        const nombreArchivo = Date.now() + "_" + archivo.name;


        // carpeta videos en Firebase
        const referencia = ref(storage, "videos/" + nombreArchivo);


        // subir video
        await uploadBytes(referencia, archivo);


        // obtener URL
        const urlVideo = await getDownloadURL(referencia);


        // enviar a tu API Flask
        const datos = new FormData();

        datos.append("titulo", titulo);
        datos.append("descripcion", descripcion);
        datos.append("url_video", urlVideo);


        const respuesta = await fetch("https://www.creantunegocio.com/api/videos", {
            method: "POST",
            body: datos
        });


        const resultado = await respuesta.json();


        alert(resultado.mensaje);


        formulario.reset();


    } catch(error) {

        console.log(error);
        alert("Error subiendo video");

    }

});