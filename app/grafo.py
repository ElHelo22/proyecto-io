"""
grafo.py
Modelo de datos del grafo: vertices, aristas, matriz y lista de adyacencia.
Practica Integradora - Teoria de Grafos - Investigacion Operativa II
"""
 
import csv
import os
 
 
class Grafo:
    """Representa un grafo no dirigido y ponderado mediante listas de adyacencia."""
 
    def __init__(self, dirigido: bool = False):
        self.dirigido = dirigido
        self.vertices = {}      # id -> descripcion
        self.adyacencia = {}    # id -> {vecino: peso}
 
    # ------------------------------------------------------------------
    # Construccion del grafo
    # ------------------------------------------------------------------
    def agregar_vertice(self, id_vertice: str, nombre: str = "", descripcion: str = ""):
        id_vertice = id_vertice.strip()
        if id_vertice in self.vertices:
            raise ValueError(f"El vertice '{id_vertice}' ya existe.")
        self.vertices[id_vertice] = {"nombre": nombre, "descripcion": descripcion}
        self.adyacencia[id_vertice] = {}
 
    def modificar_vertice(self, id_vertice: str, nombre: str = None, descripcion: str = None):
        if id_vertice not in self.vertices:
            raise ValueError(f"El vertice '{id_vertice}' no existe.")
        if nombre is not None:
            self.vertices[id_vertice]["nombre"] = nombre
        if descripcion is not None:
            self.vertices[id_vertice]["descripcion"] = descripcion
 
    def eliminar_vertice(self, id_vertice: str):
        if id_vertice not in self.vertices:
            raise ValueError(f"El vertice '{id_vertice}' no existe.")
        del self.vertices[id_vertice]
        del self.adyacencia[id_vertice]
        for v in self.adyacencia:
            self.adyacencia[v].pop(id_vertice, None)
 
    def agregar_arista(self, origen: str, destino: str, peso: float):
        if origen not in self.vertices or destino not in self.vertices:
            raise ValueError("Ambos vertices deben existir antes de crear la arista.")
        if destino in self.adyacencia[origen]:
            raise ValueError(f"La arista {origen}-{destino} ya existe (posible duplicado).")
        if peso < 0:
            raise ValueError("El peso de la arista no puede ser negativo para este sistema.")
        self.adyacencia[origen][destino] = peso
        if not self.dirigido:
            self.adyacencia[destino][origen] = peso
 
    def modificar_arista(self, origen: str, destino: str, nuevo_peso: float):
        if destino not in self.adyacencia.get(origen, {}):
            raise ValueError(f"La arista {origen}-{destino} no existe.")
        self.adyacencia[origen][destino] = nuevo_peso
        if not self.dirigido:
            self.adyacencia[destino][origen] = nuevo_peso
 
    def eliminar_arista(self, origen: str, destino: str):
        self.adyacencia.get(origen, {}).pop(destino, None)
        if not self.dirigido:
            self.adyacencia.get(destino, {}).pop(origen, None)
 
    # ------------------------------------------------------------------
    # Carga desde archivos
    # ------------------------------------------------------------------
    def cargar_desde_csv(self, ruta_vertices: str, ruta_aristas: str):
        with open(ruta_vertices, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                self.agregar_vertice(fila["id"], fila.get("nombre", ""), fila.get("descripcion", ""))
        with open(ruta_aristas, newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                self.agregar_arista(fila["origen"], fila["destino"], float(fila["peso"]))
 
    # ------------------------------------------------------------------
    # Representaciones
    # ------------------------------------------------------------------
    def lista_vertices(self):
        return list(self.vertices.keys())
 
    def lista_aristas(self):
        vistas = set()
        resultado = []
        for u in self.adyacencia:
            for v, w in self.adyacencia[u].items():
                clave = tuple(sorted((u, v))) if not self.dirigido else (u, v)
                if clave not in vistas:
                    vistas.add(clave)
                    resultado.append((u, v, w))
        return resultado
 
    def matriz_adyacencia(self):
        nodos = sorted(self.vertices.keys())
        matriz = []
        for u in nodos:
            fila = [self.adyacencia[u].get(v, 0) for v in nodos]
            matriz.append(fila)
        return nodos, matriz
 
    def lista_adyacencia(self):
        return {u: list(vecinos.items()) for u, vecinos in self.adyacencia.items()}
 
    def grado(self, vertice: str) -> int:
        return len(self.adyacencia.get(vertice, {}))
 
    def es_conexo(self) -> bool:
        if not self.vertices:
            return True
        inicio = next(iter(self.vertices))
        visitados = set()
        pila = [inicio]
        while pila:
            actual = pila.pop()
            if actual not in visitados:
                visitados.add(actual)
                pila.extend(self.adyacencia[actual].keys())
        return len(visitados) == len(self.vertices)
 
    def tiene_pesos_negativos(self) -> bool:
        return any(w < 0 for _, _, w in self.lista_aristas())
