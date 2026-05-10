# tkinter: Librería estándar de Python para crear interfaces gráficas de usuario.
# pandas: Librería para leer y manipular archivos CSV.
# matplotlib.pyplot: Librería para generar gráficos estadísticos.
# matplotlib.animation: Módulo para crear animaciones dinámicas en los gráficos.
# FigureCanvasTkAgg: Módulo para incrustar gráficos de matplotlib dentro de ventanas de tkinter.
# messagebox: Submódulo para mostrar cuadros de diálogo emergentes (advertencias, errores).
# filedialog: Submódulo para abrir exploradores de archivos y guardar/exportar elementos.
# urllib.request: Librería para descargar archivos desde internet (el icono).
# io: Librería para manejar flujos de datos binarios en memoria.
# PIL.Image y PIL.ImageTk: Librería Pillow para procesar imágenes y convertirlas a formatos compatibles con Tkinter.

import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import urllib.request
import io
from PIL import Image, ImageTk

class AppINIFED:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis INIFED 2020-2022")
        self.root.geometry("1050x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F2F5") 
        
        self.datos_procesados = False
        self.internet_rural = 0
        self.internet_urbano = 0
        self.bebedero_rural = 0
        self.bebedero_urbano = 0
        
        self.figuras_activas = []
        self.anims_activas = []
        
        self.cargar_icono_desde_url()
        self.pantalla_bienvenida()
     def cargar_icono_desde_url(self):
        url_imagen = "https://z-cdn-media.chatglm.cn/files/4da1d2cd-d4cb-47a7-9d7b-ccf1eed79a6b.jpg?auth_key=1878435784-6719940e8477484f826e2e0a48557a3b-0-a1077fa7c662ab264ec13026728ebb00"
        try:
            with urllib.request.urlopen(url_imagen) as response:
                datos_imagen = response.read()
            imagen = Image.open(io.BytesIO(datos_imagen))
            imagen = imagen.resize((64, 64), Image.Resampling.LANCZOS)
            icono_tk = ImageTk.PhotoImage(imagen)
            self.root.iconphoto(False, icono_tk)
            self.icono_referencia = icono_tk
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")
     def pantalla_bienvenida(self):
        color_fondo = "#102A43"
        self.frame_bienvenida = tk.Frame(self.root, bg=color_fondo) 
        self.frame_bienvenida.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        frame_sombra = tk.Frame(self.frame_bienvenida, bg="#0A1929", padx=6, pady=6)
        frame_sombra.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        frame_card = tk.Frame(frame_sombra, bg="#FFFFFF", padx=80, pady=50)
        frame_card.pack()
        
        lbl_icono = tk.Label(frame_card, text="📈", bg="#FFFFFF", font=("Segoe UI", 70))
        lbl_icono.pack()
        lbl_texto = tk.Label(frame_card, text="INIFED", bg="#FFFFFF", fg=color_fondo, font=("Segoe UI", 38, "bold"))
        lbl_texto.pack(pady=(15, 0))
        lbl_sub = tk.Label(frame_card, text="Análisis de Infraestructura Educativa", bg="#FFFFFF", fg="#546E7A", font=("Segoe UI", 12))
        lbl_sub.pack(pady=(0, 30))
        lbl_status = tk.Label(frame_card, text="Cargando módulos, por favor espere...", bg="#FFFFFF", fg="#90A4AE", font=("Segoe UI", 10))
        lbl_status.pack(pady=(0, 25))
        
        progress_bg = tk.Frame(frame_card, bg="#ECEFF1", padx=3, pady=3)
        progress_bg.pack()
        self.progress_container = tk.Frame(progress_bg, bg="#ECEFF1", width=350, height=10)
        self.progress_container.pack_propagate(False)
        self.progress_container.pack()
        self.barra_progreso = tk.Frame(self.progress_container, bg="#1565C0", width=0, height=10)
        self.barra_progreso.place(x=0, y=0, relheight=1.0, width=0)
        self.animar_carga(0)
