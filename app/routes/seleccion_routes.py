# app/routes/seleccion_routes.py

from flask import Blueprint, session, send_file, request, make_response, jsonify
from app.models.postulante_model import Postulante
from app.controllers import seleccion_controller
from app.services.generador_reporte_service import GeneradorReporteService
import json

seleccion_bp = Blueprint('seleccion', __name__)

@seleccion_bp.route('/procesar-filtros', methods=['POST'])
def procesar_filtros_route():
    return seleccion_controller.procesar_filtros()


@seleccion_bp.route('/generar_informe', methods=['POST'])
def generar_informe():
    try:
        # Obtener datos del formulario
        seleccionados_json = request.form.get('SeleccionadosJSON', '[]')
        no_seleccionados_json = request.form.get('NoSeleccionadosJSON', '[]')

        seleccionados_raw = json.loads(seleccionados_json)
        no_seleccionados_raw = json.loads(no_seleccionados_json)

        def crear_postulante(data):
            return Postulante(
                nombre=data.get("nombre"),
                genero=data.get("genero"),
                nivel_socioeconomico=data.get("nivel_socioeconomico"),
                ocupacion=data.get("ocupacion"),
                indice=float(data.get("indice", 0)) if data.get("indice") else 0.0,
                monto_requerido=float(data.get("monto_requerido", 0)) if data.get("monto_requerido") else 0.0,
                edad=int(data.get("edad", 0)) if data.get("edad") else 0,
                provincia=data.get("provincia"),
                discapacidad=data.get("discapacidad"),
                tipo_institucion=data.get("tipo_institucion")
            )

        seleccionados = [crear_postulante(p) for p in seleccionados_raw]
        no_seleccionados = [crear_postulante(p) for p in no_seleccionados_raw]

        # Procesar presupuesto
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

        # Solo incluir filtros verdaderos
        filtros = {
            k: v for k, v in request.form.items()
            if k not in ['SeleccionadosJSON', 'NoSeleccionadosJSON', 'Presupuesto', 'PresupuestoSobrante', 'PresupuestoInvertido']
        }

        service = GeneradorReporteService()
        pdf = service.generar_reporte(seleccionados, no_seleccionados, presupuesto, restante, inversion, filtros)
        return pdf

    except Exception as e:
        print('Error generando el informe:', str(e))
        return 'Error interno', 500
