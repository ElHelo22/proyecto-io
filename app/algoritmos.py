"""
algoritmos.py
Implementacion propia (sin librerias externas de grafos) de:
DFS, BFS, Dijkstra, Kruskal y Prim.
Practica Integradora - Teoria de Grafos - Investigacion Operativa II
"""
 
import heapq
 
 
# ---------------------------------------------------------------------
# DFS - Busqueda en profundidad
# ---------------------------------------------------------------------
def dfs(grafo, origen):
    visitados = []
    aristas_usadas = []
    marca = set()
 
    def _dfs(u):
        marca.add(u)
        visitados.append(u)
        for v in sorted(grafo.adyacencia[u].keys()):
            if v not in marca:
                aristas_usadas.append((u, v))
                _dfs(v)
 
    _dfs(origen)
    alcanzables = set(visitados)
    return {
        "orden": visitados,
        "aristas": aristas_usadas,
        "alcanzables": sorted(alcanzables),
    }
 
 
# ---------------------------------------------------------------------
# BFS - Busqueda en amplitud
# ---------------------------------------------------------------------
def bfs(grafo, origen):
    visitados = [origen]
    marca = {origen}
    cola = [origen]
    aristas_usadas = []
    nivel = {origen: 0}
 
    while cola:
        u = cola.pop(0)
        for v in sorted(grafo.adyacencia[u].keys()):
            if v not in marca:
                marca.add(v)
                nivel[v] = nivel[u] + 1
                visitados.append(v)
                aristas_usadas.append((u, v))
                cola.append(v)
 
    niveles = {}
    for nodo, lvl in nivel.items():
        niveles.setdefault(lvl, []).append(nodo)
 
    return {"orden": visitados, "aristas": aristas_usadas, "niveles": niveles}
 
 
def camino_minimo_bfs(grafo, origen, destino):
    """Numero minimo de aristas (grafo no ponderado) entre origen y destino."""
    if origen == destino:
        return [origen]
    marca = {origen}
    cola = [origen]
    padre = {origen: None}
    while cola:
        u = cola.pop(0)
        for v in grafo.adyacencia[u]:
            if v not in marca:
                marca.add(v)
                padre[v] = u
                if v == destino:
                    camino = [destino]
                    while padre[camino[-1]] is not None:
                        camino.append(padre[camino[-1]])
                    return list(reversed(camino))
                cola.append(v)
    return None  # no alcanzable
 
 
# ---------------------------------------------------------------------
# DIJKSTRA
# ---------------------------------------------------------------------
def dijkstra(grafo, origen):
    if grafo.tiene_pesos_negativos():
        raise ValueError("ADVERTENCIA: existen pesos negativos. Dijkstra no es aplicable.")
 
    distancias = {v: float("inf") for v in grafo.vertices}
    predecesor = {v: None for v in grafo.vertices}
    distancias[origen] = 0
    visitados = set()
    heap = [(0, origen)]
 
    while heap:
        dist_u, u = heapq.heappop(heap)
        if u in visitados:
            continue
        visitados.add(u)
        for v, peso in grafo.adyacencia[u].items():
            nueva = dist_u + peso
            if nueva < distancias[v]:
                distancias[v] = nueva
                predecesor[v] = u
                heapq.heappush(heap, (nueva, v))
 
    return distancias, predecesor
 
 
def reconstruir_camino(predecesor, origen, destino):
    if predecesor.get(destino) is None and destino != origen:
        return None
    camino = [destino]
    while camino[-1] != origen:
        anterior = predecesor[camino[-1]]
        if anterior is None:
            return None
        camino.append(anterior)
    return list(reversed(camino))
 
 
# ---------------------------------------------------------------------
# KRUSKAL (con Union-Find)
# ---------------------------------------------------------------------
class UnionFind:
    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}
 
    def encontrar(self, x):
        while self.padre[x] != x:
            x = self.padre[x]
        return x
 
    def unir(self, x, y):
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False
        self.padre[rx] = ry
        return True
 
 
def kruskal(grafo):
    aristas = sorted(grafo.lista_aristas(), key=lambda a: a[2])
    uf = UnionFind(grafo.vertices.keys())
    aceptadas, rechazadas = [], []
 
    for u, v, w in aristas:
        if uf.unir(u, v):
            aceptadas.append((u, v, w))
        else:
            rechazadas.append((u, v, w))
 
    costo_total = sum(w for _, _, w in aceptadas)
    return {"aceptadas": aceptadas, "rechazadas": rechazadas, "costo_total": costo_total}
 
 
# ---------------------------------------------------------------------
# PRIM
# ---------------------------------------------------------------------
def prim(grafo, origen):
    visitados = {origen}
    aem = []
    heap = []
    for v, w in grafo.adyacencia[origen].items():
        heapq.heappush(heap, (w, origen, v))
 
    while heap and len(visitados) < len(grafo.vertices):
        w, u, v = heapq.heappop(heap)
        if v in visitados:
            continue
        visitados.add(v)
        aem.append((u, v, w))
        for v2, w2 in grafo.adyacencia[v].items():
            if v2 not in visitados:
                heapq.heappush(heap, (w2, v, v2))
 
    costo_total = sum(w for _, _, w in aem)
    return {"aem": aem, "costo_total": costo_total, "nodos_incorporados": sorted(visitados)}
