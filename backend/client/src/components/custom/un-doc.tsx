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
import { Expand, Radar } from "lucide-solid";
import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from "~/components/ui/sheet";
import Highlighter from "./highlighter";
import SimilarSearchBtn from "./search-for-similar";
import FullUNDoc from "./full-doc";
import { UNmeta } from "~/lib/parse";

const UNDoc = (props: { id: string; currentQuery?: string }) => {
    const previewEndpoint: Endpoint = {
        name: "getdocpreview",
        doc: { docID: props.id, docType: "un" },
    };

    const [previewData] = createResource(previewEndpoint, fetcher);

    return (
        <Show
            when={!(previewData.loading || previewData.error)}
            fallback={<CustomLoader />}
        >
            <Card class='bg-zinc-100/10 border-none shadow-sm text-white'>
                <CardHeader>
                    <CardTitle>
                        {UNmeta(previewData()[0].contents).country}
                        &nbsp;—&nbsp;
                        <span class='text-zinc-100/50'>
                            {UNmeta(previewData()[0].contents).year}
                        </span>
                    </CardTitle>
                    <CardDescription class='text-zinc-100/40'>
                        UN Position {previewData()[0].docID}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Highlighter
                        textToHighlight={
                            UNmeta(previewData()[0].contents).remaining
                        }
                        searchText={props.currentQuery}
                    />
                </CardContent>
                <CardFooter class='flex flex-row justify-between items-center w-full'>
                    <Sheet>
                        <SheetTrigger>
                            <Button class='flex flex-row gap-2 bg-transparent text-zinc-100/40 hover:bg-transparent hover:text-zinc-100 px-0'>
                                <Expand class='size-5' />{" "}
                                <span>View Full Document</span>
                            </Button>
                        </SheetTrigger>
                        <SheetContent class='w-3/5 bg-zinc-900/90 text-white border-none'>
                            <FullUNDoc id={previewData()[0].docID} />
                        </SheetContent>
                    </Sheet>

                    <SimilarSearchBtn currentDoc={previewData()[0]} />
                </CardFooter>
            </Card>
        </Show>
    );
};

export default UNDoc;
