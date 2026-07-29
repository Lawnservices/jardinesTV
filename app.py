from flask import Flask, render_template, request, redirect, flash
import os
import uuid
import mysql.connector
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = "jardintv-secreto"


# =========================
# CONEXION MYSQL
# =========================

def get_db():

    return mysql.connector.connect(
        host="MLaguna.mysql.pythonanywhere-services.com",
        user="MLaguna",
        password="VQV4vZ9.%M(Yt9^",
        database="MLaguna$jardinestv",
         connection_timeout=5
    )



# =========================
# CARPETA DE VIDEOS
# =========================

UPLOAD_FOLDER = "static/uploads/videos"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)



# Tamaño máximo 200 MB

app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024



# =========================
# EXTENSIONES
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
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )



# =========================
# INICIO
# =========================

@app.route("/")
def inicio():

    db = get_db()

    cursor = db.cursor(dictionary=True)


    cursor.execute(
        "SELECT * FROM videos ORDER BY id DESC"
    )


    videos = cursor.fetchall()


    cursor.close()
    db.close()


    return render_template(
        "index.html",
        videos=videos
    )



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

            flash("Falta título o video")

            return redirect("/upload")



        if video.filename == "":

            flash("Archivo vacío")

            return redirect("/upload")



        if not allowed_file(video.filename):

            flash("Formato de video no permitido")

            return redirect("/upload")



        extension = os.path.splitext(video.filename)[1]


        filename = uuid.uuid4().hex + extension



        ruta = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )



        # Guardar video en Render

        video.save(ruta)



        # Guardar datos en MySQL

        db = get_db()

        cursor = db.cursor()



        cursor.execute("""
            INSERT INTO videos
            (titulo, descripcion, filename)
            VALUES (%s,%s,%s)
        """,
        (
            titulo,
            descripcion,
            filename
        ))



        db.commit()


        cursor.close()

        db.close()



        flash("Video publicado correctamente")


        return redirect("/watch")



    return render_template("upload.html")



# =========================
# WATCH
# =========================

@app.route("/watch")
def watch():


    db = get_db()


    cursor = db.cursor(dictionary=True)



    cursor.execute(
        "SELECT * FROM videos ORDER BY id DESC"
    )



    videos = cursor.fetchall()



    cursor.close()

    db.close()



    return render_template(
        "watch.html",
        videos=videos
    )



# =========================
# ARRANQUE
# =========================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)