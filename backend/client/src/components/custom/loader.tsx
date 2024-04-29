import { Loader } from "lucide-solid";
import { Show, createEffect, createSignal } from "solid-js";

const CustomLoader = () => {
    const [stillTrying, setStillTrying] = createSignal(true);

    createEffect(() => {
        setTimeout(() => {
            setStillTrying(false);
        }, 3000);
    });

    return (
        <Show
            when={stillTrying()}
            fallback={
                <div class='w-full h-full flex flex-row items-center justify-center p-8'>
                    <p class='text-zinc-100/50'>No results.</p>
                </div>
            }
        >
            <div class='w-full h-full flex flex-row items-center justify-center p-8'>
                <Loader class='size-8 animate-spin text-zinc-100/50' />
            </div>
        </Show>
    );
};

export default CustomLoader;
