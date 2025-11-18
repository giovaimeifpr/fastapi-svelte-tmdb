import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv

# carrega variáveis de ambiente (.env)
load_dotenv(find_dotenv(".env"))
MONGODB_URL = os.environ["MONGODB_URL"]
TOKEN = os.environ["TMDB_TOKEN"]

# cria cliente Mongo
client = AsyncIOMotorClient(MONGODB_URL)

# seleciona o banco padrão
db = client.sample_mflix

# aqui você já pode expor collections específicas, se quiser:
favorite_actors_collection = db.get_collection("favorite_actors")


