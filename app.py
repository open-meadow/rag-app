from typing import Annotated
from fastapi import FastAPI, File, HTTPException, status, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pathlib import Path
from pydantic import BaseModel

from ingest import ingest
from query import query_llm
from auth import login_for_access_token, get_current_active_user, User

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

@app.post("/token")(login_for_access_token)

# Adds file to /data/unstructured, and re-ingests the data in that file
@app.post("/ingest")
async def ingest_data(current_user: Annotated[User, Depends(get_current_active_user)], file: UploadFile = File(None)):
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

# Sends query to LLM
@app.post("/query")
async def user_query(current_user: Annotated[User, Depends(get_current_active_user)], query: Query):
    llm_answers = query_llm(query.user_query)
    return llm_answers


@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }
