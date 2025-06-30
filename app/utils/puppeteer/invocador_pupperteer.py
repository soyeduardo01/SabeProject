import subprocess
import json
import os

def obtener_graficos_base64(ruta_json: str) -> list:
    """
    Ejecuta el script Puppeteer que genera gráficos con Chart.js y extrae
    sus representaciones en base64.

    :param ruta_json: Ruta absoluta del archivo JSON con los datos estadísticos
    :return: Lista de strings base64 (una por cada gráfico)
    """
    script_path = os.path.abspath("utils/puppeteer/generar_graficos.js")
    
    try:
        resultado = subprocess.run(
            ["node", script_path, ruta_json],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(resultado.stdout)
    
    except subprocess.CalledProcessError as e:
        print("[ERROR Puppeteer]", e.stderr)
        return []

    except json.JSONDecodeError:
        print("[ERROR] La salida no es JSON válido.")
        return []
