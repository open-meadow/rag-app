from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel

from ingest import ingest
from query import query_llm

UPLOAD_DIR = Path("./data/unstructured")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Query(BaseModel):
    user_query: str

@app.post("/ingest")
async def ingest_data(file: UploadFile = File(None)):
# async def ingest_data():
    print("The data in the \"ingest\" folder will now be ingested.")
    print("This is the file: ", file)
    
    content = await file.read()
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    ingest()
    return {
        "message": "Data has been ingested",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content)
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

# Use vLLM from HuggingFace
# 
