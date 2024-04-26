import { createStore } from "solid-js/store";
import {
    DocType,
    Document,
    Rep_Document,
    UN_Document,
    X_Document,
} from "./types";
import { createResource, createSignal } from "solid-js";
import { Endpoint, fetcher } from "./fetch";

const MAX_DOCS = 25;

type State =
    | {
          stage: "not-started";
          initialSearch: string;
      }
    | {
          stage: "initial-search";
          initialSearch: string;
          results: {
              status: "loading" | "loaded";
              un_results: UN_Document[];
              rep_results: Rep_Document[];
              x_results: X_Document[];
          };
      }
    | {
          stage: "doc-search";
          initialSearch: string;
          docSearch: Document;
          results: {
              status: "loading" | "loaded";
              similarDocs: Document[];
          };
      }
    | {
          stage: "doc-view";
          doc: Document;
      };

const [state, setState] = createStore<State>({
    stage: "not-started",
    initialSearch: "",
});

const stateMachine = {
    get getState() {
        return state;
    },

    makeInitialSearch(queryStr: string) {
        setState({
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
            setState((prev) => {
                if (prev.stage !== "initial-search") return prev;
                return {
                    ...prev,
                    results: {
                        ...prev.results,
                        status: "loaded",
                        un_results: res,
                    },
                };
            });
        });
        fetcher({
            name: "termsearch",
            queryStr,
            doc: { docType: "x" },
            limit: MAX_DOCS,
        }).then((res) => {
            setState((prev) => {
                if (prev.stage !== "initial-search") return prev;
                return {
                    ...prev,
                    results: {
                        ...prev.results,
                        x_results: res,
                    },
                };
            });
        });
        fetcher({
            name: "termsearch",
            queryStr,
            doc: { docType: "rep" },
            limit: MAX_DOCS,
        }).then((res) => {
            setState((prev) => {
                if (prev.stage !== "initial-search") return prev;
                return {
                    ...prev,
                    results: {
                        ...prev.results,
                        rep_results: res,
                    },
                };
            });
        });
    },

    makeDocSearch(doc: Document) {
        setState({
            stage: "doc-search",
            initialSearch: "",
            docSearch: doc,
            results: {
                status: "loading",
                similarDocs: [],
            },
        });
        fetcher({ name: "docsearch", doc, limit: MAX_DOCS }).then((res) => {
            setState((prev) => {
                if (prev.stage !== "doc-search") return prev;
                return {
                    ...prev,
                    results: {
                        ...prev.results,
                        status: "loaded",
                        similarDocs: res,
                    },
                };
            });
        });
    },

    viewFullDoc(doc: Document) {
        setState({
            stage: "doc-view",
            doc,
        });
    },
};

export default stateMachine;
