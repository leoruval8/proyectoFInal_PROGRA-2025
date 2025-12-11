import random
from time import sleep
import tkinter as tk
from tkinter import messagebox

anchoCanvas = 420
altoCanvas = 300
palabras = ["leonel", "koala", "programacion", "python", "ahorcado"]

palabraSecreta = ""
palabraProgreso = []
vidas = 0
letrasAdivinadas = set()


def seleccionar_palabra(): 
    """Seleccionar una palabra al azar de la lista."""
    global palabraSecreta
    palabraSecreta = random.choice(palabras)

def inicializar_juego(): 
    """
    Reinicia el estado del juego (palabra, vidas, progreso).
    """
    global vidas, palabraProgreso, letrasAdivinadas

    seleccionar_palabra()
    vidas = 6  
    palabraProgreso = ["_"] * len(palabraSecreta)
    letrasAdivinadas = set()

    actualizar_interfaz()
    dibujar_ahorcado()
    etiquetaEstado.config(text="Adivina la palabra secreta")
    botonIntentar.config(state=tk.NORMAL) # Habilita el botón de intento
    entradaLetra.config(state=tk.NORMAL) # Habilita la entrada
    entradaLetra.delete(0, tk.END) # Limpia la entrada

def actualizar_interfaz():
    """
    Actualiza las etiquetas y el progreso de la palabra en la interfaz
    """
    etiquetaProgreso.config(text=" ".join(palabraProgreso))
    etiquetaLetrasIntentadas.config(text=f"Letras probadas: {", ".join(sorted(list(letrasAdivinadas)))}")

def dibujar_ahorcado():
    """
    Dibuja el ahorcado en el lienzo del canvas
    """
    lienzo.delete("all") #"all", le estás indicando al Canvas que borre absolutamente todos los elementos dibujados.

    # Base
    lienzo.create_line(50, altoCanvas - 20, 150, altoCanvas - 20, width=3) #Base del poste
    lienzo.create_line(100, altoCanvas - 20, 100, 30, width=3) #Poste del ahorcado
    lienzo.create_line(100, 30, 250, 30, width=3) #Poste horizontal
    lienzo.create_line(250, 30, 250, 60, width=3) #Cuerda
    
    #Dibujar monito
    if vidas <= 5: #Cabeza
        lienzo.create_oval(230, 60, 270, 100, width=2)
    if vidas <= 4: #Cuerpo
        lienzo.create_line(250, 100, 250, 180, width=2)
    if vidas <= 3: #brazo derecho
        lienzo.create_line(250, 120, 280, 160, width=2)
    if vidas <= 2: #Brazo izquierdo
        lienzo.create_line(250, 120, 220, 160, width=2)
    if vidas <= 1: #Pierna derecha 
        lienzo.create_line(250, 180, 280, 230, width=2)
    if vidas <= 0: #Pierna izquierda
        lienzo.create_line(250, 180, 220, 230, width=2)

def procesar_intento(letra):
    """
    Procesa la letra ingresada y actualiza el estado del juego y la interfaz
    """
    global vidas, palabraProgreso

    letraCorrecta = False

    if letra in palabraSecreta: #Verifica si la letra está en la palabra secreta
        for i in range(len(palabraSecreta)):
            if palabraSecreta[i] == letra:
                    if palabraProgreso[i] == "_":
                        palabraProgreso[i] = letra
                        letraCorrecta = True

    if not letraCorrecta: #Actualizar vidas si la letra es incorrecta 
        vidas -= 1
        etiquetaEstado.config(text=f"Letra incorrecta.")
    else:
        etiquetaEstado.config(text=f"Letra correcta")

    actualizar_interfaz()
    dibujar_ahorcado()
    verificar_fin_juego()
    
def manejar_intento_boton(): 
    """
    Función llamada al hacer clic en el botón "intentar" 
    """
    letra = entradaLetra.get().lower()
    entradaLetra.delete(0, tk.END) #Limpia la entrada 

    if len(letra) != 1 or not letra.isalpha():
        messagebox.showwarning("Invalida", "Por favor ingresa una única letra válida.")
        return
    
    if letra in letrasAdivinadas:
        etiquetaEstado.config(text=f"Ya probaste la letra {letra}. ")
        return

    #Añadir a letras probadas
    letrasAdivinadas.add(letra)

    #Procesar la letra
    procesar_intento(letra)

