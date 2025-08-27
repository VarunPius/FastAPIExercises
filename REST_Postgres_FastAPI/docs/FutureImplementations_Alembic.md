# Alembic Migrations
## Prompt:
I have a FastAPI project with the following structure:
```
FastAPI_project
├── docker-compose.yml
├── requirements.txt
├── resources
│   └── Dockerfile
├── run.py
└── src
    ├── __init__.py
    ├── config
    │   ├── db.py
    │   └── db_init.py
    ├── models
    │   ├── index.py
    │   └── user.py
    ├── routes
    │   ├── index.py
    │   └── user.py
    └── schemas
        ├── index.py
        └── user.py
```
The `db_init.py` file creates the database and the tables using the `Base.metadata.create_all(bind=engine)`. I want to migrate to using alembic instead.
What changes do I need to make and how do I create tables using Alembic before my web server starts.

# Gemini Solution:
## 1: Install Alembic:
First, add Alembic to your `requirements.txt` file:
```
fastapi
uvicorn
SQLAlchemy
psycopg2  # Or your database driver
alembic
```

Then, run `pip install -r requirements.txt` to install it.

## 2: Initialize Alembic:
Navigate to the root of your project (`FastAPI_project`) in your terminal and run the Alembic initialization command:
```bash
alembic init alembic
```
This will create an `alembic` directory (`migrations` would bebetter option as it seems to be the standard) with the followingstructure:
```sh
alembic/
├── alembic.ini
├── env.py
├── README
└── versions/
```

## 3: Configure Alembic:
- `alembic.ini`: This file contains Alembic's configuration settings. You'll need to update the `sqlalchemy.url` to match your database connection string defined in your FastAPI application (likely in `src/config/db.py`).

    Open `alembic.ini` and find the line starting with `sqlalchemy.url`. Modify it to point to your database URL. For example:
    ```toml
    sqlalchemy.url = postgresql://user:password@host:port/database
    ```
    
- `alembic/env.py`: This script is executed when you run Alembic commands. You need to configure it to connect to your SQLAlchemy engine and import your metadata.

    Open `alembic/env.py` and make the following changes:
    ```python
    import os
    import sys
    from logging.config import fileConfig

    from sqlalchemy import engine_from_config
    from sqlalchemy import pool

    from alembic import context

    # Add the path to your src directory to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

    # Import your database models and Base
    from src.config.db import Base, engine  # Import your engine if not using config
    from src.models import user  # Import all your model files

    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config

    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    target_metadata = Base.metadata

    # other values from the config, defined by the needs of env.py,
    # can be acquired:
    # my_important_option = config.get_main_option("my_important_option")
    # ... etc.


    def run_migrations_offline() -> None:
        """Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.

        Calls to context.execute() here emit the given string to the
        script output.

        """
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


    def run_migrations_online() -> None:
        """Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.

        """
        connectable = engine  # Use your existing engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()


    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
    ```

    Explanation of changes in `env.py`:   
    - `sys.path.append(...)`: This ensures that your `src` directory is in Python's path so that you can import your application modules.
    - `from src.config.db import Base, engine`: Import your SQLAlchemy `Base` and `engine` objects.
    - `from src.models import user`: Import your model files. Make sure to import all files containing your SQLAlchemy model definitions.
    - `target_metadata = Base.metadata`: This tells Alembic where to find your table definitions.

## 4. Remove Database Creation from `db_init.py`:
Delete or comment out the line `Base.metadata.create_all(bind=engine)` in your `src/config/db_init.py` file. Alembic will now handle the table creation.

## 5: Create Your First Migration:
Navigate to the root of your project (`FastAPI_project`) in your terminal and run the following command to generate your initial migration script:
```Bash
alembic revision -m "Initial database setup"
```
This will create a new Python file in the `alembic/versions` directory. This file will contain the instructions to create your tables based on your currentmodels.

## 6: Run the Migration:
To apply the migration and create the tables in your database, run:
```Bash
alembic upgrade head
```
This command tells Alembic to run all pending migrations up to the "head" revision (the latest one).

## 7: Integrating Alembic into Your FastAPI Startup:
You need to ensure that Alembic runs the migrations before your FastAPI application starts. You can achieve this in several ways:

### Method 1: Running Alembic in your run.py before starting Uvicorn:
Modify your `run.py` file to include the Alembic upgrade command:
```Python
import subprocess
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Import your routes
from src.routes import index, user

app.include_router(index.router)
app.include_router(user.router)

def run_migrations():
    """Runs Alembic migrations."""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        # Optionally, exit the application if migrations fail
        # import sys
        # sys.exit(1)

if __name__ == "__main__":
    run_migrations()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Method 2: Creating a separate script to run migrations:
Create a new Python file (e.g., `migrate.py`) in the root of your project:
```Python
import subprocess

def run_migrations():
    """Runs Alembic migrations."""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        # Optionally, exit the application if migrations fail
        # import sys
        # sys.exit(1)

if __name__ == "__main__":
    run_migrations()
