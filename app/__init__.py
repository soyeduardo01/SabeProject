from flask import Flask
from datetime import datetime
from app.routes.home_routes import home_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave-secreta-sabe'

    # Blueprint
    app.register_blueprint(home_bp)

    # Context processor para pasar current_year a todas las vistas
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}

    return app
