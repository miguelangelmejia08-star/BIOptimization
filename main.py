# main.py
import numpy as np
from src.aco import AntColonyTSP
from src.ssa import SalpSwarmAlgorithm, rastrigin_function

def nearest_neighbor_tsp(coordinates):
    """Heuristica del Vecino Mas Cercano como linea base."""
    n_cities = len(coordinates)
    
    # Matriz de distancias euclidianas vectorizada
    diff = coordinates[:, np.newaxis, :] - coordinates[np.newaxis, :, :]
    distances = np.linalg.norm(diff, axis=-1)
            
    current_city = int(np.random.randint(0, n_cities))
    visited = {current_city}
    path = [current_city]
    
    while len(visited) < n_cities:
        unvisited = [j for j in range(n_cities) if j not in visited]
        next_city = min(unvisited, key=lambda j: distances[current_city, j])
        visited.add(next_city)
        path.append(next_city)
        current_city = next_city
        
    # Calcular longitud total del trayecto cerrado
    total_length = sum(distances[path[i], path[(i + 1) % n_cities]] for i in range(n_cities))
        
    return path, float(total_length)

def ejercicio_1_tsp():
    """Ejercicio 1: Optimizacion de TSP con ACO vs Vecino Mas Cercano."""
    np.random.seed(42)

    n_cities = 15
    coordinates = np.random.rand(n_cities, 2) * 100

    print("=== EJERCICIO 1: COMPARACION DE ALGORITMOS PARA EL TSP (15 CIUDADES) ===\n")

    # 1. Ejecutar Heuristica del Vecino Mas Cercano
    nn_path, nn_length = nearest_neighbor_tsp(coordinates)
    print("[Linea Base] Vecino Mas Cercano:")
    print(f"  - Ruta: {nn_path}")
    print(f"  - Distancia Total: {nn_length:.4f}\n")

    # 2. ACO - Configuracion 1 (Alta importancia de visibilidad)
    print("[ACO] Configuracion 1 (Alfa=1.0, Beta=4.0, Rho=0.1):")
    aco_1 = AntColonyTSP(coordinates, n_ants=20, n_iterations=100, alpha=1.0, beta=4.0, rho=0.1)
    path_1, length_1 = aco_1.run()
    print(f"  - Ruta: {path_1}")
    print(f"  - Distancia Total: {length_1:.4f}\n")

    # 3. ACO - Configuracion 2 (Mayor peso a feromona y evaporacion rapida)
    print("[ACO] Configuracion 2 (Alfa=3.0, Beta=2.0, Rho=0.3):")
    aco_2 = AntColonyTSP(coordinates, n_ants=20, n_iterations=100, alpha=3.0, beta=2.0, rho=0.3)
    path_2, length_2 = aco_2.run()
    print(f"  - Ruta: {path_2}")
    print(f"  - Distancia Total: {length_2:.4f}\n")

    print("=== Ejercicio 1 completado con exito ===\n")

def test_ssa_rastrigin():
    """Ejercicio 2: Algoritmo Salp Swarm Algorithm (SSA) para Rastrigin."""
    np.random.seed(42)

    print("=== EJERCICIO 2: SSA MINIMIZANDO FUNCION DE RASTRIGIN ===\n")
    
    dim = 5  # 5 dimensiones de prueba
    ssa = SalpSwarmAlgorithm(
        objective_func=rastrigin_function,
        dim=dim,
        n_salps=30,
        max_iter=100,
        lb=-5.12,
        ub=5.12
    )

    best_pos, best_fit, convergence = ssa.optimize()
    
    print(f"Mejor valor de fitness encontrado: {best_fit:.6f}")
    print(f"Posicion optima (cercana a ceros): {best_pos}")
    print(f"Evolucion de fitness: {convergence[0]:.4f} -> {convergence[-1]:.4f}")
    print(f"Longitud de la curva de convergencia guardada: {len(convergence)} iteraciones\n")
    print("=== Ejercicio 2 completado con exito ===")

if __name__ == "__main__":
    # Puedes descomentar para ejecutar ambos secuencialmente:
    # ejercicio_1_tsp()
    test_ssa_rastrigin()