Semantic Search

This project is about understading how semantic search compares with regular search.
Also how to actually use semantic search with PgVector and with Redis.

![App](https://github.com/mathurajai/semantic_search/blob/main/Screenshot%202025-01-18%20231605.png)

##########
Step 1
To start the Postgres with PgVector as docker container
On terminal, go to the directory where the project is cloned and run the following command
\```bash
cd ./db-setup
docker compose up -d
\```
It will start PgVector on port 5432
##########

##########
Step 2
To run the application directly from source file, follow below steps
1. Install Python (if not already installed)
Download the latest version of Python: Python Downloads(https://www.python.org/downloads/)

Install Python following the instructions on the download page.

2. Create Virtual environment and activate
On the terminal, go to the directory where the project is cloned and create the virtual env
\```bash
## Setting Up a Python Virtual Environment
python -m venv .venv
./.venv/Scripts/activate
\```

3. Install all the required packages on this virtual env
\```bash
pip install -r app/requirements.txt
\```