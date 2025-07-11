from app.interfaces.estrategia_interface import IEstrategiaSeleccion
from app.models.postulante_model import Postulante
from typing import List

class EstrategiaDinamica(IEstrategiaSeleccion):
    def seleccionar_postulantes(self, postulantes: List[Postulante], presupuesto: float) -> dict:
        # 100 = precisión de RD$1.00
        # Nota: Mientras menor sea la granularidad, tendrá mayor presición y tiempo de procesamiento.
        granularidad = 100  

        presupuesto_unidades = int(round(presupuesto * 100 / granularidad))
        pesos = [int(round(p.monto_requerido * 100 / granularidad)) for p in postulantes]
        valores = [p.prioridad for p in postulantes]
        n = len(postulantes)

        dp = [0] * (presupuesto_unidades + 1)
        keep = [[False] * (presupuesto_unidades + 1) for _ in range(n)]

        for i in range(n):
            peso = pesos[i]
            valor = valores[i]
            for w in range(presupuesto_unidades, peso - 1, -1):
                if dp[w - peso] + valor > dp[w]:
                    dp[w] = dp[w - peso] + valor
                    keep[i][w] = True

        # Reconstrucción
        w = presupuesto_unidades
        seleccionados = []
        no_seleccionados = []

        for i in range(n - 1, -1, -1):
            if keep[i][w]:
                seleccionados.append(postulantes[i])
                w -= pesos[i]
            else:
                no_seleccionados.append(postulantes[i])

        # Convertimos de vuelta a pesos con centavos
        presupuesto_sobrante = (w * granularidad) / 100.0
        presupuesto_invertido = presupuesto - presupuesto_sobrante


        return {
            "seleccionados": seleccionados[::-1],
            "no_seleccionados": no_seleccionados[::-1],
            "presupuesto_invertido": presupuesto_invertido,
            "presupuesto_sobrante": presupuesto_sobrante
        }
