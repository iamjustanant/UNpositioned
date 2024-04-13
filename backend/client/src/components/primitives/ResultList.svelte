
<script lang="ts">
    import type { DocType } from '$lib/types';
    import { buildURL } from '../../lib/util';
    import LimitSelector from './LimitSelector.svelte';
    import { Loader } from 'lucide-svelte';
    import Tweet from './Tweet.svelte';
    import Document from './Document.svelte';
  
    export let query: {
      type: "text-search",
      text: string,
      desiredType: DocType
    } | {
      type: "sim-search",
      docType: DocType,
      docID: string,
      desiredType: DocType,
    };
  
    let limit = 10;
  
    let promise: any;
    $: {
      switch (query.type) {
        case 'text-search':
          switch (query.desiredType) {
            case 'Rep':
              promise = fetch(
                buildURL('/api/searchrep', 
                { text: query.text, limit }))
                .then(res => res.json());
              break;
            case 'UN':
              promise = fetch(
                buildURL('/api/searchun', 
                { text: query.text, limit }))
                .then(res => res.json());
              break;
            case 'X':
              promise = fetch(
                buildURL('/api/searchx', 
                { text: query.text, limit }))
                .then(res => res.json());
              break;
          }
          break;
        case 'sim-search':
          // TODO: IMPLEMENT
          break;
      }
    }
</script>
  
<div class='res-col'>
  <div class='top-row'>
    <LimitSelector onSelectionChange={(value) => limit = value} />
  </div>

  {#await promise}
    <Loader />
  {:then res}
    <div class="entry-display">
      {#each res.res as entry, i}
        {#if query.desiredType === 'UN'}
          <Document documentContents={entry} origQuery={query.type==='text-search' ? query.text : null} />
        {:else if query.desiredType === 'Rep'}
          <Tweet tweetContents={entry} fromSenator={true} origQuery={query.type==='text-search' ? query.text : null} />
        {:else if query.desiredType === 'X'}
          <Tweet tweetContents={entry} fromSenator={false} origQuery={query.type==='text-search' ? query.text : null} />
        {/if}
      {/each}
    </div>
  {:catch error}
    <p class='error'>{error.message}</p>
  {/await}
</div>
  
<style>
  div.res-col {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 1rem;
    width: 100%;
    height: 100vw;
    overflow-y: scroll;
  }

  div.top-row {
    display: flex;
    flex-direction: row-reverse;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .entry-display {
    display: flex;
    flex-direction: column;
    gap: 12px;
    height: 100%;
    overflow-y: scroll;
  }

  .error {
    color: red;
  }
</style>
  