<script lang="ts">
  import InfiniteScroll from "svelte-infinite-scroll";
  import { navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import EventIcon from "./components/EventIcon.svelte";

  export let currentMonth: Date = new Date();
  export let gardenPath: string = "";
  export let monthData: Array<[Date, ...Array<String>]> = [];

  let size = 5;
  let page = 0;
  let timelineData = [];
  let commitsData = [];
  let newBatch = [];
  let newCommits = [];

  const goCalendar = () => {
    navigate("/calendar");
  };

  onMount(() => {
    recomputeBatch();
  });

  const recomputeBatch = async () => {
    newBatch = monthData.splice(size * page, size * (page + 1) - 1);
    let newCommitsTmp: Array<Array<{ sha: string; message: string }>> = [];
    for (const entry of newBatch) {
      const response = await fetch(
        `http://localhost:5000/commits?path=${encodeURIComponent(
          entry[1].replace(gardenPath, "")
        )}&date=${Math.floor(entry[0].getTime() / 1000)}`
      );
      const json = await response.json();
      newCommitsTmp = newCommitsTmp.concat([
        json.diffs as Array<{ sha: string; message: string }>,
      ]);
    }
    newCommits = newCommitsTmp;
  };

  $: timelineData = [...timelineData, ...newBatch];
  $: commitsData = [...commitsData, ...newCommits];

  const goEvent = (entry: [Date, ...Array<string>]) => {
    navigate(`/day?day=${+entry[0]}&file=${entry[1].replace(gardenPath, "")}`);
  };

  let timelineElement: HTMLDivElement;

  const truncate = (fullStr: string, strLen: number) => {
    if (fullStr.length <= strLen) return fullStr;

    const separator = "…";

    var sepLen = separator.length,
      charsToShow = strLen - sepLen,
      frontChars = Math.ceil(charsToShow / 2),
      backChars = Math.floor(charsToShow / 2);

    return (
      fullStr.substr(0, frontChars) +
      separator +
      fullStr.substr(fullStr.length - backChars)
    );
  };
</script>

<main>
  <h1>
    {currentMonth
      .toLocaleDateString("en-US", {
        month: "long",
      })
      .toLowerCase()}
    <span class="dark-green">
      <em>
        {currentMonth.getFullYear()}
      </em>
    </span>
  </h1>
  <div id="timeline" bind:this={timelineElement}>
    {#each timelineData as entry, i}
      <div class="entry">
        <div class="entry-header">
          <h3>
            {truncate(entry[1].replace(gardenPath, ""), 30)}
            <EventIcon state={entry[2]} />
          </h3>
        </div>
        <div class="vl" />
        <div class="hl" />
        <div class="entry-info">
          <h3>
            ‹ On {entry[0].toLocaleDateString(undefined, {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
            })} ›
          </h3>
          <div class="flex-commits">
            {#if commitsData[i] && commitsData[i].length != 0}
              {#each commitsData[i] as diff}
                <div class="circle">
                  {diff.sha.substring(0, 6)}
                </div>
              {/each}
            {/if}
          </div>
          <button
            on:click={() => goEvent(entry)}
            on:keydown={() => goEvent(entry)}>view event</button
          >
        </div>
      </div>
    {/each}
    <InfiniteScroll
      hasMore={newBatch.length}
      threshold={10}
      on:loadMore={() => {
        page++;
        recomputeBatch();
      }}
      horizontal={true}
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
    flex-direction: row;
    width: 100%;
    height: max-content;
    max-height: max-content;
    overflow-x: scroll;
    overflow-y: hidden;
    padding-top: 1rem;
    z-index: 3;
  }
  #timeline::-webkit-scrollbar {
    height: 10px;
    width: 10px;
  }
  #timeline::-webkit-scrollbar-thumb {
    background-color: #9fe399;
    border-radius: 8px;
  }
  #timeline > :global(:nth-child(1) > .hl) {
    border-image: linear-gradient(to left, #406e45, #ffffff00) 1;
  }
  #timeline > :global(:nth-last-child(-n + 1) > .hl) {
    border-image: linear-gradient(to right, #406e45, #ffffff00) 1;
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
    padding: 32px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .entry-info > h3 {
    text-align: center;
    width: 100%;
  }
  .entry-info > button {
    margin-top: 0.5rem;
    border: 1px solid #b8d6c0;
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
  .circle {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border: 1px solid #b8d6c0;
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
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.4);
  }
  .flex-commits {
    display: flex;
    gap: 1rem;
    padding: 0.5rem;
    width: fit-content;
  }
</style>
