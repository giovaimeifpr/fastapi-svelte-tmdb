from pydantic import BaseModel, field_validator, Field
from typing import List

class Actor(BaseModel):
      id: int
      name: str
      gender: str | None = None
      birthday: str | None = None
      popularity: float
      profile_path: str | None = None
      known_for_department: str | None = None
      is_favorite: bool = False
      
      
      @field_validator("gender", mode="before")
      def map_gender(cls, v):
            if isinstance(v, int):
                  if v == 1:
                        return "Feminino"
                  elif v == 2:
                        return "Masculino"
                  else:
                        return "Desconhecido"
            return v
      
class ActorSearchResult(BaseModel):
    """Modelo de resposta que inclui a lista de atores e metadados de paginação."""
    
    total_results: int = Field(..., description="Número total de resultados na TMDB para a pesquisa.")
    total_pages: int = Field(..., description="Número total de páginas disponíveis.")
    actors: List['Actor'] = Field(..., description="A lista filtrada de atores (página atual).")