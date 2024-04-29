import {
    Component,
    createEffect,
    createSignal,
    For,
    Match,
    Show,
    Suspense,
    Switch,
} from "solid-js";
import { Input } from "~/components/ui/input";
import { Col, Grid } from "~/components/ui/grid";
import {
    DocType,
    AnyDocument,
    Rep_Document,
    UN_Document,
    X_Document,
} from "~/lib/types";
import { createStore } from "solid-js/store";
import { fetcher } from "~/lib/fetch";
import { ArrowRight, Landmark, Loader, Radar } from "lucide-solid";
import { Search as SearchIcon } from "lucide-solid";
import { Button } from "~/components/ui/button";
import CustomLoader from "~/components/custom/loader";
import MainSearch from "~/components/custom/main-search";
import { Separator } from "~/components/ui/separator";
import UNDoc from "~/components/custom/un-doc";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "~/components/ui/tabs";
import Tweet from "~/components/custom/tweet";
import FullDoc from "~/components/custom/full-doc";
import stateAPI from "~/lib/state-engine";
import { HistoryNav } from "~/components/custom/history-nav";

export default function Search() {
    const [searchText, setSearchText] = createSignal("");

    createEffect(() => {
        setSearchText(stateAPI.searchQuery);
    });

    return (
        <section class='background-dots h-fit min-h-screen w-screen'>
            <Switch fallback={<CustomLoader />}>
                <Match when={stateAPI.state.stage === "not-started"}>
                    <div class='w-screen h-screen flex flex-col items-center justify-between py-32'>
                        <MainSearch
                            searchText={searchText()}
                            setSearchText={setSearchText}
                        />
                        <div class='flex flex-row gap-2 text-zinc-100/50 mb-12'>
                            <Landmark class='size-7' />
                            <span class='text-xl'>Unpositioned</span>
                        </div>
                    </div>
                </Match>
                <Match
                    when={
                        stateAPI.state.stage === "initial-search" &&
                        stateAPI.state.results.status === "loaded"
                    }
                >
                    <>
                        <HistoryNav />
                        <div class='flex flex-row justify-between w-full h-full'>
                            <div class='flex flex-col w-[810px] gap-4 p-12'>
                                <MainSearch
                                    searchText={searchText()}
                                    setSearchText={setSearchText}
                                />

                                <div class='flex flex-col gap-4 w-full py-8'>
                                    <span class='text-zinc-100/50 text-sm font-bold pl-4'>
                                        Official UN Responses
                                    </span>
                                    <For
                                        each={
                                            stateAPI.state["results"].un_results
                                        }
                                    >
                                        {(doc: UN_Document, index) => (
                                            <UNDoc
                                                id={doc.docID}
                                                currentQuery={searchText()}
                                            />
                                        )}
                                    </For>
                                </div>
                            </div>
                            <div class='flex flex-col w-fit gap-4 bg-zinc-100/5 p-12 shadow-sm'>
                                <span class='text-zinc-100/50 text-sm font-bold pl-4 w-full flex flex-row items-center justify-center'>
                                    Viewpoints from the Web
                                </span>
                                <Tabs defaultValue='rep' class='w-[405px]'>
                                    <TabsList class='grid w-full grid-cols-2 bg-zinc-100/10'>
                                        <TabsTrigger value='rep'>
                                            Posts by Politicians
                                        </TabsTrigger>
                                        <TabsTrigger value='x'>
                                            Other Tweets
                                        </TabsTrigger>
                                    </TabsList>
                                    <TabsContent value='rep'>
                                        <div class='flex flex-col gap-4 w-full py-8'>
                                            <For
                                                each={
                                                    stateAPI.state["results"]
                                                        .rep_results
                                                }
                                            >
                                                {(doc: Rep_Document, index) => (
                                                    <Tweet
                                                        id={doc.docID}
                                                        type='rep'
                                                    />
                                                )}
                                            </For>
                                        </div>
                                    </TabsContent>
                                    <TabsContent value='x'>
                                        <div class='flex flex-col gap-4 w-full py-8'>
                                            <For
                                                each={
                                                    stateAPI.state["results"]
                                                        .x_results
                                                }
                                            >
                                                {(doc: X_Document, index) => (
                                                    <Tweet
                                                        id={doc.docID}
                                                        type='x'
                                                    />
                                                )}
                                            </For>
                                        </div>
                                    </TabsContent>
                                </Tabs>
                            </div>
                        </div>
                    </>
                </Match>
                <Match
                    when={
                        stateAPI.state.stage === "doc-search" &&
                        stateAPI.state.results.status === "loaded"
                    }
                >
                    <>
                        <HistoryNav />
                        <div class='flex flex-row-reverse justify-between w-full h-full'>
                            <div class='flex flex-col w-[810px] gap-4 p-12'>
                                <div class='flex flex-col gap-4 w-full'>
                                    <span class='text-zinc-100/50 text-sm font-bold pl-4'>
                                        Most Relevant Results
                                    </span>
                                    <For
                                        each={
                                            stateAPI.state["results"]
                                                .similarDocs
                                        }
                                    >
                                        {(doc: UN_Document, index) => (
                                            <Show
                                                when={
                                                    doc.docID !==
                                                    stateAPI.state["docSearch"]
                                                        .docID
                                                }
                                            >
                                                <UNDoc id={doc.docID} />
                                            </Show>
                                        )}
                                    </For>
                                </div>
                            </div>
                            <div class='flex flex-col w-fit max-w-[400px] gap-4 bg-zinc-100/5 p-12 shadow-sm'>
                                <h1 class='text-white text-lg flex flex-row gap-4 mb-8'>
                                    <Radar class='size-7' /> Showing Results
                                    Similar To
                                </h1>
                                <FullDoc
                                    id={stateAPI.state["docSearch"].docID} // BUG: reactivity?
                                    type={stateAPI.state["docSearch"].docType}
                                />
                            </div>
                        </div>
                    </>
                </Match>
            </Switch>
        </section>
    );
}
