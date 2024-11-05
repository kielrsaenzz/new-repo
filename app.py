from flask import Flask, render_template, abort, request, redirect, url_for, Response
import sqlite3
from models import Post, SessionLocal


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
    sesion = SessionLocal()
    posts = sesion.query(Post).all()
    sesion.close()
    # conn = get_db_connection()
    # posts = conn.execute("SELECT * FROM posts").fetchall()
    # conn.close()
    return render_template("post/posts.html", posts=posts)


@app.route("/posts/<int:post_id>", methods=["GET"])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return render_template("post/post.html", post=post)


@app.route("/post/create", methods=["GET", "POST"])
def create_one_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO post (title, content) VALUES (?, ?)",
            (
                title.capitalize(),
                content,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("get_all_post"))
    abort(404)


@app.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "GET":
        conn = get_db_connection()
        post = conn.execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()
        conn.close()
        if post is None:
            abort(404)
        return render_template("post/edit.html", post=post)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute(
            "UPDATE post SET title = ?, content = ? WHERE id = ?",
            (title.capitalize(), content, post_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("get_all_post"))
    abort(404)


@app.route("/post/delete/<int:post_id>", methods=["DELETE"])
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM post WHERE id = ?",
        (post_id,),
    )
    conn.commit()
    conn.close()
    return Response(status=200)
    # return redirect(url_for("get_all_post"))


if __name__ == "__main__":
    app.run(debug=True)
