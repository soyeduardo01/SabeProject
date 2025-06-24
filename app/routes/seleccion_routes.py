# app/routes/seleccion_routes.py

from flask import Blueprint
from app.controllers import seleccion_controller

# Definimos el Blueprint para las rutas relacionadas con selección
seleccion_bp = Blueprint('seleccion', __name__)

# Ruta para procesar los filtros enviados por el usuario
@seleccion_bp.route('/procesar-filtros', methods=['POST'])
def procesar_filtros_route():
    return seleccion_controller.procesar_filtros()
