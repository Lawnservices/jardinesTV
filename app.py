from flask import Flask, render_template, request, redirect, flash, send_from_directory
import os
import uuid
import requests


app = Flask(__name__)

app.secret_key = "jardintv-secreto"


# =========================
# CARPETA VIDEOS EN RENDER
# =========================

UPLOAD_FOLDER = "static/uploads/videos"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# 200 MB máximo

app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024



# =========================
# API
# =========================

API_URL = "https://www.creantunegocio.com/api/videos"



# =========================
# FORMATOS PERMITIDOS
# =========================

ALLOWED_EXTENSIONS = {
    "mp4",
    "mov",
    "webm",
    "m4v"
}



def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".",1)[1].lower()
        in ALLOWED_EXTENSIONS
    )



# =========================
# INICIO
# =========================

@app.route("/")
def inicio():

    videos = []

    try:

        respuesta = requests.get(
            API_URL,
            timeout=15
        )


        print("API GET:", respuesta.status_code)
        print(respuesta.text)


        videos = respuesta.json()


    except Exception as e:

        print("ERROR GET API:", e)



    return render_template(
        "index.html",
        videos=videos
    )




# =========================
# SUBIR VIDEO
# =========================

@app.route("/upload", methods=["GET","POST"])
def upload():


    if request.method == "POST":


        titulo = request.form.get("titulo")

        descripcion = request.form.get("descripcion")

        video = request.files.get("video")



        if not titulo or not video:

            flash("Faltan datos")

            return redirect("/upload")



        if video.filename == "":

            flash("Archivo vacío")

            return redirect("/upload")



        if not allowed_file(video.filename):

            flash("Formato no permitido")

            return redirect("/upload")



        extension = os.path.splitext(
            video.filename
        )[1].lower()



        filename = uuid.uuid4().hex + extension



        ruta = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )



        # Guardar video en Render

        video.save(ruta)


        print("VIDEO GUARDADO:")
        print(ruta)



        # =========================
        # ENVIAR A API
        # =========================


        try:

            respuesta = requests.post(

                API_URL,

                data={

                    "titulo": titulo,

                    "descripcion": descripcion,

                    "filename": filename

                },

                timeout=15

            )


            print("API POST STATUS:")
            print(respuesta.status_code)


            print("API POST RESPUESTA:")
            print(respuesta.text)



            if respuesta.status_code != 200:

                flash("Error guardando en base de datos")

                return redirect("/upload")



        except Exception as e:


            print("ERROR POST API:")
            print(e)


            flash("No se pudo conectar con la API")

            return redirect("/upload")




        flash(
            "Video publicado correctamente"
        )


        return redirect("/watch")



    return render_template(
        "upload.html"
    )




# =========================
# WATCH
# =========================

@app.route("/watch")
def watch():


    videos = []


    try:


        respuesta = requests.get(
            API_URL,
            timeout=15
        )


        print("WATCH API:")
        print(respuesta.text)


        videos = respuesta.json()



    except Exception as e:

        print("ERROR WATCH:")
        print(e)



    return render_template(
        "watch.html",
        videos=videos
    )




# =========================
# SERVIR VIDEOS
# =========================

@app.route("/uploads/<filename>")
def uploaded_file(filename):


    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        filename

    )




# =========================
# START
# =========================

if __name__ == "__main__":


    app.run(
        host="0.0.0.0",
        port=5000
    )