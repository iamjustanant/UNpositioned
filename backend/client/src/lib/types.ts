export type DocType = "un" | "rep" | "x";

export type FullDocument<T extends DocType = DocType> = {
    docID: string;
    docType: T;
    contents: string;
};

export type UN_Document = {
    docID: string;
    docType: "un";
};

export type Rep_Document = {
    docID: string;
    docType: "rep";
};

export type X_Document = {
    docID: string;
    docType: "x";
};

export type Document = UN_Document | Rep_Document | X_Document;
