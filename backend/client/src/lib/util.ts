export const buildURL = (
    baseURL: string,
    queries: {
        [key: string]: string | number | boolean | null | undefined;
    }
) => {
    const cleanText = (
        query: string | number | boolean | null | undefined
    ): string => {
        if (query === null || query === undefined) {
            return "";
        }
        // remove leading and trailing whitespaces, replace spaces with %20, and encodeURI
        return encodeURI(query.toString().trim().replace(/ /g, "+"));
    };

    const removeTrailingSlash = (url: string): string => {
        // remove trailing slash at end of url
        while (url[url.length - 1] === "/") {
            url = url.slice(0, -1);
        }
        return url;
    };

    const url = removeTrailingSlash(baseURL) + "?";
    const query = Object.keys(queries)
        .map((key) => {
            if (queries[key] === null || queries[key] === undefined) {
                return "";
            }
            return `${cleanText(key)}=${cleanText(queries[key])}`;
        })
        .join("&");

    return removeTrailingSlash(url + query);
};

export const debounce = (callback: Function, wait = 600) => {
    let timeout: ReturnType<typeof setTimeout>;

    return (...args: any[]) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => callback(...args), wait);
    };
};
