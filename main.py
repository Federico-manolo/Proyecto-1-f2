# Importaciones necesarias
import tkinter as tk
from interfaz import AplicacionCampoElectrico
from calculador_campo import CalculadorCampoElectrico
from visualizador_campo import VisualizadorCampoElectrico
from gestor_cargas import GestorCargas
from calculador_potencial import CalculadorPotencialElectrico

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    
    # Inicializar componentes principales
    calculador_campo = CalculadorCampoElectrico()
    visualizador_campo = VisualizadorCampoElectrico()
    gestor_cargas = GestorCargas()
    calculador_potencial = CalculadorPotencialElectrico()
    
    # Crear y ejecutar la aplicación
    app = AplicacionCampoElectrico(root, calculador_campo, calculador_potencial, visualizador_campo, gestor_cargas)
    root.mainloop()