import os
import json
from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from vector_db import VECTOR_STORE

DATA_PATH = Path("./data/unstructured/")
VECTOR_DB_LIST = Path("./data/vector_db_list.json")


def load_pdf_pages(file_path: str) -> list[Document]:
    reader = PdfReader(file_path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]


def split_text(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        add_start_index=True
    )

    all_splits = text_splitter.split_documents(docs)

    return all_splits

def add_to_vector_db(all_splits):
    vector_store = VECTOR_STORE

    print("all_splits: ", all_splits)

    indexes = vector_store.add_documents(documents=all_splits)
    return indexes


def ingest():
    print(f"Will convert contents of {DATA_PATH} into embeddings and will add them to the vector database")

    # Using JSON file to check if a file already exists in vectordb
    # If it exists, the program does not add that file to VectorDB
    with open(VECTOR_DB_LIST, "r") as f:
        vector_db_json = json.load(f)

    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf") and file not in vector_db_json["files_in_vector_db"]:
            print(f"Adding file {file} to vector database")

            vector_db_json["files_in_vector_db"].append(file)

            loaded_pdf_pages = load_pdf_pages(f"{DATA_PATH}/{file}")
            all_splits = split_text(loaded_pdf_pages)
            add_to_vector_db(all_splits)

            print(f"Added file {file} to vector database")
        print("---------------------------------")

    with open(VECTOR_DB_LIST, "w") as f:
        json.dump(vector_db_json, f)
