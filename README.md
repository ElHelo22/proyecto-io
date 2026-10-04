# 📊 Proyecto IO — Investigación Operativa

Aplicación desarrollada para la materia de **Investigación Operativa**, orientada al modelado y análisis de **grafos ponderados, conexos y no dirigidos**.

El proyecto permite representar una red de puntos mediante vértices y conexiones, almacenar la información en archivos CSV y visualizar el grafo mediante una interfaz web desarrollada con **Streamlit**.

---

## 👥 Integrantes

* **Apaza Casas Alexix Andrew**
* **Apaza Mamani Helmer Rudel**
* **Callizaya Lopez Naeli Daniela**
* **Chavez Mamani Joel Alexix**
* **Mamani Arias Karen Belen**
* **Mamani Quispe Miguel Angel**
* **Mendoza Paye Cristian Rodrigo**
* **Quispe Quispe Hector**

---

## 🛠️ Tecnologías utilizadas

* 🐍 **Python 3**
* 🎈 **Streamlit** — Interfaz web
* 🕸️ **NetworkX** — Modelado y análisis de grafos
* 📈 **Matplotlib** — Visualización de gráficos
* 🐼 **Pandas** — Manejo y procesamiento de datos
* 📄 **CSV** — Almacenamiento de vértices y aristas

---

## 📋 Requisitos

Antes de ejecutar el proyecto, es necesario tener instalado:

* **Python 3.x**
* **pip**
* Conexión a Internet para instalar las dependencias

Para comprobar que Python está instalado:

```bash
py --version
```

Para comprobar `pip`:

```bash
py -m pip --version
```

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/proyecto-io.git
```

Ingresar a la carpeta:

```bash
cd proyecto-io
```

> **Nota:** Reemplazar `USUARIO` por el nombre de usuario propietario del repositorio.

### 2. Actualizar pip

Este paso es opcional, pero recomendado:

```bash
py -m pip install --upgrade pip
```

### 3. Instalar las dependencias

El proyecto incluye un archivo `requirements.txt` con las librerías necesarias.

Ejecutar:

```bash
py -m pip install -r requirements.txt
```

---

## ▶️ Ejecución

Para iniciar la aplicación, ejecutar:

```bash
py -m streamlit run app/main.py
```

Después de ejecutar el comando, Streamlit proporcionará una dirección local para acceder a la aplicación desde el navegador.

Normalmente será similar a:

```text
http://localhost:8501
```

---

## 📚 Librerías utilizadas

| Librería       | Función                                       |
| -------------- | --------------------------------------------- |
| **Matplotlib** | Generación y visualización de gráficos        |
| **NetworkX**   | Creación, representación y análisis de grafos |
| **Pandas**     | Lectura y procesamiento de datos              |
| **Streamlit**  | Desarrollo de la interfaz web                 |

Además, el proyecto utiliza `heapq`, una biblioteca incluida en Python que permite trabajar con colas de prioridad y **no requiere instalación mediante pip**.

---

## 📁 Estructura del proyecto

```text
proyecto-io/
│
├── app/
│   ├── main.py
│   └── grafo.py
│
├── datos/
│   ├── vertices.csv
│   └── aristas.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

### 📂 `app/`

Contiene el código principal de la aplicación.

* `main.py` → Interfaz y ejecución de la aplicación.
* `grafo.py` → Implementación y operaciones relacionadas con los grafos.

### 📂 `datos/`

Contiene los archivos CSV utilizados para cargar la información del grafo.

* `vertices.csv` → Información de los vértices.
* `aristas.csv` → Información de las conexiones y sus pesos.

### 📄 `requirements.txt`

Contiene las dependencias externas necesarias para ejecutar el proyecto.

### 📄 `README.md`

Contiene la documentación e instrucciones del proyecto.

---

## 🧩 Modelo del grafo

El sistema trabaja con:

* **Vértices:** representan puntos o lugares de la red.
* **Aristas:** representan conexiones entre los puntos.
* **Peso:** representa el costo o distancia asociada a una conexión.
* **Grafo no dirigido:** las conexiones pueden recorrerse en ambos sentidos.
* **Grafo ponderado:** las aristas poseen un peso asociado.

Los datos pueden ser cargados desde archivos CSV para facilitar la modificación y ampliación de la red.

---

## 📌 Uso del proyecto

El proyecto tiene como finalidad aplicar conceptos de **Investigación Operativa y Teoría de Grafos** mediante una aplicación práctica.

Entre las operaciones que pueden implementarse o utilizarse en el sistema se encuentran:

* Representación de grafos.
* Carga de vértices y aristas desde archivos CSV.
* Visualización gráfica de la red.
* Trabajo con grafos ponderados.
* Búsqueda de rutas.
* Cálculo de distancias o costos.
* Aplicación de algoritmos de teoría de grafos.

---

## ⚠️ Solución de problemas

### `ModuleNotFoundError`

Si aparece un error como:

```text
ModuleNotFoundError: No module named 'networkx'
```

ejecutar:

```bash
py -m pip install -r requirements.txt
```

### `streamlit no se reconoce como un comando`

Utilizar:

```bash
py -m streamlit run app/main.py
```

en lugar de:

```bash
streamlit run app/main.py
```

### No se encuentra `vertices.csv`

Verificar que la estructura de carpetas sea:

```text
proyecto-io/
├── app/
│   ├── main.py
│   └── grafo.py
│
└── datos/
    ├── vertices.csv
    └── aristas.csv
```

Los archivos CSV deben encontrarse dentro de la carpeta `datos`.

---

## 🎓 Proyecto académico

**Materia:** Investigación Operativa

**Proyecto:** Aplicación de conceptos de grafos mediante una aplicación desarrollada en Python.

**Gestión:** 2026

---

## 📄 Licencia

Proyecto desarrollado con fines **académicos y educativos**.
