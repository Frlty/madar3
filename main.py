from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/server-info")
def server_info():
    return JSONResponse(content={"version": "1.90.0", "status": "ready"})

