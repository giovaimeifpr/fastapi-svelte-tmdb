#!/bin/bash
echo "--- Configuração do Ambiente virtual do Python ---"

# 1. Cria a Pasta de Projetos
PROJECTS_FOLDER="projetos"
if [ ! -d "$PROJECTS_FOLDER" ]; then
    echo "Criando a pasta de trabalho '$PROJECTS_FOLDER'..."
    mkdir "$PROJECTS_FOLDER"
else
    echo "Pasta '$PROJECTS_FOLDER' já existe."
fi

# 2. Cria o Virtual Environment
ENV_FOLDER="env"
if [ ! -d "$ENV_FOLDER" ]; then
    echo "Criando o ambiente virtual '$ENV_FOLDER'..."
    python3 -m venv "$ENV_FOLDER"
else
    echo "Ambiente virtual '$ENV_FOLDER' já existe."
fi

# 3. Ativa o Ambiente Virtual
source "$ENV_FOLDER/bin/activate"
echo "Ambiente virtual '$ENV_FOLDER' ativado."

# 4. Instala as Dependências
REQUIREMENTS_FILE="requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Instalando dependências de '$REQUIREMENTS_FILE'..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
    echo "Instalação de dependências concluída."
else
    echo "AVISO: Arquivo '$REQUIREMENTS_FILE' não encontrado."
    echo "Nenhuma dependência instalada."
fi

echo "--- Setup concluído! ---"
echo "Você agora está dentro do ambiente virtual. Para desativar, digite 'deactivate'."
