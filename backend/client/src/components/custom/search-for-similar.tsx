import { Radar } from "lucide-solid";
import { Button } from "../ui/button";
import stateMachine from "~/lib/state";
import { Document } from "~/lib/types";

const SimilarSearchBtn = (props: { currentDoc: Document }) => {
    return (
        <Button
            onClick={() => stateMachine.makeDocSearch(props.currentDoc)}
            class='flex flex-row gap-2 bg-transparent text-zinc-100/40 hover:bg-transparent hover:text-zinc-100 px-0'
        >
            <Radar class='size-5' /> <span>Find Similar</span>
        </Button>
    );
};

export default SimilarSearchBtn;
