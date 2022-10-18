<script lang="ts">
  import Calendar from "./lib/Calendar.svelte";

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
</script>

<main>
  {#await fetchData}
    <p>...Waiting</p>
  {:then data}
    <div id="main-wrapper"><Calendar {data} /></div>
  {:catch error}
    <p>Error! {error}</p>
  {/await}
</main>

<style>
  div:global(#main-wrapper) {
    width: 100%;
  }
</style>
