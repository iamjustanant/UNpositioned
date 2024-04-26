import { BACKEND_URL } from "~/constants";
import { buildURL } from "./utils";
import { DocType, Document, FullDocument } from "./types";

export type Endpoint = (
    | {
          // Gets you search results, of any desired type, given a word
          name: "termsearch";
          queryStr: string;
          doc: {
              docType: DocType;
          };
      }
    | {
          // Gets you similar results of UN type given a document of any type
          name: "docsearch";
          doc: Document;
      }
    | {
          // Gets you the preview of a document of any type
          name: "getdocpreview";
          doc: Document;
      }
    | {
          // Gets you the full document of any type
          name: "getdoc";
          doc: Document;
      }
) & {
    limit?: number;
};

const buildParams = (e: Endpoint) => {
    const limit = e.limit ?? 10;

    switch (e.name) {
        case "termsearch":
            return {
                text: e.queryStr,
                type: e.doc.docType,
                limit,
            };
        case "docsearch":
            return {
                doc_id: e.doc.docID,
                doc_type: e.doc.docType,
                limit,
            };
        case "getdocpreview":
            return {
                doc_id: e.doc.docID,
                doc_type: e.doc.docType,
            };
        case "getdoc":
            return {
                doc_id: e.doc.docID,
                doc_type: e.doc.docType,
            };
        default:
            throw new Error("Invalid endpoint name");
    }
};

const parseRes = (e: Endpoint, res: Array<string>) => {
    switch (e.name) {
        case "termsearch":
            return res.map((str) => {
                const [docID, docContents] = str.split("|||");
                return {
                    docID,
                    docType: e.doc.docType,
                    contents: docContents,
                };
            });
        case "docsearch":
            return res.map((str) => {
                const [docID, docContents] = str.split("|||");
                return {
                    docID,
                    docType: e.doc.docType,
                    contents: docContents,
                };
            });
        case "getdocpreview":
            if (res.length !== 1) throw new Error("Invalid response");
            return [
                {
                    docID: e.doc.docID,
                    docType: e.doc.docType,
                    contents: res[0],
                },
            ];
        case "getdoc":
            if (res.length !== 1) throw new Error("Invalid response");
            return [
                {
                    docID: e.doc.docID,
                    docType: e.doc.docType,
                    contents: res[0],
                },
            ];
        default:
            throw new Error("Invalid endpoint name");
    }
};

export const fetcher = async <T extends Endpoint = Endpoint>(
    e: T | null
): Promise<Array<FullDocument<T["doc"]["docType"]>>> => {
    if (!e) return [];

    const url = buildURL(`${BACKEND_URL}/api/${e.name}`, buildParams(e));

    const { res } = await (await fetch(url)).json();

    const parsedRes = parseRes(e, res);

    return parsedRes;
};
