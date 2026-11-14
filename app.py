import os
import json
import uuid
import tempfile
import subprocess

import requests

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    send_from_directory
)

import firebase_admin
from firebase_admin import credentials, storage


# ==================================================
# FLASK
# ==================================================

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

live_url = ""


# ==================================================
# FIREBASE
# ==================================================

firebase_json = os.environ.get("FIREBASE_KEY")

if not firebase_json:
    raise RuntimeError(
        "FIREBASE_KEY no está configurada."
    )

firebase_data = json.loads(firebase_json)

cred = credentials.Certificate(firebase_data)

firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": "jardines-4e1db.firebasestorage.app"
    }
)


# ==================================================
# API
# ==================================================

API_URL = "https://www.creantunegocio.com/api/videos"


# ==================================================
# FORMATOS PERMITIDOS
# ==================================================

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


# ==================================================
# MINIATURA
# ==================================================

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
            "-y"
        ]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if resultado.returncode != 0:

            print(
                "ERROR FFMPEG:",
                resultado.stderr.decode(
                    errors="ignore"
                )
            )

            return False

        return os.path.exists(image_path)

    except Exception as e:

        print(
            "ERROR THUMBNAIL:",
            e
        )

        return False


# ==================================================
# PÁGINA PRINCIPAL
# ==================================================

@app.route("/")
def inicio():

    videos = []

    try:

        respuesta = requests.get(
            API_URL,
            timeout=15
        )

        respuesta.raise_for_status()

        videos = respuesta.json()

    except Exception as e:

        print(
            "ERROR API:",
            e
        )

    return render_template(
        "index.html",
        videos=videos
    )


# ==================================================
# SUBIR VIDEO
# ==================================================

@app.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    if request.method == "POST":

        titulo = request.form.get(
            "titulo",
            ""
        ).strip()

        descripcion = request.form.get(
            "descripcion",
            ""
        ).strip()

        video = request.files.get(
            "video"
        )

        if not titulo or not video:

            flash(
                "Faltan datos"
            )

            return redirect(
                "/upload"
            )

        if video.filename == "":

            flash(
                "Archivo vacío"
            )

            return redirect(
                "/upload"
            )

        if not allowed_file(
            video.filename
        ):

            flash(
                "Formato no permitido"
            )

            return redirect(
                "/upload"
            )

        # ==========================================
        # ARCHIVOS TEMPORALES
        # ==========================================

        extension = os.path.splitext(
            video.filename
        )[1].lower()

        nombre = uuid.uuid4().hex

        temp_dir = tempfile.gettempdir()

        video_temp = os.path.join(
            temp_dir,
            nombre + extension
        )

        thumbnail_temp = os.path.join(
            temp_dir,
            nombre + ".jpg"
        )

        try:

            # ======================================
            # GUARDAR VIDEO TEMPORAL
            # ======================================

            video.save(
                video_temp
            )

            # ======================================
            # CREAR MINIATURA
            # ======================================

            creado = crear_thumbnail(
                video_temp,
                thumbnail_temp
            )

            if not creado:

                flash(
                    "No se pudo crear la miniatura"
                )

                return redirect(
                    "/upload"
                )

            # ======================================
            # FIREBASE
            # ======================================

            bucket = storage.bucket()

            # ======================================
            # SUBIR VIDEO
            # ======================================

            video_blob = bucket.blob(
                "videos/"
                + nombre
                + extension
            )

            content_types = {
                ".mp4": "video/mp4",
                ".mov": "video/quicktime",
                ".webm": "video/webm",
                ".m4v": "video/x-m4v"
            }

            content_type = content_types.get(
                extension,
                "application/octet-stream"
            )

            video_blob.upload_from_filename(
                video_temp,
                content_type=content_type
            )

            video_blob.make_public()

            url_video = (
                video_blob.public_url
            )

            # ======================================
            # SUBIR MINIATURA
            # ======================================

            img_blob = bucket.blob(
                "thumbnails/"
                + nombre
                + ".jpg"
            )

            img_blob.upload_from_filename(
                thumbnail_temp,
                content_type="image/jpeg"
            )

            img_blob.make_public()

            thumbnail = (
                img_blob.public_url
            )

            print(
                "VIDEO:",
                url_video
            )

            print(
                "THUMBNAIL:",
                thumbnail
            )

            # ======================================
            # GUARDAR EN API / MYSQL
            # ======================================

            respuesta = requests.post(
                API_URL,
                data={
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url_video": url_video,
                    "thumbnail": thumbnail
                },
                timeout=15
            )

            print(
                "API POST:",
                respuesta.text
            )

            if respuesta.status_code not in (
                200,
                201
            ):

                flash(
                    "Error guardando los datos"
                )

                return redirect(
                    "/upload"
                )

            flash(
                "Video publicado correctamente"
            )

            return redirect(
                "/watch"
            )

        except Exception as e:

            print(
                "ERROR SUBIENDO VIDEO:",
                e
            )

            flash(
                "Ocurrió un error al subir el video"
            )

            return redirect(
                "/upload"
            )

        finally:

            # ======================================
            # BORRAR TEMPORALES
            # ======================================

            if os.path.exists(
                video_temp
            ):

                os.remove(
                    video_temp
                )

            if os.path.exists(
                thumbnail_temp
            ):

                os.remove(
                    thumbnail_temp
                )

    return render_template(
        "upload.html"
    )


