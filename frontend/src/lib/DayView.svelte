<script lang="ts">
  import SummaryView from "./components/SummaryView.svelte";

  const urlParams = new URLSearchParams(window.location.search);
  const file = urlParams.has("file") ? urlParams.get("file") : "";

  export let currentMonth = new Date();
  export let gardenPath: String;

  const fetchData = (async () => {
    currentMonth = urlParams.has("day")
      ? new Date(parseInt(urlParams.get("day")))
      : currentMonth;
    const response = await fetch("http://localhost:5000/timeline");
    const json = await response.json();
    const today = new Date(currentMonth.getTime());
    const thisMonth = json
      .map(
        (entry: Array<string>) =>
          [new Date(entry[0]), ...entry.slice(1)] as [Date, ...Array<string>]
      )
      .filter((entry: [Date, ...Array<string>]) => {
        return entry[0].toDateString() == today.toDateString();
      });
    return thisMonth;
  })();
</script>

<main>
  {#await fetchData}
    <p>Loading...</p>
  {:then data}
    <SummaryView
      {data}
      {gardenPath}
      {currentMonth}
      month={false}
      {file}
      returnPath={urlParams.has("day") ? "/timeline" : "/calendar"}
    />
  {:catch error}
    <p>Error! {error}</p>
  {/await}
</main>
