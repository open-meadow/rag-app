import os
import json
from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTOR_DB_PATH = "./data/onboarding_documents_collection"
DATA_PATH = Path("./data/unstructured/")
VECTOR_DB_LIST = Path("./data/vector_db_list.json")

def load_pdf_pages(file_path: str) -> list[Document]:
    reader = PdfReader(file_path)
    return [
        Document(
            page_content = page.extract_text() or "",
            metadata = { "source": file_path, "page": i },
        )
        for i, page in enumerate(reader.pages)
    ]

def split_text(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20,
        add_start_index = True
    )
    
    all_splits = text_splitter.split_documents(docs)
    
    return all_splits

def load_vector_db():
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs = { "normalize_embeddings": True },
    )
    
    vector_store = Chroma(
        collection_name = "onboarding_documents_collection",
        embedding_function = embeddings,
        persist_directory = VECTOR_DB_PATH
    )
    
    return vector_store

def add_to_vector_db(all_splits):
    vector_store = load_vector_db()

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