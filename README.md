# Pipeline de Optimización Bioinspirada (BIOptimization)

Proyecto integral de Inteligencia Computacional que implementa el algoritmo metaheurístico de Enjambre de Salpas (**SSA**) para la optimización de Redes de Función de Base Radial (**RBF**), con persistencia de métricas en la nube mediante **MongoDB Atlas** y análisis estadístico avanzado en Jupyter Notebooks.

---

## 📌 Enlaces del Proyecto

* **Repositorio en GitHub:** [https://github.com/miguelangelmejia08-star/BIOptimization](https://github.com/miguelangelmejia08-star/BIOptimization)

---

## 📁 Estructura del Proyecto

`	ext
BIOptimization/
├── notebooks/
│   └── analisis.ipynb     # Cuaderno de análisis estadístico y curvas de convergencia
├── src/
│   ├── __init__.py
│   ├── aco.py             # Algoritmo complementario (ACO)
│   ├── db.py              # Gestión y conexión con MongoDB Atlas
│   ├── experiment.py      # Orquestador de corridas experimentales (10 ejecuciones)
│   ├── rbf.py             # Arquitectura de Red Neuronal RBF
│   └── ssa.py             # Algoritmo de Enjambre de Salpas (SSA)
├── tests/
│   ├── __init__.py
│   └── test_project.py    # Pruebas unitarias automatizadas (pytest)
├── .env.example           # Plantilla de variables de entorno
├── .gitignore             # Archivos ignorados por Git
├── main.py                # Script principal de ejecución
├── README.md              # Documentación del proyecto
└── requirements.txt       # Dependencias del proyecto
`

---

## 🧬 Módulos del Proyecto

1. **Módulo SSA (src/ssa.py)**:
   * Implementa la heurística de optimización basada en el comportamiento de enjambre de las salpas.
2. **Módulo RBF (src/rbf.py)**:
   * Modelo de Redes Neuronales de Base Radial evaluado mediante el Error Cuadrático Medio (MSE).
3. **Módulo de Experimentos (src/experiment.py)**:
   * Automatiza las corridas múltiples y almacena las métricas en la nube.
4. **Módulo de Base de Datos (src/db.py)**:
   * Conexión segura con MongoDB Atlas mediante variables de entorno (.env).

---

## 🧪 Pruebas Unitarias

Para ejecutar las pruebas automatizadas:

`powershell
python -m pytest tests/
`

---

## 📊 Ejecución y Análisis

1. **Ejecutar experimentos hacia MongoDB Atlas:**
   `powershell
   python -m src.experiment
   `

2. **Abrir el Jupyter Notebook de análisis:**
   `powershell
   jupyter notebook notebooks/analisis.ipynb
   `
