from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from services.actor_service import ActorService
from repositories.actor_repository import ActorRepository
from models import Actor



app = FastAPI()

origins = [
 "http://localhost",
 "http://localhost:*",
 "http://localhost:5173",
]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)


@app.get("/actors/search")
def search_actors(name: str = None, person_id: int = None):
    return ActorService.search_actors(name, person_id)

@app.post("/actors/save_favorite", status_code=status.HTTP_201_CREATED)  
async def save_actor(actor: Actor):
    # Chama apenas o Service, delegando toda a lógica e I/O para as camadas abaixo.
    return await ActorService.save_favorite_actor(actor)

@app.get ("/actors/favorites")
async def list_favorite_actors(max_rows: int = 5):
    return await ActorService.list_favorite_actors(max_rows)

@app.delete("/actors/delete_favorite/{actor_id}")
async def delete_favorite_actor(actor_id: int):
    return await ActorService.delete_favorite_actor(actor_id) 
    