```
Then, you would run this script separately before starting your FastAPI application (e.g., in your Dockerfile or a separate terminal).

### Method 3: Integrating with Docker Compose (Recommended for Dockerized Applications):
This is often the cleanest approach for Dockerized applications. You can create a separate service in your `docker-compose.yml` that runs the Alembic migrations before your main application service starts.

Modify your `docker-compose.yml` like this:
```YAML
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  api:
    build:
      context: ./resources
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
    depends_on:
      - db
      - migrations  # Ensure migrations run before the API

  migrations:
    build:
      context: ./resources
      dockerfile: Dockerfile
    command: alembic upgrade head
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
    depends_on:
      - db
    volumes:
      - ./src:/app/src
      - ./alembic:/app/alembic  # Mount the alembic directory

volumes:
  db_data:
```

Explanation of Docker Compose changes:
- A new service migrations is added.
- It uses the same Dockerfile as your `api` service (assuming your dependencies are installed there).
- The command: `alembic upgrade head` specifies the command to run when this service starts.
- It depends on the `db` service to ensure the database is running.
- The `api` service now depends on the `migrations` service, ensuring that `migrations` are complete before the API starts.
- Volumes are mounted to make your application code and Alembic configuration available inside the container.

Dockerfile (in `resources/Dockerfile`):

Your Dockerfile should include steps to install your requirements:
```Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /app/src
COPY ./alembic /app/alembic
COPY ./FastAPI_project/alembic.ini /app/alembic.ini

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Important Considerations:
- **Database URL**: Ensure the `DATABASE_URL` environment variable in your Docker Compose file (and potentially in your `alembic.ini` if you're not using environment variables there) correctly points to your database service.
- **Environment Variables**: It's good practice to use environment variables for database credentials.
- **Migration History**: Alembic keeps track of your migrations in the `alembic/versions` directory. Don't manually edit these files unless you know what you're doing.
- **Downgrading**: Alembic also allows you to downgrade migrations using the `alembic downgrade <revision>` command.
- **Testing**: Always test your migrations in a development environment before applying them to production.

By following these steps, you can successfully migrate your FastAPI project to use Alembic for database schema management and ensure that your tables are created before your web server starts. The Docker Compose method is generally recommended for containerized applications as it provides a clear and automated way to manage the database and migrations during deployment.   

# Claude Solution:
Setting Up Alembic in Your FastAPI Project
To migrate from manually creating tables with SQLAlchemy's Base.metadata.create_all() to using Alembic for database migrations, you'll need to make several changes. Here's a step-by-step guide:
## 1: Install Alembic
First, add Alembic to your requirements:
```sh
pip install alembic
echo "alembic>=1.7.5" >> requirements.txt
```

## 2: Initialize Alembic
Create an Alembic configuration in your project:
```sh
cd FastAPI_project
alembic init migrations
```
This will create a `migrations` directory and an `alembic.ini` file in your project root.

## 3: Configure Alembic
Edit the `alembic.ini` file to point to your database URL. Find the line with `sqlalchemy.url` and update it to match your database configuration. If you want to keep your database URL in your application config, you can leave this as is and override it in the next step.

## 4: Update the Alembic Environment
Modify the `migrations/env.py` file to use your SQLAlchemy models and configuration:
```py
# Add these imports at the top
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.config.db import Base, engine
from src.models.user import User  # Import all your models here

# Replace the existing target_metadata = None line with:
target_metadata = Base.metadata

# Update the run_migrations_online function to use your engine
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine  # Use your existing engine
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True  # For SQLite, you can remove this for other DBs
        )

        with context.begin_transaction():
            context.run_migrations()
```

## 5: Remove the Direct Table Creation
Modify your `db_init.py` file to stop using `Base.metadata.create_all()`:
```python
from src.config.db import engine
import alembic.config
import os
import sys

def init_db():
    # Optional: Run migrations programmatically instead of through CLI
    # This is one approach to run migrations when your app starts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    alembic_args = [
        '--raiseerr',
        '-c', os.path.join(project_root, 'alembic.ini'),
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)
```

## 6: Create Initial Migration
Generate your first migration based on your existing models:
```sh
alembic revision --autogenerate -m "Initial migration"
```

## 7: Apply Migrations
To create the tables, run:
```sh
alembic upgrade head
```

Or if you want to apply migrations programmatically when your server starts, use the updated `init_db()` function you modified in step 5.

## 8: Update Your Project Structure
Your project structure will now look like:
```
FastAPI_project
├── alembic.ini
├── docker-compose.yml
├── migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── xxxx_initial_migration.py
├── requirements.txt
├── resources
│   └── Dockerfile
├── run.py
└── src
    ├── __init__.py
    ├── config
    │   ├── db.py
    │   └── db_init.py
    ├── models
    │   ├── index.py
    │   └── user.py
    ├── routes
    │   ├── index.py
    │   └── user.py
    └── schemas
        ├── index.py
        └── user.py
```

## 9: Using Alembic in Docker
If you're using Docker, add the Alembic initialization to your startup script or Dockerfile:
```Dockerfile
# In your Dockerfile or a startup script
RUN alembic upgrade head
```

Or, keep the programmatic approach in your application startup code.

## Best Practices
- Never modify migration files after they've been applied to production.
- Create new migrations for each schema change.
- Test migrations thoroughly, especially downgrades.
- Include migrations in version control.

This setup gives you a robust migration system that tracks all database schema changes and allows for safe upgrades and downgrades.