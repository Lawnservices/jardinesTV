from flask import Flask, render_template, request, redirect, flash
import uuid
import requests
import os
import tempfile
import subprocess

import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)
app.secret_key = "jardintv-secreto"


# =========================
# CONFIGURAR FIREBASE
# =========================

firebase_json = os.getenv("FIREBASE_KEY")


with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as temp_file:
    temp_file.write(firebase_json)
    temp_path = temp_file.name


cred = credentials.Certificate(temp_path)


firebase_admin.initialize_app(
    cred, {"storageBucket": "jardines-4e1db.firebasestorage.app"}
)


# =========================
# API
# =========================

API_URL = "https://www.creantunegocio.com/api/videos"


# =========================
# FORMATOS
# =========================

ALLOWED_EXTENSIONS = {"mp4", "mov", "webm", "m4v"}


def allowed_file(filename):

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# CREAR MINIATURA
# =========================


def crear_thumbnail(video_path, image_path):

    try:

        comando = [
            "ffmpeg",
            "-i",
            video_path,
            "-ss",
            "00:00:01",
            "-vframes",
            "1",
            image_path,
            "-y",
        ]

        subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return os.path.exists(image_path)

    except Exception as e:

        print("ERROR THUMBNAIL:", e)

        return False


# =========================
# PAGINA PRINCIPAL
# =========================


@app.route("/")
def inicio():

    videos = []

    try:

        respuesta = requests.get(API_URL, timeout=15)

        videos = respuesta.json()

    except Exception as e:

        print("ERROR API:", e)

    return render_template("index.html", videos=videos)


# =========================
# SUBIR VIDEO
# =========================


@app.route("/upload", methods=["GET", "POST"])
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

        # =========================
        # GUARDAR TEMPORAL VIDEO
        # =========================

        extension = os.path.splitext(video.filename)[1]

        nombre = uuid.uuid4().hex

        video_temp = f"/tmp/{nombre}{extension}"

        video.save(video_temp)

        # =========================
        # CREAR THUMBNAIL
        # =========================

        thumbnail_temp = f"/tmp/{nombre}.jpg"

        creado = crear_thumbnail(video_temp, thumbnail_temp)

        if not creado:

            flash("No se pudo crear miniatura")

            return redirect("/upload")

        bucket = storage.bucket()

        # =========================
        # SUBIR VIDEO FIREBASE
        # =========================

        video_blob = bucket.blob("videos/" + nombre + extension)

        video_blob.upload_from_filename(video_temp, content_type="video/mp4")

        video_blob.make_public()

        url_video = video_blob.public_url

        # =========================
        # SUBIR THUMBNAIL FIREBASE
        # =========================

        img_blob = bucket.blob("thumbnails/" + nombre + ".jpg")

        img_blob.upload_from_filename(thumbnail_temp, content_type="image/jpeg")

        img_blob.make_public()

        thumbnail = img_blob.public_url

        print("VIDEO:")
        print(url_video)

        print("THUMBNAIL:")
        print(thumbnail)

        # =========================
        # GUARDAR MYSQL POR API
        # =========================

        try:

            respuesta = requests.post(
                API_URL,
                data={
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url_video": url_video,
                    "thumbnail": thumbnail,
                },
                timeout=15,
            )

            print("API POST:", respuesta.text)

            if respuesta.status_code != 200:

                flash("Error guardando datos")

                return redirect("/upload")

        except Exception as e:

            print("ERROR API POST:", e)

            flash("Error conectando API")

            return redirect("/upload")

        # borrar temporales

        os.remove(video_temp)
        os.remove(thumbnail_temp)

        flash("Video publicado correctamente")

        return redirect("/watch")

    return render_template("upload.html")


# =========================
# WATCH
# =========================


@app.route("/watch")
def watch():

    videos = []

    try:

        respuesta = requests.get(API_URL, timeout=15)

        videos = respuesta.json()

    except Exception as e:

        print("ERROR WATCH:", e)

    return render_template("watch.html", videos=videos)


# prueva
@app.route("/shorts")
def shorts():

    videos = []

    try:

        respuesta = requests.get(API_URL, timeout=15)

        videos = respuesta.json()

    except Exception as e:

        print("ERROR WATCH:", e)

    return render_template("watch.html", videos=videos)


if __name__ == "__main__":

    app.run(debug=True)
