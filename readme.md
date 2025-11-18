ARQUIVO README - MICROSERVIÇO FASTAPI + SVELTE

Este documento explica como configurar e executar o projeto de microserviço que integra FastAPI, Pydantic, MongoDB e as APIs externas TMDB.

==================================================
I. PRÉ-REQUISITOS E CONFIGURAÇÃO INICIAL
==================================================

Você precisa das seguintes contas e ferramentas:
- Python 3.9+
- Node.js e npm
- Conta no TMDB para o Access Token.
- Conta no MongoDB Atlas para a URI de conexão.

1. CONFIGURAÇÃO DO BACKEND (PYTHON / FASTAPI)

    a. Ambiente Virtual: Crie e ative o ambiente virtual (ex: 'env').
       (Linux/macOS): source env/bin/activate
       O script install_venv.sh funciona no linux para criar o env e instalar
       as bibliotecas, rodar sem o sudo.

    b. Dependências: Instale as bibliotecas listadas no 'requirements.txt'.
       pip install -r requirements.txt

    c. Arquivo .env: Crie um arquivo .env na pasta raiz do projeto com suas credenciais:
       TMDB_TOKEN="SEU_TMDB_API_ACCESS_TOKEN_AQUI"
       MONGO_URI="SUA_STRING_DE_CONEXAO_DO_MONGODB_AQUI"

2. CONFIGURAÇÃO DO MONGODB (ATLAS)

    a. Autorização de IP: Acesse o Dashboard do MongoDB Atlas, vá em 'Security' -> 'Network Access'.
    b. Adicione seu IP: Adicione o seu endereço IP público atual à lista de acesso para permitir que o backend se conecte.

3. CONFIGURAÇÃO DO FRONTEND (SVELTE)

    a. Módulos: Navegue até a pasta do frontend no terminal e instale os módulos Node.js.
       npm install

==================================================
II. EXECUÇÃO DAS APLICAÇÕES
==================================================

1. INICIAR BACKEND (FASTAPI)
   Rode este comando na raiz do projeto (com o ambiente Python ativado):
   uvicorn main:app --reload

2. INICIAR FRONTEND (SVELTE)
   Rode este comando dentro da pasta do frontend:
   npm run dev

==================================================
III. ESTRUTURA E MICROSERVIÇOS
==================================================

O backend segue o padrão MVCR (Model-View-Controller-Repository).

CAMADAS DO BACKEND:

- MODEL (models.py): Define schemas de dados (Pydantic), garantindo a estrutura e validação (ex: Actor, Movie).
- REPOSITORY (actor_repository.py): Lida com o I/O (Input/Output). Contém as funções de baixo nível do MongoDB (find_one, insert_one, delete_one).
- SERVICE (actor_service.py): Contém a Lógica de Negócio (ex: verificar se ator já existe, tratar 404/409, traduzir IDs).
- CONTROLLER/ENDPOINT (main.py): Define as rotas URL e o método HTTP (GET, POST, DELETE).

PRINCIPAIS ENDPOINTS:

- GET /actors/trending: Busca atores mais populares (trending).
- GET /actors/search: Pesquisa atores por nome (ou ID).
- GET /actors/favorites: Retorna a lista de favoritos do MongoDB.
- POST /actors/save_favorite: Salva um ator no MongoDB (lança 409 se já existir).
- DELETE /actors/delete_favorite/{id}: Remove um ator do MongoDB (lança 404 se não existir).

FRONTEND (SVELTE):

O frontend utiliza dois componentes principais para exibição de favoritos:
1. Componente Pai (Ex: FavoriteActor): Responsável por buscar a lista completa (fetch) e gerenciar o array de resultados.
2. Componente Filho (Ex: FavoriteActorCard): Recebe o objeto do ator via 'props', exibe os detalhes e contém o botão 'Remover'.
A atualização da lista