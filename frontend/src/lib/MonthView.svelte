<script lang="ts">
  import SummaryView from "./components/SummaryView.svelte";

  export let monthData: Array<[Date, ...Array<string>]> = [];
  export let currentMonth = new Date();
  export let gardenPath: String;
</script>

<main>
  <SummaryView data={monthData} {gardenPath} {currentMonth} month={true} />
</main>
