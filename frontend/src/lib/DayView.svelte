<script lang="ts">
  export let currentMonth = new Date();

  const fetchData = (async () => {
    const response = await fetch("http://localhost:5000/timeline");
    const json = await response.json();
    const today = new Date(currentMonth.getTime());
    const thisMonth = json
      .map(
        (entry: Array<string>) =>
          [new Date(entry[0]), ...entry.slice(1)] as [Date, ...Array<string>]
      )
      .filter((entry: [Date, ...Array<string>]) => {
        console.log(entry);
        return entry[0].toDateString() == today.toDateString();
      });
    return thisMonth;
  })();
</script>

<main>
  <div id="main-block">
    <h1>
      ‹ {currentMonth
        .toLocaleDateString("en-US", { month: "long", day: "numeric" })
        .toLowerCase()}
      <span class="dark-green">
        <em>
          {currentMonth.getFullYear()}
        </em>
      </span>
    </h1>
    <div id="main-wrapper">
      <div id="files-list">
        {#await fetchData}<p>Loading...</p>{:then data}<p>{data}</p>
        {:catch error}<p>Error! {error}</p>{/await}
      </div>
      <div id="file-preview">
        <h1>‹ preview ›</h1>
      </div>
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100vh;
    width: 100vw;
  }
  .dark-green {
    color: #406e45;
  }
  #main-block {
    width: 80%;
    padding: 5% 0;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  #main-wrapper {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    padding-top: 20px;
    flex-grow: 1;
  }
  #files-list {
    height: fit-content;
  }
  #file-preview,
  #files-list {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    padding: 24px;
  }
  #file-preview {
    color: #a4a4a4;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80%;
  }
</style>
