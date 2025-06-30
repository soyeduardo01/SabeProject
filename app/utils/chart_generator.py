import os
import json
import subprocess
from uuid import uuid4
from flask import current_app


def guardar_datos_graficos(datos: dict) -> str:
    """
    Guarda los datos de gráficos en un archivo JSON temporal.

    :param datos: Diccionario con la información estadística
    :return: Ruta absoluta al archivo JSON generado
    """
    carpeta_temp = os.path.join(current_app.root_path, 'temp')
    os.makedirs(carpeta_temp, exist_ok=True)

    nombre_archivo = f"graficos_{uuid4().hex[:8]}.json"
    ruta_completa = os.path.join(carpeta_temp, nombre_archivo)

    with open(ruta_completa, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    return ruta_completa


def generar_graficos_base64(ruta_json: str) -> list:
    """
    Llama al script Puppeteer para generar gráficos en base64 a partir del HTML y JSON.

    :param ruta_json: Ruta al archivo JSON con los datos estadísticos
    :return: Lista de imágenes base64 codificadas
    """
    script_path = os.path.join(current_app.root_path, 'utils', 'puppeteer', 'generar_graficos.js')
    template_path = os.path.join(current_app.root_path, 'static', 'chart_template.html')

    comando = ['node', script_path, template_path, ruta_json]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        return json.loads(resultado.stdout)
    except subprocess.CalledProcessError as e:
        print("Error al generar los gráficos con Puppeteer:", e.stderr)
        return []
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON desde stdout de Puppeteer:", e)
        return []
