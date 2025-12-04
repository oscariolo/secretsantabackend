from fastapi import FastAPI

app = FastAPI()

@app.get("/api/secret-santa/health")
async def healthCheck():
    return {"status": "ok"}

