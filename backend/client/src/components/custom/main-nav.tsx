import { Landmark } from "lucide-solid";
import type { ComponentProps } from "solid-js";
import { For, Show, splitProps } from "solid-js";

import { cn } from "~/lib/utils";
import { routes } from "~/routes";

export function MainNav(props: ComponentProps<"nav">) {
    const [, rest] = splitProps(props, ["class"]);
    return (
        <nav class={cn("flex justify-between py-4", props.class)} {...rest}>
            <div class='flex items-start space-x-4 lg:space-x-6'>
                <For each={routes}>
                    {({ path, label, hidden }) => (
                        <Show when={!hidden}>
                            <a
                                href={path}
                                class='text-sm font-medium transition-colors hover:text-primary'
                            >
                                {label}
                            </a>
                        </Show>
                    )}
                </For>
            </div>
            <div class='flex items-start space-x-4 lg:space-x-6'>
                <Landmark class='size-6' />
            </div>
        </nav>
    );
}
