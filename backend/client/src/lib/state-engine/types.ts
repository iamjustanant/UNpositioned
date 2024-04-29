import { AnyDocument, Rep_Document, UN_Document, X_Document } from "../types";

export type State =
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
          docSearch: AnyDocument;
          results: {
              status: "loading" | "loaded";
              similarDocs: AnyDocument[];
          };
      };

export type StateHistory = State[];
