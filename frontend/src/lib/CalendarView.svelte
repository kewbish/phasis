<script lang="ts">
  import Calendar from "./Calendar.svelte";
  import { fade, scale } from "svelte/transition";
  import { quintOut } from "svelte/easing";

  const monthDiff = (dateFrom: Date, dateTo: Date) => {
    return (
      dateTo.getMonth() -
      dateFrom.getMonth() +
      12 * (dateTo.getFullYear() - dateFrom.getFullYear())
    );
  };

  const fetchData = (async () => {
    const response = await fetch("http://localhost:5000/timeline");
    const json = await response.json();
    const today = new Date();
    const thisMonth = json
      .map(
        (entry: Array<string>) =>
          [new Date(entry[0]), ...entry.slice(1)] as [Date, ...Array<string>]
      )
      .filter(
        (entry: [Date, ...Array<string>]) => monthDiff(entry[0], today) == 0
      );
    return thisMonth;
  })();

  export let currentMonth = new Date();

  const goPrevious = () => {
    currentMonth.setMonth(currentMonth.getMonth() - 1);
    currentMonth = new Date(currentMonth.getTime());
  };
  const goNext = () => {
    currentMonth.setMonth(currentMonth.getMonth() + 1);
    currentMonth = new Date(currentMonth.getTime());
  };

  let previousMonth: String;
  let nextMonth: String;
  $: {
    let current = new Date(currentMonth.getTime());
    current.setMonth(current.getMonth() - 1);
    previousMonth =
      current
        .toLocaleString("default", {
          month: "long",
        })
        .toLowerCase() +
      " " +
      current.getFullYear();
  }
  $: {
    let current = new Date(currentMonth.getTime());
    current.setMonth(current.getMonth() + 1);
    nextMonth =
      current
        .toLocaleString("default", {
          month: "long",
        })
        .toLowerCase() +
      " " +
      current.getFullYear();
  }

  export let gardenPath = "";
</script>

<main>
  <div id="to-prev" on:click={goPrevious} on:keydown={goPrevious}>
    {#key previousMonth}
      <h2>{previousMonth} ‹</h2>
    {/key}
  </div>
  <div id="main-block">
    {#key currentMonth}
      <h1 transition:scale>
        {currentMonth
          .toLocaleString("default", { month: "long" })
          .toLowerCase()}
        <span class="dark-green">{currentMonth.getFullYear()}</span>
      </h1>
    {/key}
    {#await fetchData}
      <p>...Waiting</p>
    {:then data}
      <div id="main-wrapper"><Calendar {data} /></div>
    {:catch error}
      <p>Error! {error}</p>
    {/await}
  </div>
  <div id="to-next" on:click={goNext} on:keydown={goNext}>
    {#key nextMonth}
      <h2>› {nextMonth}</h2>
    {/key}
  </div>
</main>

<style>
  main {
    background: linear-gradient(
      90deg,
      rgba(179, 244, 173, 0.44) 0%,
      rgba(255, 255, 255, 0) 30%,
      rgba(255, 255, 255, 0) 70%,
      rgba(179, 244, 173, 0.44) 100%
    );
    height: 100vh;
    width: 100vw;
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
  }
  #main-wrapper {
    width: 100%;
  }
  #to-next > h2,
  #to-prev > h2 {
    margin: 35% 16px 16px;
    color: #808080;
    transition: ease-in-out 0.2s;
    cursor: pointer;
  }
  #to-next > h2:hover,
  #to-prev > h2:hover {
    font-size: 30px;
    color: #406e45;
  }
  #to-next {
    display: flex;
    justify-content: end;
  }
  .dark-green {
    color: #406e45;
  }
  #main-block {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 64px;
  }
</style>