# ==================================================
# WATCH
# ==================================================

@app.route("/watch")
def watch():

    videos = []

    try:

        respuesta = requests.get(
            API_URL,
            timeout=15
        )

        respuesta.raise_for_status()

        videos = respuesta.json()

    except Exception as e:

        print(
            "ERROR WATCH:",
            e
        )

    return render_template(
        "watch.html",
        videos=videos
    )


# ==================================================
# SHORTS
# ==================================================

@app.route("/shorts")
def shorts():

    videos = []

    try:

        respuesta = requests.get(
            API_URL,
            timeout=15
        )

        respuesta.raise_for_status()

        videos = respuesta.json()

    except Exception as e:

        print(
            "ERROR SHORTS:",
            e
        )

    return render_template(
        "shorts.html",
        videos=videos
    )


# ==================================================
# ERROR 404
# ==================================================

@app.errorhandler(404)
def pagina_no_encontrada(error):

    return redirect("/")


# ==================================================
# LIVE
# ==================================================

# @app.route("/live")
# def live():

#     return render_template(
#         "live.html",
#         live_url=live_url
#     )
@app.route("/live")
def live():

    live_url = ""
    activo = False

    try:

        respuesta = requests.get(
            "https://www.creantunegocio.com/api/live",
            timeout=15
        )

        if respuesta.status_code == 200:

            datos = respuesta.json()

            live_url = datos.get(
                "live_url",
                ""
            )

            activo = datos.get(
                "activo",
                False
            )

    except Exception as e:

        print(
            "ERROR LIVE:",
            e
        )

    return render_template(
        "live.html",
        live_url=live_url if activo else ""
    )

# ==================================================
# ADMIN LOGIN
# ==================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        if password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect(
                "/admin/live"
            )

        return render_template(
            "admin_login.html",
            error="Contraseña incorrecta"
        )

    return render_template(
        "admin_login.html"
    )


# ==================================================
# ADMIN LIVE
# ==================================================

# @app.route(
#     "/admin/live",
#     methods=["GET", "POST"]
# )
# def admin_live():

#     global live_url

#     if not session.get("admin"):

#         return redirect(
#             "/admin/login"
#         )

#     if request.method == "POST":

#         live_url = request.form.get(
#             "live_url",
#             ""
#         ).strip()

#         return redirect(
#             "/live"
#         )

#     return render_template(
#         "admin_live.html",
#         live_url=live_url
#     )

@app.route(
    "/admin/live",
    methods=["GET", "POST"]
)
def admin_live():

    if not session.get("admin"):
        return redirect("/admin/login")

    if request.method == "POST":

        live_url = request.form.get(
            "live_url",
            ""
        ).strip()

        try:

            respuesta = requests.post(
                "https://www.creantunegocio.com/api/live",
                data={
                    "live_url": live_url,
                    "activo": 1
                },
                timeout=15
            )

            if respuesta.status_code != 200:

                flash(
                    "Error guardando Live"
                )

                return redirect(
                    "/admin/live"
                )

        except Exception as e:

            print(
                "ERROR API LIVE:",
                e
            )

            flash(
                "Error conectando con la API"
            )

            return redirect(
                "/admin/live"
            )

        return redirect("/live")

    # Obtener Live actual

    live_url = ""

    try:

        respuesta = requests.get(
            "https://www.creantunegocio.com/api/live",
            timeout=15
        )

        if respuesta.status_code == 200:

            datos = respuesta.json()

            live_url = datos.get(
                "live_url",
                ""
            )

    except Exception as e:

        print(
            "ERROR OBTENIENDO LIVE:",
            e
        )

    return render_template(
        "admin_live.html",
        live_url=live_url
    )
# ==================================================
# ADMIN LOGOUT
# ==================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        "/admin/login"
    )


# ==================================================
# EJECUTAR
# ==================================================
# install
@app.route('/sw.js')
def service_worker():
    response = send_from_directory(
        app.static_folder,
        'sw.js'
    )
    response.headers['Service-Worker-Allowed'] = '/'
    response.headers['Content-Type'] = 'application/javascript'
    return response



if __name__ == "__main__":

    app.run(
        debug=True
    )