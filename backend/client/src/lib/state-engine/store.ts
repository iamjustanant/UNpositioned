import { createStore } from "solid-js/store";
import { State, StateHistory } from "./types";
import { defaultState } from "./constants";
import spAPI from "./stack-pointer";

const [state, setState] = createStore<StateHistory>([defaultState]);

const stateMachine = {
    getState() {
        const [slice] = state.slice(spAPI.getSP, spAPI.getSP + 1);
        return slice;
    },

    pushState(s: State) {
        const historyUpToSP = state.slice(0, spAPI.getSP + 1);
        const newStateStack = [...historyUpToSP, s];
        const newSP = newStateStack.length - 1;
        setState(newStateStack);
        spAPI.setSP(newSP);
    },

    replaceState(s: State) {
        const historyUpToSP = state.slice(0, spAPI.getSP);
        const newStateStack = [...historyUpToSP, s];
        const newSP = newStateStack.length - 1;
        setState(newStateStack);
        spAPI.setSP(newSP);
    },

    get canTraverseBack() {
        return spAPI.getSP > 0;
    },

    get canTraverseFwd() {
        return spAPI.getSP < state.length - 1;
    },

    traverseBack() {
        if (spAPI.getSP === 0) {
            return;
        }
        spAPI.setSP(spAPI.getSP - 1);
    },

    traverseFwd() {
        if (spAPI.getSP === state.length - 1) {
            return;
        }
        spAPI.setSP(spAPI.getSP + 1);
    },
};

export default stateMachine;
