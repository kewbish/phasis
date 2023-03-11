<script lang="ts">
  export let filePath: string;

  const fetchContents = async () => {
    const response = await fetch(
      `http://localhost:5000/commits?path=${encodeURIComponent(filePath)}`
    );
    const json = await response.json();
    return json.diffs;
  };

  const fetchChatGPT = async () => {
    const response = await fetch(
      `http://localhost:5000/fetch_commit?path=${encodeURIComponent(
        filePath
      )}&commit=${currentSha}`
    );
    const json = await response.json();
    chatGPTResponse = json.message;
    document.getElementById(currentSha).innerHTML = currentSha.substring(0, 6);
    return json.message;
  };

  let currentSha: string = "";
  let chatGPTResponse: string = "";

  let fetchData = fetchContents();

  $: {
    if (currentSha != "") {
      fetchChatGPT();
    }
  }

  const setSha = (sha: str) => {
    currentSha = sha;
    document.getElementById(sha).innerHTML =
      '<div class="lds-dual-ring"></div>';
  };
</script>

<div>
  <div class="flex-commits">
    {#await fetchData}
      <p>Loading...</p>
    {:then data}
      {#each data as diff}
        <div
          class="circle"
          on:click={() => setSha(diff.sha)}
          on:keydown={() => setSha(diff.sha)}
          id={diff.sha}
        >
          {diff.sha.substring(0, 6)}
        </div>
      {/each}
    {:catch error}
      <p>Error! {error}</p>
    {/await}
  </div>
  {#if chatGPTResponse}
    <hr style="border-top: 1px solid #406e45; margin-top: 1rem" />
    <p class="dark-green" style="padding-top: 0.5rem">
      <em>{chatGPTResponse}</em>
    </p>
  {/if}
</div>

<style>
  .circle {
    background: #ffffff;
    box-shadow: 1px 1px 5px #bcecb4;
    border-radius: 16px;
    width: fit-content;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    transition: ease-in-out 0.2s;
    padding: 0 0.5rem;
  }
  .circle:hover {
    box-shadow: rgba(9, 186, 58, 0.3) 2px 4px 4px;
    background-color: #f5fff5;
  }
  .flex-commits {
    display: flex;
    gap: 1rem;
    padding-top: 1rem;
    width: fit-content;
  }
</style>
