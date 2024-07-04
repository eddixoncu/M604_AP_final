from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'M604'
    app.config['TEMPLATE_FOLDER'] = "templates/"

    from .views import infractions
    app.register_blueprint(infractions, url_prefix="/")

    return app
