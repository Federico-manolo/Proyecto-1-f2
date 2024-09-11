from abc import ABC, abstractmethod
import numpy as np

class ICalculadorPotencial(ABC):
    @abstractmethod
    def calcular_campo(self, punto, cargas):
        pass

class CalculadorPotencialElectrico(ICalculadorPotencial):
    def __init__(self, k=8.99e9):
        self.k = k

    def calcular_campo(self, punto, cargas):
        V_total = 0
        for carga in cargas:
            r = punto - carga.obtener_posicion()
            r_magnitud = np.linalg.norm(r)
            if r_magnitud < 1e-10:
                continue
            V = self.k * carga.obtener_valor() / r_magnitud
            V_total += V
        return V_total