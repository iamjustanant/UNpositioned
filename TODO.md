# TODOs

## Notes (EVERYONE READ)

1. I made a `Makefile`. Now, running the server should be as simple as `make dev`. You should see the project frontend.
   a. If the frontend is ever out of date, run `make client-build` to rebuild it, and then run `make dev` again.
   b. If you don't have `make`, you'll need to install it (via [brew](https://formulae.brew.sh/formula/make) on Mac, or via this [guide](https://medium.com/@samsorrahman/how-to-run-a-makefile-in-windows-b4d115d7c516) for Windows).
   c. If you run Windows, it might be easier actually to just copy-paste the commands in the `Makefile` into your terminal. Fucking Windows.
   d. This won't work until _at least Phase 2 is complete_ because y'all need to fill in the function definitions or else Python will complain.

2. You'll want to create a database called `ourdb` in MySQL Workbench. You don't have to put any tables in it for now.

3. In general, should you want to run SQL, it'll look something like this:
   `data = mysql_engine.query_selector(query)` where `query` is your SQL query string.

## Phase 1: DUE TUES 3/19 11:59PM

**Assigned to: [ONE PERSON: Juan, Bing, or Ant]**

Create a SQL file that creates a table for each of our data-sets, and inserts all the data. I don't really care how it's done.

Follow the example of the current, existing `init.sql` -- for each table: first, drop the existing table if it exists, then create the table and define its schema, and then insert the data.

Once done, make sure to replace the `init.sql` file in the root directory with the one you just created, commit, and push to Git.

Then, see Item 3 in **Introduction**.

## Phase 2: DUE SATURDAY 3/22 11:59PM

**Assigned to: [TWO REMAINING PEOPLE]**

Person 1: complete the TODO in `backend/routes/DocSearchUN.py`.
Person 2: complete the TODO in `backend/routes/DocSearchX.py`.

## Phase 3: DUE TUES 3/26 11:59PM

**Assigned to: @Dan**

Create a functional frontend for the project.

You'll want to quickly learn [Svelte](https://svelte.dev/docs/introduction) and then edit the Svelte project within `backend/client`.

## Phase 4 (OPTIONAL)

**Assigned to: whoever wants to do it**

Implement the TODO in `backend/routes/Summarize.py`
