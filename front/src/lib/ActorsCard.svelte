     <script>
        import { createEventDispatcher } from "svelte";

        
        let {item} = $props();
        let debug = $state(false);
        const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w200';
     
        const dispatch = createEventDispatcher();

        // função para salvar o ator
        async function saveActor() {
            try {
                const res = await fetch("http://localhost:8000/actors/save_favorite", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(item)
                });
                const data = await res.json();
                if (res.ok) {
                    alert("Ator salvo com sucesso!");
                    dispatch("saved", item); // dispara evento para o parent, se quiser usar
                } else {       
                    alert ("Erro ao salvar: " + JSON.stringify(data));
                }
            } catch (error) {
                console.error(error);
                alert("Erro na requisição: " + error.message);
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
              <button class="save-button" onclick={saveActor}>Favoritar</button>
              
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

.save-button {
    margin-top: auto; 
    padding: 0.5rem; 
    background-color: #28a745; 
    color: white; 
    border: none; 
    border-radius: 4px; 
    cursor: pointer; 
    font-size: 0.9rem; 
}


</style>