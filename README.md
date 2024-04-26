# Unpositioned

Quickly look for official international perspectives on various topics.

## Setup

1. Clone the repository to a local directory.
2. Install [Node.js](https://nodejs.org/), [Python](https://www.python.org/), [MySQL](https://www.mysql.com/), [Docker](https://www.docker.com/), and [Make](https://formulae.brew.sh/formula/make).
3. Make sure that Docker and MySQL are running in the background.

## Running Locally

```bash
make client-build # Every time you make changes to the frontend
make dev # Start the server
```

## Running Locally, with Docker

```bash
TEAM_NAME=teamname APP_PORT=5175 docker-compose up
```

## Deployment

Uncomment lines 22-23 in `backend/lib/Text_Processing_Utils.py` and line 26 in `backend/app.py`.

Change the URL in `backend/client/src/constants.ts` from "http://localhost:5000" to the server's URL (I think).

Then, upload to the INFO 4300 website as standard.

## Project Structure

-   `backend/`: Flask backend, in Python
    -   `backend/routes/`: API endpoints
    -   `backend/sql/`: Toolkit for executing MySQL queries
    -   `backend/lib/`: Utility and other shared functions
    -   `backend/init.sql`: Database schema
    -   `backend/app.py`: Main application
-   `backend/client/`: Svelte frontend, in TypeScript
-   `init.sql`: Database schema and data imports
