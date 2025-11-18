<script>
import "../app.css"
let {children} = $props();
</script>

<main>
  <header>
    <h1><a href={`/`}>app</a></h1>
		<nav>
			<a href={`/actors`}>Actors</a>
      <a href={`/favorite_actors`}>Favorite Actors</a>
	
		</nav>
  </header>

	{@render children?.()}

</main>

<style>
  header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #1a1a1a;
  color: #dcdcdc;
  font-family: "Roboto", sans-serif;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

header h1 {
  font-size: 1.5rem;
  margin: 0;
}

header h1 a, 
header h1 a:visited {
  color: #ffffff;
  text-decoration: none;
}

header nav {
  display: flex;
  gap: 20px;
}

header nav a, 
header nav a:visited {
  color: #dcdcdc;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease-in-out;
}

header nav a:hover {
  color: #5dade2;
  text-decoration: underline;
}

/* Opcional: Efeito de 'botão' nos links */
header nav a {
  padding: 5px 10px;
  border-radius: 5px;
}

header nav a:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>