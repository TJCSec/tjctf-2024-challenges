from flask import Flask, render_template, request
import uuid

app = Flask(__name__)
app.static_folder = "static"


@app.route("/static/<path:path>")
def static_file(filename):
    return app.send_static_file(filename)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create_playlist", methods=["POST"])
def post_playlist():
    try:
        username = request.form["username"]
        text = request.form["text"]
        if len(text) > 10_000:
            return "Too much!", 406
        if "{{" in text or "}}" in text:
            return "Nice try!", 406
        text = [line.split(",") for line in text.splitlines()]
        text = [line[:4] + ["?"] * (4 - min(len(line), 4)) for line in text]
        filled = render_template("playlist.html", username=username, songs=text)
        this_id = str(uuid.uuid4())
        with open(f"templates/uploads/{this_id}.html", "w") as f:
            f.write(filled)
        return render_template("created_playlist.html", uuid_val=this_id), 200
    except Exception as e:
        print(e)
        return "Internal server error", 500


@app.route("/view_playlist/<uuid:name>")
def view_playlist(name):
    name = str(name)
    try:
        return render_template(f"uploads/{name}.html")
    except Exception as e:
        print(e)
        return "checkout not found", 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
