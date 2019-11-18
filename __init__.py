import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='5c8fce510fa3c5f9bb251cd1b13fd6eb',
        DATABASE=os.path.join(app.instance_path, 'hw13.db'),
    )
    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return "hello world!"

    return app