# Pipeline de Optimizacion Bioinspirada (BIOptimization)

Proyecto integral de Inteligencia Computacional que implementa el algoritmo metaheuristico de Enjambre de Salpas (**SSA**) para la optimizacion de Redes de Funcion de Base Radial (**RBF**), con persistencia de metricas en la nube mediante **MongoDB Atlas** y analisis estadistico avanzado en Jupyter Notebooks.

---

## 📌 Enlaces del Proyecto

* **Repositorio en GitHub:** [https://github.com/miguelangelmejia08-star/BIOptimization](https://github.com/miguelangelmejia08-star/BIOptimization)

---

## 📁 Estructura del Proyecto

```text
BIOptimization/
├── notebooks/
│   └── analisis.ipynb     # Cuaderno de analisis estadistico y curvas de convergencia
├── src/
│   ├── __init__.py
│   ├── aco.py             # Algoritmo de Colonia de Hormigas para TSP
│   ├── db.py              # Gestion y conexion con MongoDB Atlas
│   ├── experiment.py      # Orquestador de corridas experimentales (10 ejecuciones RBF+SSA)
│   ├── rbf.py             # Arquitectura de Red Neuronal RBF
│   └── ssa.py             # Algoritmo de Enjambre de Salpas (SSA)
├── tests/
│   ├── __init__.py
│   └── test_project.py    # Pruebas unitarias automatizadas (pytest)
├── .env.example           # Plantilla de variables de entorno (MongoDB Atlas)
├── .gitignore             # Archivos ignorados por Git
├── main.py                # Script principal de ejecucion
├── README.md              # Documentacion del proyecto
└── requirements.txt       # Dependencias del proyecto
```

---

## 🧬 Modulos del Proyecto

1. **Modulo ACO (`src/aco.py`)**:
   * Algoritmo de Colonia de Hormigas (ACO) para resolver el Problema del Viajante de Comercio (TSP).
2. **Modulo SSA (`src/ssa.py`)**:
   * Heuristica de optimizacion basada en el comportamiento de enjambre de las salpas para funciones continuas (Rastrigin y RBF).
3. **Modulo RBF (`src/rbf.py`)**:
   * Modelo de Redes Neuronales de Base Radial con seleccion de centros por K-Means y regularizacion Ridge.
4. **Modulo de Base de Datos (`src/db.py`)**:
   * Conexion segura con MongoDB Atlas mediante variables de entorno (`.env`) y serializacion de arrays NumPy a BSON.
5. **Modulo de Experimentos (`src/experiment.py`)**:
   * Orquestador de 10 corridas independientes para evaluar la optimizacion de hiperparametros ($M, \sigma, \lambda$) de la RBF con SSA sobre California Housing.

---

## 🧪 Pruebas Unitarias

Para ejecutar las pruebas automatizadas con `pytest`:

```powershell
python -m pytest tests/
```

---

## 📊 Ejecucion y Analisis

1. **Ejecutar el script principal con todos los ejercicios:**
   ```powershell
   python main.py
   ```

2. **Ejecutar el experimento completo de 10 corridas hacia MongoDB Atlas:**
   ```powershell
   python -m src.experiment
   ```

3. **Abrir el Jupyter Notebook de analisis estadistico:**
   ```powershell
   jupyter notebook notebooks/analisis.ipynb
   ```
