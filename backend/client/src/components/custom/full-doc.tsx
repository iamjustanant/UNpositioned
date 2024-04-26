import { Show, createResource } from "solid-js";
import { Endpoint, fetcher } from "~/lib/fetch";
import { UNmeta } from "~/lib/parse";
import CustomLoader from "./loader";

const FullUNDoc = (props: { id: string }) => {
    const fullEndpoint: Endpoint = {
        name: "getdoc",
        doc: { docID: props.id, docType: "un" },
    };

    const [fullData] = createResource(fullEndpoint, fetcher);

    return (
        <Show
            when={!(fullData.loading || fullData.error)}
            fallback={<CustomLoader />}
        >
            <h1 class='text-xl'>
                <span class='text-zinc-100'>
                    {UNmeta(fullData()[0].contents).country}
                    &nbsp;—&nbsp;
                </span>
                <span class='text-zinc-300 italic'>
                    {UNmeta(fullData()[0].contents).year}
                </span>
            </h1>
            <h2 class='text-sm font-semibold text-zinc-100/40'>
                UN Position {props.id}
            </h2>
            <p class='mt-8 text-md text-zinc-100/80'>
                {fullData()[0].contents.substring(
                    fullData()[0].contents.indexOf(" said: ") + 7
                )}
            </p>
        </Show>
    );
};

export default FullUNDoc;
