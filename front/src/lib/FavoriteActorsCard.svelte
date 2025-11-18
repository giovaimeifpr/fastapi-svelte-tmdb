     <script>
        import { createEventDispatcher, onMount } from "svelte";

        
        let {item} = $props();
        let debug = $state(false);
        const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w200';
     
        const dispatch = createEventDispatcher();

        // função para deletar o ator
        async function deleteActor(id) {
        // Confirmação para evitar exclusões acidentais (boa prática)
        if (!confirm(`Tem certeza que deseja remover ${item.name} dos favoritos?`)) {
            return;
        }

        try {
            // 1. Usa o método DELETE
            // 2. Não envia body, pois o ID já está no URL
            const res = await fetch(`http://localhost:8000/actors/delete_favorite/${id}`, {
                method: "DELETE", // <--- CORREÇÃO: Usar DELETE
            });
            
            // Tenta ler o JSON, mas lida com o caso de resposta vazia (204 No Content)
            const data = res.status === 204 ? {} : await res.json(); 

            if (res.ok) {
                // Notifica o sucesso e dispara o evento para o pai atualizar a lista
                alert("Ator removido dos favoritos com sucesso!");                
                dispatch("deleted", item.id); 
            } else {       
                // Exibe o erro retornado pelo FastAPI (ex: 404 Not Found)
                alert ("Erro ao remover: " + JSON.stringify(data.detail || data));
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            alert("Erro na requisição: Verifique o console.");
        }
    }
     
     
    </script>
     
     
     <div class="actor-card"> 
                <p>Id: {item.id}</p> 
                <p>Nome: {item.name}</p>
                <p>Popularidade: {item.popularity}</p>
                <p>Aniversário: {item.birthday || 'Não Informado'}</p>
                <p>Gênero: {item.gender}</p>       
                {#if item.profile_path}
                        <img src="{IMAGE_BASE_URL}{item.profile_path}" alt="{item.name} poster"/>
                    {:else}
                        <p>Pôster do ator não disponível</p>
                {/if}                
           
                <!-- Botão Salvar -->
              <button class="delete-button" onclick={() => deleteActor(item.id)}>Remover dos Favoritos</button>
              
    </div>

    

<style>
/* Estilos do Card (Mantidos e Otimizados) */
.actor-card {
    padding: 0.5rem; 
    border: 1px solid red;
    width: 200px; 
    max-width: 200px; 
    margin-bottom: 1rem;    
    margin-left: 1rem;     
    display: flex; 
    flex-direction: column;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}
img {
    width: 100%; 
    height: auto;
    margin-bottom: 0.5rem;
}
p {
    font-size: 0.8rem; 
    margin: 0.2rem 0; 
    line-height: 1.2;
}

.delete-button {
    margin-top: auto; 
    padding: 0.5rem; 
    background-color: #b80e0e; 
    color: white; 
    border: none; 
    border-radius: 4px; 
    cursor: pointer; 
    font-size: 0.9rem; 
}


</style>