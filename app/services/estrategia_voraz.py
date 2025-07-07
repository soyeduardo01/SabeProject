from app.interfaces.estrategia_interface import IEstrategiaSeleccion
from app.models.postulante_model import Postulante
from typing import List

class EstrategiaVoraz(IEstrategiaSeleccion):
    def seleccionar_postulantes(self, postulantes: List[Postulante], presupuesto: float) -> dict:
        # Ordenar por prioridad por peso (mayor eficiencia primero)
        postulantes_ordenados = sorted(
            postulantes,
            key=lambda p: p.prioridad / p.monto_requerido if p.monto_requerido != 0 else 0,
            reverse=True
        )

        seleccionados = []
        no_seleccionados = []
        presupuesto_restante = presupuesto

        for p in postulantes_ordenados:
            if p.monto_requerido <= presupuesto_restante:
                seleccionados.append(p)
                presupuesto_restante -= p.monto_requerido
            else:
                no_seleccionados.append(p)

        presupuesto_invertido = presupuesto - presupuesto_restante

        return {
            "seleccionados": seleccionados,
            "no_seleccionados": no_seleccionados,
            "presupuesto_invertido": presupuesto_invertido,
            "presupuesto_sobrante": presupuesto_restante
        }