<script>
    import { onMount } from "svelte";
    import ActorsCard from "./ActorsCard.svelte";

    // --- 1. VARIÁVEIS DE ESTADO PARA OS FILTROS ---
    let results = $state(null);
    
    // Variáveis vinculadas aos campos de formulário (inputs)
    let name = $state('');
    let id = $state(''); // Nome do Gênero (ex: "Action")


    // --- 2. FUNÇÃO QUE CONSTRÓI E CHAMA A API ---
    async function getActors() {
        // Constrói a URLSearchParams com base nas variáveis de estado.
        // Isso cuida de formatar os parâmetros de URL (ex: ?title=Batman&genres=Action)
        const params = new URLSearchParams();

        if (name) params.append('name', name);
        if (id) params.append('id', id); 

        // A URL base da sua API
        let endpoint = `http://localhost:8000/actors/search/?${params.toString()}`;
        
        // Exibe a URL no console para debug (opcional)
        console.log("Chamando API com:", endpoint);

        try {
            const res = await fetch(endpoint);
            const data = await res.json();
            
            if (res.ok) {
                return data;
            } else {
                // Trata erros da API, como 404
                throw new Error(data.detail || JSON.stringify(data));
            }
        } catch (error) {
            console.error("Erro ao buscar ator:", error);
            // Você pode limpar os resultados ou definir uma mensagem de erro aqui
            results = []; 
            alert(`Erro na API: ${error.message}`);
        }
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
 
</script>

<div class="filters-container">
    <input type="text" placeholder="Nome do ator" bind:value={name}>
    <input type="text" placeholder="Id do ator" bind:value={id}>
    
    
    <button onclick={handleClick}>Filter Actors</button>
</div>


<div class="results">
    
    {#if results === null}
        <p>Preencha pelo menos um campo de pesquisa...</p>
    {:else if results.length === 0}
        <p>Nenhum ator encontrado com os filtros selecionados.</p>
    {:else}
        {#each results as item}
            <ActorsCard {item}/>
        {/each}
    {/if}   

</div>

<style>
.filters-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;
    align-items: center;
    border-bottom: 1px solid #ccc;
    margin-bottom: 2rem;
}
.results {
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    
    /* MUDANÇA CRUCIAL: Define o espaçamento horizontal e vertical */
    gap: 1rem; 
    
    /* Adiciona um padding nas bordas laterais do contêiner, se desejar */
    padding: 1rem; 
}

</style>
