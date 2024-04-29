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
import { Check, Expand, Radar, TextSearch, Twitter } from "lucide-solid";
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
                <CardHeader>
                    <CardTitle>
                        <div class='flex flex-row gap-2 items-center justify-start'>
                            <Show when={props.type === "x"}>
                                <Twitter class='w-5 h-5 text-sky-400' />@
                            </Show>
                            {Tweetmeta(data()[0].contents, props.type).name}
                        </div>
                    </CardTitle>
                    <CardDescription class='text-zinc-100/40'>
                        <Show when={props.type === "rep"}>
                            {Tweetmeta(data()[0].contents, props.type).position}
                        </Show>
                        <Show when={props.type === "x"}>
                            <Show
                                when={
                                    Tweetmeta(data()[0].contents, props.type)
                                        .verified
                                }
                            >
                                <span class='text-sky-400 flex flex-row gap-2 items-center justify-start'>
                                    <Check class='w-4 h-4' />
                                    Verified
                                </span>
                            </Show>
                            <div class='flex flex-row gap-1 items-center justify-start ml-6'>
                                <span class='text-white'>
                                    {
                                        Tweetmeta(
                                            data()[0].contents,
                                            props.type
                                        ).followers
                                    }{" "}
                                </span>
                                <span>Followers</span>
                            </div>
                        </Show>
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div
                        class={cn(
                            "mb-4 grid grid-cols-[25px_1fr] items-start pb-4 last:mb-0 last:pb-0"
                        )}
                    >
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
                    <div class='flex flex-row gap-3 justify-between items-center w-[400px]'>
                        <Show when={props.type === "rep"}>
                            <p class='tracking-wide capitalize text-sm font-semibold'>
                                BIAS:{" "}
                                <span
                                    class={cn(
                                        Tweetmeta(
                                            data()[0].contents,
                                            props.type
                                        ).biasStr === "partisan"
                                            ? "text-red-500"
                                            : "text-green-500"
                                    )}
                                >
                                    {
                                        Tweetmeta(
                                            data()[0].contents,
                                            props.type
                                        ).biasConfidenceNum
                                    }
                                    %{" "}
                                    {
                                        Tweetmeta(
                                            data()[0].contents,
                                            props.type
                                        ).biasStr
                                    }
                                </span>
                            </p>
                        </Show>
                        <SimilarSearchBtn currentDoc={data()[0]} />
                    </div>
                </CardFooter>
            </Card>
        </Show>
    );
};

export default Tweet;
