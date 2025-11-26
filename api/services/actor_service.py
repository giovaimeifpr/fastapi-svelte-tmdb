from fastapi import HTTPException
import httpx
from models import Actor
from core.database import TOKEN
from repositories.actor_repository import ActorRepository


async def get_json(url: str, params: dict = None) -> dict:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        # Use await para a requisição de rede
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status() # Lança erro para status 4xx/5xx
        return response.json()

class ActorService:
        
    @staticmethod
    async def get_actor_by_id(person_id: int) -> dict | None:
      
        url = f"https://api.themoviedb.org/3/person/{person_id}"        
        
        try:
            # Assume que get_json é async e usa httpx
            data = await get_json(url) 
            
            # Retorna o dicionário bruto para a validação externa
            return data
            
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            
            if status_code == 404:
                # Retorna None para IDs não encontrados, conforme esperado pelo Service
                return None
            
            # Relança qualquer outro erro HTTP (401, 500, etc.)
            raise e
            
        except Exception as e:
            # Captura erros inesperados (rede, JSON malformado, etc.)
            # Para manter o fluxo limpo, retorna None e o Service lida com o erro
            # (Você pode relançar se for um erro crítico não esperado)
            return None
   
    @staticmethod
    async def search_actors(name: str = None, person_id: int = None, page: int = 1 ) -> dict:
        
        # 1. PRIORIDADE MÁXIMA: BUSCA POR ID
        # Se um ID for fornecido (mesmo que o nome também seja), executa a busca por ID e ignora o nome.
        if person_id is not None:
            actor_details = await ActorService.get_actor_by_id(person_id)
            print(f"Detalhes do ator recebidos: {actor_details}")
            
            if not actor_details:
                return {
                    "total_results": 0,
                    "total_pages": 0,
                    "actors": []
                    }
            
            actor_obj = Actor.model_validate(actor_details)
            is_in_favorites = await ActorRepository.find_favorite_actor(actor_obj.id)
            actor_obj.is_favorite = bool(is_in_favorites)
            
            # Retorna o único ator encontrado em uma lista (ou lista vazia se não encontrado)
            return {
                "total_results": len([actor_obj]),
                "total_pages": 1,
                "actors": [actor_obj]
            }
            
        # 2. SEGUNDA PRIORIDADE: BUSCA POR NOME
        # Executa apenas se o ID não foi fornecido OU se o ID for None.
        elif name and name.strip():
            
            # LÓGICA: Busca por Nome
            url = "https://api.themoviedb.org/3/search/person"
            params = {
                "query": name.strip(), 
                "language": "en-US",
                "page": page
            }
            
            data = await get_json(url, params) # Assumindo get_json agora é async
            results = data.get("results", [])
            total_results = data.get("total_results", 0)
            total_pages = data.get("total_pages", 0)
            
            # Filtragem inicial "known_for_department": "Acting"
            filtered_tmdb_results = [
                actor for actor in results if actor.get("known_for_department") == "Acting"
            ]
            
            # --- OTIMIZAÇÃO: BUSCA PARALELA NO MONGODB ---
            
            # 1. Pega todos os IDs dos atores filtrados
            actor_ids = [actor.get("id") for actor in filtered_tmdb_results if actor.get("id")]
            
            # 2. Se houver IDs, busca o status de favorito no MongoDB em lote
            if actor_ids:
                favorite_actors_raw = await ActorRepository.find_multiple_favorite_actors(actor_ids)
                # Cria um set para checagem O(1)
                favorite_ids = {a.get("id") for a in favorite_actors_raw}
            else:
                favorite_ids = set()

            # --- PROCESSAMENTO E ENRIQUECIMENTO ---
            
            actors = []
            for actor_data in filtered_tmdb_results:
                actor_obj = Actor.model_validate(actor_data)
                
                # Checa o status de favorito usando o SET (instantâneo)
                if actor_obj.id in favorite_ids:
                    actor_obj.is_favorite = True
                
                actors.append(actor_obj)
            
            return {
                "total_results": total_results,
                "total_pages": total_pages,
                "actors": actors
            }
        
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