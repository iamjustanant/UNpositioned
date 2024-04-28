import findAll from "highlight-words-core";
import memoizeOne from "memoize-one";
import { Component, createSignal, For, mergeProps, Show } from "solid-js";
import { Dynamic } from "solid-js/web";
import highlightWords from "highlight-words";
import { cn } from "~/lib/utils";

/**
 * Highlights all occurrences of search terms (searchText) within a string (textToHighlight).
 * This function returns an array of strings and <span>s (wrapping highlighted words).
 */
export default function Highlighter(props: {
    textToHighlight: string;
    searchText?: string;
}) {
    const chunks = highlightWords({
        text: props.textToHighlight,
        query: props.searchText ?? "",
    });

    return (
        <Show when={props.searchText} fallback={<p>{props.textToHighlight}</p>}>
            <p>
                <For each={chunks}>
                    {({ text, match }, index) => (
                        <span class={cn(match ? "bg-sky-500/40" : "")}>
                            {text}
                        </span>
                    )}
                </For>
            </p>
        </Show>
    );
}
