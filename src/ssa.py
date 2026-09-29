# src/ssa.py
import numpy as np

def rastrigin_function(x):
    """Funcion objetivo de Rastrigin (minimo global en x = [0, ..., 0] con f(x) = 0)."""
    x = np.asarray(x)
    n = len(x)
    A = 10
    return float(A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x)))

class SalpSwarmAlgorithm:
    def __init__(self, objective_func, dim, n_salps=30, max_iter=100, lb=-5.12, ub=5.12):
        self.objective_func = objective_func
        self.dim = dim          # Numero de dimensiones (variables)
        self.n_salps = n_salps  # Cantidad de salpas en el enjambre
        self.max_iter = max_iter
        self.lb = np.asarray(lb)  # Limite inferior del espacio de busqueda
        self.ub = np.asarray(ub)  # Limite superior del espacio de busqueda

    def optimize(self):
        # Inicializar las posiciones de las salpas aleatoriamente dentro de los limites
        salp_positions = np.random.uniform(self.lb, self.ub, (self.n_salps, self.dim))
        
        # Encontrar la mejor fuente de alimento (food position)
        food_position = np.zeros(self.dim)
        food_fitness = float('inf')

        # Evaluar poblacion inicial
        for i in range(self.n_salps):
            fitness = self.objective_func(salp_positions[i])
            if fitness < food_fitness:
                food_fitness = fitness
                food_position = salp_positions[i].copy()

        convergence_curve = []

        # Ciclo principal de iteraciones
        for iteration in range(self.max_iter):
            # Coeficiente c1 disminuye adaptativamente a lo largo de las iteraciones
            c1 = 2.0 * np.exp(-((4.0 * iteration / self.max_iter) ** 2))

            for i in range(self.n_salps):
                if i == 0:
                    # Actualizar la posicion del lider en todas las dimensiones
                    c2 = np.random.rand(self.dim)
                    c3 = np.random.rand(self.dim)
                    step = c1 * ((self.ub - self.lb) * c2 + self.lb)
                    salp_positions[0] = np.where(c3 >= 0.5, food_position + step, food_position - step)
                else:
                    # Actualizar la posicion de los seguidores en todas las dimensiones
                    salp_positions[i] = 0.5 * (salp_positions[i] + salp_positions[i - 1])

                # Aplicar restricciones de limites (bounds)
                salp_positions[i] = np.clip(salp_positions[i], self.lb, self.ub)

                # Evaluar nueva posicion
                fitness = self.objective_func(salp_positions[i])
                if fitness < food_fitness:
                    food_fitness = fitness
                    food_position = salp_positions[i].copy()

            convergence_curve.append(food_fitness)

        return food_position, food_fitness, convergence_curve