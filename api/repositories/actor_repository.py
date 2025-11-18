from core.database import favorite_actors_collection
from models import Actor


class ActorRepository:
    @staticmethod
    async def find_favorite_actor(actor_id: int):
        return await favorite_actors_collection.find_one({"id": actor_id})
    
    @staticmethod
    async def insert_favorite_actor(actor_dict: dict):   
        result = await favorite_actors_collection.insert_one(actor_dict)
        return result
   
    @staticmethod
    async def list_favorite_actors(max_rows: int = 5):
        results = await favorite_actors_collection.find({}, {"_id": 0}).to_list(max_rows)        
        return results
    
    @staticmethod
    async def delete_favorite_actor(actor_id: int):
        result = await favorite_actors_collection.delete_one({"id": actor_id})
        return result
    
    

