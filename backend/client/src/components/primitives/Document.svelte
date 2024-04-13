<script lang='ts'>
  import { onMount } from 'svelte';
  export let origQuery: string | null;
  export let documentContents: string;

  let highlightedContents: string;
  $: highlightedContents = 
      origQuery 
      ? documentContents.replaceAll(origQuery.trim(), `<span class='highlight'>${origQuery}</span>`)
      : documentContents;
</script>

<div class='document'>
  {@html highlightedContents}
</div>

<style>
  .document {
    background-color: #222;
    border-radius: 12px;
    padding: 1rem 2rem;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    min-height: 200px;
    height: fit-content;
    max-height: 400px;
    overflow-y: auto;
  }

  :global(.highlight) {
    background-color: yellow;
    color: #222;
  }
</style>