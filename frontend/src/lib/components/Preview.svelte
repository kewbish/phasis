<script lang="ts">
  import CommitsList from "./CommitsList.svelte";

  export let path: string = "";

  const fetchContents = async () => {
    const response = await fetch(
      "http://localhost:5000/contents?path=" + encodeURIComponent(path)
    );
    const json = await response.json();
    return json.contents;
  };
  let fetchData = fetchContents();

  $: {
    if (path !== "") {
      fetchData = fetchContents();
    }
  }
</script>

{#await fetchData}
  <p>Loading...</p>
{:then contents}
  {#key contents}
    <pre>
{contents}
</pre>
  {/key}
  <CommitsList bind:filePath={path} />
{/await}

<style>
  pre {
    font-family: monospace;
    color: dimgrey;
    max-width: 100%;
    overflow-x: scroll;
  }

  * {
    scrollbar-width: auto;
    scrollbar-color: #9fe399 #ffffff;
  }

  *::-webkit-scrollbar {
    height: 10px;
    width: 10px;
  }

  *::-webkit-scrollbar-thumb {
    background-color: #9fe399;
    border-radius: 8px;
  }
</style>
