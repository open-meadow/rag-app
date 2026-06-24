import os
import json
from pathlib import Path
from ingest import load_pdf_pages, split_text, add_to_vector_db, load_vector_db

DATA_PATH = Path("./data/unstructured/")
VECTOR_DB_LIST = Path("./data/vector_db_list.json")

def main(*args):
    while True:
        user_input = int(input("Press 1 to ingest, 2 to query and 3 to exit: "))
        
        match user_input:
            case 1:
                print(f"Will convert contents of {DATA_PATH} into embeddings and will add them to the vector database")

                # Using JSON file to check if a file already exists in vectordb
                # If it exists, the program does not add that file to VectorDB
                with open(VECTOR_DB_LIST, "r") as f:
                    vector_db_json = json.load(f)
                
                for file in os.listdir(DATA_PATH):
                    if file.endswith(".pdf") and file not in vector_db_json["files_in_vector_db"]:
                        vector_db_json["files_in_vector_db"].append(file)
                        
                        loaded_pdf_pages = load_pdf_pages(Path(file))
                        print("loaded_pdf_pages")
                        
                
                with open(VECTOR_DB_LIST, "w") as f:
                    json.dump(vector_db_json, f)
                
                break
            case 2:
                break
            case 3:
                print("Exiting")
                return
            case _:
                print("Incorrect input. Please try again")

    # file_path = args[0][1]
    # docs = load_pdf_pages(file_path)
    # all_splits = split_text(docs)
    # indexes = add_to_vector_db(all_splits)
    
    # print("indexes: ", indexes)
    
    # vector_store = load_vector_db()
    # results = vector_store.similarity_search_with_score("How many days of annual leave per calendar year?")
    # print("results: ", results)
    
    

if __name__ == "__main__":
    main()
