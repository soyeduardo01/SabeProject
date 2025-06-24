# app/services/seleccion_services.py

from app.interfaces.estrategia_interface import IEstrategiaSeleccion
from app.models.postulante_model import Postulante
from typing import List

class SeleccionService:
    """
    Servicio que encapsula la lógica de negocio para aplicar filtros
    y seleccionar postulantes según una estrategia configurable.
    """

    def __init__(self, estrategia: IEstrategiaSeleccion):
        self.estrategia = estrategia

    def aplicar_filtros(self, postulantes: List[Postulante], filtros: dict) -> List[Postulante]:
        for p in postulantes:
            if filtros.get("provincia") and p.provincia == filtros["provincia"]:
                p.prioridad += 1
            if filtros.get("genero") and p.genero == filtros["genero"]:
                p.prioridad += 1
            if filtros.get("nivel_socioeconomico") and p.nivel_socioeconomico == filtros["nivel_socioeconomico"]:
                p.prioridad += 1
            if filtros.get("discapacidad") and p.discapacidad == filtros["discapacidad"]:
                p.prioridad += 1
            if filtros.get("tipo_institucion") and p.tipo_institucion == filtros["tipo_institucion"]:
                p.prioridad += 1
            if filtros.get("ocupacion") and p.ocupacion == filtros["ocupacion"]:
                p.prioridad += 1
            if filtros.get("edad_min") is not None and filtros.get("edad_max") is not None:
                if filtros["edad_min"] <= p.edad <= filtros["edad_max"]:
                    p.prioridad += 1
            if filtros.get("indice_min") is not None and filtros.get("indice_max") is not None:
                if filtros["indice_min"] <= p.indice <= filtros["indice_max"]:
                    p.prioridad += 1
        return postulantes

    def seleccionar_postulantes(self, postulantes: List[Postulante], filtros: dict, presupuesto: float) -> dict:
        postulantes_filtrados = self.aplicar_filtros(postulantes, filtros)
        return self.estrategia.seleccionar_postulantes(postulantes_filtrados, presupuesto)
