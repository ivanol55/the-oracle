# The Oracle
A tool to get answers to your doubts. Ask your questions, the human way.

## Starting the oracle
1. Make sure you have Docker installed running in your target machine
2. Make sure you have Docker's `compose` plugin installed
3. Clone this repository
4. Start up the project by running `create.sh` (future startups can just use `docker compose down` or `docker compose up -d --build` as necessary)
5. Navigate to `http://localhost:3000`
6. Start asking questions! (The first ever request might take a bit, the model needs to locally download)
7. Change `POPULATE_CHROMA` to `False` on `docker-compose.yaml` for future startups, as chroma will be properly populated then

## Adding knowledge to the Oracle
Data is fed to the oracle through the database found over at `data/knowledge/data.json` in this project. Just add entries there following that format! Keep in mind, refreshing the knowledgebase right now requires recreating ChromaDB's data by deleting `data/chroma/` and recreating the docker compose stack setting `POPULATE_CHROMA` to `True`. Remember setting it to `False` again after!
