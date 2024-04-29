import { Match, Show, Switch, createResource } from "solid-js";
import { Endpoint, fetcher } from "~/lib/fetch";
import { Tweetmeta, UNmeta } from "~/lib/parse";
import CustomLoader from "./loader";
import { DocType } from "~/lib/types";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "../ui/card";
import { cn } from "~/lib/utils";

const FullDoc = (props: { id: string; type?: DocType }) => {
    const fullEndpoint: Endpoint = {
        name: "getdoc",
        doc: { docID: props.id, docType: props.type ?? "un" },
    };

    const [fullData] = createResource(fullEndpoint, fetcher);

    return (
        <Show
            when={!(fullData.loading || fullData.error)}
            fallback={<CustomLoader />}
        >
            <Switch fallback={<CustomLoader />}>
                <Match when={props.type === "un" || !props.type}>
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
                </Match>
                <Match when={props.type === "x" || props.type === "rep"}>
                    <Card class='bg-zinc-100/10 border-none shadow-sm text-white'>
                        <Show when={props.type === "rep"}>
                            <CardHeader>
                                <CardTitle>
                                    {
                                        Tweetmeta(
                                            fullData()[0].contents,
                                            props.type as any
                                        ).name
                                    }
                                </CardTitle>
                                <CardDescription class='text-zinc-100/40'>
                                    {
                                        Tweetmeta(
                                            fullData()[0].contents,
                                            props.type as any
                                        ).position
                                    }
                                </CardDescription>
                            </CardHeader>
                        </Show>
                        <CardContent>
                            <div
                                class={cn(
                                    "mb-4 grid grid-cols-[25px_1fr] items-start pb-4 last:mb-0 last:pb-0",
                                    props.type === "x" ? "pt-8" : "pt-0"
                                )}
                            >
                                <span class='flex size-2 translate-y-1 rounded-full bg-sky-500' />
                                <div class='space-y-3'>
                                    <p class='text-sm font-medium'>
                                        {
                                            Tweetmeta(
                                                fullData()[0].contents,
                                                props.type as any
                                            ).remaining
                                        }
                                    </p>
                                    <Show when={props.type === "rep"}>
                                        <p class='text-sm text-muted-foreground'>
                                            VIA{" "}
                                            {
                                                Tweetmeta(
                                                    fullData()[0].contents,
                                                    props.type as any
                                                ).platform
                                            }
                                        </p>
                                    </Show>
                                    <Show when={props.type === "x"}>
                                        <p class='text-sm text-muted-foreground'>
                                            {
                                                Tweetmeta(
                                                    fullData()[0].contents,
                                                    props.type as any
                                                ).name
                                            }
                                        </p>
                                    </Show>
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter>
                            {/* <SimilarSearchBtn currentDoc={data()[0]} /> */}
                        </CardFooter>
                    </Card>
                </Match>
            </Switch>
        </Show>
    );
};

export default FullDoc;
