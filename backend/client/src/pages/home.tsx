import { Command, Landmark } from "lucide-solid";
import { createSignal } from "solid-js";
import { Button } from "~/components/ui/button";
import { cn } from "~/lib/utils";
import { Timeline } from "~/components/ui/timeline";

export default function Home() {
    return (
        <>
            <div class='container relative h-[820px] flex-col items-center justify-center px-0 max-w-none'>
                <div class='relative h-full bg-muted p-10 text-white dark:border-r flex flex-col md:justify-between'>
                    <div class='absolute inset-0 bg-zinc-900 background-dots' />
                    <div class='relative z-20 flex items-center text-xl font-medium'>
                        <Landmark class='mr-2 size-6' />
                        Unpositioned
                    </div>
                    <div class='relative z-20 w-full flex flex-row justify-between'>
                        <div class='flex flex-col gap-12'>
                            <blockquote class='space-y-2'>
                                <p class='text-6xl max-w-[800px]'>
                                    The international positions database for the
                                    modern political researcher.
                                </p>
                            </blockquote>
                            <Timeline
                                items={[
                                    {
                                        title: "Search with any keyword.",
                                        description:
                                            "Get the most relevant UN positions on your topic of choice.",
                                    },
                                    {
                                        title: "Cross-reference positions.",
                                        description:
                                            "Check opinions against Western political commentators on Twitter.",
                                    },
                                    {
                                        title: "Dive deeper.",
                                        description:
                                            "Repeat the search with your current position as the starting point.",
                                    },
                                ]}
                                activeItem={0}
                            />
                            <a
                                class='bg-white text-zinc-900 hover:bg-zinc-200 w-fit py-3 px-6 text-xl rounded-lg hover:cursor-pointer'
                                href='/search'
                            >
                                Start Searching
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
