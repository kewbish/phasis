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
  {currentMonth}
  <div id="timeline">
    {#each timelineData as entry}
      <p>{entry}</p>
    {/each}
  </div>
  <InfiniteScroll threshold={10} on:loadMore={() => page++} />
</main>

<style>
  #timeline {
    overflow-x: scroll;
  }
</style>
