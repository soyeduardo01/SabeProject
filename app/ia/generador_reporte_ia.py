import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde la variable de entorno
clave = os.getenv('GOOGLE_API_KEY')
print(clave)
# Configurar la librería de Gemini (Generative AI)
genai.configure(api_key=clave)

def generar_texto_reporte(seleccionados, no_seleccionados, presupuesto, restante, inversion, filtros):
    total_postulantes = len(seleccionados) + len(no_seleccionados)
    año_actual   = datetime.now().year
    fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Ej: 26/06/2025

 # Construir una lista legible sólo con los filtros aplicados:
    filtros_aplicados = []
    defaults = {
        "provincia":            "SELECCIONAR",
        "genero":               "SELECCIONAR",
        "nivel_socioeconomico": "SELECCIONAR",
        "discapacidad":         "SELECCIONAR",
        "tipo_institucion":     "SELECCIONAR",
        "ocupacion":            "SELECCIONAR",
        "edad_min":             "10",
        "edad_max":             "70",
        "indice_min":           "0",
        "indice_max":           "100",
        "monto_requerido":      "SELECCIONAR"
    }
    for clave, valor in filtros.items():
        if valor is None:
            continue
        texto_valor = str(valor).strip()
        if defaults.get(clave) and texto_valor.upper() == defaults[clave]:
            continue
        etiqueta = clave.replace('_', ' ').capitalize()
        filtros_aplicados.append(f"- {etiqueta}: {texto_valor}")
    descripcion_filtros = (
        "No se aplicaron filtros específicos."
        if not filtros_aplicados
        else "\n".join(filtros_aplicados)
    )

    prompt = f"""
Eres un analista de negocios y estadístico encargado de redactar un informe profesional detallado para el "Sistema de Asignación de Becas Educativas (SABE)".

Genera un reporte formal de aproximadamente 1500 palabras, con buena redacción, claridad técnica y dirigido a tomadores de decisión.

Utiliza la siguiente estructura con marcas claras:

- Usa ## antes de los títulos principales (Introducción, Detalle Presupuestario, etc.).
- Usa ### antes de subtítulos si los requieres.
- Usa **texto** para marcar fragmentos importantes en negrita.

NO utilices etiquetas HTML ni tablas.

Incluye la siguiente información:

---

## Introducción  
Propósito del presente informe.

## Resumen del Proceso de Priorización  
- Total de postulantes: {total_postulantes}  
- Seleccionados: {len(seleccionados)}  
- No seleccionados: {len(no_seleccionados)}

## Detalle Presupuestario  
- Presupuesto total asignado: RD${presupuesto:,.2f}  
- Monto invertido: RD${inversion:,.2f}  
- Presupuesto sobrante: RD${restante:,.2f}  
Análisis del uso eficiente del presupuesto y comentarios sobre la demanda.

## Filtros Aplicados  
{descripcion_filtros}

## Análisis de Resultados  
Tendencias observadas, criterios determinantes y análisis de impacto.

## Conclusiones y Recomendaciones  
Sugerencias para futuras convocatorias, evaluación de efectividad y aportes del sistema SABE.

---
Para fines de documentación en párrafos tienes estás fechas:
Año: {año_actual}  
Fecha de generación: {fecha_actual}
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error generando texto con IA:", e)
        return "No se pudo generar el informe automáticamente."
