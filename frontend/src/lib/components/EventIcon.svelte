<script lang="ts">
  export let state: String = "";
</script>

<span class="tooltip">
  {#if state == "CREATE"}🌱
  {:else if state == "MENTION"}
    🌼
  {:else if state == "SICK"}🥀
  {:else}
    💀
  {/if}
  <span class="tooltiptext">
    {#if state == "CREATE"}The file was created.
    {:else if state == "MENTION"}
      This date was mentioned in the file.
    {:else if state == "SICK"}The file hasn't been updated in a while.
    {:else}
      The file is considered dormant.
    {/if}
  </span>
</span>

<style>
  .tooltip {
    position: relative;
    display: inline-block;
    border-bottom: dotted 2px #406e45;
    transition: ease-in-out 0.2s;
    text-shadow: none;
  }

  .tooltip > .tooltiptext {
    visibility: hidden;
    width: max-content;
    background-color: #406e45;
    color: #fff;
    text-align: center;
    padding: 8px 4px;
    border-radius: 8px;
    position: absolute;
    z-index: 1;
    margin-top: -40%;
    margin-left: 8px;
  }

  .tooltip:hover {
    text-shadow: 2px 1px 1px #abd7b875;
    border-color: #abd7b875;
  }

  .tooltip:hover > .tooltiptext {
    visibility: visible;
    text-shadow: none;
  }

  .tooltip .tooltiptext::after {
    content: " ";
    position: absolute;
    top: 50%;
    right: 100%;
    margin-top: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent #406e45 transparent transparent;
  }

  .tooltip .tooltiptext {
    opacity: 0;
    transition: opacity 1s;
  }

  .tooltip:hover .tooltiptext {
    opacity: 1;
  }
</style>
