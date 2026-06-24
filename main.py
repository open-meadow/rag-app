import os
import json
import requests
from pathlib import Path
from ingest import ingest, load_vector_db

DATA_PATH = Path("./data/unstructured/")
VECTOR_DB_LIST = Path("./data/vector_db_list.json")
OLLAMA_API_URL = "http://localhost:11434/api"

def main(*args):
    while True:
        user_input = int(input("Press 1 to ingest, 2 to query, 3 to get LLM response and 4 to exit: "))
        
        match user_input:
            case 1:
                # print(f"Will convert contents of {DATA_PATH} into embeddings and will add them to the vector database")

                # # Using JSON file to check if a file already exists in vectordb
                # # If it exists, the program does not add that file to VectorDB
                # with open(VECTOR_DB_LIST, "r") as f:
                #     vector_db_json = json.load(f)
                
                # for file in os.listdir(DATA_PATH):
                #     if file.endswith(".pdf") and file not in vector_db_json["files_in_vector_db"]:
                #         vector_db_json["files_in_vector_db"].append(file)
                        
                #         loaded_pdf_pages = load_pdf_pages(f"{DATA_PATH}/{file}")
                #         all_splits = split_text(loaded_pdf_pages)
                #         add_to_vector_db(all_splits)

                #         print(f"Added file {file} to vector database")
                        
                
                # with open(VECTOR_DB_LIST, "w") as f:
                #     json.dump(vector_db_json, f)
                
                ingest()
                
                break
            case 2:
                user_question: str = input("Input your question to retrieve answers from the vector database: ")

                vector_store = load_vector_db()
                results = vector_store.similarity_search_with_score(user_question)
                
                print("RESULTS: ", results)
                
                break
            
            case 3:
                user_question: str = input("Input your question to retrieve answers from the LLM: ")
                
                vector_store = load_vector_db()
                results = vector_store.similarity_search(user_question)
                
                context = [result.page_content for result in results]
                
                data = {
                    "model": "qwen3.5:4b",
                    "prompt": user_question,
                    "system": f"""
                        You are an HR representative answering questions about your company's onboarding process from a new hire.
                        You will be give a question from the new hire.
                        Only answer from the provided context. Do not make up answers.
                        
                        ### CONTEXT
                        {context}
                        
                    """,
                    "stream": False
                }
                
                with requests.post(f"{OLLAMA_API_URL}/generate", json=data) as res:
                    response = res.json()
                
                print("LLM thinking: ", response["thinking"])
                print("------------------------------------")
                print("LLM response: ", response["response"])
                
                break
                
            case 4:
                print("Exiting")
                return
            case _:
                print("Incorrect input. Please try again")


if __name__ == "__main__":
    main()