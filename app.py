from flask import Flask, render_template, request, redirect, flash
import os
import uuid
import requests

import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)
app.secret_key = "jardintv-secreto"


# =========================
# CONFIGURAR FIREBASE
# =========================

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "jardines-4e1db.firebasestorage.app"
})


# =========================
# API
# =========================

API_URL = "https://www.creantunegocio.com/api/videos"


# =========================
# FORMATOS PERMITIDOS
# =========================

ALLOWED_EXTENSIONS = {"mp4", "mov", "webm", "m4v"}

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================
# INICIO
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
        # SUBIR A FIREBASE STORAGE
        # =========================

        extension = os.path.splitext(video.filename)[1].lower()
        filename = uuid.uuid4().hex + extension

        bucket = storage.bucket()
        blob = bucket.blob(filename)

        blob.upload_from_file(video, content_type="video/mp4")
        blob.make_public()

        url_video = blob.public_url

        print("VIDEO SUBIDO A FIREBASE:")
        print(url_video)

        # =========================
        # GUARDAR EN API
        # =========================

        try:
            respuesta = requests.post(
                API_URL,
                data={
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url_video": url_video
                },
                timeout=15
            )

            print("API POST:", respuesta.text)

            if respuesta.status_code != 200:
                flash("Error guardando datos en API")
                return redirect("/upload")

        except Exception as e:
            print("ERROR API POST:", e)
            flash("Error conectando API")
            return redirect("/upload")

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


# =========================
# START
# =========================

if __name__ == "__main__":
    app.run()
