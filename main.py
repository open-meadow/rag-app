import sys
from ingest import load_pdf_pages, split_text, add_to_vector_db

def main(*args):
    print("Hello from rag-app!")
    print("You have passed: ", args)
    print(f"Will pass {args[0][1]} to ingest")

    file_path = args[0][1]
    docs = load_pdf_pages(file_path)
    all_splits = split_text(docs)
    indexes = add_to_vector_db(all_splits)
    
    print("indexes: ", indexes)
    
    

if __name__ == "__main__":
    main(sys.argv)
