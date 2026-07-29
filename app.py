from flask import Flask, render_template, request, redirect, flash, send_from_directory
import os
import uuid
import requests
import cv2


app = Flask(__name__)

app.secret_key = "jardintv-secreto"


# =========================
# CARPETA VIDEOS
# =========================

UPLOAD_FOLDER = "static/uploads/videos"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================
# CARPETA MINIATURAS
# =========================

THUMBNAIL_FOLDER = "static/uploads/thumbnails"

app.config["THUMBNAIL_FOLDER"] = THUMBNAIL_FOLDER

os.makedirs(
    THUMBNAIL_FOLDER,
    exist_ok=True
)



# =========================
# LIMITE VIDEO
# =========================

app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024



# =========================
# API
# =========================

API_URL = "https://www.creantunegocio.com/api/videos"



# =========================
# FORMATOS
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
# CREAR MINIATURA
# =========================

def crear_thumbnail(video_path, thumbnail_path):

    try:

        video = cv2.VideoCapture(video_path)

        exito, imagen = video.read()


        if exito:

            cv2.imwrite(
                thumbnail_path,
                imagen
            )


        video.release()


    except Exception as e:

        print("ERROR THUMBNAIL:", e)



# =========================
# INICIO
# =========================

@app.route("/")
def inicio():

    videos=[]

    try:

        respuesta = requests.get(
            API_URL,
            timeout=15
        )

        videos = respuesta.json()


    except Exception as e:

        print("ERROR API:", e)



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



        filename = (
            uuid.uuid4().hex
            +
            extension
        )



        ruta = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )



        # guardar video

        video.save(ruta)



        print("VIDEO:")
        print(ruta)



        # =========================
        # CREAR THUMBNAIL
        # =========================

        thumbnail = (
            filename.rsplit(".",1)[0]
            +
            ".jpg"
        )



        thumbnail_path = os.path.join(
            app.config["THUMBNAIL_FOLDER"],
            thumbnail
        )



        crear_thumbnail(
            ruta,
            thumbnail_path
        )



        print("THUMBNAIL:")
        print(thumbnail_path)



        # =========================
        # GUARDAR EN API
        # =========================


        try:

            respuesta = requests.post(

                API_URL,

                data={

                    "titulo": titulo,

                    "descripcion": descripcion,

                    "filename": filename,

                    "thumbnail": thumbnail

                },

                timeout=15
            )


            print(
                "API:",
                respuesta.text
            )



            if respuesta.status_code != 200:

                flash(
                    "Error guardando datos"
                )

                return redirect("/upload")



        except Exception as e:


            print(e)

            flash(
                "Error conectando API"
            )

            return redirect("/upload")



        flash(
            "Video publicado"
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

    videos=[]


    try:

        respuesta = requests.get(
            API_URL,
            timeout=15
        )


        videos = respuesta.json()


    except Exception as e:

        print(e)



    return render_template(
        "watch.html",
        videos=videos
    )



# =========================
# VIDEOS
# =========================

@app.route("/uploads/<filename>")
def videos(filename):

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        filename
    )



# =========================
# MINIATURAS
# =========================

@app.route("/thumbnails/<filename>")
def thumbnails(filename):

    return send_from_directory(

        app.config["THUMBNAIL_FOLDER"],

        filename
    )



# =========================
# START
# =========================

if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )