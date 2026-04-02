from flask import Flask, render_template
from app.server.web import web_bp
from app.server.api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)
app.register_blueprint(web_bp)
