<script lang="ts">
  import { link, navigate } from "svelte-routing";
  import Calendar from "./components/Calendar.svelte";
  import { fly } from "svelte/transition";

  const monthDiff = (dateFrom: Date, dateTo: Date) => {
    return (
      dateTo.getMonth() -
      dateFrom.getMonth() +
      12 * (dateTo.getFullYear() - dateFrom.getFullYear())
    );
  };

  export let monthData: Array<[Date, ...Array<String>]> = [];

  const fetchData = async () => {
    const response = await fetch("http://localhost:5000/timeline");
    const json = await response.json();
    const today = new Date(currentMonth.getTime());
    const thisMonth = json
      .map(
        (entry: Array<string>) =>
          [new Date(parseInt(entry[0]) * 1000), ...entry.slice(1)] as [
            Date,
            ...Array<string>
          ]
      )
      .filter(
        (entry: [Date, ...Array<string>]) => monthDiff(entry[0], today) == 0
      );
    monthData = thisMonth;
    return thisMonth;
  };
  let newData = fetchData();

  $: {
    if (currentMonth) {
      newData = fetchData();
    }
  }

  export let currentMonth = new Date();

  const goPrevious = () => {
    currentMonth.setMonth(currentMonth.getMonth() - 1);
    currentMonth = new Date(currentMonth.getTime());
    monthDirection = false;
  };
  const goNext = () => {
    currentMonth.setMonth(currentMonth.getMonth() + 1);
    currentMonth = new Date(currentMonth.getTime());
    monthDirection = true;
  };
  const goTimeline = () => {
    navigate("/timeline");
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
  let monthDirection = true; // true for right, false for left
</script>

<main>
  <div id="to-prev" on:click={goPrevious} on:keydown={goPrevious}>
    {#key previousMonth}
      <h2>{previousMonth} ‹</h2>
    {/key}
  </div>
  <div id="main-block">
    <a href="/month" use:link>
      {#key currentMonth}
        <h1 in:fly={{ x: 50 * (monthDirection ? 1 : -1) }}>
          {currentMonth
            .toLocaleString("default", { month: "long" })
            .toLowerCase()}
          <span class="dark-green"><em>{currentMonth.getFullYear()}</em></span>
        </h1>
      {/key}
    </a>
    {#await newData}
      <p>...Waiting</p>
    {:then data}
      {#key currentMonth}
        <div id="main-wrapper">
          <Calendar {data} {currentMonth} />
          <button on:click={goTimeline} on:keydown={goTimeline}
            >timeline view</button
          >
        </div>
      {/key}
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
  #to-next > h2,
  #to-prev > h2 {
    margin: 55% 16px 16px;
    color: #808080;
    transition: ease-in-out 0.2s;
  }
  #to-next:hover > h2,
  #to-prev:hover > h2 {
    font-size: 30px;
    color: #406e45;
  }
  #to-next {
    display: flex;
    justify-content: end;
  }
  #to-next,
  #to-prev {
    cursor: pointer;
  }
  .dark-green {
    color: #406e45;
  }
  #main-block {
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 20%;
  }
  #main-wrapper {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 32px;
    flex-direction: column;
    gap: 16px;
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
  button {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    border: 0;
    padding: 8px 16px;
    transition: ease-in-out 0.2s;
    cursor: pointer;
  }
  button:hover {
    background: rgba(159, 227, 153, 0.35);
    padding: 12px 20px;
  }
</style>
