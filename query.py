import json
import requests
from ingest import load_vector_db

OLLAMA_API_URL = "http://localhost:11434/api"

def query_vectordb():
    user_question: str = input("Input your question to retrieve answers from the vector database: ")
    
    vector_store = load_vector_db()
    results = vector_store.similarity_search_with_score(user_question)
                
    print("RESULTS: ", results)

def query_llm():
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