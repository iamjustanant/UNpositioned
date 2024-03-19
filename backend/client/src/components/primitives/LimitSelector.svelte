<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  export let selectedValue = 10;
  export let onSelectionChange: (value: number) => void;

  const options = [10, 25, 50, 100, 500];
  const selected = writable(selectedValue);

  onMount(() => {
    selected.subscribe(value => {
      onSelectionChange(value);
    });
  });
</script>

<div>
  <select bind:value={$selected} id="limit">
    {#each options as option (option)}
      <option value={option}>{option}</option>
    {/each}
  </select>
</div>

<style>
  div {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  select {
    padding: 8px 16px;
    border: 2px solid #ddd;
    background-color: white;
  }
</style>