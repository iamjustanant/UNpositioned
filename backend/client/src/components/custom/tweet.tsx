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
import { Expand, Radar, TextSearch } from "lucide-solid";
import { cn } from "~/lib/utils";
import SimilarSearchBtn from "./search-for-similar";

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
                            {meta(data()[0].contents, props.type).name}
                        </CardTitle>
                        <CardDescription class='text-zinc-100/40'>
                            {meta(data()[0].contents, props.type).position}
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
                                {meta(data()[0].contents, props.type).remaining}
                            </p>
                            <Show when={props.type === "rep"}>
                                <p class='text-sm text-muted-foreground'>
                                    VIA{" "}
                                    {
                                        meta(data()[0].contents, props.type)
                                            .platform
                                    }
                                </p>
                            </Show>
                            <Show when={props.type === "x"}>
                                <p class='text-sm text-muted-foreground'>
                                    {meta(data()[0].contents, props.type).name}
                                </p>
                            </Show>
                        </div>
                    </div>
                </CardContent>
                {/* <CardFooter>
                    <SimilarSearchBtn currentDoc={data()[0]} />
                </CardFooter> */}
            </Card>
        </Show>
    );
};

const meta = (contents: string, type: "x" | "rep") => {
    switch (type) {
        case "x":
            const firstLast = contents
                .substring(0, contents.indexOf(":") - 5)
                .trim();
            const actualTwt = contents.substring(contents.indexOf(":") + 1);
            return { name: firstLast, remaining: actualTwt };
        case "rep":
            const firstPart = contents.substring(0, contents.indexOf(":"));
            const name = firstPart.substring(0, contents.indexOf("(")).trim();
            const position = firstPart.substring(
                firstPart.indexOf("(") + 1,
                firstPart.indexOf(")")
            );
            const platform = firstPart.substring(
                firstPart.lastIndexOf(" ") + 1
            );
            const remaining = contents.substring(contents.indexOf(":") + 1);
            return { name, position, platform, remaining };
    }
};

export default Tweet;
