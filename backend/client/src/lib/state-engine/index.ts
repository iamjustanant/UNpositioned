import { fetcher } from "../fetch";
import stateMachine from "./store";
import { AnyDocument } from "../types";
import limitAPI from "./limit";

const loadTextQuery = (queryStr: string) => {
    fetcher({
        name: "termsearch",
        queryStr,
        doc: { docType: "un" },
        limit: limitAPI.getLimit,
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
        limit: limitAPI.getLimit,
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
        limit: limitAPI.getLimit,
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
};

const loadDocQuery = (doc: AnyDocument) => {
    fetcher({ name: "docsearch", doc, limit: limitAPI.getLimit }).then(
        (res) => {
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
        }
    );
};

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
        loadTextQuery(queryStr);
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
        loadDocQuery(doc);
    },

    reload() {
        if (stateMachine.getState().stage === "initial-search") {
            loadTextQuery(stateMachine.getState()["initialSearch"]);
        } else if (stateMachine.getState().stage === "doc-search") {
            loadDocQuery(stateMachine.getState()["docSearch"]);
        }
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
