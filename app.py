from flask import Flask, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.secret_key = "jardintv-secreto"


UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Tamaño máximo: 200 MB
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Extensiones permitidas
ALLOWED_EXTENSIONS = {
    "mp4",
    "mov",
    "webm"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )



@app.route("/")
def inicio():

    return render_template("index.html")



@app.route("/upload", methods=["GET", "POST"])
def upload():


    if request.method == "POST":


        video = request.files.get("video")


        if not video:

            flash("No seleccionaste ningún video")

            return redirect("/upload")



        if video.filename == "":

            flash("Archivo vacío")

            return redirect("/upload")



        if not allowed_file(video.filename):

            flash(
                "Solo se permiten videos MP4, MOV o WEBM"
            )

            return redirect("/upload")



        filename = secure_filename(video.filename)



        ruta = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        video.save(ruta)



        return redirect("/watch")



    return render_template("upload.html")





@app.route("/watch")
def watch():


    videos = os.listdir(
        app.config["UPLOAD_FOLDER"]
    )


    return render_template(
        "watch.html",
        videos=videos
    )




@app.route("/uploads/<filename>")
def uploaded_file(filename):

    from flask import send_from_directory

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )




if __name__ == "__main__":

    app.run(debug=True)