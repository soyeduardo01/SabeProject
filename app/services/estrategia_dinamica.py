# app/services/estrategia_dinamica.py

from app.interfaces.estrategia_interface import IEstrategiaSeleccion
from app.models.postulante_model import Postulante
from typing import List

class EstrategiaDinamica(IEstrategiaSeleccion):
    """
    Implementación de una estrategia de selección usando Programación Dinámica (tipo mochila 0/1).
    Prioriza postulantes con mayor prioridad sin exceder el presupuesto.
    """

    def seleccionar_postulantes(self, postulantes: List[Postulante], presupuesto: float) -> dict:
        n = len(postulantes)
        presupuesto_entero = int(presupuesto)

        pesos = [int(p.monto_requerido) for p in postulantes]
        valores = [p.prioridad for p in postulantes]

        dp = [[0] * (presupuesto_entero + 1) for _ in range(n + 1)]

        # Construcción de la tabla de DP
        for i in range(1, n + 1):
            for w in range(presupuesto_entero + 1):
                if pesos[i - 1] <= w:
                    dp[i][w] = max(
                        valores[i - 1] + dp[i - 1][w - pesos[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]

        # Reconstrucción del subconjunto óptimo
        w = presupuesto_entero
        seleccionados = []
        no_seleccionados = []

        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                seleccionados.append(postulantes[i - 1])
                w -= pesos[i - 1]
            else:
                no_seleccionados.append(postulantes[i - 1])

        return {
            "seleccionados": seleccionados[::-1],
            "no_seleccionados": no_seleccionados[::-1],
            "presupuesto_sobrante": w
        }
