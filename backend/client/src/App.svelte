<script lang="ts">
  import DocsUn from "./components/DocsUN.svelte";
  import DocsX from "./components/DocsX.svelte";
  import { debounce } from '$lib/util';

  let text = '';

  const updateText = (e: any) => {
    text = e.target.value;
  }

</script>

<main>
  <h1>Unpositioned</h1>
  <h2>Quickly cross-check official UN national stances against Western sentiment on any topic.</h2>

  <input on:keyup={debounce(updateText)} placeholder="Enter any term, issue, or topic..." />

  <hr>

  <div class='column-layout'>
    <DocsUn text={text} />
    <DocsX text={text} />
  </div>

</main>

<style>
main {
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;
  padding: 0 64px;
  font-family: Helvetica, sans-serif;
}

h1 {
  color: #333;
  font-size: 6rem;
  margin-left: -4px;
}

h2 {
  color: #333;
  font-size: 0.9rem;
  margin-top: -4rem;
  margin-bottom: 2rem;
}

input {
  width: 100%;
  max-width: 600px;
  margin-bottom: 20px;
  padding: 8px 16px;
  border: 2px solid #ddd;
}

hr {
  margin: 20px 0;
  border: 0;
  border-top: 1px solid #ddd;
}

p {
  color: #666;
  font-size: 1em;
  margin-bottom: 20px;
}

:global(.column-layout) {
  display: flex;
  flex: 1 1 0px;
  flex-direction: row;
  justify-content: space-between;
  align-items: start;
  gap: 64px;
  margin-bottom: 20px;
}

.column-layout :global(.col-child) {
    width: 100%;
    max-width: 600px;
    margin-bottom: 20px;
    padding: 8px 16px;
    flex-basis: 0;
    flex-grow: 1;
    font-family: Helvetica, sans-serif;
    color: #333;
}

:global(.row-layout) {
  display: flex;
  flex: 1 1 0px;
  flex-direction: row;
  justify-content: space-between;
  align-items: end;
}
</style>
