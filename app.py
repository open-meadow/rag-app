from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ingest import ingest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/ingest")
def ingest_data():
    print("The data in the \"ingest\" folder will now be ingested.")
    ingest()
    return {
        "message": "Data has been ingested"
    }

@app.post("/query")
async def user_query():
    print("Backend received request")
    return { "message": "2" }

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }