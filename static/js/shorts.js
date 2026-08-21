const API_URL="https://www.creantunegocio.com/api/videos";
const feed=document.getElementById("video-feed");
const loading=document.getElementById("loading");

let audioActivado=false;


/* =================================
   CARGAR VIDEOS
================================= */

async function cargarVideos(){

    try{

        const respuesta=await fetch(API_URL);

        if(!respuesta.ok){
            throw new Error("Error HTTP: "+respuesta.status);
        }

        const videos=await respuesta.json();

        loading.remove();

        if(!Array.isArray(videos)||videos.length===0){

            feed.innerHTML=`
                <div class="error">
                    <h2>No hay videos todavía</h2>
                </div>
            `;

            return;
        }

        videos.forEach(video=>{

            const container=document.createElement("div");

            container.className="video-container";

            container.innerHTML=`

                <video
                    class="short-video"
                    poster="${video.thumbnail||""}"
                    playsinline
                    webkit-playsinline
                    muted
                    loop
                    controls
                    preload="metadata">

                    <source
                        src="${video.url_video}"
                        type="video/mp4">

                </video>

                <div class="video-info">

                    <h3>
                        🌱 ${escapeHTML(video.titulo||"")}
                    </h3>

                    <p>
                        ${escapeHTML(video.descripcion||"")}
                    </p>

                </div>
            `;

            feed.appendChild(container);

        });

        iniciarReproduccion();

    }catch(error){

        console.error(error);

        loading.remove();

        feed.innerHTML=`

            <div class="error">

                <div>

                    <h2>No se pudieron cargar los videos</h2>

                    <p>${escapeHTML(error.message)}</p>

                </div>

            </div>
        `;
    }
}


/* =================================
   PROTEGER HTML
================================= */

function escapeHTML(text){

    const div=document.createElement("div");

    div.textContent=text;

    return div.innerHTML;
}


/* =================================
   REPRODUCCIÓN TIPO  shors
================================= */

function iniciarReproduccion(){

    const videos=document.querySelectorAll(".short-video");


    /* =================================
       CLICK EN VIDEO = ACTIVAR AUDIO
    ================================= */

    videos.forEach(video=>{

        video.addEventListener("click",()=>{

            audioActivado=true;

            videos.forEach(otroVideo=>{

                if(otroVideo!==video){
                    otroVideo.pause();
                }

            });

            video.muted=false;

            video.play().catch(()=>{});

        });

    });


    /* =================================
       DETECTAR VIDEO VISIBLE
    ================================= */

    const observer=new IntersectionObserver(entries=>{

        entries.forEach(entry=>{

            const video=entry.target;

            if(entry.isIntersecting&&entry.intersectionRatio>=0.75){

                videos.forEach(otroVideo=>{

                    if(otroVideo!==video){
                        otroVideo.pause();
                    }

                });

                video.muted=!audioActivado;

                video.play().catch(()=>{});

            }else{

                video.pause();

            }

        });

    },{
        threshold:0.75
    });


    videos.forEach(video=>{

        observer.observe(video);


        /* =================================
           CUANDO TERMINA
        ================================= */

        video.addEventListener("ended",()=>{

            video.currentTime=0;

            video.muted=!audioActivado;

            video.play().catch(()=>{});

        });

    });

}


/* =================================
   FLECHAS ↑ ↓
================================= */

document.addEventListener("keydown",event=>{

    if(event.key!=="ArrowDown"&&event.key!=="ArrowUp"){
        return;
    }

    const containers=document.querySelectorAll(".video-container");

    if(!containers.length){
        return;
    }

    event.preventDefault();

    let actual=0;
    let distanciaMenor=Infinity;

    const centroPantalla=window.innerHeight/2;

    containers.forEach((container,index)=>{

        const rect=container.getBoundingClientRect();

        const centroVideo=rect.top+(rect.height/2);

        const distancia=Math.abs(centroVideo-centroPantalla);

        if(distancia<distanciaMenor){

            distanciaMenor=distancia;
            actual=index;

        }

    });


    let siguiente=actual;


    if(event.key==="ArrowDown"){

        if(actual<containers.length-1){
            siguiente=actual+1;
        }

    }


    if(event.key==="ArrowUp"){

        if(actual>0){
            siguiente=actual-1;
        }

    }


    if(siguiente===actual){
        return;
    }


    containers[siguiente].scrollIntoView({
        behavior:"smooth",
        block:"center"
    });

});


/* =================================
   ESPACIO = PLAY / PAUSA
   NO ACTIVA EL AUDIO
================================= */

document.addEventListener("keydown",event=>{

    if(event.code!=="Space"){
        return;
    }

    event.preventDefault();

    const videos=document.querySelectorAll(".short-video");

    if(!videos.length){
        return;
    }


    let videoActual=null;
    let distanciaMenor=Infinity;

    const centroPantalla=window.innerHeight/2;


    videos.forEach(video=>{

        const rect=video.getBoundingClientRect();

        const centroVideo=rect.top+(rect.height/2);

        const distancia=Math.abs(centroVideo-centroPantalla);

        if(distancia<distanciaMenor){

            distanciaMenor=distancia;
            videoActual=video;

        }

    });


    if(!videoActual){
        return;
    }


    /* PAUSA */

    if(!videoActual.paused){

        videoActual.pause();

        return;
    }

    /*
       IMPORTANTE:
       La barra espaciadora NO activa
       el sonido.
    */

    videoActual.muted=!audioActivado;

    videoActual.play().catch(()=>{});

});


/* =================================
   INICIAR
================================= */

cargarVideos();

 