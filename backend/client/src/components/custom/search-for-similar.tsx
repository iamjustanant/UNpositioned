import { Radar } from "lucide-solid";
import { Button } from "../ui/button";
import stateAPI from "~/lib/state-engine";
import { AnyDocument } from "~/lib/types";
import { createEffect } from "solid-js";

const SimilarSearchBtn = (props: { currentDoc: AnyDocument }) => {
    return (
        <Button
            onClick={() => stateAPI.makeDocSearch(props.currentDoc)}
            class='flex flex-row gap-2 bg-transparent text-zinc-100/40 hover:bg-transparent hover:text-zinc-100 px-0 py-0'
        >
            <Radar class='size-5' /> <span>Find Similar</span>
        </Button>
    );
};

export default SimilarSearchBtn;
