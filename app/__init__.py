from flask import Flask
from datetime import datetime
from dotenv import load_dotenv
from app.routes.home_routes import home_bp
from app.routes.seleccion_routes import seleccion_bp
import os

def create_app():
    load_dotenv()  # Carga las variables de entorno desde .env
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave-secreta-sabe'
    app.config['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

    # Blueprint
    app.register_blueprint(home_bp)
    app.register_blueprint(seleccion_bp)

    # Context processor para pasar current_year a todas las vistas
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.now().year}

    return app


