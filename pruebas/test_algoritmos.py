"""
test_algoritmos.py
Casos de prueba minimos para los algoritmos del sistema.
Ejecutar con: python -m pytest pruebas/ -v   (desde la raiz del proyecto)
Nota: esto no se explica en el pdf pero sirvio para detectar errores, probablemente en produccion ya no funcione
"""
 
import os
import sys
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))
 
from grafo import Grafo
from algoritmos import dfs, bfs, dijkstra, reconstruir_camino, kruskal, prim
 
 
def construir_grafo_ejemplo():
    g = Grafo()
    for v in ["A", "B", "C", "D"]:
        g.agregar_vertice(v)
    g.agregar_arista("A", "B", 1)
    g.agregar_arista("B", "C", 2)
    g.agregar_arista("C", "D", 1)
    g.agregar_arista("A", "D", 5)
    return g
 
 
def test_dfs_visita_todos_los_nodos():
    g = construir_grafo_ejemplo()
    resultado = dfs(g, "A")
    assert set(resultado["orden"]) == {"A", "B", "C", "D"}
 
 
def test_bfs_orden_por_niveles():
    g = construir_grafo_ejemplo()
    resultado = bfs(g, "A")
    assert resultado["niveles"][0] == ["A"]
    assert set(resultado["niveles"][1]) == {"B", "D"}
 
 
def test_dijkstra_camino_mas_corto():
    g = construir_grafo_ejemplo()
    dist, pred = dijkstra(g, "A")
    assert dist["D"] == 4  # A-B-C-D (1+2+1) es mas corto que A-D (5)
    camino = reconstruir_camino(pred, "A", "D")
    assert camino == ["A", "B", "C", "D"]
 
 
def test_dijkstra_rechaza_pesos_negativos():
    g = construir_grafo_ejemplo()
    g.adyacencia["A"]["B"] = -1
    g.adyacencia["B"]["A"] = -1
    try:
        dijkstra(g, "A")
        assert False, "Debia lanzar ValueError por peso negativo"
    except ValueError:
        assert True
 
 
def test_arista_duplicada_lanza_error():
    g = construir_grafo_ejemplo()
    try:
        g.agregar_arista("A", "B", 9)
        assert False, "Debia lanzar ValueError por arista duplicada"
    except ValueError:
        assert True
 
 
def test_kruskal_y_prim_igual_costo():
    g = construir_grafo_ejemplo()
    rk = kruskal(g)
    rp = prim(g, "A")
    assert abs(rk["costo_total"] - rp["costo_total"]) < 1e-9
 
 
def test_grafo_no_conexo_detectado():
    g = Grafo()
    g.agregar_vertice("X")
    g.agregar_vertice("Y")
    g.agregar_vertice("Z")
    g.agregar_arista("X", "Y", 1)
    assert g.es_conexo() is False  # Z esta aislado
