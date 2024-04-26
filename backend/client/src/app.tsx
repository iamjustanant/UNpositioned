import type { Component } from "solid-js";
import { Link, useRoutes, useLocation } from "@solidjs/router";

import { routes } from "./routes";
import { MainNav } from "./components/custom/main-nav";

const App: Component = () => {
    const location = useLocation();
    const Route = useRoutes(routes);

    return (
        <>
            <MainNav />

            <main>
                <Route />
            </main>
        </>
    );
};

export default App;
