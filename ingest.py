from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

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

def add_to_vector_db(all_splits):
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs = { "normalize_embeddings": True },
    )

    vector_store = Chroma(
        collection_name = "onboarding_documents_collection",
        embedding_function = embeddings,
        persist_directory = "./chroma_langchain_db"
    )
    
    indexes = vector_store.add_documents(documents=all_splits)
    return indexes 