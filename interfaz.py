# Importaciones necesarias
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from carga import CargaPuntual
from calculador_campo import ICalculadorCampo
from calculador_potencial import ICalculadorPotencial
from visualizador_campo import IVisualizadorCampo
from gestor_cargas import IGestorCargas

# Clase para el marco de entrada de cargas
class FrameEntradaCarga(ttk.LabelFrame):
    def __init__(self, parent, gestor_cargas, aplicacion_principal):
        super().__init__(parent, text="Agregar Carga", padding="10")
        self.gestor_cargas = gestor_cargas
        self.aplicacion_principal = aplicacion_principal
        self.crear_widgets()

    # Método para crear los widgets del marco de entrada
    def crear_widgets(self):
        # Creación de etiquetas y campos de entrada para posición X, Y y carga
        ttk.Label(self, text="Posición X:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_x = ttk.Entry(self, width=10)
        self.entrada_x.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self, text="Posición Y:").grid(row=1, column=0, sticky=tk.W)
        self.entrada_y = ttk.Entry(self, width=10)
        self.entrada_y.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(self, text="Carga (C):").grid(row=2, column=0, sticky=tk.W)
        self.entrada_carga = ttk.Entry(self, width=10)
        self.entrada_carga.grid(row=2, column=1, padx=5, pady=2)

        # Botones para agregar carga y quitar todas las cargas
        self.boton_agregar = ttk.Button(self, text="Agregar Carga", command=self.agregar_carga)
        self.boton_agregar.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.boton_quitar = ttk.Button(self, text="Quitar Cargas", command=self.quitar_cargas)
        self.boton_quitar.grid(row=4, column=0, columnspan=2, pady=10)

    # Método para agregar una nueva carga
    def agregar_carga(self):
        try:
            x = float(self.entrada_x.get())
            y = float(self.entrada_y.get())
            carga = float(self.entrada_carga.get())
            nueva_carga = CargaPuntual([x, y], carga)
            self.aplicacion_principal.agregar_carga(nueva_carga)
            self.limpiar_entradas()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
    
    # Método para quitar todas las cargas
    def quitar_cargas(self):
        self.aplicacion_principal.quitar_cargas()

    # Método para limpiar los campos de entrada
    def limpiar_entradas(self):
        self.entrada_x.delete(0, tk.END)
        self.entrada_y.delete(0, tk.END)
        self.entrada_carga.delete(0, tk.END)

# Clase para el marco de lista de cargas
class FrameListaCargas(ttk.LabelFrame):
    def __init__(self, parent, gestor_cargas):
        super().__init__(parent, text="Cargas Agregadas", padding="10")
        self.gestor_cargas = gestor_cargas
        self.lista_cargas = tk.Listbox(self, height=6)
        self.lista_cargas.pack(fill=tk.BOTH, expand=True)

    # Método para actualizar la lista de cargas mostrada
    def actualizar_lista(self):
        self.lista_cargas.delete(0, tk.END)
        for carga in self.gestor_cargas.obtener_cargas():
            self.lista_cargas.insert(tk.END, str(carga))

