import { fetcher } from "../fetch";
import { MAX_DOCS } from "./constants";
import stateMachine from "./store";
import { AnyDocument } from "../types";

const stateAPI = {
    get state() {
        return stateMachine.getState();
    },

    makeInitialSearch(queryStr: string) {
        stateMachine.pushState({
            stage: "initial-search",
            initialSearch: queryStr,
            results: {
                status: "loading",
                un_results: [],
                rep_results: [],
                x_results: [],
            },
        });
        fetcher({
            name: "termsearch",
            queryStr,
            doc: { docType: "un" },
            limit: MAX_DOCS,
        }).then((res) => {
            const prev = stateMachine.getState();
            if (prev.stage !== "initial-search")
                throw new Error("State Invariant Violation");
            stateMachine.replaceState({
                ...prev,
                results: {
                    ...prev.results,
                    status: "loaded",
                    un_results: res,
                },
            });
        });
        fetcher({
            name: "termsearch",
            queryStr,
            doc: { docType: "x" },
            limit: MAX_DOCS,
        }).then((res) => {
            const prev = stateMachine.getState();
            if (prev.stage !== "initial-search")
                throw new Error("State Invariant Violation");
            stateMachine.replaceState({
                ...prev,
                results: {
                    ...prev.results,
                    x_results: res,
                },
            });
        });
        fetcher({
            name: "termsearch",
            queryStr,
            doc: { docType: "rep" },
            limit: MAX_DOCS,
        }).then((res) => {
            const prev = stateMachine.getState();
            if (prev.stage !== "initial-search")
                throw new Error("State Invariant Violation");
            stateMachine.replaceState({
                ...prev,
                results: {
                    ...prev.results,
                    rep_results: res,
                },
            });
        });
    },

    makeDocSearch(doc: AnyDocument) {
        stateMachine.pushState({
            stage: "doc-search",
            initialSearch: "",
            docSearch: doc,
            results: {
                status: "loading",
                similarDocs: [],
            },
        });
        fetcher({ name: "docsearch", doc, limit: MAX_DOCS }).then((res) => {
            const prev = stateMachine.getState();
            if (prev.stage !== "doc-search")
                throw new Error("State Invariant Violation");
            stateMachine.replaceState({
                ...prev,
                results: {
                    ...prev.results,
                    status: "loaded",
                    similarDocs: res,
                },
            });
        });
    },

    get canGoBack() {
        return stateMachine.canTraverseBack;
    },

    get canGoForward() {
        return stateMachine.canTraverseFwd;
    },

    goBack() {
        stateMachine.traverseBack();
    },

    goForward() {
        stateMachine.traverseFwd();
    },

    get searchQuery() {
        return stateMachine.getState().initialSearch;
    },

    updateSearchQuery(queryStr: string) {
        stateMachine.replaceState({
            ...stateMachine.getState(),
            initialSearch: queryStr,
        });
    },
};

export default stateAPI;
