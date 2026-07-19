from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Crear la carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        video = request.files.get("video")

        if video and video.filename != "":
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], video.filename)
            video.save(ruta)

            return redirect("/watch")

    return render_template("upload.html")


@app.route("/watch")
def watch():

    videos = os.listdir(app.config["UPLOAD_FOLDER"])

    return render_template("watch.html", videos=videos)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    from flask import send_from_directory

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def inicio():
#     return render_template("index.html")


# @app.route("/upload")
# def upload():
#     return render_template("upload.html")


# @app.route("/watch")
# def watch():
#     return render_template("watch.html")


# if __name__ == "__main__":
#     app.run(debug=True)