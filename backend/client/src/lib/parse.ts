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
            const [ignore0, followersSec, verifiedSec, userSaidWhatSec] =
                contents.split("|||").map((x) => x.trim());

            // Parse numbers
            const numFollowers = parseInt(followersSec);
            const isVerified = verifiedSec === "true";

            // Parse the rest
            const firstLast = userSaidWhatSec
                .substring(0, userSaidWhatSec.indexOf(":") - 5)
                .trim();
            const actualTwt = userSaidWhatSec.substring(
                userSaidWhatSec.indexOf(":") + 1
            );

            // Return
            return {
                name: firstLast,
                remaining: actualTwt,
                followers: numFollowers,
                verified: isVerified,
            };
        case "rep":
            const [ignore1, ignore2, biasConfidence, bias, rest] = contents
                .split("|||")
                .map((x) => x.trim());

            // Parse bias info
            const biasConfidenceNum = parseInt(biasConfidence);
            const biasStr = bias;

            // Parse the rest
            const firstPart = rest.substring(0, rest.indexOf(":"));
            const name = firstPart.substring(0, rest.indexOf("(")).trim();
            const position = firstPart.substring(
                firstPart.indexOf("(") + 1,
                firstPart.indexOf(")")
            );
            const platform = firstPart.substring(
                firstPart.lastIndexOf(" ") + 1
            );
            const remaining = rest.substring(rest.indexOf(":") + 1);

            // Return
            return {
                name,
                position,
                platform,
                remaining,
                biasConfidenceNum,
                biasStr,
            };
    }
};