def verificar_fin_juego():
    """
    Verifica si el juego ha terminado (ganar o perder)
    """
    if "_" not in palabraProgreso:
        etiquetaEstado.config(text="¡Ganaste!")
        botonIntentar.config(state=tk.DISABLED)
        entradaLetra.config(state=tk.DISABLED)
        messagebox.showinfo("Felicidades", f"Adivinaste la palabra. La palabra es: {palabraSecreta.upper()}")

    elif vidas <= 0:
        etiquetaEstado.config(text="Game Over")
        botonIntentar.config(state=tk.DISABLED)
        entradaLetra.config(state=tk.DISABLED)
        etiquetaProgreso.config(text=palabraSecreta.upper())
        messagebox.showerror("Fin del juego", f"Te has quedado sin vidas \nLa palabra era: {palabraSecreta.upper()}")

def guardar_archivo():
    global ventanaGuardar, entradaArchivo

    # Crear la ventana de diálogo
    ventanaGuardar = tk.Toplevel(ventana)
    ventanaGuardar.title("Guardar Partida")
    ventanaGuardar.resizable(False, False)
    ventanaGuardar.transient(ventana) # .transiet es para que aparezca encima de la principal
    ventanaGuardar.grab_set() # Bloquea la ventana principal

    # Widgets
    tk.Label(ventanaGuardar, text="Nombre de archivo (.txt):", padx=8, pady=8).grid(row=0, column=0, sticky="w")
    entradaArchivo = tk.Entry(ventanaGuardar, width=25)
    entradaArchivo.grid(row=1, column=0, padx=8, pady=4)
    entradaArchivo.insert(0, "ahorcado_partida.txt")
    
    botonConfirmar = tk.Button(ventanaGuardar, text="Guardar", width=10, command=guardar_estado_juego)
    botonConfirmar.grid(row=2, column=0, padx=8, pady=8)
    
    entradaArchivo.focus_set()
    ventanaGuardar.wait_window()

def guardar_estado_juego():
    """
    Guarda el estado actual del juego (palabra, vidas, progreso y letras intentadas) en un archivo .txt.
    """
    global entradaArchivo, ventanaGuardar, vidas, palabraSecreta, palabraProgreso, letrasAdivinadas

    nombreArchivo = entradaArchivo.get().strip()
    if nombreArchivo == "":
        messagebox.showinfo("Guardar", "Escribe un nombre de archivo.")
        return

    if not nombreArchivo.endswith(".txt"):
        nombreArchivo = nombreArchivo + ".txt"

    # Preparar los datos para guardarlos en líneas separadas y fáciles de leer
    datos_a_guardar = [
        f"Palabra Secreta: {palabraSecreta}",
        f"Vidas: {vidas}",
        f"Progreso: {''.join(palabraProgreso)}",
        f"Letras Intentadas: {','.join(sorted(list(letrasAdivinadas)))}"
    ]

    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            for linea in datos_a_guardar:
                archivo.write(linea + "\n")
                
        messagebox.showinfo("Guardar", f"Partida guardada como: {nombreArchivo}")
        ventanaGuardar.destroy()
    except Exception as e:
        # Si ocurre cualquier error ('Exception'), se ejecuta este código
        messagebox.showerror("Error", f"No se pudo guardar el archivo. {e}")

def cargar_estado_juego():
    """
    Muestra una ventana para cargar un juego guardado.
    """
    
    # Función interna para manejar la acción de cargar 
    def confirmar_cargar(nombre_archivo):
        global vidas, palabraSecreta, palabraProgreso, letrasAdivinadas
        
        if not nombre_archivo.endswith(".txt"):
            nombre_archivo += ".txt"
            
        try:
            datos = {}
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    if ":" in linea:
                        clave, valor = linea.split(":", 1)
                        datos[clave.strip()] = valor.strip()
            
            # Asignar los valores globales cargados
            palabraSecreta = datos.get("Palabra Secreta")
            vidas = int(datos.get("Vidas"))
            palabraProgreso = list(datos.get("Progreso"))
            letrasAdivinadas = set(datos.get("Letras Intentadas").split(',')) if datos.get("Letras Intentadas") else set()
            
            # Actualizar la interfaz y habilitar el juego
            actualizar_interfaz()
            dibujar_ahorcado()
            etiquetaEstado.config(text="Partida cargada. ¡Continúa jugando!")
            botonIntentar.config(state=tk.NORMAL)
            entradaLetra.config(state=tk.NORMAL)
            
            ventanaCargar.destroy()
            messagebox.showinfo("Cargar", f"Partida cargada exitosamente desde: {nombre_archivo}")
            
        except FileNotFoundError:
            messagebox.showerror("Error de Carga", f"El archivo '{nombre_archivo}' no fue encontrado.")
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Error al procesar el archivo. Asegúrate de que es un archivo de guardado válido.\nError: {e}")
            
    # Crear la ventana de diálogo para cargar 
    ventanaCargar = tk.Toplevel(ventana)
    ventanaCargar.title("Cargar Partida")
    ventanaCargar.transient(ventana) 
    ventanaCargar.grab_set() 

    tk.Label(ventanaCargar, text="Nombre del archivo a cargar (.txt):", padx=10, pady=10).pack()

    entradaArchivoCargar = tk.Entry(ventanaCargar, width=40)
    entradaArchivoCargar.pack(padx=10, pady=5)
    entradaArchivoCargar.insert(0, "ahorcado_partida.txt") 

    botonConfirmarCargar = tk.Button(ventanaCargar, 
                                     text="Cargar", 
                                     command=lambda: confirmar_cargar(entradaArchivoCargar.get().strip()), 
#lambda permite que la función confirmar_cargar se ejecute solo cuando se presiona el botón, y además le pasa el valor actual de la caja de texto como argumento
                                     bg="#c8e6c9")
    botonConfirmarCargar.pack(pady=10)
    
    entradaArchivoCargar.focus_set() #.focus_set() se asegura de que, en cuanto la ventana aparezca, el cursor parpadeante esté dentro de la caja de texto 
    #y el usuario pueda empezar a escribir el nombre del archivo de inmediato.
    ventanaCargar.wait_window()

