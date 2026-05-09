# tkinter: Librería estándar de Python para crear interfaces gráficas de usuario (ventanas, botones, etiquetas).
# pandas: Librería especializada en la manipulación y análisis de estructuras de datos, ideal para leer y filtrar archivos CSV.
# matplotlib.pyplot: Librería para la generación de gráficos estadísticos (en este caso, gráficos de barras).
# FigureCanvasTkAgg: Módulo de integración que permite incrustar figuras de matplotlib dentro de ventanas de tkinter.
# messagebox: Submódulo de tkinter utilizado para mostrar cuadros de diálogo emergentes (advertencias, confirmaciones, errores).
# filedialog: Submódulo de tkinter que proporciona cuadros de diálogo para abrir o guardar archivos en el sistema operativo.

import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class AppINIFED:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis INIFED 2020-2022")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        
        # Variables para almacenar los datos procesados
        self.datos_procesados = False
        self.internet_rural = 0
        self.internet_urbano = 0
        self.bebedero_rural = 0
        self.bebedero_urbano = 0
        
        # Iniciar con la pantalla de bienvenida
        self.pantalla_bienvenida()

    def pantalla_bienvenida(self):
        """Muestra la pantalla de carga con color rojo vino y letras negras."""
        self.frame_bienvenida = tk.Frame(self.root, bg="#722F37") # Color rojo vino
        self.frame_bienvenida.pack(fill=tk.BOTH, expand=True)
        
        lbl_texto = tk.Label(
            self.frame_bienvenida, 
            text="¡Bienvenido! Por favor espere... ", 
            bg="#722F37", 
            fg="black", 
            font=("Arial", 20, "bold")
        )
        lbl_texto.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Simular el tiempo de carga del CSV (3 segundos)
        self.root.after(3000, self.cargar_datos)
