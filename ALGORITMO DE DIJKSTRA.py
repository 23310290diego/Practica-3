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