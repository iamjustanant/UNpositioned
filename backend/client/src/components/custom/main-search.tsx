import { SearchIcon } from "lucide-solid";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import stateMachine from "~/lib/state";

const MainSearch = (props: {
    searchText: string;
    setSearchText: (text: string) => void;
}) => {
    return (
        <div class='flex flex-row gap-8 w-[810px] h-fit'>
            <Input
                class='h-fit shadow-md text-white py-4 px-4 font-medium text-lg w-[600px] bg-zinc-800 border-none focus:border-none'
                placeholder='Enter any keywords to search...'
                value={props.searchText}
                onChange={(e) => props.setSearchText(e.currentTarget.value)}
            />
            <Button
                onClick={() => stateMachine.makeInitialSearch(props.searchText)}
                class='shadow-md h-full bg-white text-zinc-900 hover:bg-zinc-200 w-fit py-4 px-6 text-lg hover:cursor-pointer flex flex-row gap-2'
            >
                <SearchIcon class='size-5' /> Search
            </Button>
        </div>
    );
};

export default MainSearch;
