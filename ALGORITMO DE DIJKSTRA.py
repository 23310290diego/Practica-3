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