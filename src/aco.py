# src/aco.py
import numpy as np

class AntColonyTSP:
    def __init__(self, coordinates, n_ants=20, n_iterations=100, alpha=1.0, beta=3.0, rho=0.1, q=100):
        self.coordinates = np.array(coordinates)
        self.n_cities = len(coordinates)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha  # Importancia de la feromona
        self.beta = beta    # Importancia de la visibilidad (distancia inversa)
        self.rho = rho      # Tasa de evaporacion
        self.q = q          # Constante de deposito de feromona
        
        # Calcular matriz de distancias euclidianas (vectorizado)
        if self.n_cities > 0:
            diff = self.coordinates[:, np.newaxis, :] - self.coordinates[np.newaxis, :, :]
            self.distances = np.linalg.norm(diff, axis=-1)
        else:
            self.distances = np.zeros((0, 0))
                
        # Matriz de visibilidad (evitamos divisiones por cero de forma segura)
        self.visibility = np.divide(
            1.0,
            self.distances,
            out=np.zeros_like(self.distances, dtype=float),
            where=(self.distances > 0)
        )

        # Inicializar feromonas
        self.pheromones = np.ones((self.n_cities, self.n_cities)) * 0.1

    def _select_next_city(self, current_city, visited):
        visited_set = set(visited) if not isinstance(visited, set) else visited
        unvisited = [node for node in range(self.n_cities) if node not in visited_set]
        if not unvisited:
            return None
        if len(unvisited) == 1:
            return int(unvisited[0])
        
        # Calcular probabilidades segun la formula de ACO
        tau = self.pheromones[current_city, unvisited] ** self.alpha
        eta = self.visibility[current_city, unvisited] ** self.beta
        probabilities = tau * eta
        
        sum_prob = np.sum(probabilities)
        if sum_prob <= 0 or not np.isfinite(sum_prob):
            # Si hay estancamiento o valores no finitos, elegir al azar entre los no visitados
            return int(np.random.choice(unvisited))
            
        probabilities = probabilities / sum_prob
        probabilities = np.nan_to_num(probabilities, nan=0.0, posinf=0.0, neginf=0.0)
        sum_prob = np.sum(probabilities)
        if sum_prob <= 0:
            return int(np.random.choice(unvisited))
        probabilities /= sum_prob

        return int(np.random.choice(unvisited, p=probabilities))

    def _calculate_path_length(self, path):
        if not path or len(path) <= 1:
            return 0.0
        length = 0.0
        n = len(path)
        for i in range(n):
            length += self.distances[path[i], path[(i + 1) % n]]
        return float(length)

    def run(self):
        if self.n_cities == 0:
            return [], 0.0
        if self.n_cities == 1:
            return [0], 0.0

        best_path = None
        best_length = float('inf')
        
        for iteration in range(self.n_iterations):
            all_paths = []
            all_lengths = []
            
            for ant in range(self.n_ants):
                start_city = int(np.random.randint(0, self.n_cities))
                path = [start_city]
                visited = {start_city}
                
                while len(path) < self.n_cities:
                    next_city = self._select_next_city(path[-1], visited)
                    if next_city is None:
                        break
                    path.append(next_city)
                    visited.add(next_city)
                    
                length = self._calculate_path_length(path)
                all_paths.append(path)
                all_lengths.append(length)
                
                if length < best_length:
                    best_length = length
                    best_path = list(path)
                    
            # Evaporacion de feromonas
            self.pheromones *= (1.0 - self.rho)
            
            # Deposito de nuevas feromonas
            for path, length in zip(all_paths, all_lengths):
                if length <= 0:
                    continue
                deposit = self.q / length
                n = len(path)
                for i in range(n):
                    u = path[i]
                    v = path[(i + 1) % n]
                    self.pheromones[u, v] += deposit
                    self.pheromones[v, u] = self.pheromones[u, v] # Simetria
                    
        return best_path, best_length