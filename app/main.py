"""
main.py
Sistema Inteligente de Analisis y Optimizacion de Rutas de Recoleccion (SIAORR)
Interfaz web interactiva construida con Streamlit.
 
Ejecutar con:  streamlit run app/main.py
 
Practica Integradora - Teoria de Grafos
Investigacion Operativa II / Estructuras Discretas
Universidad Publica de El Alto - Carrera de Ingenieria de Sistemas
Estudiante: Hector Quispe Quispe - Sexto Semestre "B"
Docente: M.Sc. Ing. Juan Carlos Catunta Choquecalle - Gestion 2026
"""
 
import os
import sys
 
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st
 
sys.path.append(os.path.dirname(__file__))
from grafo import Grafo
from algoritmos import dfs, bfs, dijkstra, reconstruir_camino, kruskal, prim, camino_minimo_bfs
from validaciones import validar_vertice, validar_arista, validar_grafo_para_kruskal_prim
from reportes import generar_reporte
 
RUTA_DATOS = os.path.join(os.path.dirname(__file__), "..", "datos")
 
st.set_page_config(page_title="SIAORR - Teoria de Grafos", layout="wide")
 
 
# ----------------------------------------------------------------------
# Estado inicial
# ----------------------------------------------------------------------
def cargar_grafo_inicial():
    g = Grafo(dirigido=False)
    g.cargar_desde_csv(
        os.path.join(RUTA_DATOS, "vertices.csv"),
        os.path.join(RUTA_DATOS, "aristas.csv"),
    )
    return g
 
 
if "grafo" not in st.session_state:
    st.session_state.grafo = cargar_grafo_inicial()
 
grafo = st.session_state.grafo
 
 
def dibujar_grafo(grafo, resaltar_nodos=None, resaltar_aristas=None):
    G = nx.Graph()
    for v in grafo.vertices:
        G.add_node(v)
    for u, v, w in grafo.lista_aristas():
        G.add_edge(u, v, weight=w)
 
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))
 
    resaltar_nodos = resaltar_nodos or []
    resaltar_aristas = set(resaltar_aristas or [])
    colores_nodos = ["#ff8800" if n in resaltar_nodos else "#87ceeb" for n in G.nodes()]
 
    colores_aristas = []
    anchos = []
    for u, v in G.edges():
        if (u, v) in resaltar_aristas or (v, u) in resaltar_aristas:
            colores_aristas.append("#ff0000")
            anchos.append(3)
        else:
            colores_aristas.append("#999999")
            anchos.append(1)
 
    nx.draw_networkx_nodes(G, pos, node_color=colores_nodos, node_size=700, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=colores_aristas, width=anchos, ax=ax)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)
    ax.axis("off")
    return fig
 
 
st.title("Sistema Inteligente de Analisis y Optimizacion de Rutas de Recoleccion (SIAORR)")
st.caption(
    "Practica Integradora de Teoria de Grafos - Investigacion Operativa II"
)
 
menu = st.sidebar.radio(
    "Menu",
    [
        "1. Grafo y representaciones",
        "2. Administrar vertices y aristas",
        "3. DFS",
        "4. BFS",
        "5. Dijkstra",
        "6. Kruskal",
        "7. Prim",
        "8. Comparacion Kruskal vs Prim",
        "9. Reporte final",
    ],
)
 
# ------------------------------------------------------------------
# 1. Grafo y representaciones
# ------------------------------------------------------------------
if menu.startswith("1"):
    st.subheader("Representacion del grafo")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(dibujar_grafo(grafo))
    with col2:
        st.write("**Vertices:**", grafo.lista_vertices())
        st.write("**Numero de vertices:", len(grafo.vertices), "| Numero de aristas:", len(grafo.lista_aristas()))
        st.write("**Es conexo:**", grafo.es_conexo())
 
    st.markdown("### Matriz de adyacencia (pesos)")
    nodos, matriz = grafo.matriz_adyacencia()
    st.dataframe(pd.DataFrame(matriz, index=nodos, columns=nodos))
 
    st.markdown("### Lista de adyacencia")
    for nodo, vecinos in grafo.lista_adyacencia().items():
        st.write(f"**{nodo}**: {vecinos}")
 
