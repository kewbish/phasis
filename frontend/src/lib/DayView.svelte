<script lang="ts">
  export let currentMonth = new Date();
</script>

<main>
  <div id="main-wrapper">
    <div id="files-list">{currentMonth}</div>
    <div id="file-preview">
      <h1>‹ preview ›</h1>
    </div>
  </div>
</main>

<style>
  #file-preview,
  #files-list {
    background: rgba(159, 227, 153, 0.18);
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
  }
  #file-preview {
    color: #a4a4a4;
  }
</style>
