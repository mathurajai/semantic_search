Semantic Search

This project is about understading how semantic search compares with regular search.
Also how to actually use semantic search with PgVector and with Redis.

![App](https://github.com/mathurajai/semantic_search/blob/main/Screenshot%202025-01-18%20231605.png)

##########<br>
Step 1<br>
To start the Postgres with PgVector as docker container<br>
On terminal, go to the directory where the project is cloned and run the following command<br>
\```bash
cd ./db-setup
docker compose up -d

It will start PgVector on port 5432<br>
##########<br>

##########<br>
Step 2<br>
To run the application directly from source file, follow below steps<br>
1. Install Python (if not already installed)<br>
Download the latest version of Python: Python Downloads(https://www.python.org/downloads/)<br>

Install Python following the instructions on the download page.<br>

2. Create Virtual environment and activate<br>
On the terminal, go to the directory where the project is cloned and create the virtual env<br>
\```bash
## Setting Up a Python Virtual Environment
python -m venv .venv
./.venv/Scripts/activate
\```

3. Install all the required packages on this virtual env<br>
\```bash
pip install -r app/requirements.txt
\```