# ------------------------------------------------------------------
# 2. Administrar vertices y aristas (CRUD + carga CSV)
# ------------------------------------------------------------------
elif menu.startswith("2"):
    st.subheader("Administrar vertices y aristas")
 
    tab1, tab2, tab3 = st.tabs(["Vertices", "Aristas", " "])
 
    with tab1:
        with st.form("form_vertice"):
            vid = st.text_input("ID del vertice (ej. V13)")
            nombre = st.text_input("Nombre")
            desc = st.text_input("Descripcion")
            if st.form_submit_button("Agregar vertice"):
                errores = validar_vertice(vid, grafo.vertices)
                if errores:
                    st.error(" / ".join(errores))
                else:
                    grafo.agregar_vertice(vid, nombre, desc)
                    st.success(f"Vertice {vid} agregado.")
 
        elim = st.selectbox("Eliminar vertice", [""] + grafo.lista_vertices())
        if st.button("Eliminar vertice seleccionado") and elim:
            grafo.eliminar_vertice(elim)
            st.success(f"Vertice {elim} eliminado.")
            st.rerun()
 
    with tab2:
        with st.form("form_arista"):
            o = st.selectbox("Origen", grafo.lista_vertices())
            d = st.selectbox("Destino", grafo.lista_vertices())
            peso = st.number_input("Peso (km)", min_value=0.0, step=0.1)
            if st.form_submit_button("Agregar arista"):
                aristas_existentes = {tuple(sorted((u, v))) for u, v, _ in grafo.lista_aristas()}
                errores = validar_arista(o, d, peso, grafo.vertices, aristas_existentes)
                if errores:
                    st.error(" / ".join(errores))
                else:
                    grafo.agregar_arista(o, d, peso)
                    st.success(f"Arista {o}-{d} agregada.")
 
    with tab3:
        st.write("Sube tus propios archivos de vertices.csv y aristas.csv (formato indicado en el informe).")
        f_vert = st.file_uploader("vertices.csv", type="csv")
        f_arist = st.file_uploader("aristas.csv", type="csv")
        if f_vert and f_arist and st.button("Cargar archivos"):
            nuevo = Grafo(dirigido=False)
            import io
            nuevo.cargar_desde_csv(io.StringIO(f_vert.getvalue().decode("utf-8")),
                                    io.StringIO(f_arist.getvalue().decode("utf-8")))
            st.session_state.grafo = nuevo
            st.success("Grafo cargado desde los archivos subidos.")
            st.rerun()
 
# ------------------------------------------------------------------
# 3. DFS
# ------------------------------------------------------------------
elif menu.startswith("3"):
    st.subheader("Busqueda en profundidad (DFS)")
    origen = st.selectbox("Nodo inicial", grafo.lista_vertices())
    if st.button("Ejecutar DFS"):
        resultado = dfs(grafo, origen)
        st.write("**Orden de visita:**", resultado["orden"])
        st.write("**Aristas utilizadas:**", resultado["aristas"])
        st.write("**Nodos alcanzables desde el origen:**", resultado["alcanzables"])
        if len(resultado["alcanzables"]) < len(grafo.vertices):
            st.warning("El grafo no es conexo desde este origen: existen nodos no alcanzables.")
        st.pyplot(dibujar_grafo(grafo, resaltar_nodos=resultado["orden"], resaltar_aristas=resultado["aristas"]))
 
# ------------------------------------------------------------------
# 4. BFS
# ------------------------------------------------------------------
elif menu.startswith("4"):
    st.subheader("Busqueda en amplitud (BFS)")
    origen = st.selectbox("Nodo inicial", grafo.lista_vertices(), key="bfs_origen")
    if st.button("Ejecutar BFS"):
        resultado = bfs(grafo, origen)
        st.write("**Orden de visita (por niveles):**", resultado["orden"])
        st.write("**Niveles:**", resultado["niveles"])
        st.write("**Aristas utilizadas:**", resultado["aristas"])
        st.pyplot(dibujar_grafo(grafo, resaltar_nodos=resultado["orden"], resaltar_aristas=resultado["aristas"]))

 
# ------------------------------------------------------------------
# 5. Dijkstra
# ------------------------------------------------------------------
elif menu.startswith("5"):
    st.subheader("Algoritmo de Dijkstra")
    c1, c2 = st.columns(2)
    origen = c1.selectbox("Nodo origen", grafo.lista_vertices(), key="dij_o")
    destino = c2.selectbox("Nodo destino", grafo.lista_vertices(), key="dij_d")
    if st.button("Ejecutar Dijkstra"):
        try:
            distancias, predecesor = dijkstra(grafo, origen)
            camino = reconstruir_camino(predecesor, origen, destino)
            st.write(f"**Distancia minima {origen} -> {destino}:**", distancias[destino])
            st.write("**Camino:**", camino)
            st.markdown("**Tabla de distancias y predecesores:**")
            tabla = pd.DataFrame({
                "Nodo": list(distancias.keys()),
                "Distancia": list(distancias.values()),
                "Predecesor": [predecesor[n] for n in distancias.keys()],
            })
            st.dataframe(tabla)
            aristas_camino = list(zip(camino, camino[1:])) if camino else []
            st.pyplot(dibujar_grafo(grafo, resaltar_nodos=camino, resaltar_aristas=aristas_camino))
        except ValueError as e:
            st.error(str(e))
 
