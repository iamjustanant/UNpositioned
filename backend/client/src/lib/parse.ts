export const UNmeta = (contents: string) => {
    const year = contents.substring(3, contents.indexOf(","));
    const country = contents.substring(
        contents.indexOf(",") + 2,
        contents.indexOf(" said: ")
    );
    const remaining = contents.substring(contents.indexOf(" said: ") + 7);
    return { year, country, remaining };
};

export const Tweetmeta = (contents: string, type: "x" | "rep") => {
    switch (type) {
        case "x":
            const firstLast = contents
                .substring(0, contents.indexOf(":") - 5)
                .trim();
            const actualTwt = contents.substring(contents.indexOf(":") + 1);
            return { name: firstLast, remaining: actualTwt };
        case "rep":
            const firstPart = contents.substring(0, contents.indexOf(":"));
            const name = firstPart.substring(0, contents.indexOf("(")).trim();
            const position = firstPart.substring(
                firstPart.indexOf("(") + 1,
                firstPart.indexOf(")")
            );
            const platform = firstPart.substring(
                firstPart.lastIndexOf(" ") + 1
            );
            const remaining = contents.substring(contents.indexOf(":") + 1);
            return { name, position, platform, remaining };
    }
};