ventana = tk.Tk()
ventana.title("Ahorcado")
ventana.resizable(False, False)

panel = tk.Frame(ventana, padx=15, pady=15)
panel.grid(row=0, column=0, sticky="ns")

lienzo = tk.Canvas(ventana, width=anchoCanvas, height=altoCanvas, bg="lightyellow")
lienzo.grid(row=0, column=1, padx=15, pady=15)

# Panel de control

etiquetaEstado = tk.Label(panel, text="Presiona el botón 'Nuevo Juego' para empezar", font=("Arial", 12, "bold"))
etiquetaEstado.grid(row=0, column=0, columnspan=3, pady=(0, 15))

tk.Label(panel, text="Palabra:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=(0, 5))
etiquetaProgreso = tk.Label(panel, text="", font=("Courier", 24, "bold"), fg="darkblue")
etiquetaProgreso.grid(row=2, column=0, columnspan=3, pady=(0, 15))


etiquetaLetrasIntentadas = tk.Label(panel, text="letras probadas: ", font=("Arial", 8))
etiquetaLetrasIntentadas.grid(row=4, column=0, columnspan=3, sticky="w",pady=(0,15))

#Un separador
tk.Frame()

#Entrada de la letra
tk.Label(panel, text="Ingresa una letra: ", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w", pady=10)
entradaLetra = tk.Entry(panel, width=5, justify="center", font=("Arial", 12))
entradaLetra.grid(row=7, column=0, padx=5, pady=2, sticky="w")
#Llama a tu función real (manejar_intento_boton()): La ejecuta sin pasarle el objeto event
entradaLetra.bind("<Return>", lambda event: manejar_intento_boton()) # Permite usar la tecla Enter
#En tkinter, las pulsaciones de teclas se identifican con nombres específicos encerrados entre corchetes angulares (<>)

#Botón intentar
botonIntentar = tk.Button(panel, text="Intentar", command=manejar_intento_boton, bg="#e0f7fa")
botonIntentar.grid(row=7, column=1, sticky="w", padx=(0, 10))

#Boton Nuevo juego
botonNuevoJuego = tk.Button(panel, text="Nuevo Juego", command=inicializar_juego, font=("Arial", 10, "bold"), bg="#c8e6c9")
botonNuevoJuego.grid(row=8, column=0, columnspan=2, pady=(20,5))

# Botón Guardar Partida
botonGuardarPartida = tk.Button(panel, text="Guardar Partida", command=guardar_archivo, bg="#e0f7fa")
botonGuardarPartida.grid(row=10, column=0, columnspan=2, pady=(5, 0)) 

# Botón Cargar Partida 
botonCargarPartida = tk.Button(panel, text="Cargar Partida", command=cargar_estado_juego, bg="#fffde7")
botonCargarPartida.grid(row=11, column=0, columnspan=2, pady=(5, 0))


# Inicializar al cargar (deshabilitado hasta Nuevo Juego)
botonIntentar.config(state=tk.DISABLED)
entradaLetra.config(state=tk.DISABLED)
actualizar_interfaz()
dibujar_ahorcado()

#Boton salir
def salir():
    if messagebox.askyesno("¿Seguro que deseas salir del juego?"):
     ventana.destroy()

botonSalir = tk.Button(panel, text="Salir", command=salir, bg="#ffcdd2")
botonSalir.grid(row=12, column=0, columnspan=2, pady=(5, 0))

ventana.protocol("WM_DELETE_WINDOW", salir) # Maneja el cierre con la X de la ventana
ventana.mainloop()
