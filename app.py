from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return { "token": token }

def fake_decode_token(token):
    return User(
        username = token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

# Adds file to /data/unstructured, and re-ingests the data in that file
@app.post("/ingest")
async def ingest_data(file: UploadFile = File(None)):
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
async def user_query(query: Query):
    llm_answers = query_llm(query.user_query)
    return llm_answers


@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }
