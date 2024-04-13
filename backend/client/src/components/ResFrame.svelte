<script lang='ts'>
  import ResultList from "./primitives/ResultList.svelte";
  import FullDocument from "./primitives/FullDocument.svelte";
  import type { Doc, DocType } from "$lib/types";

  export let stack: Doc[];
  export let doc: Doc;

  let searchSimilarFor: DocType = 'UN';
</script>

{#if stack[stack.length - 1] === doc}
  <div class='full-frame'>
    <button class='back' on:click={stack.pop}>
      BACK
    </button>
    <FullDocument {doc} />
    <ResultList query={{
      type: 'sim-search',
      docType: doc.type,
      docID: doc.id,
      desiredType: searchSimilarFor
    }} />
  </div>
{/if}

<style>
  button.back {
    margin: 1rem;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 4px;
  }
</style>