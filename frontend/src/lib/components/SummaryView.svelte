<script lang="ts">
  import { link } from "svelte-routing";
  import EventIcon from "./EventIcon.svelte";
  import Preview from "./Preview.svelte";

  export let month: boolean;
  export let returnPath: string = "/calendar";
  export let file: string;

  export let data: Array<[Date, ...Array<string>]> = [];
  let filteredData: Array<[Date, ...Array<string>]> = [];

  export let currentMonth: Date;
  export let gardenPath: String;
  let filter = "";
  let lastClickedPath = file;

  const setLastClickedPath = (path: string) => {
    lastClickedPath = path;
  };

  const FILTER_MAP = {
    CREATE: "🌱",
    MENTION: "🌼",
    SICK: "🥀",
    DEATH: "💀",
  };

  const shortenedGardenPath =
    gardenPath.length > 30
      ? gardenPath.slice(
          0,
          30 - gardenPath.split("\\").pop().split("/").pop().length
        ) +
        (gardenPath
          .slice(0, 30 - gardenPath.split("\\").pop().split("/").pop().length)
          .endsWith("/")
          ? " "
          : "/") +
        gardenPath.split("\\").pop().split("/").pop()
      : gardenPath;

  $: filteredData = data.filter(
    (entry) => !filter || FILTER_MAP[entry[2]] == filter
  );
</script>

<main>
  <div id="main-block">
    <h1>
      <a href={returnPath} use:link>
        ‹ {currentMonth
          .toLocaleDateString("en-US", {
            month: "long",
            ...(!month && { day: "numeric" }),
          })
          .toLowerCase()}

        <span class="dark-green">
          <em>
            {currentMonth.getFullYear()}
          </em>
        </span>
      </a>
    </h1>
    <div id="main-wrapper">
      <div id="files-list">
        <div id="header-picker">
          <p>{month ? "This month" : "That day"}...</p>
          <div id="picker">
            <p
              class={"picker-item" + (filter == "🌱" ? " selected" : "")}
              on:click={() => {
                filter = filter == "🌱" ? "" : "🌱";
              }}
              on:keydown={() => {
                filter = filter == "🌱" ? "" : "🌱";
              }}
            >
              🌱
            </p>
            <p
              class={"picker-item" + (filter == "🌼" ? " selected" : "")}
              on:click={() => {
                filter = filter == "🌼" ? "" : "🌼";
              }}
              on:keydown={() => {
                filter = filter == "🌼" ? "" : "🌼";
              }}
            >
              🌼
            </p>
            <p
              class={"picker-item" + (filter == "🥀" ? " selected" : "")}
              on:click={() => {
                filter = filter == "🥀" ? "" : "🥀";
              }}
              on:keydown={() => {
                filter = filter == "🥀" ? "" : "🥀";
              }}
            >
              🥀
            </p>
            <p
              class={"picker-item" + (filter == "💀" ? " selected" : "")}
              on:click={() => {
                filter = filter == "💀" ? "" : "💀";
              }}
              on:keydown={() => {
                filter = filter == "💀" ? "" : "💀";
              }}
            >
              💀
            </p>
          </div>
        </div>
        <ul>
          {#each filteredData as entry}
            <li
              on:click={() => setLastClickedPath(entry[1])}
              on:keydown={() => setLastClickedPath(entry[1])}
            >
              <span class="dark-green">{shortenedGardenPath}/</span>{entry[1]}
              -
              <EventIcon state={entry[2]} />
            </li>
          {/each}
          {#if !filteredData.length && data.length}
            <p class="dark-green">No {filter}'ed files found.</p>
          {/if}
          {#if !data.length}
            <p class="dark-green">No file events found.</p>
          {/if}
        </ul>
      </div>
      <div id="file-preview" class={lastClickedPath.length ? " flex-top" : ""}>
        {#if !lastClickedPath.length}
          <h1>‹ preview ›</h1>
        {:else}
          <Preview bind:path={lastClickedPath} />
        {/if}
      </div>
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    width: 100vw;
  }
  #main-block {
    width: 80%;
    padding: 5% 0;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  #main-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    padding-top: 20px;
    flex-grow: 1;
  }
  #files-list {
    height: fit-content;
  }
  #file-preview,
  #files-list {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    padding: 24px;
    min-width: 0;
  }
  #file-preview {
    color: #a4a4a4;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 80%;
  }
  .flex-top {
    align-items: start !important;
    height: fit-content !important;
  }
  li {
    margin-left: 24px;
  }
  a {
    text-decoration: none;
    color: black;
    cursor: pointer;
    transition: ease-in-out 0.2s;
  }
  a:hover {
    text-shadow: 2px 1px 1px #28763e75;
  }
  ul {
    padding-top: 8px;
  }
  #header-picker {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  #picker {
    position: relative;
    border-radius: 8px;
    padding: 8px;
    display: flex;
    flex-direction: row;
    gap: 2px;
  }
  #picker::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 8px;
    padding: 2px;
    background: linear-gradient(180deg, #bcecb4 0%, #88d08159 100%),
      linear-gradient(0deg, #e0ffdd, #e0ffdd);
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
  }
  .picker-item {
    z-index: 1;
    cursor: pointer;
    box-sizing: border-box;
    border-bottom: solid 2px transparent;
    transition: ease-in-out 0.2s;
  }
  .selected {
    border-bottom: dotted 2px #406e45;
  }
  li {
    cursor: pointer;
  }
</style>
