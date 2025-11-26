<script>
    import { onMount } from "svelte";
    import ActorsCard from "./ActorsCard.svelte";

    // --- 1. VARIÁVEIS DE ESTADO PARA OS FILTROS ---
    let searchResponse = $state(null);
    
    // Variáveis vinculadas aos campos de formulário (inputs)
    let name = $state('');
    let id = $state(''); // Nome do Gênero (ex: "Action")
    let page = $state(''); // Página de resultados (ex: 1, 2, 3...)


    // --- 2. FUNÇÃO QUE CONSTRÓI E CHAMA A API ---
    async function getActors() {
        // Constrói a URLSearchParams com base nas variáveis de estado.
        // Isso cuida de formatar os parâmetros de URL (ex: ?title=Batman&genres=Action)
        const params = new URLSearchParams();

        if (name) params.append('name', name);
        if (id) params.append('person_id', id); 
        if (page) params.append('page', page);

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
            searchResponse = {total_results: 0, total_pages: 0, actors: []};
            alert(`Erro na API: ${error.message}`);
        }
    }

    // --- 3. FUNÇÃO DE DISPARO ---
    function handleClick() {
        page = 1; // Reseta para a primeira página a cada nova busca
        // Chamamos getActors() e atualizamos a variável 'results' com os dados
        getActors().then((data)=>{
            // Somente atualiza 'results' se os dados não forem null/undefined (em caso de erro)
            if (data !== undefined) {
                searchResponse = data;
            }
        });
    }
    function handlePageChange() {
        // Dispara a busca com o novo valor de 'page' que já foi definido pelo 'bind:value'.
        getActors().then((data)=>{
            if (data !== undefined) {
                 searchResponse = data;
            }
        });
    }
    
 
</script>

<div class="filters-container">
    <input type="text" placeholder="Nome do ator" bind:value={name}>
    <input type="text" placeholder="Id do ator" bind:value={id}>
    
    <select bind:value={page} onchange={handlePageChange}>
        <option value="" disabled selected>Página</option>
        {#if searchResponse && searchResponse.total_pages > 0}
            {#each Array(searchResponse.total_pages) as _, index}
                <option value={index + 1}>{index + 1}</option>
            {/each}
        {/if}
    </select>
    
    <button onclick={handleClick}>Filter Actors</button>
</div>


<div class="results">
    
    {#if searchResponse === null}
        <p>Preencha pelo menos um campo de pesquisa...</p>
    {:else}
        <p class="total-info">
            Total de resultados para sua pesquisa: {searchResponse.total_results}
            <br>
            Exibindo {searchResponse.actors.length} resultados nesta página.
            <br>
            Página atual: {page || 1} de {searchResponse.total_pages}
        </p>
        
        {#if searchResponse.actors.length === 0}
            <p>Nenhum ator encontrado com os filtros selecionados.</p>
        {:else}
            <div class="actor-cards-container">
                {#each searchResponse.actors as item}
                    <ActorsCard {item}/>
                {/each}
            </div>
        {/if}   
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
}
.results {
    display: block; 
    padding: 1rem;
}

.total-info {
    width: 100%; 
    margin-bottom: 1.5rem; /* Adiciona espaço abaixo do texto de resumo */
    padding: 0 1rem;
    line-height: 1.6; /* Melhora a leitura das linhas quebradas */
}

/* NOVO: A classe que realmente fará os cards ficarem lado a lado */
.actor-cards-container {
    display: flex; /* Ativa o Flexbox */
    flex-wrap: wrap; /* Permite que os cards quebrem para a próxima linha */
    gap: 1rem; /* Define o espaçamento entre os cards */
    padding: 0 1rem; /* Mantém o padding lateral */
}

</style>
