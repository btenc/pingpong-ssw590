from flask import Flask
from app.server.routes.web import web_bp
from app.server.routes.api import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)
app.register_blueprint(web_bp)
