import sys
from ingest import load_pdf_pages

def main(*args):
    print("Hello from rag-app!")
    print("You have passed: ", args)
    print(f"Will pass {args[0][1]} to ingest")

    file_path = args[0][1]
    docs = load_pdf_pages(file_path)
    
    print("docs", docs)

if __name__ == "__main__":
    main(sys.argv)
