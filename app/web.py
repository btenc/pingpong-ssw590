from flask import Flask, render_template
from app.database import get_all_endpoints

app = Flask(__name__)


@app.route("/")
def index():
    endpoints = get_all_endpoints()

    if endpoints is None:
        endpoints = []

    return render_template("index.html", endpoints=endpoints)
