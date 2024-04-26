import { Loader } from "lucide-solid";

const CustomLoader = () => (
    <div class='w-full h-full flex flex-row items-center justify-center p-8'>
        <Loader class='animate-spin text-zinc-100' />
    </div>
);

export default CustomLoader;
