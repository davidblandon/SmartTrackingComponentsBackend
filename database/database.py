import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

if not MONGO_URI:
    raise ValueError("Not .env variable MONGO_URI")

try:
    print(client.list_database_names())
    print("Conexión exitosa 👍")
except Exception as e:
    print("Error de conexión:", e)


db = client.get_database("AURORA_Smart_Tracking")

