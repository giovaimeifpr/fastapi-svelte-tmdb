#!/bin/bash
echo "--- Configuração do Ambiente Python da CAROLICIA ---"

if ! command -v python3 &> /dev/null
then
    echo "ERRO: O comando 'python3' não foi encontrado. Tentando instalar..."
    
    # Tenta instalar o Python 3 via APT (padrão em Debian/Ubuntu)
    if command -v apt-get &> /dev/null
    then
        echo "Usando 'sudo apt-get install' para instalar Python 3. Isso requer privilégios de administrador (sudo)."
        
        # O script VAI PARAR aqui e pedir a senha do sudo se necessário.
        sudo apt-get update && sudo apt-get install -y python3 python3-venv
        
        # Verifica novamente após a instalação
        if [ $? -ne 0 ] || ! command -v python3 &> /dev/null; then
            echo "ERRO CRÍTICO: Falha na instalação do Python 3 ou permissão negada."
            echo "O ambiente não pode ser configurado sem o Python 3. Saindo."
            exit 1
        fi
        echo "✅ Python 3 instalado com sucesso."
    else
        echo "ERRO CRÍTICO: Python 3 não encontrado e 'apt-get' não está disponível para instalação automática."
        echo "Por favor, instale o Python 3 manualmente."
        exit 1
    fi
fi

echo "✅ Python 3 encontrado: $(python3 --version)"


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