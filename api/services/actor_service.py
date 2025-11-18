from fastapi import HTTPException
import requests
from models import Actor
from core.database import TOKEN
from repositories.actor_repository import ActorRepository


def get_json(url: str, params: dict = None) -> dict:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    data = requests.get(url, headers=headers, params=params)
    return data.json()

class ActorService:
        
    @staticmethod
    def get_actor_by_id(person_id: int) -> Actor | None:
        """Busca os detalhes de um único ator por ID."""
        url = f"https://api.themoviedb.org/3/person/{person_id}"        
        
        try:
            data = get_json(url)
        except requests.exceptions.HTTPError as e:
            # Se o ID não for encontrado (404), a exceção é tratada aqui.
            if e.response.status_code == 404:
                return None
            raise # Relança outros erros
            
        # TMDB retorna o objeto do ator diretamente, sem um campo 'results'.
        return Actor.model_validate(data) if data else None
    
    @staticmethod
    def search_actors(name: str = None, person_id: int = None) -> list['Actor']:
        
        # 1. PRIORIDADE MÁXIMA: BUSCA POR ID
        # Se um ID for fornecido (mesmo que o nome também seja), executa a busca por ID e ignora o nome.
        if person_id is not None:
            actor_details = ActorService.get_actor_by_id(person_id)
            
            # Retorna o único ator encontrado em uma lista (ou lista vazia se não encontrado)
            return [actor_details] if actor_details else []
            
        # 2. SEGUNDA PRIORIDADE: BUSCA POR NOME
        # Executa apenas se o ID não foi fornecido OU se o ID for None.
        elif name and name.strip():
            
            # LÓGICA: Busca por Nome
            url = "https://api.themoviedb.org/3/search/person"
            params = {
                "query": name.strip(), 
                "language": "en-US",
                "page": 1
            }
            
            data = get_json(url, params)
            results = data.get("results", [])
            
            return [Actor.model_validate(actor) for actor in results]

        # 3. NENHUM CRITÉRIO ATINGIDO
        else:
            return []
        
    @staticmethod
    async def save_favorite_actor(actor: Actor):
        # 1. (Lógica de Negócio) Checar existência:
        existing = await ActorRepository.find_favorite_actor(actor.id)
        
        if existing:
            # 2. (Lógica de Negócio) Lançar exceção padronizada
            raise HTTPException(status_code=409, detail="Ator já existe na sua lista de favoritos.") # 409 Conflict é melhor que 200 OK
        
        actor_dict = actor.model_dump()  # Converte o modelo Pydantic em um dicionário
        # 3. (Coordenação) Chamar o Repositório para inserir
        result = await ActorRepository.insert_favorite_actor(actor_dict)
        
        return {"message": "Ator salvo com sucesso!", "inserted_id": str(result.inserted_id)}
    
    @staticmethod
    async def delete_favorite_actor(actor_id: int):
        """Coordena a deleção e trata o caso de 'não encontrado'."""        
        # 1. Chama o Repositório
        result = await ActorRepository.delete_favorite_actor(actor_id)
        
        # 2. Lógica de Negócio: Verificar se algo foi deletado
        if result.deleted_count == 0:
            # 3. Lança a exceção HTTP 404 se nada foi afetado
            raise HTTPException(
                status_code=404, 
                detail=f"Ator com ID {actor_id} não encontrado na sua lista de favoritos."
            )        
        # 4. Retorna a mensagem de sucesso (status 200/204)
        return {"message": "Ator removido com sucesso."}
    
    @staticmethod
    async def list_favorite_actors(max_rows: int = 5):
        # Chamar o Repositório para listar
        results = await ActorRepository.list_favorite_actors(max_rows)
        return results