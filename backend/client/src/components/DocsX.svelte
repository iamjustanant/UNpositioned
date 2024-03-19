
<script lang="ts">
  import { buildURL } from '../lib/util';
    import LimitSelector from './primitives/LimitSelector.svelte';

  export let text: string;

  let limit = 10;

  let promise: any;
  $: promise = fetch(buildURL('/api/searchx', { text, limit })).then(res => res.json());

  $: console.log("X Updated:", text);
  $: console.log("Promise:", promise);

</script>

<div class='col-child'>
  <div class='row-layout'>
    <h2>Relevant X Tweets</h2>
    <LimitSelector onSelectionChange={(value) => limit = value} />
  </div>

  {#await promise}
    <p>loading...</p>
  {:then res}
    <div class="entry-display">
      {#each res.res as entry, i}
        <p>{i+1}. {entry}</p>
      {/each}
    </div>
  {:catch error}
    <p>{error.message}</p>
  {/await}
</div>

<style>
  h2 {
    color: #333;
    font-size: 2rem;
    margin-bottom: 0;
  }

  .entry-display {
    display: flex;
    flex-direction: column;
    gap: 0px;
  }
</style>
