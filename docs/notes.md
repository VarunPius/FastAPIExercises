# FastAPI

# Start application
We start the application with `uvicorn`. [$$$explain what's uvicorn]
```sh
# Basic start
uvicorn run:app --reload

# with ports
uvicorn run:app --port 8000 --reload

# when start is within a directory; here its under `src`
uvicorn src.main:app --reload
```
