import { createStore } from "solid-js/store";
import { Limit } from "./types";
import { defaultLimit } from "./constants";

export const [limit, setLimit] = createStore<Limit>(defaultLimit);
