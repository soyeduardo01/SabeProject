# app/interfaces/estrategia_interfaces.py

from abc import ABC, abstractmethod
from typing import List
from app.models.postulante_model import Postulante

class IEstrategiaSeleccion(ABC):
    """
    Interfaz para definir la estrategia de selección de postulantes.
    Permite implementar diferentes algoritmos (programación dinámica, voraz, etc.)
    respetando el principio de inversión de dependencias (D - SOLID).
    """

    @abstractmethod
    def seleccionar_postulantes(self, postulantes: List[Postulante], presupuesto: float) -> dict:
        pass
