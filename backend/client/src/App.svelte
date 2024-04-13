<script lang="ts">
  import { MoveDownRight } from 'lucide-svelte';
  import BaseFrame from './components/BaseFrame.svelte';
  import ResFrame from './components/ResFrame.svelte';
  import type { Doc, DocType } from '$lib/types';

  let showBaseFrame = false;
  
  let stack: Doc[] = []; // stack of documents that are being rendered

</script>

<main>
  <div class='main-row'>
    <div class='sub-row'>
      <span class='un'>UN</span>
      <span class='narrow'>POSITIONED</span>
      <img src='https://pngimg.com/uploads/un/small/un_PNG13.png' alt='UN logo' class='un-logo' height="64" />
    </div>
    <div>
      <button class='cta' on:click={() => showBaseFrame = true}>
        <MoveDownRight size='24' />
        GO
      </button>
    </div>
  </div>
  {#if showBaseFrame}
    <BaseFrame goBack={() => showBaseFrame = false} />
  {/if}
  {#each stack as doc}
    <ResFrame {doc} {stack} />
  {/each}
</main>

<style>

  main {
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: 100vh;
    align-items: left;
    justify-content: end;
    font-family: Helvetica, sans-serif;
    background-image: url('https://images.unsplash.com/photo-1612119617147-e4e78bdaacdd?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    color: #333;
    background-color: rgba(0, 0, 0, 0.5);
    background-blend-mode: darken;
  }

  div.main-row {
    color: #fff;
    font-optical-sizing: auto;
    border-top: 1px solid #aaa;
    border-bottom: 1px solid #aaa;
    margin: 8rem 0;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  img.un-logo {
    margin-left: 2rem;
  }

  div.main-row div.sub-row {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  div.main-row span.narrow {
    font-family: "Archivo Narrow", sans-serif;
    font-weight: 800;
    font-style: normal;
    font-size: 160px;
    padding: 0;
    /* border-left: 1px solid #aaa; */
  }

  div.main-row span.un {
    font-family: "Jersey 15", sans-serif;
    font-weight: 400;
    font-style: normal;
    font-size: 200px;
    margin-top: 7px;
    margin-left: 2rem;
  }

  button.cta {
    background-color: transparent;
    color: #fff;
    font-size: 2rem;
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid #fff;
    padding: 1rem 2rem;
    margin: 0 4rem;
  }

  button.cta:hover {
    background-color: #fff;
    color: #333;
  }

  :global(.full-frame) {
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: 100vh;
    align-items: center;
    justify-content: start;
    font-family: Helvetica, sans-serif;
    background-color: #f0f0f0;
  }

</style>
