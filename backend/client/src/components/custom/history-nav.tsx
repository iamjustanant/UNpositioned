import {
    CircleChevronUp,
    Landmark,
    Redo2,
    RotateCcw,
    Undo2,
} from "lucide-solid";
import type { ComponentProps } from "solid-js";
import { For, Show, createSignal, splitProps } from "solid-js";
import {
    NumberField,
    NumberFieldDecrementTrigger,
    NumberFieldIncrementTrigger,
    NumberFieldInput,
} from "../ui/number-field";

import { cn } from "~/lib/utils";
import { Button } from "../ui/button";
import stateAPI from "~/lib/state-engine";
import limitAPI from "~/lib/state-engine/limit";

export function HistoryNav(props: ComponentProps<"div">) {
    const [, rest] = splitProps(props, ["class"]);
    const [changedLimit, setChangedLimit] = createSignal<boolean>(false);
    return (
        <div
            class={cn(
                "flex flex-row fixed bottom-0 w-screen justify-between py-0 px-0 bg-zinc-800 border-t border-zinc-100/10 shadow-lg text-white",
                props.class
            )}
            {...rest}
        >
            {/* <Button
                onClick={stateAPI.goBack}
                disabled={!stateAPI.canGoBack}
                class='bg-zinc-100/5 rounded-none hover:bg-zinc-100/10 text-zinc-100 hover:text-zinc-100 flex flex-row gap-2'
            >
                <Undo2 class='size-5' />
                <span>Back</span>
            </Button> */}
            <Button
                onClick={(e) => {
                    e.preventDefault();
                    window.location.reload();
                }}
                class='text-sm bg-zinc-100/5 rounded-none hover:bg-zinc-100/10 text-zinc-100 hover:text-zinc-100 flex flex-row gap-2'
            >
                <RotateCcw class='size-4' />
                <span>Restart</span>
            </Button>
            <div class='flex flex-row gap-2 items-center bg-zinc-100/5 pl-4'>
                <span>Limit to </span>
                <NumberField
                    class='w-[48px]'
                    rawValue={limitAPI.getLimit}
                    onRawValueChange={(n) => {
                        limitAPI.setLimit(n);
                        setChangedLimit(true);
                    }}
                >
                    <div class='relative'>
                        <NumberFieldInput class='border-none rounded-none focus:bg-zinc-100/10 text-center' />
                    </div>
                </NumberField>
                <span>results</span>
                <Show when={changedLimit}>
                    <Button
                        class='bg-zinc-100/5 hover:bg-zinc-100/10 ml-4 rounded-none'
                        onClick={() => {
                            stateAPI.reload();
                            setChangedLimit(false);
                        }}
                    >
                        Go
                    </Button>
                </Show>
            </div>
            <a
                href='#navigation'
                class='text-sm bg-zinc-100/5 rounded-none hover:bg-zinc-100/10 text-zinc-100 hover:text-zinc-100 flex flex-row gap-2 px-3 items-center'
            >
                <CircleChevronUp class='size-4' />
                <span>Back to Top</span>
            </a>
        </div>
    );
}
