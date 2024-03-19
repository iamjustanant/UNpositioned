# SPRINT 1 TODOS: FOR P03 (DUE WEDNESDAY, 3/27/24)

## Notes

I made a `Makefile`. Now, running the server should be as simple as `make dev`. You should see the project frontend at `localhost:5000`.

-   If the frontend is ever out of date, run `make client-build` to rebuild it, and then run `make dev` again.
-   If you don't have `make`, you'll need to install it (via [brew](https://formulae.brew.sh/formula/make) on Mac, or via this [guide](https://medium.com/@samsorrahman/how-to-run-a-makefile-in-windows-b4d115d7c516) for Windows).

## Phase 1: DUE WEDNESDAY 3/19 11:59PM

**Assigned to: @Anthony**

Complete the TODO in `init.sql`.

## Phase 2: DUE SUNDAY 3/22 11:59PM

**Assigned to: @Anthony, @Bing, @Juan**

Person 1: complete the TODO in `backend/routes/DocSearchUN.py`.
Person 2: complete the TODO in `backend/routes/DocSearchX.py`.

For both, I have an honestly kinda-working naive implementation already there.
Go do your data-science dark magic to make it better, idk.

## Phase 3: DUE TUES 3/26 11:59PM

**Assigned to: @Dan**

Create a functional frontend for the project.

You'll want to quickly learn [Svelte](https://svelte.dev/docs/introduction) and then edit the Svelte project within `backend/client`.

# SPRINT 2 OVERVIEW (DUE honestly no fucking clue)

No TODOs yet here, just vibes/thoughts.

_NOTE_: Anytime I reference **dark magic**, I'm saying this is a great place to insert data science code that shows you paid attention in class or whatever. idk what we're learning but whatever is on-brand for frenchie's teachings.

1. You'll see I setup a schema in `init.sql`. Try to understand it. Basically,

    - `x_docs`, `un_docs` will contain raw document data.
    - `topics` lets us index for issues.
    - `rel_x_topics` specifies a many-to-many relationship between topics and tweets.

        How this would look, for instance, is each tweet could reference >=1 topics, and a topic can be referenced in >=1 tweet.

    - `rel_un_topics` does the same between topics and UN papers.

2. We should aim to _precompute_ this data to make it super processable later?

    First, in `app.py`, we should add a new section after initial DB setup, where we call some kind of "optimize function". The function should do the following:

    1. For each tweet, parse the tweet to find what topics it references, and then build the corresponding entries in `rel_x_topics`. Do the same for `rel_un_topics`.

        That requires computing, for each entry in both tables, a relevancy and agreement score. This way, when querying later, we can instantly just sort for the most relevant/agreed-upon topics.

        This is **dark magic** territory.

3. Then, we should modify the backend to support more complex queries.

    In `routes`, we can add a new route called `MainSearch.py` or something. This route should support taking as input a query of the following form:

    ```ts
    {
      // a single human-language text query (i.e. "balancing climate change and the economy")
      "query": string;
    }
    ```

    It will then do the following:

    1. Translate the query into a set of topics (somehow??). This is **dark magic** territory. This should also probably be a sub-function.

    2. Perform a SQL query to then efficiently pull up, using our precomputed data, the most relevant tweets and UN papers.

    3. Summarize the opinion presented in the UN papers, taking into light consideration the opinion of the tweets, somehow. This _might_ be **dark magic** territory. It could also be ChatGPT territory.

    4. Return the summarized opinion, and the most relevant tweets and UN papers in one JSON response.

    Once done, we should be able to remove the other routes (i.e. `DocSearchUN.py`, `DocSearchX.py`), as they'll be redundant.

If this doesn't meet TA requirements, we could uh, store lots more metadata in each of the tables. Maybe who they agree with, how impactful the message was, idk. This would let us do a lot more **dark magic** precomputing and querying.
