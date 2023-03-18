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

  let show_all: boolean = false;
</script>

{#await fetchData}
  <p>Loading...</p>
{:then contents}
  {#key contents}
    <pre>
{show_all
        ? contents
        : contents.substr(0, 350) + (contents.length >= 350 ? "…" : "")}
</pre>
    {#if !show_all}
      <span
        class="dark-green"
        style="margin-top: 0.25rem"
        on:click={() => {
          show_all = true;
        }}
        on:keydown={() => {
          show_all = true;
        }}>(click to show more...)</span
      >
    {/if}
  {/key}
  <CommitsList bind:filePath={path} />
{/await}

<style>
  pre {
    font-family: monospace;
    color: dimgrey;
    max-width: 100%;
    overflow-x: scroll;
    white-space: pre-line;
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
  .dark-green {
    color: #406e45;
  }
</style>
