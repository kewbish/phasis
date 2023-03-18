<script lang="ts">
  import { Router, Route } from "svelte-routing";
  import HomeView from "./lib/HomeView.svelte";
  import FindGardenView from "./lib/FindGardenView.svelte";
  import CalendarView from "./lib/CalendarView.svelte";
  import DayView from "./lib/DayView.svelte";
  import MonthView from "./lib/MonthView.svelte";
  import TimelineView from "./lib/TimelineView.svelte";
  import { writable } from "svelte/store";

  let url = "";

  const storedGardenPath = localStorage.getItem("gardenPath");
  let gardenPathWritable = writable(storedGardenPath);
  gardenPathWritable.subscribe((value) => {
    localStorage.setItem("gardenPath", value);
  });

  let gardenPath = storedGardenPath;
  $: {
    gardenPathWritable.set(gardenPath);
  }

  let currentMonth = new Date();
  let monthData: Array<[Date, ...Array<String>]> = [];
</script>

<svelte:head>
  <link
    rel="icon"
    href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌱</text></svg>"
  />
</svelte:head>
<Router {url}>
  <div>
    <Route path="/"><HomeView /></Route>
    <Route path="/findGarden"><FindGardenView bind:gardenPath /></Route>
    <Route path="/calendar"
      ><CalendarView bind:currentMonth bind:monthData /></Route
    >
    <Route path="/day"><DayView bind:gardenPath bind:currentMonth /></Route>
    <Route path="/month"
      ><MonthView bind:gardenPath bind:currentMonth bind:monthData /></Route
    >
    <Route path="/timeline"
      ><TimelineView bind:currentMonth bind:monthData bind:gardenPath /></Route
    >
  </div>
</Router>
