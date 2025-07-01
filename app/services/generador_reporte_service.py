from typing import List
from app.ia.generador_reporte_ia import generar_texto_reporte
from app.ia.generador_pdf import generar_pdf
from app.models.postulante_model import Postulante
from app.services.grafico_data_service import GraficoDataService
from app.utils.chart_generator import guardar_datos_graficos, generar_graficos_base64


class GeneradorReporteService:
    """
    Servicio principal que coordina la generación completa del reporte:
    - Generación de texto con IA.
    - Extracción de datos estadísticos.
    - Creación del PDF con anexos gráficos.
    """

    def generar_reporte(
        self,
        seleccionados: List[Postulante],
        no_seleccionados: List[Postulante],
        presupuesto: float,
        restante: float,
        inversion: float,
        filtros: dict
    ) -> bytes:
        """
        Genera el informe completo en PDF con texto, presupuesto y gráficos.

        :param seleccionados: Lista de postulantes seleccionados
        :param no_seleccionados: Lista de postulantes no seleccionados
        :param presupuesto: Monto total del presupuesto
        :param restante: Presupuesto restante
        :param inversion: Monto invertido
        :param filtros: Diccionario con los filtros aplicados
        :return: Contenido binario del PDF generado
        """
        # Paso 1: Generar el contenido textual con Gemini
        texto = generar_texto_reporte(
            seleccionados,
            no_seleccionados,
            presupuesto,
            restante,
            inversion,
            filtros
        )

        # Paso 2: Extraer datos para los gráficos
        grafico_data_service = GraficoDataService(
            seleccionados=seleccionados,
            presupuesto=presupuesto,
            inversion=inversion,
            restante=restante
        )
        datos_graficos = grafico_data_service.obtener_todos()

        # Paso 3: Guardar archivo JSON temporal
        ruta_json = guardar_datos_graficos(datos_graficos)

        # Paso 4: Generar imágenes base64 con Puppeteer
        imagenes_base64 = generar_graficos_base64(ruta_json)

        # Paso 5: Generar el PDF incluyendo texto y gráficos
        return generar_pdf(texto, ruta_json, imagenes_base64)
