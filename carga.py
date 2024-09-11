import numpy as np
from abc import ABC, abstractmethod

class ICarga(ABC):
    @abstractmethod
    def obtener_posicion(self):
        pass

    @abstractmethod
    def obtener_valor(self):
        pass

class CargaPuntual(ICarga):
    def __init__(self, posicion, valor):
        self._posicion = np.array(posicion)
        self._valor = valor

    def obtener_posicion(self):
        return self._posicion.copy()

    def obtener_valor(self):
        return self._valor

    def __str__(self):
        return f"Carga en ({self._posicion[0]}, {self._posicion[1]}) con valor {self._valor} C"
