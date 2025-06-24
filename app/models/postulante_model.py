# app/models/postulante_model.py

class Postulante:
    """
    Modelo que representa a un postulante a beca.
    Encapsula toda su información relevante y se usa a lo largo del sistema.
    """

    def __init__(self, nombre, genero, nivel_socioeconomico, ocupacion, indice, monto_requerido,
                 edad, provincia, discapacidad, tipo_institucion):
        self.nombre = nombre
        self.genero = genero
        self.nivel_socioeconomico = nivel_socioeconomico
        self.ocupacion = ocupacion
        self.indice = float(indice)
        self.monto_requerido = float(monto_requerido)
        self.edad = int(edad)
        self.provincia = provincia
        self.discapacidad = discapacidad
        self.tipo_institucion = tipo_institucion
        self.prioridad = 0  # Se calculará según filtros aplicados

    def to_dict(self):
        """
        Convierte el objeto Postulante a un diccionario para facilitar su serialización.
        """
        return {
            "nombre": self.nombre,
            "genero": self.genero,
            "nivel_socioeconomico": self.nivel_socioeconomico,
            "ocupacion": self.ocupacion,
            "indice": self.indice,
            "monto_requerido": f"RD${self.monto_requerido:,.0f}",
            "edad": self.edad,
            "provincia": self.provincia,
            "discapacidad": self.discapacidad,
            "tipo_institucion": self.tipo_institucion,
            "prioridad": self.prioridad
        }
