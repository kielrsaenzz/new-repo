from flask import Flask, render_template
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    context = {
        "name": "BASE",
        "project": "Web developer Flask",
    }
    return render_template(template_name_or_list="base.html", **context)


@app.route("/home", methods=["GET"])
def home():
    context = {"name": "HOME", "my_name": "Kiel"}
    return render_template("home.html", **context)


@app.route("/posts", methods=["GET"])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    for post in posts:
        print("========================")
        print("=====>", post["id"])
        print("=====>", post["title"])
        print("=====>", post["content"])
        print("=====>", post["created"])
    return render_template("posts.html", posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
