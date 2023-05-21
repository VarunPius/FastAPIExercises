# FastAPI

# Installing FastApi
To install FastAPI using uvicorn:
```
poetry add fastapi uvicorn
```

# Start application
We start the application with `uvicorn`. [//TODOexplain what's uvicorn]
```sh
# Basic start
uvicorn run:app --reload

# with ports
uvicorn run:app --port 8000 --reload

# when start is within a directory; here its under `src`
uvicorn src.main:app --reload
```
