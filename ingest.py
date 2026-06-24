import pypdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
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