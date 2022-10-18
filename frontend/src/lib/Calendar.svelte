<script lang="ts">
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

  const generateCalendar = (data: Array<[Date, ...Array<string>]>) => {
    let table = "<table id='main-calendar'>";
    table +=
      "<tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>";
    for (let i = 0; i <= firstDay; i++) {
      table += "<td> </td>";
    }
    for (let i = 0; i < lastDay; i++) {
      let today = [];
      for (const entry of data) {
        if (entry[0].getDate() - 1 == i) {
          today = today.concat(entry.slice(1).join(" - "));
        }
      }
      if ((i + firstDay) % 7 == 0) {
        table += "<tr>";
      }
      table +=
        "<td>" +
        (today.length
          ? `<details><summary>${i + 1}</summary>${today.join(
              "<br>"
            )}</details>`
          : i + 1) +
        "</td>";
      if ((i + firstDay) % 7 == 6) {
        table += "</tr>";
      }
    }
    return table;
  };

  const date = new Date();
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
              {dateEntries[(i / cols) * cols + j]}
            {:else if dateEntries[(i / cols) * cols + j] == undefined}{" "}
            {:else}
              <details>
                <summary>{(i / cols) * cols + j}</summary>{dateEntries[
                  (i / cols) * cols + j
                ]}
              </details>
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
  }
</style>
