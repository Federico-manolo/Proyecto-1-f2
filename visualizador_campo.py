# Importaciones necesarias
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Interfaz abstracta para el visualizador de campo
class IVisualizadorCampo(ABC):
    @abstractmethod
    def generar_grafico(self, ax, cargas, calculador):
        pass

# Implementación concreta del visualizador de campo eléctrico
class VisualizadorCampoElectrico(IVisualizadorCampo):
    def generar_grafico(self, ax, cargas, calculador_campo, calculador_potencial):
        # Limpiar el eje para un nuevo gráfico
        ax.clear()
        
        # Calcular los límites del gráfico basados en las posiciones de las cargas
        if cargas:
            posiciones = np.array([carga.obtener_posicion() for carga in cargas])
            min_x, min_y = np.min(posiciones, axis=0) - 0.5
            max_x, max_y = np.max(posiciones, axis=0) + 0.5
        else:
            # Si no hay cargas, usar un rango predeterminado
            min_x, min_y = -1, -1
            max_x, max_y = 1, 1

        # Crear una malla de puntos para calcular el campo eléctrico
        x = np.linspace(min_x, max_x, 20)
        y = np.linspace(min_y, max_y, 20)
        X, Y = np.meshgrid(x, y)

        # Inicializar matrices para almacenar las componentes del campo eléctrico
        Ex, Ey = np.zeros_like(X), np.zeros_like(Y)

        # Calcular el campo eléctrico en cada punto de la malla
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                punto = np.array([X[i,j], Y[i,j]])
                E = calculador_campo.calcular_campo(punto, cargas)
                Ex[i,j], Ey[i,j] = E

        # Normalizar el campo eléctrico para la visualización
        E_norm = np.sqrt(Ex**2 + Ey**2)
        Ex_norm, Ey_norm = Ex / E_norm, Ey / E_norm
        mask = E_norm != 0
        Ex_norm[mask], Ey_norm[mask] = Ex[mask] / E_norm[mask], Ey[mask] / E_norm[mask]

        # Dibujar las líneas de campo eléctrico
        ax.streamplot(X, Y, Ex_norm, Ey_norm, density=1.5, linewidth=1, arrowsize=1.5, color='b')

        # Calcular el potencial eléctrico
        V = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                punto = np.array([X[i,j], Y[i,j]])
                V[i,j] = calculador_potencial.calcular_campo(punto, cargas)

        # Dibujar las líneas equipotenciales sin etiquetas
        ax.contour(X, Y, V, levels=20, colors='r', linestyles='solid', linewidths=0.5)

        # Dibujar las cargas en el gráfico
        for carga in cargas:
            pos = carga.obtener_posicion()
            valor = carga.obtener_valor()
            color = 'r' if valor > 0 else 'g'  # Rojo para cargas positivas, verde para negativas
            ax.plot(pos[0], pos[1], 'o', color=color, markersize=10)

        # Configurar los límites y aspecto del gráfico
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal')
        ax.set_title('Campo Eléctrico y Líneas Equipotenciales')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