# ------------------------------------------------------------------
# 6. Kruskal
# ------------------------------------------------------------------
elif menu.startswith("6"):
    st.subheader("Algoritmo de Kruskal")
    errores = validar_grafo_para_kruskal_prim(grafo)
    if errores:
        st.error(" / ".join(errores))
    elif st.button("Ejecutar Kruskal"):
        resultado = kruskal(grafo)
        st.write("**Aristas aceptadas (arbol de expansion minima):**")
        st.table(pd.DataFrame(resultado["aceptadas"], columns=["Origen", "Destino", "Peso"]))
        st.write("**Aristas rechazadas (generaban ciclo):**")
        st.table(pd.DataFrame(resultado["rechazadas"], columns=["Origen", "Destino", "Peso"]))
        st.success(f"Costo total del AEM: {resultado['costo_total']}")
        aristas_aem = [(u, v) for u, v, _ in resultado["aceptadas"]]
        st.pyplot(dibujar_grafo(grafo, resaltar_aristas=aristas_aem))
 
# ------------------------------------------------------------------
# 7. Prim
# ------------------------------------------------------------------
elif menu.startswith("7"):
    st.subheader("Algoritmo de Prim")
    origen = st.selectbox("Nodo inicial", grafo.lista_vertices(), key="prim_o")
    errores = validar_grafo_para_kruskal_prim(grafo)
    if errores:
        st.error(" / ".join(errores))
    elif st.button("Ejecutar Prim"):
        resultado = prim(grafo, origen)
        st.write("**Arbol de expansion minima (orden de incorporacion):**")
        st.table(pd.DataFrame(resultado["aem"], columns=["Desde", "Hacia", "Peso"]))
        st.write("**Nodos incorporados:**", resultado["nodos_incorporados"])
        st.success(f"Costo total del AEM: {resultado['costo_total']}")
        aristas_aem = [(u, v) for u, v, _ in resultado["aem"]]
        st.pyplot(dibujar_grafo(grafo, resaltar_aristas=aristas_aem))
 
# ------------------------------------------------------------------
# 8. Comparacion
# ------------------------------------------------------------------
elif menu.startswith("8"):
    st.subheader("Comparacion entre Kruskal y Prim")
    errores = validar_grafo_para_kruskal_prim(grafo)
    if errores:
        st.error(" / ".join(errores))
    else:
        rk = kruskal(grafo)
        rp = prim(grafo, grafo.lista_vertices()[0])
        comp = pd.DataFrame({
            "Criterio": ["Costo total", "Numero de aristas"],
            "Kruskal": [rk["costo_total"], len(rk["aceptadas"])],
            "Prim": [rp["costo_total"], len(rp["aem"])],
        })
        st.table(comp)
        if abs(rk["costo_total"] - rp["costo_total"]) < 1e-9:
            st.success("Ambos algoritmos coinciden en el costo total del arbol de expansion minima.")
        else:
            st.error("Los costos difieren: revisar la implementacion.")
 
# ------------------------------------------------------------------
# 9. Reporte final
# ------------------------------------------------------------------
elif menu.startswith("9"):
    st.subheader("Reporte final")
    origen = st.selectbox("Nodo origen para DFS/BFS/Dijkstra", grafo.lista_vertices(), key="rep_o")
    destino = st.selectbox("Nodo destino para Dijkstra", grafo.lista_vertices(), key="rep_d")
    if st.button("Generar reporte"):
        resultados = {
            "dfs": dfs(grafo, origen),
            "bfs": bfs(grafo, origen),
        }
        try:
            dist, pred = dijkstra(grafo, origen)
            resultados["dijkstra"] = (dist[destino], reconstruir_camino(pred, origen, destino))
        except ValueError as e:
            st.warning(str(e))
        errores_mst = validar_grafo_para_kruskal_prim(grafo)
        if not errores_mst:
            resultados["kruskal"] = kruskal(grafo)
            resultados["prim"] = prim(grafo, origen)
        texto = generar_reporte(grafo, resultados)
        st.text(texto)
        st.download_button("Descargar reporte (.txt)", texto, file_name="reporte_siaorr.txt")
