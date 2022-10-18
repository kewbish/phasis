<script lang="ts">
  import { Link } from "svelte-routing";
</script>

<main>
  <div id="header">
    <h1>welcome to your digital garden</h1>
    <p>ready to track your thoughts through time?</p>
    <Link to="/findGarden"><button>🪴 💐 🌿</button></Link>
  </div>
  <p id="experiment">
    an experiment by <a href="https://kewbi.sh">kewbish</a>.
  </p>
</main>

<style>
  main {
    background: linear-gradient(180deg, #b3f4ad 0%, #fff 100%);
    display: flex;
    height: 100vh;
    width: 100vw;
    justify-content: center;
    align-items: center;
  }
  #header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    transform: translateY(-50%);
  }
  button {
    background: #9fe399;
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border-radius: 8px;
    border: 0;
    padding: 8px 16px;
    font-size: larger;
    transition: ease-in-out 0.2s;
    cursor: pointer;
  }
  button:hover {
    background: #88d081;
    padding: 12px 20px;
  }
  #experiment {
    position: absolute;
    bottom: 2%;
    left: 2%;
  }
  #experiment > a {
    color: black;
  }
</style>
