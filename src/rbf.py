# src/rbf.py
import numpy as np
from sklearn.cluster import KMeans

class RBFRegression:
    def __init__(self, M=10, sigma=1.0, reg_lambda=0.01):
        self.M = M                  # Numero de centros
        self.sigma = sigma          # Ancho (spread) de la funcion gaussiana
        self.reg_lambda = reg_lambda # Parametro de regularizacion (Ridge)
        self.centers = None
        self.weights = None
        self.y_ndim = 1

    def _gaussian_kernel(self, X, centers):
        """Calcula la matriz de activaciones usando la funcion base radial gaussiana."""
        # X shape: (N, features), centers shape: (M, features)
        # Distancias euclidianas al cuadrado directas (sin calcular raiz para luego elevar al cuadrado)
        diff = X[:, np.newaxis, :] - centers[np.newaxis, :, :]
        distances_sq = np.sum(diff ** 2, axis=-1)
        safe_sigma = max(float(self.sigma), 1e-8)
        return np.exp(-distances_sq / (2.0 * (safe_sigma ** 2)))

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)

        # Asegurar formato 2D para X
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        self.y_ndim = y.ndim
        if y.ndim == 1:
            y = y.reshape(-1, 1)

        # Asegurar que M no sea mayor que el numero de muestras
        n_samples = X.shape[0]
        actual_M = min(self.M, n_samples)
        
        # Seleccionar centros usando K-Means
        kmeans = KMeans(n_clusters=actual_M, n_init=10, random_state=42)
        kmeans.fit(X)
        self.centers = kmeans.cluster_centers_
        self.M = actual_M

        # Construir matriz de diseno G (kernel matrix)
        G = self._gaussian_kernel(X, self.centers)
        
        # Agregar columna de sesgo (bias)
        G_bias = np.hstack([G, np.ones((n_samples, 1))])

        # Regularizacion de Ridge: W = (G^T G + lambda * I)^(-1) G^T y
        n_weights = G_bias.shape[1]
        I = np.eye(n_weights)
        I[-1, -1] = 0.0  # No penalizar el sesgo
        
        # Resolver pesos analiticamente usando pseudoinversa
        A = G_bias.T @ G_bias + self.reg_lambda * I
        self.weights = np.linalg.pinv(A) @ G_bias.T @ y

    def predict(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        n_samples = X.shape[0]
        G = self._gaussian_kernel(X, self.centers)
        G_bias = np.hstack([G, np.ones((n_samples, 1))])
        predictions = G_bias @ self.weights

        if self.y_ndim == 1:
            return predictions.ravel()
        return predictions

    def evaluate_mse(self, X, y):
        predictions = self.predict(X)
        y_arr = np.asarray(y, dtype=float)
        if self.y_ndim == 1:
            y_arr = y_arr.ravel()
        return float(np.mean((y_arr - predictions) ** 2))