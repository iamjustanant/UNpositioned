export const UNmeta = (contents: string) => {
    const year = contents.substring(3, contents.indexOf(","));
    const country = contents.substring(
        contents.indexOf(",") + 2,
        contents.indexOf(" said: ")
    );
    const remaining = contents.substring(contents.indexOf(" said: ") + 7);
    return { year, country, remaining };
};
