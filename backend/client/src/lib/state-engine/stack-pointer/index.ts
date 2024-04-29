import { setSP, sp } from "./store";

const spAPI = {
    get getSP() {
        return sp.n;
    },

    setSP(n: number) {
        setSP({
            n,
        });
    },

    inc() {
        setSP({
            n: sp.n + 1,
        });
    },

    dec() {
        setSP({
            n: sp.n - 1,
        });
    },

    reset() {
        setSP({
            n: 0,
        });
    },
};

export default spAPI;
