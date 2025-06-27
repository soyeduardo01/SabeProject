from app.ia.generador_reporte_ia import generar_texto_reporte
from app.ia.generador_pdf import generar_pdf

class GeneradorReporteService:
    def generar_reporte(self, seleccionados, no_seleccionados, presupuesto, restante, inversion, filtros):
        texto = generar_texto_reporte(seleccionados, no_seleccionados, presupuesto, restante, inversion, filtros)
        return generar_pdf(texto)


