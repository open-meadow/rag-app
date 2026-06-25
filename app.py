from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingest import ingest
from query import query_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Query(BaseModel):
    user_query: str

@app.get("/ingest")
def ingest_data():
    print("The data in the \"ingest\" folder will now be ingested.")
    ingest()
    return {
        "message": "Data has been ingested"
    }

@app.post("/query")
async def user_query(query: Query):
    print("Backend received request: ", query)
    llm_answers = query_llm(query.user_query)
    return llm_answers

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }