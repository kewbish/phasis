<script lang="ts">
  import { link } from "svelte-routing";
  import EventIcon from "./EventIcon.svelte";

  export let data: Array<[Date, ...Array<string>]> = [];
  export let currentMonth: Date;
  export let gardenPath: String;

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
</script>

<main>
  <div id="main-block">
    <h1>
      <a href="/calendar" use:link>
        ‹ {currentMonth
          .toLocaleDateString("en-US", { month: "long", day: "numeric" })
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
        <ul>
          {#each data as entry}
            <li>
              <span class="dark-green">{shortenedGardenPath}/</span>{entry[1]}
              -
              <EventIcon state={entry[2]} />
            </li>
          {/each}
        </ul>
      </div>
      <div id="file-preview">
        <h1>‹ preview ›</h1>
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
  .dark-green {
    color: #406e45;
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
  }
  #file-preview {
    color: #a4a4a4;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80%;
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
</style>
