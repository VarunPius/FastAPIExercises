from src import app

@app.get("/")
async def home():
    return {"Hello":"World"}