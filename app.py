from fastapi import FastAPI
from ingest import ingest

app = FastAPI()

@app.get("/ingest")
def ingest_data():
    print("The data in the \"ingest\" folder will now be ingested.")
    ingest()
    return {
        "message": "Data has been ingested"
    }

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }