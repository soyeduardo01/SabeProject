import pdfkit
import uuid
import os
import re
import base64
from datetime import datetime
from flask import make_response, current_app


def generar_html_graficos(imagenes, fecha_actual):
    if not imagenes:
        return ''

    TITULOS = [
        ("Figura 1.", "Distribución de postulantes por provincia.",
         "Este gráfico muestra la cantidad de postulantes seleccionados por cada provincia."),
        ("Figura 2.", "Distribución de postulantes según género.",
         "Representación porcentual de los géneros de los postulantes seleccionados."),
        ("Figura 3.", "Nivel socioeconómico por tipo de institución.",
         "Se comparan los niveles socioeconómicos en función del tipo de institución."),
        ("Figura 4.", "Postulantes seleccionados por rango de edad.",
         "Clasificación de postulantes según rangos de edad."),
        ("Figura 5.", "Distribución de postulantes por índice académico.",
         "Rangos de índice académico alcanzado por los postulantes."),
        ("Figura 6.", "Distribución del presupuesto.",
         "Comparativa entre el monto invertido y el presupuesto sobrante.")
    ]

    html = '<div class="section-title">Análisis Gráfico de Resultados</div>'

    for i, img in enumerate(imagenes):
        titulo, subtitulo, nota = TITULOS[i] if i < len(TITULOS) else (f"Figura {i+1}.", "Gráfico", "Nota: generado por el SABE.")
        html += f'''
        <div class="grafico-img">
          <div class="titulo-figura">
            <strong>{titulo}</strong>
            <p><em>{subtitulo}</em></p>
          </div>
          <img src="{img}" alt="Gráfico {i+1}" />
          <div class="nota-figura">
            Nota. {nota} Generado por SABE el {fecha_actual}.
          </div>
        </div>
        '''

    return html


def generar_pdf(texto, imagenes_base64=None):
    if not isinstance(texto, str):
        texto = str(texto)
    if imagenes_base64 is None:
        imagenes_base64 = []

    meses_es = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    ahora = datetime.now()
    dia = ahora.day
    mes = meses_es[ahora.month - 1].capitalize()
    año = ahora.year
    fecha_actual = f"{dia} de {mes} de {año}"

    logo_path = os.path.join(current_app.root_path, "static", "img", "logo_sabe.png")
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

    def procesar_contenido(txt):
        txt = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', txt)
        txt = re.sub(r'##\s*(.+)', r'<h2 class="section-title">\1</h2>', txt)
        txt = re.sub(r'###\s*(.+)', r'<h3 class="section-subtitle">\1</h3>', txt)

        html = ""
        bloques = [b.strip() for b in txt.split('\n\n') if b.strip()]
        for bloque in bloques:
            if bloque.startswith('- '):
                html += '<ul>'
                for linea in bloque.splitlines():
                    item = linea.lstrip('- ').strip()
                    html += f'<li>{item}</li>'
                html += '</ul>'
            elif bloque.startswith('<h2') or bloque.startswith('<h3'):
                html += bloque
            else:
                contenido = bloque.replace('\n', '<br>')
                html += f'<p>{contenido}</p>'
        return html       

    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"es\">
    <head>
      <meta charset=\"UTF-8\">
      <title>INFORME - SABE</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
          font-family:'Poppins',sans-serif;
          font-size:12pt;
          color:#2d3748;
          padding:20mm 25mm;
        }}
        .header {{ text-align:center; margin-bottom:12px; }}
        .header img {{
          width:150px;
          margin-bottom:20px;
        }}
        .header .org-subtitle {{
          font-size:10pt; font-weight:600; color:#027155;
          text-transform:uppercase; letter-spacing:1px;
        }}
        .header .report-title {{
          font-size:18pt; font-weight:600; color:#1a202c;
          margin-top:8px;
        }}
        .header .report-date {{
          font-size:9pt; color:#718096; margin-top:4px;
        }}
        .header .divider {{
          position: relative;
          height: 4px;
          width: 90%;
          background-color: #027155;
          margin: 12px auto 20px;
        }}
        .header .divider::before {{
          content: '';
          position: absolute;
          left: 0; top: 0;
          width: 15%;
          height: 100%;
          background-color: #00f7b9;
        }}
        .section-title {{
          font-size:14pt; font-weight:600; color:#027155;
          margin:20px 0 10px; border-bottom:1px solid #e2e8f0;
          padding-bottom:4px;
        }}
        .section-subtitle {{
          font-size:12pt; font-weight:500; color:#027155;
          margin:12px 0 6px;
        }}
        p {{ margin-bottom:12px; text-align:justify; line-height:1.6; }}
        strong {{ color:#004030; }}
        ul {{
          margin:8px 0 16px 20px;
          list-style: disc;
        }}
        ul li {{ margin-bottom:6px; }}

        .grafico-img {{
          margin: 20px auto;
          text-align: center;
        }}
        .grafico-img img {{
          max-width: 650px;
          max-height: 400px;
          border: 1px solid #ccc;
        }}
        .titulo-figura {{
          font-size: 12pt;
          color: #027155;
          font-weight: 600;
          text-align: left;
          margin-bottom: 8px;
        }}
        .titulo-figura em {{
          font-weight: normal;
          color: #000000;
          font-style: italic;
        }}
        .nota-figura {{
          font-size: 10pt;
          color: #2d3748;
          text-align: left;
          margin-top: 6px;
        }}

        .document-footer {{
          margin-top:30px; text-align:center;
          font-size:9pt; color:#718096;
          border-top:1px solid #e2e8f0; padding-top:8px;
        }}
        .footer-note {{
          font-size:7pt; color:#718096; margin-top:6px;
        }}
      </style>

    </head>
    <body>
      <div class="header">
        <img src="data:image/png;base64,{logo_b64}" alt="Logo SABE">
        <div class="org-subtitle">Sistema de Asignación de Becas Educativas</div>
        <div class="report-title">Informe de Asignación de Becas</div>
        <div class="report-date">Generado el {fecha_actual}</div>
        <div class="divider"></div>
      </div>
      {procesar_contenido(texto)}
      {generar_html_graficos(imagenes_base64, fecha_actual)}
      <div class="document-footer">
        Sistema de Asignación de Becas Educativas (SABE) – {fecha_actual}
        <div class="footer-note">
          Informe generado con IA de Google Gemini AI. El contenido puede estar sujeto a errores.
        </div>
      </div>
    </body>
    </html>
    """

    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': None
    }

    config = pdfkit.configuration(
        wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    )
    pdf_bytes = pdfkit.from_string(html_content, False, options=options, configuration=config)

    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=INFORME_SABE_{uuid.uuid4().hex[:8]}.pdf'
    response.headers['Cache-Control'] = 'no-cache'
    return response
