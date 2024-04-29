import { Show, createResource } from "solid-js";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "~/components/ui/card";
import { Endpoint, fetcher } from "~/lib/fetch";
import CustomLoader from "./loader";
import { Button } from "../ui/button";
import { Check, Expand, Radar, TextSearch } from "lucide-solid";
import { cn } from "~/lib/utils";
import SimilarSearchBtn from "./search-for-similar";
import { Tweetmeta } from "~/lib/parse";

const Tweet = (props: { id: string; type: "x" | "rep" }) => {
    const resource: Endpoint = {
        name: "getdoc",
        doc: { docID: props.id, docType: props.type },
    };

    const [data] = createResource(resource, fetcher);

    return (
        <Show when={!(data.loading || data.error)} fallback={<CustomLoader />}>
            <Card class='bg-zinc-100/10 border-none shadow-sm text-white'>
                <Show when={props.type === "rep"}>
                    <CardHeader>
                        <CardTitle>
                            {Tweetmeta(data()[0].contents, props.type).name}
                        </CardTitle>
                        <CardDescription class='text-zinc-100/40'>
                            {Tweetmeta(data()[0].contents, props.type).position}
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
                        <Show when={props.type === "x"}>
                            <div class='flex w-full items-center justify-between'>
                                <span class='flex flex-row items-center justify-start gap-2'>
                                    <p class='text-sm text-muted-foreground'>
                                        {
                                            Tweetmeta(
                                                data()[0].contents,
                                                props.type
                                            ).name
                                        }
                                    </p>
                                    <Show
                                        when={
                                            Tweetmeta(
                                                data()[0].contents,
                                                props.type
                                            ).verified
                                        }
                                    >
                                        <Check class='w-4 h-4 text-sky-400' />
                                    </Show>
                                </span>
                                <p class='text-sm text-muted-foreground'>
                                    {
                                        Tweetmeta(
                                            data()[0].contents,
                                            props.type
                                        ).followers
                                    }{" "}
                                    Followers
                                </p>
                            </div>
                        </Show>
                        <span class='flex size-2 translate-y-1 rounded-full bg-sky-500' />
                        <div class='space-y-3'>
                            <p class='text-sm font-medium'>
                                {
                                    Tweetmeta(data()[0].contents, props.type)
                                        .remaining
                                }
                            </p>
                            <Show when={props.type === "rep"}>
                                <p class='text-sm text-muted-foreground'>
                                    VIA{" "}
                                    {
                                        Tweetmeta(
                                            data()[0].contents,
                                            props.type
                                        ).platform
                                    }
                                </p>
                            </Show>
                        </div>
                    </div>
                </CardContent>
                <CardFooter>
                    <SimilarSearchBtn currentDoc={data()[0]} />
                </CardFooter>
            </Card>
        </Show>
    );
};

export default Tweet;
