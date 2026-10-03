"""
reportes.py
Genera un reporte de texto con los resultados obtenidos y recomendaciones.
"""
 
from datetime import datetime
 
 
def generar_reporte(grafo, resultados: dict) -> str:
    lineas = []
    lineas.append("REPORTE - SISTEMA DE ANALISIS Y OPTIMIZACION DE RUTAS DE RECOLECCION")
    lineas.append(f"Fecha de generacion: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lineas.append(f"Vertices: {len(grafo.vertices)}  |  Aristas: {len(grafo.lista_aristas())}")
    lineas.append("-" * 60)
 
    if "dfs" in resultados:
        lineas.append(f"DFS - orden de visita: {resultados['dfs']['orden']}")
    if "bfs" in resultados:
        lineas.append(f"BFS - orden de visita: {resultados['bfs']['orden']}")
    if "dijkstra" in resultados:
        d, camino = resultados["dijkstra"]
        lineas.append(f"Dijkstra - camino: {camino}, distancia total: {d}")
    if "kruskal" in resultados:
        k = resultados["kruskal"]
        lineas.append(f"Kruskal - costo total AEM: {k['costo_total']}")
    if "prim" in resultados:
        p = resultados["prim"]
        lineas.append(f"Prim - costo total AEM: {p['costo_total']}")
 
    lineas.append("-" * 60)
    lineas.append("Recomendaciones:")
    lineas.append("- Priorizar la ruta de costo minimo (Dijkstra) para recorridos puntuales.")
    lineas.append("- Usar el arbol de expansion minima (Kruskal/Prim) para planificar la red de recoleccion permanente al menor costo total.")
    return "\n".join(lineas)
