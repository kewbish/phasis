<script lang="ts">
  import InfiniteScroll from "svelte-infinite-scroll";

  export let currentMonth: Date = new Date();

  let page = 0;
  let size = 3;
  let timelineData = [];
  export let monthData: Array<[Date, ...Array<String>]> = [];

  $: timelineData = [
    ...timelineData,
    ...monthData.splice(size * page, size * (page + 1) - 1),
  ];
</script>

<main>
  <h1>
    {currentMonth
      .toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
      })
      .toLowerCase()}
    <span class="dark-green">
      <em>
        {currentMonth.getFullYear()}
      </em>
    </span>
  </h1>
  <div id="timeline">
    {#each timelineData as entry}
      <div class="entry">
        <div class="entry-header">
          <h3>{entry[1]}</h3>
        </div>
        <div class="vl" />
        <div class="hl" />
        <div class="entry-info">
          <h3>‹ {entry} ›</h3>
        </div>
      </div>
    {/each}
  </div>
  <InfiniteScroll threshold={10} on:loadMore={() => page++} />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    width: 100vw;
    gap: 32px;
    overflow-x: hidden;
  }
  main > h1 {
    padding: 10% 0 0;
  }
  #timeline {
    display: flex;
    flex-direction: row;
    width: 100%;
    justify-content: space-evenly;
  }
  .entry {
    flex: 1;
  }
  .entry > .entry-info {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    margin: 16px;
    padding: 16px;
    height: 60%;
    display: flex;
    align-items: center;
  }
  .entry > .entry-header {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    padding: 16px 24px;
    width: max-content;
    margin: 0 auto;
  }
  .entry > .vl {
    border-left: 4px solid #406e45;
    height: 30px;
    position: relative;
    left: 50%;
    margin-left: -2px;
    top: 0;
  }
  .entry > .hl {
    width: 100%;
    border-top: 4px solid #406e45;
  }
  .entry > .entry-info > h3 {
    color: #a4a4a4;
  }
</style>
