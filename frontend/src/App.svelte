<script lang="ts">
import {Router, Route} from "svelte-routing";
import HomeView from "./lib/HomeView.svelte";
import FindGardenView from "./lib/FindGardenView.svelte";

export let url = "";
</script>

<Router url="{url}">
  <div>
    <Route path="/"><HomeView /></Route>
    <Route path="/findGarden"><FindGardenView /></Route>
  </div>
</Router>

