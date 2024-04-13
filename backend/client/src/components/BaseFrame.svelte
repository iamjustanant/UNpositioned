<script lang='ts'>
  import ResultList from "./primitives/ResultList.svelte";
  import { fade, slide } from "svelte/transition";

  export let goBack: () => void;

  let searchQuery = '';
  let senatorsOnly = true;
</script>

<div class='full-frame' transition:slide>
  <div class='top-row'>
    <input class='search' type='text' bind:value={searchQuery} placeholder='Search by anything...' />
    <button class='back' on:click={goBack}>UN</button>
  </div>
  <div class='main-row'>
    <div class='main-results'>
      <div class='main-header'>
        <h1>Found matching documents...</h1>
      </div>
      <div class='main-content'>
        <ResultList query={{
          type: "text-search",
          text: searchQuery,
          desiredType: "UN"
        }} />
      </div>
    </div>
    <div class='side-results'>
      <div class='senators-toggle'>
        <button on:click={() => senatorsOnly = true} data-active={senatorsOnly}>
          Tweets from Senators
        </button>
        <button on:click={() => senatorsOnly = false} data-active={!senatorsOnly}>
          Tweets from Everyone
        </button>
      </div>
      <div class='results'>
        <ResultList query={{
          type: "text-search",
          text: searchQuery,
          desiredType: senatorsOnly ? "Rep" : "X"
        }} />
      </div>
    </div>
  </div>
</div>

<style>
  div.top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #222;
    width: 100vw;
    height: 100px;
    z-index: 100;
    box-shadow: 0 0px 24px rgba(0, 0, 0, 0.2);
  }

  div.main-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background-color: #ddd;
    width: 100vw;
    height: calc(100vh - 100px);
  }

  div.main-results {
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: baseline;
    background-color: #eee;
    width: 70%;
    height: 100%;
    padding: 0 2rem;
    color: #fff;
    box-shadow: 0 0px 24px rgba(0, 0, 0, 0.2);
    z-index: 100;
  }

  div.side-results {
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: baseline;
    background-color: #444;
    width: 30%;
    height: 100%;
    padding: 0 2rem;
    color: #fff;
    box-shadow: 0 0px 24px rgba(0, 0, 0, 0.2);
    z-index: 100;
    overflow-y: scroll;
  }

  input.search {
    font-family: "Archivo Narrow", sans-serif;
    font-weight: 400;
    font-style: normal;
    color: #999;
    font-size: 32px;
    background-color: #222;
    border: none;
    padding: 0 2rem;
    width: 80%;
  }

  input.search:focus {
    outline: none;
  }

  button.back {
    font-family: "Jersey 15", sans-serif;
    font-weight: 400;
    font-style: normal;
    color: #666;
    font-size: 48px;
    background-color: transparent;
    border: none;
    margin: 0 2rem;
    transition: all 0.3s;
    cursor: pointer;
  }

  button.back:hover {
    color: #fff;
  }

  div.senators-toggle {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    margin: 2rem 0;
    background-color: #333;
    border-radius: 8px;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    z-index: inherit;
  }

  div.senators-toggle button {
    font-family: "Archivo Narrow", sans-serif;
    font-weight: 400;
    font-style: normal;
    color: #fff;
    font-size: 16px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
  }

  div.senators-toggle button[data-active='true'] {
    border-bottom: 2px solid #fff;
  }

  div.results {
    margin-top: -90px;
    overflow-y: scroll;
  }

  div.main-header {
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    gap: 8px;
    padding: 0;
    padding-top: 24px;
    color: #333;
    display: none;
  }

  div.main-header h1 {
    font-family: "Archivo Narrow", sans-serif;
    font-weight: 400;
    font-style: italic;
    font-size: 24px;
    color:rgba(0, 0, 0, 0.1)
  }

  div.main-content {
    margin-top: 12px;
    width: 100%;
    overflow-y: scroll;
  }
</style>