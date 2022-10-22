<script lang="ts">
  import { navigate } from "svelte-routing";

  const checkValidPath = (e: Event) => {
    if (!path.trim()) {
      e.preventDefault();
      document.getElementById("error").style.color = "black";
      return;
    }
    navigate("/calendar");
  };

  export let path = "";
</script>

<main>
  <div id="link-main">
    <h2>enter a link to your local digital garden</h2>
    <div id="input-div">
      <div id="textbox">
        <svg
          width="31"
          height="25"
          viewBox="0 0 31 25"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          on:click={() => document.getElementById("text-input").focus()}
          on:keydown={() => document.getElementById("text-input").focus()}
        >
          <path
            d="M27 4H4C1.79086 4 0 5.79086 0 8V21C0 23.2091 1.79086 25 4 25H27C29.2091 25 31 23.2091 31 21V8C31 5.79086 29.2091 4 27 4Z"
            fill="#B3F4AD"
          />
          <path
            d="M7 0H2C0.895431 0 0 0.89543 0 2V7H9V2C9 0.895431 8.10457 0 7 0Z"
            fill="#B3F4AD"
          />
        </svg>
        <input type="text" bind:value={path} id="text-input" />
      </div>
      <input type="submit" value="go!" on:click={checkValidPath} />
    </div>
    <p id="error">Please enter a valid filepath.</p>
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
  }
  #link-main {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin-top: -10%;
    width: 100%;
  }
  input {
    font-family: "Source Sans Pro";
    height: 3rem;
    font-size: 18px;
    border: none;
    background: #e0ffdd;
  }
  input[type="text"] {
    width: 100%;
  }
  svg {
    padding-right: 8px;
    cursor: pointer;
  }
  #textbox {
    background: #e0ffdd;
    border-radius: 8px 0 0 8px;
    padding-left: 8px;
    flex-grow: 1;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  #textbox::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 8px 0 0 8px;
    padding: 1px;
    background: linear-gradient(180deg, #bcecb4 0%, rgba(255, 255, 255, 0) 100%),
      linear-gradient(0deg, #e0ffdd, #e0ffdd);
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
  }
  input[type="submit"] {
    background: #b8efb3;
    border-radius: 0 8px 8px 0;
    padding: 8px 12px;
    cursor: pointer;
  }
  input[type="submit"]:hover {
    background: #88d081;
    font-size: 20px;
  }
  #input-div {
    display: flex;
    flex-direction: row;
    border-radius: 8px;
    box-shadow: rgba(9, 186, 58, 0.25) 2px 4px 4px;
    width: 40%;
  }
  input {
    transition: ease-in-out 0.2s;
  }
  input:focus {
    outline: none;
    box-shadow: rgba(9, 186, 58, 0.3) 4px 8px 8px;
  }
  #error {
    color: transparent;
    transition: ease-in-out 0.2s;
  }
  input:-webkit-autofill,
  input:-webkit-autofill:hover,
  input:-webkit-autofill:focus,
  input:-webkit-autofill:active {
    transition: background-color 5000s ease-in-out 0s;
  }
</style>
