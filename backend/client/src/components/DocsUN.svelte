
<script lang="ts">
  import { buildURL } from '../lib/util';

  export let text: string;

  let limit = 10;

  let promise: any;
  $: promise = fetch(buildURL('/api/searchun', { text, limit })).then(res => res.json());
</script>

<div class='col-child'>
  <h2>Relevant UN Documents</h2>

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
