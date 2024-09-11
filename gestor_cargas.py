from abc import ABC, abstractmethod

class IGestorCargas(ABC):
    @abstractmethod
    def agregar_carga(self, carga):
        pass

    @abstractmethod
    def obtener_cargas(self):
        pass
    
    @abstractmethod
    def quitar_cargas(self):
        pass

class GestorCargas(IGestorCargas):
    def __init__(self):
        self._cargas = []

    def agregar_carga(self, carga):
        self._cargas.append(carga)

    def obtener_cargas(self):
        return self._cargas.copy()
    
    def quitar_cargas(self):
        self._cargas = []

