# src/db.py
import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

class MongoManager:
    def __init__(self, uri=None, db_name="biooptimization_db", collection_name="runs"):
        # Si no se pasa una URI, la lee del archivo .env o usa localhost por defecto
        if uri is None:
            uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
            
        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Forzar prueba de conexión con Atlas
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            self.connected = True
            print("[Éxito] Conexión establecida con MongoDB Atlas correctamente.")
        except Exception as e:
            print(f"[Advertencia] No se pudo conectar a MongoDB ({e}). Los resultados se guardarán solo de manera local.")
            self.connected = False

    def save_run(self, data):
        """Guarda un documento con los resultados de la corrida."""
        if not self.connected:
            return None
            
        document = {
            "algorithm": data.get("algorithm"),
            "seed": data.get("seed"),
            "dataset": data.get("dataset"),
            "params": data.get("params"),
            "metrics": data.get("metrics"),
            "evaluations": data.get("evaluations"),
            "convergence": data.get("convergence"),
            "timestamp": datetime.utcnow().isoformat()
        }
        result = self.collection.insert_one(document)
        return result.inserted_id