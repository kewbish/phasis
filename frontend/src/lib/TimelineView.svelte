<script lang="ts">
  import InfiniteScroll from "svelte-infinite-scroll";
  import { navigate } from "svelte-routing";

  export let currentMonth: Date = new Date();

  let page = 0;
  let size = 5;
  let timelineData = [];
  export let monthData: Array<[Date, ...Array<String>]> = [];

  const goCalendar = () => {
    navigate("/calendar");
  };

  $: timelineData = [
    ...timelineData,
    ...monthData.splice(size * page, size * (page + 1) - 1),
  ];

  let timelineElement: HTMLDivElement;
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
  <div id="timeline" bind:this={timelineElement}>
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
    <InfiniteScroll
      threshold={10}
      on:loadMore={() => page++}
      horizontal={true}
      elementScroll={timelineElement}
    />
  </div>
  <button on:click={goCalendar} on:keydown={goCalendar}>calendar view</button>
  <div id="to-prev">
    <h2>‹</h2>
  </div>
  <div id="to-next">
    <h2>›</h2>
  </div>
  <div id="navigation-overlay" />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    width: 100vw;
    gap: 16px;
    overflow-x: hidden;
  }
  main > h1 {
    padding: 10% 0 32px;
  }
  #timeline {
    display: flex;
    overflow-y: hidden;
    width: 100%;
    height: max-content;
    z-index: 3;
  }
  .entry {
    min-width: 33.3333%;
    height: max-content;
  }
  .entry > .entry-info {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    margin: 16px 32px;
    padding: 48px 16px;
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
  #to-next,
  #to-prev {
    position: absolute;
    cursor: pointer;
    height: 100vh;
    width: 10%;
    z-index: 2;
    padding: 0 16px;
  }
  #to-prev {
    left: 0;
  }
  #to-next {
    right: 0;
    text-align: right;
  }
  #to-next > h2,
  #to-prev > h2 {
    font-size: xx-large;
    margin: 110% 16px 16px;
    color: #808080;
    transition: ease-in-out 0.2s;
  }
  #to-next:hover > h2,
  #to-prev:hover > h2 {
    font-size: 40px;
    color: #406e45;
  }
  #navigation-overlay {
    background: linear-gradient(
      90deg,
      rgba(179, 244, 173, 0.44) 0%,
      rgba(255, 255, 255, 0) 30%,
      rgba(255, 255, 255, 0) 70%,
      rgba(179, 244, 173, 0.44) 100%
    );
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
  }
  button {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    border: 0;
    padding: 8px 16px;
    transition: ease-in-out 0.2s;
    cursor: pointer;
    z-index: 3;
  }
  button:hover {
    background: rgba(159, 227, 153, 0.35);
    padding: 12px 20px;
  }
</style>
