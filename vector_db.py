from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
VECTOR_DB_PATH = "./data/onboarding_documents_collection"

EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True},
)

VECTOR_STORE = Chroma(
    collection_name="onboarding_documents_collection",
    embedding_function=EMBEDDINGS,
    persist_directory=VECTOR_DB_PATH
)