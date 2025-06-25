# app/controllers/seleccion_controller.py

from flask import request, jsonify
from app.utils.excel_parser import leer_postulantes_desde_excel
from app.services.seleccion_service import SeleccionService
from app.services.estrategia_dinamica import EstrategiaDinamica  # Puedes cambiar por otra estrategia

def procesar_filtros():
    """
    Controlador que procesa los filtros enviados desde el frontend.
    Lee el archivo Excel, aplica filtros y selecciona los postulantes usando la estrategia configurada.
    """
    try:
        archivo = request.files.get('archivo')
        algoritmo = request.form.get('algoritmo')  # Por ahora no se usa para cambiar de estrategia
        
        try:
            presupuesto_str = request.form.get('Presupuesto', '0').replace(',', '')
            presupuesto = float(presupuesto_str)
        except ValueError:
            return jsonify({"error": "El valor del presupuesto no es válido."}), 400

        if not archivo or not algoritmo:
            return jsonify({"error": "Archivo o algoritmo no proporcionado"}), 400

        postulantes = leer_postulantes_desde_excel(archivo)

        # Conversión segura de valores numéricos
        def convertir_num(valor, tipo=float):
            try:
                return tipo(valor)
            except (ValueError, TypeError):
                return None

        filtros = {
            "provincia": request.form.get('provincia'),
            "genero": request.form.get('genero'),
            "edad_min": convertir_num(request.form.get('edad_min'), int),
            "edad_max": convertir_num(request.form.get('edad_max'), int),
            "indice_min": convertir_num(request.form.get('indice_min'), float),
            "indice_max": convertir_num(request.form.get('indice_max'), float),
            "nivel_socioeconomico": request.form.get('nivel_socioeconomico'),
            "discapacidad": request.form.get('discapacidad'),
            "ocupacion": request.form.get('ocupacion'),
            "tipo_institucion": request.form.get('tipo_institucion'),
            "monto_requerido": request.form.get('monto_requerido')
        }

        servicio = SeleccionService(estrategia=EstrategiaDinamica())
        resultado = servicio.seleccionar_postulantes(postulantes, filtros, presupuesto)

        return jsonify({
            "seleccionados": [p.to_dict() for p in resultado["seleccionados"]],
            "no_seleccionados": [p.to_dict() for p in resultado["no_seleccionados"]],
            "presupuesto_invertido": f"{resultado['presupuesto_invertido']:,.2f}",
            "presupuesto_sobrante": f"{resultado['presupuesto_sobrante']:,.2f}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
