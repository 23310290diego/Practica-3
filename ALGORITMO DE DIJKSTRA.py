import tkinter as tk
from tkinter import messagebox
import time

class DijkstraSimple:
    def __init__(self):
        # DEFINICIÓN DEL GRAFO 
        # Se usa un diccionario de diccionarios (lista de adyacencia).
        # Clave externa: Nodo origen. Clave interna: Nodo vecino. Valor: Peso/Costo de la arista.
        self.grafo = {
            'A': {'B': 4, 'C': 2},
            'B': {'A': 4, 'C': 1, 'D': 5},
            'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
            'D': {'B': 5, 'C': 8, 'E': 2},
            'E': {'C': 10, 'D': 2}
        }
        
        # Coordenadas (X, Y) para posicionar los nodos 
        self.posiciones = {
            'A': (50, 150),
            'B': (180, 50),
            'C': (180, 250),
            'D': (320, 50),
            'E': (320, 250)
        }

# LÓGICA DEL ALGORITMO DE DIJKSTRA
    def resolver_dijkstra(self, inicio, fin):
        print(f"\n--- RESOLVIENDO: {inicio} a {fin} ---")
        
        # 1. Inicialización de estructuras auxiliares
        # distancias: Guarda el costo mínimo para llegar a cada nodo (empiezan en infinito)
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0  # El costo de iniciar en el origen es cero

        # predecesores: Guarda el nodo anterior en la ruta óptima para poder reconstruir el camino al final
        predecesores = {nodo: None for nodo in self.grafo}
        
        # no_visitados: Lista de nodos que el algoritmo aún debe explorar
        no_visitados = list(self.grafo.keys())

        # 2. Bucle principal del algoritmo
        while no_visitados:
            # Selecciona el nodo con la menor distancia registrada que aún no haya sido visitado
            nodo_actual = min(no_visitados, key=lambda n: distancias[n])
            print(f"Visita nodo: {nodo_actual} (Distancia acumulada: {distancias[nodo_actual]})")

            # Si llegamos al destino o el nodo actual es inaccesible (distancia infinito), rompemos el ciclo
            if nodo_actual == fin or distancias[nodo_actual] == float('inf'):
                break

    # Se marca el nodo actual como visitado eliminándolo de la lista
            no_visitados.remove(nodo_actual)

            # 3. Relajación de aristas (Evaluación de vecinos)
            for vecino, peso in self.grafo[nodo_actual].items():
                if vecino in no_visitados:
                    # Calcula la distancia total acumulada viajando a través del nodo actual
                    nueva_dist = distancias[nodo_actual] + peso
                    
                    # Si encontramos un camino más corto que el previamente guardado, lo actualizamos
                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        predecesores[vecino] = nodo_actual
                        print(f"  -> Actualiza {vecino}: nuevo costo = {nueva_dist}")
    # 4. Reconstrucción del camino más corto (Hacia atrás desde el final al inicio)
        camino = []
        actual = fin
        while actual is not None:
            camino.insert(0, actual)  # Inserta al principio de la lista para mantener el orden correcto
            actual = predecesores[actual]
            
        print(f"Resultado: {' -> '.join(camino)} | Costo: {distancias[fin]}\n")
        return camino, distancias[fin]

    #Parte Grafica
    def iniciar_interfaz(self):
        # Crear ventana principal
        root = tk.Tk()
        root.title("Dijkstra Simplificado")
        root.geometry("400x400")

        # Lienzo para dibujar el grafo (Fondo blanco, diseño minimalista)
        canvas = tk.Canvas(root, width=380, height=300, bg="white")
        canvas.pack(pady=10)

        # 1. DIBUJAR CONEXIONES (Líneas negras simples)
        for nodo, vecinos in self.grafo.items():
            x1, y1 = self.posiciones[nodo]
            for vecino, peso in vecinos.items():
                x2, y2 = self.posiciones[vecino]
                # Crea la línea y le asigna un tag único identificativo para poder modificarla después
                canvas.create_line(x1, y1, x2, y2, fill="black", tags=f"linea_{nodo}_{vecino}")
                # Coloca el peso numérico en el centro exacto de la línea
                canvas.create_text((x1+x2)/2, (y1+y2)/2 - 5, text=str(peso), font=("Arial", 9))

        # 2. DIBUJAR NODOS (Círculos blancos con texto negro)
        for nodo, (x, y) in self.posiciones.items():
            # Dibuja la circunferencia del nodo
            canvas.create_oval(x-15, y-15, x+15, y+15, fill="white", outline="black", tags=f"nodo_{nodo}")
            # Dibuja la letra identificadora del nodo en el centro
            canvas.create_text(x, y, text=nodo, font=("Arial", 10, "bold"))

        # 3. CONTROLES INFERIORES (Formulario de entrada de datos)
        frame = tk.Frame(root)
        frame.pack()

        # Entrada para el nodo Origen
        tk.Label(frame, text="De:").grid(row=0, column=0)
        txt_ini = tk.Entry(frame, width=3, justify="center")
        txt_ini.insert(0, "A")
        txt_ini.grid(row=0, column=1, padx=5)

        # Entrada para el nodo Destino
        tk.Label(frame, text="A:").grid(row=0, column=2)
        txt_fin = tk.Entry(frame, width=3, justify="center")
        txt_fin.insert(0, "E")
        txt_fin.grid(row=0, column=3, padx=5)

        # 4. FUNCIÓN INTERNA PARA DETONAR LA SIMULACIÓN
        def simular():
            # Resetear estilos gráficos a su estado original (blanco y negro estático)
            for n in self.grafo:
                canvas.itemconfig(f"nodo_{n}", fill="white", outline="black")
                for v in self.grafo[n]:
                    canvas.itemconfig(f"linea_{n}_{v}", fill="black", width=1)

            # Obtener datos de las cajas de texto limpiando espacios y forzando mayúsculas
            ini, fin = txt_ini.get().upper().strip(), txt_fin.get().upper().strip()
            
            # Validación simple para evitar fallos si el usuario digita un nodo que no existe
            if ini not in self.grafo or fin not in self.grafo:
                messagebox.showerror("Error", "Nodos no válidos.")
                return

            # Ejecutar el algoritmo lógico (imprime los pasos en la terminal)
            camino, costo = self.resolver_dijkstra(ini, fin)

            # RESALTAR EN PANTALLA: Engrosar las líneas y pintar de gris claro la ruta calculada
            for i in range(len(camino) - 1):
                n1, n2 = camino[i], camino[i+1]
                # Engrosa la arista en ambos sentidos para asegurar la visualización en el grafo no dirigido
                canvas.itemconfig(f"linea_{n1}_{n2}", fill="black", width=3)
                canvas.itemconfig(f"linea_{n2}_{n1}", fill="black", width=3)
                canvas.itemconfig(f"nodo_{n1}", fill="#e0e0e0") # Gris minimalista para nodo recorrido
            
            # Pintar el último nodo de la ruta
            canvas.itemconfig(f"nodo_{camino[-1]}", fill="#e0e0e0")

            # Mostrar ventana emergente con el resultado consolidado
            messagebox.showinfo("Resultado", f"Camino: {'->'.join(camino)}\nCosto: {costo}")

        # Botón estándar para lanzar el cálculo de la simulación
        btn = tk.Button(frame, text="Calcular", command=simular)
        btn.grid(row=0, column=4, padx=10)

        # Mantener la ventana de Tkinter activa escuchando eventos
        root.mainloop()


if __name__ == "__main__":
    app = DijkstraSimple()
    app.iniciar_interfaz()