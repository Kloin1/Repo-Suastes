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
    def animar_carga(self, paso):
        if paso <= 40:
            ancho = (paso / 40.0) * 350
            self.barra_progreso.place(x=0, y=0, relheight=1.0, width=ancho)
            self.root.after(80, self.animar_carga, paso + 1)
        else:
            self.inicializar_interfaz_principal()
    def inicializar_interfaz_principal(self):
        self.frame_bienvenida.destroy()
        self.root.columnconfigure(0, weight=0, minsize=260) 
        self.root.columnconfigure(1, weight=1)              
        self.root.rowconfigure(0, weight=1)                  

        self.frame_nav = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=25, highlightbackground="#E0E0E0", highlightthickness=1)
        self.frame_nav.grid(row=0, column=0, sticky="ns")
        
        lbl_logo = tk.Label(self.frame_nav, text="INIFED", bg="#FFFFFF", fg="#102A43", font=("Segoe UI", 20, "bold"))
        lbl_logo.pack(pady=(0, 30), anchor="w")
        
        color_azul = "#0D47A1"
        frame_panel_azul = tk.Frame(self.frame_nav, bg=color_azul, padx=15, pady=15)
        frame_panel_azul.pack(fill=tk.X, pady=(0, 15))
        lbl_t1 = tk.Label(frame_panel_azul, text="GRÁFICAS DE BARRAS", bg=color_azul, fg="#90CAF9", font=("Segoe UI", 9, "bold"))
        lbl_t1.pack(anchor="w", pady=(0, 10))
        
        estilo_sidebar = {"font": ("Segoe UI", 11), "height": 2, "bd": 0, "cursor": "hand2", "activeforeground": "white", "width": 22, "anchor": "w", "pady": 4, "padx": 10}
        color_gris = "#90A4AE"
        
        self.btn_internet = tk.Button(frame_panel_azul, text="📊  Internet (Barras)", bg=color_gris, fg="white", activebackground=color_gris, state=tk.DISABLED, command=lambda: self.mostrar_confirmacion("internet", "barra"), **estilo_sidebar)
        self.btn_internet.pack(fill=tk.X, pady=(0, 5))
        self.btn_bebedero = tk.Button(frame_panel_azul, text="💧  Bebedero (Barras)", bg=color_gris, fg="white", activebackground=color_gris, state=tk.DISABLED, command=lambda: self.mostrar_confirmacion("bebedero", "barra"), **estilo_sidebar)
        self.btn_bebedero.pack(fill=tk.X)

        color_rosa = "#AD1457"
        frame_panel_rosa = tk.Frame(self.frame_nav, bg=color_rosa, padx=15, pady=15)
        frame_panel_rosa.pack(fill=tk.X, pady=(0, 15))
        lbl_t2 = tk.Label(frame_panel_rosa, text="GRÁFICAS DE PASTEL", bg=color_rosa, fg="#F48FB1", font=("Segoe UI", 9, "bold"))
        lbl_t2.pack(anchor="w", pady=(0, 10))
        
        self.btn_pastel_internet = tk.Button(frame_panel_rosa, text="🥧  Internet (Pastel)", bg=color_gris, fg="white", activebackground=color_gris, state=tk.DISABLED, command=lambda: self.mostrar_confirmacion("internet", "pastel"), **estilo_sidebar)
        self.btn_pastel_internet.pack(fill=tk.X, pady=(0, 5))
        self.btn_pastel_bebedero = tk.Button(frame_panel_rosa, text="🥧  Bebedero (Pastel)", bg=color_gris, fg="white", activebackground=color_gris, state=tk.DISABLED, command=lambda: self.mostrar_confirmacion("bebedero", "pastel"), **estilo_sidebar)
        self.btn_pastel_bebedero.pack(fill=tk.X)

        # --- NUEVO BOTÓN COMPARADOR PERSONALIZADO ---
        self.btn_comparador = tk.Button(self.frame_nav, text="⚖️  Comparador (2)", bg="#5E35B1", fg="white", activebackground="#4527A0", state=tk.DISABLED, command=self.mostrar_vista_seleccion_comparador, **estilo_sidebar)
        self.btn_comparador.pack(fill=tk.X, pady=(0, 15))

        sep = tk.Frame(self.frame_nav, bg="#E0E0E0", height=1)
        sep.pack(fill=tk.X, pady=5)

        self.btn_cargar = tk.Button(self.frame_nav, text="📂  Cargar CSV", bg="#FF9800", fg="white", activebackground="#F57C00", command=self.cargar_csv_interactivo, **estilo_sidebar)
        self.btn_cargar.pack(fill=tk.X)

        self.btn_comparar = tk.Button(self.frame_nav, text="🔄  Comparar Todo (4)", bg="#37474F", fg="white", activebackground="#263238", state=tk.DISABLED, command=self.mostrar_confirmacion_comparar, **estilo_sidebar)
        self.btn_comparar.pack(side=tk.BOTTOM, fill=tk.X)

        self.frame_contenido_base = tk.Frame(self.root, bg="#F0F2F5")
        self.frame_contenido_base.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        self.frame_titulo_fijo = tk.Frame(self.frame_contenido_base, bg="#F0F2F5")
        self.frame_titulo_fijo.pack(side=tk.TOP, fill=tk.X, pady=(10, 5))
        
        lbl_titulo = tk.Label(self.frame_titulo_fijo, text="Análisis INIFED", bg="#F0F2F5", fg="#102A43", font=("Segoe UI", 28, "bold"))
        lbl_titulo.pack(anchor="w")
        lbl_subtitulo = tk.Label(self.frame_titulo_fijo, text="Estadísticas 2020 - 2022", bg="#F0F2F5", fg="#757575", font=("Segoe UI", 12))
        lbl_subtitulo.pack(anchor="w")

        self.panel_dinamico = tk.Frame(self.frame_contenido_base, bg="#F0F2F5")
        self.panel_dinamico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.mostrar_vista_menu()
    def cargar_csv_interactivo(self):
        archivo = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")])
        if archivo:
            try:
                df = pd.read_csv(archivo)
                self.internet_urbano = len(df[(df['ambito'] == 'URBANO') & (df['internet'] == 'CON INTERNET')])
                self.internet_rural = len(df[(df['ambito'] == 'RURAL') & (df['internet'] == 'CON INTERNET')])
                self.bebedero_urbano = len(df[(df['ambito'] == 'URBANO') & (df['bebederos'] == 'CON BEBEDERO')])
                self.bebedero_rural = len(df[(df['ambito'] == 'RURAL') & (df['bebederos'] == 'CON BEBEDERO')])
                self.datos_procesados = True
                
                self.btn_internet.configure(state=tk.NORMAL, bg="#1976D2", activebackground="#1565C0")
                self.btn_bebedero.configure(state=tk.NORMAL, bg="#00897B", activebackground="#00796B")
                self.btn_pastel_internet.configure(state=tk.NORMAL, bg="#D81B60", activebackground="#C2185B")
                self.btn_pastel_bebedero.configure(state=tk.NORMAL, bg="#8E24AA", activebackground="#7B1FA2")
                
                # Habilitar nuevas funciones
                self.btn_comparador.configure(state=tk.NORMAL, bg="#5E35B1", activebackground="#4527A0")
                self.btn_comparar.configure(state=tk.NORMAL, bg="#37474F", activebackground="#263238")
                
                self.mostrar_vista_menu()
                messagebox.showinfo("Éxito", "CSV cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error de lectura", f"No se pudo leer el archivo CSV.\n{str(e)}")
    def limpiar_panel_dinamico(self):
        for anim in self.anims_activas:
            try: anim.event_source.stop()
            except: pass
        self.anims_activas = []
        for fig in self.figuras_activas:
            plt.close(fig)
        self.figuras_activas = []
        if hasattr(self, 'panel_dinamico') and self.panel_dinamico:
            self.panel_dinamico.destroy()
        self.panel_dinamico = tk.Frame(self.frame_contenido_base, bg="#F0F2F5")
        self.panel_dinamico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    def mostrar_vista_seleccion_comparador(self):
        self.limpiar_panel_dinamico()
        
        frame_card = tk.Frame(self.panel_dinamico, bg="#FFFFFF", highlightbackground="#E0E0E0", highlightthickness=1, padx=40, pady=40)
        frame_card.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        
        lbl_titulo = tk.Label(frame_card, text="Comparador de Gráficas", bg="#FFFFFF", fg="#5E35B1", font=("Segoe UI", 24, "bold"))
        lbl_titulo.pack(pady=(0, 5))
        
        lbl_inst = tk.Label(frame_card, text="Selecciona exactamente 2 gráficas para comparar:", bg="#FFFFFF", fg="#757575", font=("Segoe UI", 12))
        lbl_inst.pack(pady=(0, 30))
        
        # Variables para los Checkbuttons
        self.var_barras_int = tk.IntVar()
        self.var_barras_beb = tk.IntVar()
        self.var_pastel_int = tk.IntVar()
        self.var_pastel_beb = tk.IntVar()
        
        # Guardamos las variables y widgets para la lógica de bloqueo
        self.opciones_check = [
            (self.var_barras_int, "📊 Barras: Internet"),
            (self.var_barras_beb, "💧 Barras: Bebedero"),
            (self.var_pastel_int, "🥧 Pastel: Internet"),
            (self.var_pastel_beb, "🥧 Pastel: Bebedero")
        ]
        
        self.checks_widgets = []
        frame_checks = tk.Frame(frame_card, bg="#FFFFFF")
        frame_checks.pack()
        
        for i, (var, texto) in enumerate(self.opciones_check):
            row, col = divmod(i, 2) # Grid de 2x2
            cb = tk.Checkbutton(frame_checks, text=texto, variable=var, bg="#FFFFFF", fg="#333333", selectcolor="#EDE7F6", font=("Segoe UI", 13), activebackground="#FFFFFF", command=self.controlar_limite_seleccion)
            cb.grid(row=row, column=col, padx=40, pady=15, sticky="w")
            self.checks_widgets.append((var, cb))
            
        self.btn_generar_comp = tk.Button(frame_card, text="Generar Comparación", bg="#5E35B1", fg="white", state=tk.DISABLED, font=("Segoe UI", 13, "bold"), bd=0, padx=20, pady=10, cursor="hand2", activebackground="#4527A0")
        self.btn_generar_comp.pack(pady=(30, 0))
    def controlar_limite_seleccion(self):
        """Bloquea las casillas no seleccionadas cuando ya hay 2 elegidas."""
        seleccionadas = sum(var.get() for var, cb in self.checks_widgets)
        
        if seleccionadas == 2:
            # Habilitar solo la que está marcada, deshabilitar las demás
            for var, cb in self.checks_widgets:
                cb.configure(state=tk.NORMAL if var.get() == 1 else tk.DISABLED)
            self.btn_generar_comp.configure(state=tk.NORMAL, command=self.ejecutar_comparacion_personalizada)
        else:
            # Si hay 0 o 1, habilitar todas y botón deshabilitado
            for var, cb in self.checks_widgets:
                cb.configure(state=tk.NORMAL)
            self.btn_generar_comp.configure(state=tk.DISABLED)
    def ejecutar_comparacion_personalizada(self):
        """Obtiene las 2 gráficas seleccionadas y las manda a dibujar."""
        mapeo = [
            (self.var_barras_int, "internet", "barra"),
            (self.var_barras_beb, "bebedero", "barra"),
            (self.var_pastel_int, "internet", "pastel"),
            (self.var_pastel_beb, "bebedero", "pastel")
        ]
        
        seleccionadas = [(tipo, estilo) for var, tipo, estilo in mapeo if var.get() == 1]
        
        if len(seleccionadas) == 2:
            self.mostrar_vista_comparacion_personalizada(seleccionadas)
    def mostrar_vista_comparacion_personalizada(self, seleccionadas):
        """Dibuja 2 gráficas en paralelo (1 fila, 2 columnas) y agrega el footer."""
        self.limpiar_panel_dinamico()
        # Reutilizamos el footer pasando True para que aparezca "Dejar de comparar"
        self.agregar_footer(es_comparacion=True)
        
        frame_grid = tk.Frame(self.panel_dinamico, bg="#F0F2F5")
        frame_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        frame_grid.columnconfigure(0, weight=1)
        frame_grid.columnconfigure(1, weight=1)
        frame_grid.rowconfigure(0, weight=1)
        
        for i, (tipo, estilo) in enumerate(seleccionadas):
            card = tk.Frame(frame_grid, bg="#FFFFFF", highlightbackground="#E0E0E0", highlightthickness=1)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            if estilo == "barra":
                self.crear_grafica_barras(card, tipo)
            else:
                self.crear_grafica_pastel(card, tipo)
    def mostrar_vista_menu(self):
        self.limpiar_panel_dinamico()
        frame_centro = tk.Frame(self.panel_dinamico, bg="#FFFFFF", highlightbackground="#E0E0E0", highlightthickness=1)
        frame_centro.place(relx=0.5, rely=0.4, anchor=tk.CENTER, width=500, height=200)
        
        if not self.datos_procesados:
            lbl_aviso = tk.Label(frame_centro, text="No hay datos disponibles.\nUsa 'Cargar CSV' para comenzar.", bg="#FFFFFF", fg="#757575", font=("Segoe UI", 12), justify=tk.CENTER)
        else:
            lbl_aviso = tk.Label(frame_centro, text="✅ Datos listos\nSelecciona una opción en el menú lateral", bg="#FFFFFF", fg="#2E7D32", font=("Segoe UI", 13, "bold"), justify=tk.CENTER)
        lbl_aviso.pack(expand=True)
        btn_salir = tk.Button(frame_centro, text="🚪  Salir de la aplicación", font=("Segoe UI", 11, "bold"), bg="#E53935", fg="white", bd=0, cursor="hand2", activebackground="#C62828", activeforeground="white", command=self.confirmar_salida, width=25, pady=5)
        btn_salir.pack(pady=(0, 20))
    def confirmar_salida(self):
        if messagebox.askyesno("Confirmar Salida", "¿Está seguro de que desea cerrar la aplicación?", icon=messagebox.WARNING):
            self.root.destroy()
    def mostrar_confirmacion(self, tipo, estilo_grafica):
        if not self.datos_procesados:
            messagebox.showwarning("Sin Datos", "no hay csv disponible, carga tu csv para que se muestren las graficas")
            return
        titulo = f"{estilo_grafica.capitalize()} de {tipo.capitalize()}"
        if messagebox.askyesno("Confirmación", f"¿Desea generar: {titulo}?", icon=messagebox.QUESTION):
            self.mostrar_vista_individual(tipo, estilo_grafica)

