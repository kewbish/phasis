<script lang="ts">
  import { navigate } from "svelte-routing";
  import DayView from "./DayView.svelte";

  export let data: Array<[Date, ...Array<string>]>;

  const toDateEntries = (data: Array<[Date, ...Array<string>]>) => {
    const entries = Array.from(Array(firstDay)).concat(
      Array.from(Array(lastDay)).map((_, i) => {
        let today = [];
        for (const entry of data) {
          if (entry[0].getDate() - 1 == i) {
            today = today.concat(entry.slice(1).join(" - "));
          }
        }
        return today.length ? today : i + 1;
      })
    ) as Array<Array<String> | number | undefined>;
    return entries;
  };

  export let currentMonth = new Date();

  const date = new Date(currentMonth.getTime());
  const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();
  const cols = 7;
  const dateEntries = toDateEntries(data);
</script>

<table id="main-calendar">
  <tr
    ><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th
      >Sat</th
    ></tr
  >
  {#each dateEntries as date, i}
    {#if i % cols === 0}
      <tr>
        {#each Array(cols) as _, j}
          <td>
            {#if typeof dateEntries[(i / cols) * cols + j] == "number"}
              <div class="circle">{dateEntries[(i / cols) * cols + j]}</div>
            {:else if dateEntries[(i / cols) * cols + j] == undefined}{" "}
            {:else}
                <div class="circle with-details" on:click={() => navigate('/day')} on:keydown={() => navigate('/day')}>
                  {(i / cols) * cols + j}
                </div>
            {/if}
          </td>
        {/each}
      </tr>
    {/if}
  {/each}
</table>

<style>
  #main-calendar {
    width: 70%;
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    padding: 16px;
  }
  .circle {
    background: #ffffff;
    box-shadow: 1px 1px 5px #bcecb4;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    cursor: pointer;
    transition: ease-in-out 0.2s;
  }
  .circle:hover {
    box-shadow: rgba(9, 186, 58, 0.3) 2px 4px 4px;
    background-color: #f5fff5;
  }
  td {
    padding: 4px;
    font-size: 20px;
  }
  .with-details {
    background: #bcecb4;
  }
  .with-details:hover {
    background: #dbffd5;
  }
</style>
