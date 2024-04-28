import { Landmark, Redo2, Undo2 } from "lucide-solid";
import type { ComponentProps } from "solid-js";
import { For, Show, splitProps } from "solid-js";

import { cn } from "~/lib/utils";
import { Button } from "../ui/button";
import stateAPI from "~/lib/state-engine";

export function HistoryNav(props: ComponentProps<"div">) {
    const [, rest] = splitProps(props, ["class"]);
    return (
        <div
            class={cn(
                "flex flex-row justify-between py-0 px-0 bg-zinc-800 border-y border-zinc-100/10 shadow-lg text-white",
                props.class
            )}
            {...rest}
        >
            <Button
                onClick={stateAPI.goBack}
                disabled={!stateAPI.canGoBack}
                class='rounded-none bg-transparent hover:bg-zinc-100/5 text-zinc-100 hover:text-zinc-100 flex flex-row gap-2'
            >
                <Undo2 class='size-5' />
                <span>Back</span>
            </Button>
            <Button
                onClick={stateAPI.goForward}
                disabled={!stateAPI.canGoForward}
                class='rounded-none bg-transparent hover:bg-zinc-100/5 text-zinc-100 hover:text-zinc-100 flex flex-row gap-2'
            >
                <Redo2 class='size-5' />
                <span>Redo</span>
            </Button>
        </div>
    );
}
