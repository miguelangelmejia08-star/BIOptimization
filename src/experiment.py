# src/experiment.py
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.rbf import RBFRegression
from src.ssa import SalpSwarmAlgorithm
from src.db import MongoManager

def run_rbf_ssa_experiment():
    print("=== INICIANDO EXPERIMENTO RBF + SSA (10 CORRIDAS) ===")
    
    # 1. Cargar dataset y dividirlo (Entrenamiento / Validación / Prueba)
    data = fetch_california_housing()
    X, y = data.data[:500], data.target[:500]  # Muestra de 500 para agilizar pruebas
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Normalizar datos
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    db = MongoManager()
    seeds = [42, 100, 202, 333, 505, 777, 888, 999, 123, 456]
    
    all_mse_results = []

    for i, seed in enumerate(seeds):
        np.random.seed(seed)
        print(f"\n--- Corrida {i+1}/10 (Semilla: {seed}) ---")

        def objective_for_ssa(vector):
            m_centers = int(np.clip(round(vector[0]), 2, 25))
            sigma_val = max(0.01, vector[1])
            lambda_val = max(1e-5, vector[2])
            
            try:
                rbf = RBFRegression(M=m_centers, sigma=sigma_val, reg_lambda=lambda_val)
                rbf.fit(X_train, y_train)
                mse = rbf.evaluate_mse(X_val, y_val)
                if np.isnan(mse) or np.isinf(mse):
                    return 1e6
                return mse
            except Exception:
                return 1e6

        lb = [2, 0.1, 0.0001]
        ub = [25, 5.0, 0.1]
        
        ssa = SalpSwarmAlgorithm(
            objective_func=objective_for_ssa,
            dim=3,
            n_salps=15,
            max_iter=30,
            lb=lb,
            ub=ub
        )

        best_pos, best_fitness, convergence = ssa.optimize()

        best_M = int(round(best_pos[0]))
        best_sigma = best_pos[1]
        best_lambda = best_pos[2]

        final_rbf = RBFRegression(M=best_M, sigma=best_sigma, reg_lambda=best_lambda)
        final_rbf.fit(X_train, y_train)
        test_mse = final_rbf.evaluate_mse(X_test, y_test)
        all_mse_results.append(test_mse)

        print(f"Mejores Parámetros -> M: {best_M}, Sigma: {best_sigma:.4f}, Lambda: {best_lambda:.5f}")
        print(f"MSE en Test: {test_mse:.5f}")

        # Guardar en MongoDB Atlas
        run_data = {
            "algorithm": "ssa_rbf",
            "seed": seed,
            "dataset": "california_housing_sample",
            "params": {"M": best_M, "sigma": best_sigma, "lambda": best_lambda},
            "metrics": {"mse": test_mse},
            "evaluations": 15 * 30,
            "convergence": convergence
        }
        db.save_run(run_data)

    print("\n=== RESUMEN ESTADÍSTICO FINAL (10 CORRIDAS) ===")
    print(f"Media del MSE: {np.mean(all_mse_results):.5f}")
    print(f"Desviación Estándar: {np.std(all_mse_results):.5f}")
    print(f"Mediana: {np.median(all_mse_results):.5f}")
    print(f"Mínimo (Mejor): {np.min(all_mse_results):.5f}")
    print(f"Máximo (Peor): {np.max(all_mse_results):.5f}")

if __name__ == "__main__":
    run_rbf_ssa_experiment()