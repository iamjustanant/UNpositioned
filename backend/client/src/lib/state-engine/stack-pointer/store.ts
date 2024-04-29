import { createStore } from "solid-js/store";
import { StackPointer } from "./types";
import { defaultStackPointer } from "./constants";

export const [sp, setSP] = createStore<StackPointer>(defaultStackPointer);
