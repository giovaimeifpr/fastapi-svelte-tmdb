<script>
    import { onMount } from "svelte";
    import FavoriteActorsCard from "./FavoriteActorsCard.svelte";

    // --- 1. VARIÁVEIS DE ESTADO PARA OS FILTROS ---
    let results = $state(null);
    
    async function getActors() {
    let endpoint = `http://localhost:8000/actors/favorites`;
    const res = await fetch(endpoint);
    const data = await res.json();
    if (res.ok) {
        return data;
    } else {throw new Error(data); }
    }

    function handleActorDeleted(event) {
        // O evento traz o ID do ator deletado (o que foi enviado no dispatch)
        const deletedId = event.detail; 

        // Filtra a lista 'results', criando uma nova lista sem o item deletado
        results = results.filter(actor => actor.id !== deletedId);
        
        // 💡 Vantagem: MUITO MAIS RÁPIDO do que chamar a API novamente!
    }

    // --- 3. FUNÇÃO DE DISPARO ---
    function handleClick() {
        // Chamamos getActors() e atualizamos a variável 'results' com os dados
        getActors().then((data)=>{
            // Somente atualiza 'results' se os dados não forem null/undefined (em caso de erro)
            if (data !== undefined) {
                 results = data;
            }
        });
    }

    onMount(()=>{
  // executa a função quando a página termina de ser carregada
  handleClick()
});

</script>

<button
  onclick={()=>handleClick()}
>Atualizar Favoritos</button>

  <div class="results">
    
     {#if results === null}
        <p>Carregando lista de favoritos...</p>

    {:else if results.length === 0}
        <p>Você não tem nenhum ator favorito salvo na lista. Adicione um!</p>

    {:else}
        {#each results as item}
            <FavoriteActorsCard {item} on:deleted={handleActorDeleted}/>
        {/each}
    {/if}
</div>
<style>

.results {
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    
    /* MUDANÇA CRUCIAL: Define o espaçamento horizontal e vertical */
    gap: 1rem; 
    
    /* Adiciona um padding nas bordas laterais do contêiner, se desejar */
    padding: 1rem; 
}
button {
    margin: 1rem;
    padding: 0.5rem 1rem;
    background-color: rgb(93, 8, 93);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

</style>
