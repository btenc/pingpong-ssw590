from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h1>Ping Pong</h1>
    <p>Build web dashboard in place of this</p>
    <p>Use run_cli.py for now, I am just testing flask connection</p>
    """
