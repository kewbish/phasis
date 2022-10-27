<script lang="ts">
  import { Router, Route } from "svelte-routing";
  import HomeView from "./lib/HomeView.svelte";
  import FindGardenView from "./lib/FindGardenView.svelte";
  import CalendarView from "./lib/CalendarView.svelte";
  import DayView from "./lib/DayView.svelte";
  import MonthView from "./lib/MonthView.svelte";

  let url = "";

  let gardenPath = "";
  let currentMonth = new Date();
  let monthData: Array<[Date, ...Array<String>]> = [];
</script>

<Router {url}>
  <div>
    <Route path="/"><HomeView /></Route>
    <Route path="/findGarden"><FindGardenView bind:gardenPath /></Route>
    <Route path="/calendar"
      ><CalendarView bind:gardenPath bind:currentMonth bind:monthData /></Route
    >
    <Route path="/day"><DayView bind:gardenPath bind:currentMonth /></Route>
    <Route path="/month"
      ><MonthView bind:gardenPath bind:currentMonth bind:monthData /></Route
    >
  </div>
</Router>
