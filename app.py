from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)