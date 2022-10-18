<script lang="ts">
</script>

<main>
  <h3>enter a link to your local digital garden</h3>
  <div id="input-div">
    <input type="text" /><input type="submit" value="go!" />
  </div>
</main>

<style>
  main {
    background: linear-gradient(
      180deg,
      #b3f4ad 0%,
      #fff 25%,
      #fff 75%,
      #b3f4ad 100%
    );
    display: flex;
    height: 100vh;
    width: 100vw;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 12px;
  }
  input {
    font-family: "Source Sans Pro";
    height: 3rem;
    font-size: 18px;
    box-shadow: 2px 4px 4px rgba(9, 186, 58, 0.25);
    border: none;
  }
  input[type="text"] {
    background: #e0ffdd;
    border-radius: 8px 0 0 8px;
    padding-left: 8px;
  }
  input[type="submit"] {
    background: #b8efb3;
    border-radius: 0 8px 8px 0;
    padding: 8px;
  }
  #input-div {
    display: flex;
    justify-content: center;
  }
</style>
