<script lang='ts'>
  export let origQuery: string | null;
  export let tweetContents: string;
  export let fromSenator: boolean;

  let highlightedContents: string;
  $: highlightedContents = 
      origQuery 
      ? tweetContents.replaceAll(origQuery.trim(), `<span class='highlight'>${origQuery}</span>`)
      : tweetContents;
</script>

<div class='tweet'>
  {@html highlightedContents}
</div>

<style>
  .tweet {
    background-color: #222;
    border-radius: 12px;
    padding: 1rem 2rem;
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    min-height: 150px;
    height: 300px;
    max-height: 300px;
    overflow-y: auto;
    position: relative;
  }

  .tweet p {
    font-size: 0.8rem;
    color: #fff;
  }

  .verified-indicator {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 20px;
    height: 20px;
    background-color: lightskyblue;
    border-radius: 50%;
  }
</style>