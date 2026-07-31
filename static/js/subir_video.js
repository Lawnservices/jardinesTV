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



// =============================
// CREAR THUMBNAIL
// =============================

function crearThumbnail(videoFile) {

    return new Promise((resolve) => {


        const video = document.createElement("video");

        video.src = URL.createObjectURL(videoFile);

        video.currentTime = 1;


        video.onloadeddata = () => {

            const canvas = document.createElement("canvas");

            canvas.width = video.videoWidth;

            canvas.height = video.videoHeight;


            const ctx = canvas.getContext("2d");


            ctx.drawImage(
                video,
                0,
                0,
                canvas.width,
                canvas.height
            );


            canvas.toBlob((blob) => {

                resolve(blob);

            }, "image/jpeg", 0.90);


        };


    });

}





formulario.addEventListener("submit", async (e) => {


    e.preventDefault();


    const boton = formulario.querySelector("button");


    boton.disabled = true;

    boton.innerHTML = "⏳ Subiendo video...";



    const titulo = document.getElementById("titulo").value;

    const descripcion = document.getElementById("descripcion").value;

    const archivo = document.getElementById("video").files[0];



    if (!archivo) {

        alert("Selecciona un video");

        boton.disabled = false;

        return;

    }



    try {


        // =============================
        // NOMBRE UNICO
        // =============================

        const id = Date.now();



        // =============================
        // CREAR THUMBNAIL
        // =============================


        boton.innerHTML = "🖼️ Creando miniatura...";


        const imagenThumbnail = await crearThumbnail(archivo);



        // =============================
        // SUBIR VIDEO FIREBASE
        // =============================


        boton.innerHTML = "📹 Subiendo video...";


        const videoRef = ref(

            storage,

            "videos/" + id + "_" + archivo.name

        );



        await uploadBytes(

            videoRef,

            archivo

        );



        const urlVideo = await getDownloadURL(videoRef);





        // =============================
        // SUBIR THUMBNAIL FIREBASE
        // =============================


        const thumbnailRef = ref(

            storage,

            "thumbnails/" + id + ".jpg"

        );



        await uploadBytes(

            thumbnailRef,

            imagenThumbnail

        );



        const urlThumbnail = await getDownloadURL(thumbnailRef);




        // =============================
        // ENVIAR API
        // =============================


        boton.innerHTML = "💾 Guardando...";


        const datos = new FormData();


        datos.append(
            "titulo",
            titulo
        );


        datos.append(
            "descripcion",
            descripcion
        );


        datos.append(
            "url_video",
            urlVideo
        );


        datos.append(
            "thumbnail",
            urlThumbnail
        );



        const respuesta = await fetch(

            "https://www.creantunegocio.com/api/videos",

            {

                method: "POST",

                body: datos

            }

        );



        const resultado = await respuesta.json();



        if (!respuesta.ok) {

            throw new Error(
                resultado.error
            );

        }



        alert(
            "✅ Video publicado correctamente"
        );



        formulario.reset();



    }
    catch (error) {


        console.error(
            "ERROR:",
            error
        );


        alert(
            "❌ Error subiendo video"
        );


    }
    finally {


        boton.disabled = false;

        boton.innerHTML = "🚀 Publicar video";


    }



});

 
