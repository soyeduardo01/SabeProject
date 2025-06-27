# app/routes/seleccion_routes.py

from flask import Blueprint,  session, send_file, request, make_response, jsonify
from app.controllers import seleccion_controller
from app.services.generador_reporte_service import GeneradorReporteService
import json

# Definimos el Blueprint para las rutas relacionadas con selección
seleccion_bp = Blueprint('seleccion', __name__)

# Ruta para procesar los filtros enviados por el usuario
@seleccion_bp.route('/procesar-filtros', methods=['POST'])
def procesar_filtros_route():
    return seleccion_controller.procesar_filtros()


@seleccion_bp.route('/generar_informe', methods=['POST'])
def generar_informe():
    try:
        # Obtener datos del formulario
        seleccionados_json = request.form.get('SeleccionadosJSON', '[]')
        no_seleccionados_json = request.form.get('NoSeleccionadosJSON', '[]')
        seleccionados = json.loads(seleccionados_json)
        no_seleccionados = json.loads(no_seleccionados_json)

        try:
            presupuesto_str = request.form.get('Presupuesto', '0').replace(',', '')
            presupuesto = float(presupuesto_str)
        except ValueError:
            return jsonify({"error": "El valor del presupuesto no es válido."}), 400
        
        try:
            restante_str = request.form.get('PresupuestoSobrante', '0').replace(',', '')
            restante = float(restante_str)
        except ValueError:
            return jsonify({"error": "El valor del presupuesto sobrante no es válido."}), 400
        
        try:
            inversion_str = request.form.get('PresupuestoInvertido', '0').replace(',', '')
            inversion = float(inversion_str)
        except ValueError:
            return jsonify({"error": "El valor del presupuesto invertido no es válido."}), 400

        # Solo incluir filtros verdaderos (ignorar campos extra como Presupuesto...)
        filtros = {
            k: v for k, v in request.form.items()
            if k not in ['SeleccionadosJSON', 'NoSeleccionadosJSON', 'Presupuesto', 'PresupuestoSobrante', 'PresupuestoInvertido']
        }

        # Generar texto del reporte con IA
        service = GeneradorReporteService()
        pdf = service.generar_reporte(seleccionados, no_seleccionados, presupuesto, restante, inversion, filtros)

        # Generar PDF en memoria con pdfkit
        # from app.ia.generador_pdf import generar_pdf
        return pdf

    except Exception as e:
        print('Error generando el informe:', str(e))
        return 'Error interno', 500
