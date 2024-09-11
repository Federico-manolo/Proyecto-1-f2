from abc import ABC, abstractmethod
import numpy as np

class ICalculadorCampo(ABC):
    @abstractmethod
    def calcular_campo(self, punto, cargas):
        pass

class CalculadorCampoElectrico(ICalculadorCampo):
    def __init__(self, k=8.99e9):
        self.k = k

    def calcular_campo(self, punto, cargas):
        E_total = np.zeros(2)
        for carga in cargas:
            r = punto - carga.obtener_posicion()
            r_magnitud = np.linalg.norm(r)
            if r_magnitud < 1e-10:
                continue
            E = self.k * carga.obtener_valor() * r / r_magnitud**3
            E_total += E
        return E_total