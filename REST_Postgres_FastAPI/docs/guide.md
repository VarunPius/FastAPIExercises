# Models vs Schemas
`Models` will be used to define database tables, whereas `Schemas` will be used to define Pydantic schemas.
Models are used to interact with database, whereas schemas will determine how output will look like.

# Auto reload
Everytime you make changes in local development, these changes need to be reflected into the containers *ideally*.
How do we achieve that?

Adding `volumes` in the Docker Compose file fixes that. Add as follows:
```sh
volumes:
      - .:/app
```

The above command will override the `COPY` operation we did in the original Docker file while building the image and have the code inside the container reflect any changes that were made on your local machine. The final `docker-compose.yaml` file should therefore include so.

# Docker Shortcuts:
```sh
docker ps -a
docker compose up
docker exec -it postgres_db psql -U vpiusr postgres
```

# Colima
Docker Desktop is no longer free to use in Mac. So, for replacement/alternative I used `colima`

When you run `docker ps -a` you will get the following error:
```sh
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the
docker daemon running?
```

To fix this, we run `colima` first:
```sh
colima start
```

Then try `docker ps -a`:
```sh
$ docker ps -a
CONTAINER ID   IMAGE                       COMMAND                  CREATED        STATUS                    PORTS                                       NAMES
d3ffef9580e3   postgres:latest             "docker-entrypoint.s…"   2 months ago   Up 15 seconds             0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres_db
033978c05262   rest_postgres_fastapi-web   "uvicorn run:app --r…"   2 months ago   Exited (0) 2 months ago                                               rest_postgres_fastapi-web-1
```
