# tests/test_project.py
import numpy as np
import pytest
from src.aco import AntColonyTSP
from src.ssa import SalpSwarmAlgorithm, rastrigin_function
from src.rbf import RBFRegression
from src.db import MongoManager

def test_aco_valid_path():
    """Prueba 1: ACO devuelve una ruta válida que contiene todas las ciudades una sola vez."""
    coordinates = np.random.rand(10, 2) * 100
    aco = AntColonyTSP(coordinates, n_ants=5, n_iterations=10)
    path, length = aco.run()
    
    # Validar que la longitud de la ruta sea igual al número de ciudades
    assert len(path) == len(coordinates)
    # Validar que no haya ciudades repetidas y estén todas contenidas
    assert set(path) == set(range(len(coordinates)))
    assert length > 0

def test_ssa_bounds():
    """Prueba 2: SSA mantiene las soluciones dentro de los límites definidos."""
    lb = -5.12
    ub = 5.12
    ssa = SalpSwarmAlgorithm(
        objective_func=rastrigin_function,
        dim=3,
        n_salps=10,
        max_iter=5,
        lb=lb,
        ub=ub
    )
    best_pos, best_fit, convergence = ssa.optimize()
    
    # Verificar que la posición óptima no rebase los límites
    assert np.all(best_pos >= lb)
    assert np.all(best_pos <= ub)
    assert len(convergence) == 5

def test_rbf_matrix_and_no_nans():
    """Prueba 3: La red RBF entrena sin NaNs ni valores infinitos y predice correctamente."""
    X_train = np.random.rand(40, 3)
    y_train = np.random.rand(40)
    
    rbf = RBFRegression(M=5, sigma=1.0, reg_lambda=0.01)
    rbf.fit(X_train, y_train)
    
    # Verificar que los pesos calculados no contengan NaN o Inf
    assert not np.any(np.isnan(rbf.weights))
    assert not np.any(np.isinf(rbf.weights))
    
    # Verificar dimensiones de predicción
    preds = rbf.predict(X_train)
    assert len(preds) == len(X_train)
    assert not np.any(np.isnan(preds))

def test_db_manager_structure():
    """Prueba 4: El gestor de MongoDB procesa correctamente la estructura del documento."""
    db = MongoManager()
    
    # Datos de prueba simulados
    dummy_data = {
        "algorithm": "test_algo",
        "seed": 42,
        "dataset": "test_data",
        "params": {"M": 5, "sigma": 1.0, "lambda": 0.01},
        "metrics": {"mse": 0.05},
        "evaluations": 100,
        "convergence": [0.2, 0.1, 0.05]
    }
    
    # Si hay conexión con Atlas, intentará guardar. Si no, evaluamos que maneje el fallback de manera segura.
    inserted_id = db.save_run(dummy_data)
    if db.connected:
        assert inserted_id is not None
    else:
        assert inserted_id is None