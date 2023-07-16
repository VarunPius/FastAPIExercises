# Models vs Schemas
`Models` will be used to define database tables, whereas `Schemas` will be sued to define Pydantic schemas.
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