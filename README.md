# FeenixAI - Poem


## API

This API most use Python 3.10

To execute, run the following commands:

```bash
cd api

# install libraries
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create the `.env` file including the environment variables for the backend. To do this, run the following commands:

```bash
cp .env.example .env
```

Edit the `.env` file with the values for all the variables related to the database and the SECRET_KEY variable.

Then, create the containers for the PostgreSQL database with the following command:

```bash
# create postgres docker container
sudo docker compose up

# run api
fastapi dev main.py
```

## Frontend

This frontend app most use Node 20

To execute, run the following commands:

```bash
cd frontend

# install dependencies
npm install --save
cp .env.example .env

# run
npm run dev
```

Access [http://localhost:3000](http://localhost:3000).