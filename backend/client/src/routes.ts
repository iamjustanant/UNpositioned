import { lazy } from "solid-js";
import type { RouteDefinition } from "@solidjs/router";

import Home from "./pages/home";
import AboutData from "./pages/about.data";

type CustomRoute = RouteDefinition & {
    label: string;
    hidden?: boolean;
};

export const routes: CustomRoute[] = [
    {
        path: "/",
        component: Home,
        label: "Home",
    },
    {
        path: "/search",
        component: lazy(() => import("./pages/search")),
        label: "Search",
    },
    {
        path: "/about",
        component: lazy(() => import("./pages/about")),
        data: AboutData,
        label: "About",
    },
    {
        path: "**",
        component: lazy(() => import("./errors/404")),
        hidden: true,
        label: "Not Found",
    },
];
