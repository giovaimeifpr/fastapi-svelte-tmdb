from pydantic import BaseModel, field_validator

class Actor(BaseModel):
      id: int
      name: str
      gender: str | None = None
      birthday: str | None = None
      popularity: float
      profile_path: str | None = None
      
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