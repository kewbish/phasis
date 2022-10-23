<script lang="ts">
  import { Router, Route } from "svelte-routing";
  import HomeView from "./lib/HomeView.svelte";
  import FindGardenView from "./lib/FindGardenView.svelte";
  import CalendarView from "./lib/CalendarView.svelte";
  import DayView from "./lib/DayView.svelte";

  let url = "";

  let gardenPath = "";
  let currentMonth = new Date();
</script>

<Router {url}>
  <div>
    <Route path="/"><HomeView /></Route>
    <Route path="/findGarden"><FindGardenView bind:path={gardenPath} /></Route>
    <Route path="/calendar"
      ><CalendarView bind:gardenPath bind:currentMonth /></Route
    >
    <Route path="/day"><DayView bind:gardenPath bind:currentMonth /></Route>
  </div>
</Router>
