from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/watch")
def watch():
    return render_template("watch.html")


if __name__ == "__main__":
    app.run(debug=True)