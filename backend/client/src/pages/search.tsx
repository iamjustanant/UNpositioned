import { Component, createEffect, Suspense } from "solid-js";
import { useRouteData } from "@solidjs/router";
import type { AboutDataType } from "./about.data";

export default function Search() {
    return (
        <section class='bg-pink-100 text-gray-700 p-8'>
            <h1 class='text-2xl font-bold'>Search</h1>
        </section>
    );
}
