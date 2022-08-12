# Starting the server:
On a basic level, after the `venv` is activated/started, we start the server on which the FastAPI web app will run. 

We run the following to start the uvicorn server:
```
uvicorn main:app 
```

When in development server, we run in debug mode so that we don't have to restart everytime a change is made. It automatically reloads in debug mode everytime it senses a change. For debug mode:
```
uvicorn main:app --reload
```

When the project structure is setup, we can run it using the following:
```
uvicorn src.main:app --reload
```

# API Docs
Swagger can be access at:
http://localhost:8000/docs

Redoc can be accessed at:
http://localhost:8000/redoc
