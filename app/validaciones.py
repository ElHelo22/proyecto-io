"""
validaciones.py
Validacion de datos incompletos, duplicados o incorrectos.
"""
 
 
def validar_vertice(id_vertice, vertices_existentes):
    errores = []
    if not id_vertice or not id_vertice.strip():
        errores.append("El identificador del vertice no puede estar vacio.")
    if id_vertice in vertices_existentes:
        errores.append(f"El vertice '{id_vertice}' ya existe (duplicado).")
    return errores
 
 
def validar_arista(origen, destino, peso, vertices_existentes, aristas_existentes):
    errores = []
    if origen not in vertices_existentes:
        errores.append(f"El vertice origen '{origen}' no existe.")
    if destino not in vertices_existentes:
        errores.append(f"El vertice destino '{destino}' no existe.")
    if origen == destino:
        errores.append("No se permiten bucles (arista de un vertice a si mismo) en este modelo.")
    clave = tuple(sorted((origen, destino)))
    if clave in aristas_existentes:
        errores.append(f"La arista {origen}-{destino} ya existe (duplicada).")
    try:
        peso_f = float(peso)
        if peso_f < 0:
            errores.append("El peso no puede ser negativo (requisito para Dijkstra).")
    except (TypeError, ValueError):
        errores.append("El peso debe ser un numero valido.")
    return errores
 
 
def validar_grafo_para_kruskal_prim(grafo):
    errores = []
    if grafo.dirigido:
        errores.append("Kruskal y Prim requieren un grafo no dirigido.")
    if not grafo.es_conexo():
        errores.append("El grafo no es conexo: no existe un unico arbol de expansion minima para todos los vertices.")
    if len(grafo.lista_aristas()) == 0:
        errores.append("El grafo no tiene aristas ponderadas.")
    return errores
