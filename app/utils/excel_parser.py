# app/utils/excel_parser.py

import pandas as pd
from app.models.postulante_model import Postulante
from io import BytesIO

def leer_postulantes_desde_excel(archivo_excel):
    """
    Función que lee un archivo Excel y convierte cada fila en una instancia del modelo Postulante.
    Se espera que los encabezados estén en la fila 6 del archivo (índice 5).
    """
    try:
        df = pd.read_excel(BytesIO(archivo_excel.read()), engine='openpyxl', header=5)

        postulantes = []
        for _, row in df.iterrows():
            postulante = Postulante(
                nombre=row.get("NOMBRE"),
                genero=row.get("GÉNERO"),
                nivel_socioeconomico=row.get("NIVEL SOCIOECONÓMICO"),
                ocupacion=row.get("OCUPACIÓN"),
                indice=row.get("ÍNDICE"),
                monto_requerido=row.get("MONTO REQUERIDO"),
                edad=row.get("EDAD"),
                provincia=row.get("PROVINCIA"),
                discapacidad=row.get("¿DISCAPACIDAD?"),
                tipo_institucion=row.get("TIPO DE INSTITUCIÓN DE PROCEDENCIA")
            )
            postulantes.append(postulante)

        return postulantes

    except Exception as e:
        raise ValueError(f"Error al leer el archivo Excel: {e}")
