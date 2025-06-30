# app/services/grafico_data_service.py

from collections import Counter, defaultdict
from typing import List, Dict
from app.models.postulante_model import Postulante

class GraficoDataService:
    """
    Servicio que genera estructuras estadísticas a partir de una lista de objetos Postulante.
    """

    def __init__(self, seleccionados: List[Postulante], presupuesto: float, inversion: float, restante: float):
        self.seleccionados = seleccionados
        self.presupuesto = presupuesto
        self.inversion = inversion
        self.restante = restante
        

    def por_provincia(self) -> Dict[str, int]:
        return dict(Counter(p.provincia for p in self.seleccionados if p.provincia))

    def por_genero(self) -> Dict[str, int]:
        return dict(Counter(p.genero for p in self.seleccionados if p.genero))

    def nivel_vs_tipo(self) -> Dict[str, Dict[str, int]]:
        datos = defaultdict(lambda: defaultdict(int))
        for p in self.seleccionados:
            if p.tipo_institucion and p.nivel_socioeconomico:
                datos[p.tipo_institucion][p.nivel_socioeconomico] += 1
        return datos

    def por_rango_edad(self) -> Dict[str, int]:
        rangos = {"18-25": 0, "26-30": 0, "31-40": 0, "41+": 0}
        for p in self.seleccionados:
            edad = p.edad
            if 18 <= edad <= 25:
                rangos["18-25"] += 1
            elif 26 <= edad <= 30:
                rangos["26-30"] += 1
            elif 31 <= edad <= 40:
                rangos["31-40"] += 1
            elif edad > 40:
                rangos["41+"] += 1
        return rangos

    def por_rango_indice(self) -> Dict[str, int]:
        rangos = {"80-85": 0, "86-90": 0, "91-95": 0, "96-100": 0}
        for p in self.seleccionados:
            indice = p.indice
            if 80 <= indice <= 85:
                rangos["80-85"] += 1
            elif 86 <= indice <= 90:
                rangos["86-90"] += 1
            elif 91 <= indice <= 95:
                rangos["91-95"] += 1
            elif 96 <= indice <= 100:
                rangos["96-100"] += 1
        return rangos

    def resumen_presupuesto(self) -> Dict[str, float]:
        return {
            "Presupuesto total": self.presupuesto,
            "Monto invertido": self.inversion,
            "Presupuesto sobrante": self.restante
        }

    def obtener_todos(self) -> Dict[str, Dict]:
        """
        Devuelve todos los datos listos para ser convertidos en gráficos.
        """
        
        return {
            "provincia": self.por_provincia(),
            "genero": self.por_genero(),
            "nivel_tipo": self.nivel_vs_tipo(),
            "edad": self.por_rango_edad(),
            "indice": self.por_rango_indice(),
            "presupuesto": self.resumen_presupuesto()
        }