# Clase para el marco de cálculo de campo eléctrico
class FrameCalculoCampo(ttk.LabelFrame):
    def __init__(self, parent, calculador_campo, gestor_cargas):
        super().__init__(parent, text="Calcular Campo Eléctrico", padding="10")
        self.calculador_campo = calculador_campo
        self.gestor_cargas = gestor_cargas
        self.crear_widgets()

    # Método para crear los widgets del marco de cálculo
    def crear_widgets(self):
        ttk.Label(self, text="Punto X:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_punto_x = ttk.Entry(self, width=10)
        self.entrada_punto_x.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self, text="Punto Y:").grid(row=1, column=0, sticky=tk.W)
        self.entrada_punto_y = ttk.Entry(self, width=10)
        self.entrada_punto_y.grid(row=1, column=1, padx=5, pady=2)

        self.boton_calcular = ttk.Button(self, text="Calcular Campo Eléctrico", command=self.calcular_campo)
        self.boton_calcular.grid(row=2, column=0, columnspan=2, pady=10)

    # Método para calcular el campo eléctrico en un punto dado
    def calcular_campo(self):
        try:
            punto_x = float(self.entrada_punto_x.get())
            punto_y = float(self.entrada_punto_y.get())
            punto = np.array([punto_x, punto_y])
            cargas = self.gestor_cargas.obtener_cargas()
            if len(cargas) < 3:
                messagebox.showerror("Error", "Debe ingresar al menos 3 cargas.")
                return
            campo = self.calculador_campo.calcular_campo(punto, cargas)
            messagebox.showinfo("Resultado", f"El campo eléctrico en el punto ({punto[0]}, {punto[1]}) es:\n{campo} N/C")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para el punto.")

# Clase para el marco del gráfico de campo eléctrico
class FrameGrafico(ttk.LabelFrame):
    def __init__(self, parent, visualizador_campo, calculador_campo, calculador_potencial, gestor_cargas):
        super().__init__(parent, text="Gráfico de Campo y Potencial Eléctrico", padding="10")
        self.visualizador_campo = visualizador_campo
        self.calculador_campo = calculador_campo
        self.calculador_potencial = calculador_potencial
        self.gestor_cargas = gestor_cargas
        self.crear_widgets()

    # Método para crear los widgets del marco del gráfico
    def crear_widgets(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.boton_grafico = ttk.Button(self, text="Generar Gráfico", command=self.generar_grafico)
        self.boton_grafico.pack(pady=10)

    # Método para generar el gráfico del campo eléctrico
    def generar_grafico(self):
        cargas = self.gestor_cargas.obtener_cargas()
        if len(cargas) < 3:
            messagebox.showerror("Error", "Debe ingresar al menos 3 cargas.")
            return
        self.visualizador_campo.generar_grafico(self.ax, cargas, self.calculador_campo, self.calculador_potencial)
        self.canvas.draw()
    
    # Método para quitar el gráfico actual
    def quitar_grafico(self):
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_aspect('equal')
        self.ax.set_title('Campo Eléctrico')
        self.canvas.draw()

# Clase principal de la aplicación
class AplicacionCampoElectrico:
    def __init__(self, master, calculador_campo, calculador_potencial, visualizador_campo, gestor_cargas):
        self.master = master
        self.calculador_campo = calculador_campo
        self.calculador_potencial = calculador_potencial
        self.visualizador_campo = visualizador_campo
        self.gestor_cargas = gestor_cargas
        
        # Configuración de la ventana principal
        master.title("Calculadora de Campo Eléctrico")
        master.geometry("1000x600")
        master.configure(bg='#f0f0f0')
        
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Creación del marco principal
        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuración de las columnas y filas del marco principal
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Creación de los diferentes marcos de la aplicación
        self.frame_entrada = FrameEntradaCarga(main_frame, self.gestor_cargas, self)
        self.frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_lista = FrameListaCargas(main_frame, self.gestor_cargas)
        self.frame_lista.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_calculo = FrameCalculoCampo(main_frame, self.calculador_campo, self.gestor_cargas)
        self.frame_calculo.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_grafico = FrameGrafico(main_frame, self.visualizador_campo, self.calculador_campo, self.calculador_potencial, self.gestor_cargas)
        self.frame_grafico.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

    # Método para actualizar la interfaz
    def actualizar_interfaz(self):
        self.frame_lista.actualizar_lista()

    # Método para agregar una nueva carga
    def agregar_carga(self, nueva_carga):
        self.gestor_cargas.agregar_carga(nueva_carga)
        self.actualizar_interfaz()
    
    # Método para quitar todas las cargas
    def quitar_cargas(self):
        self.gestor_cargas.quitar_cargas()
        self.frame_grafico.quitar_grafico()
        self.actualizar_interfaz()
