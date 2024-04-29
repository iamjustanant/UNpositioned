import { setLimit, limit } from "./store";

const limitAPI = {
    get getLimit() {
        return limit.limit;
    },

    setLimit(n: number) {
        setLimit({
            limit: n,
        });
    },
};

export default limitAPI;
