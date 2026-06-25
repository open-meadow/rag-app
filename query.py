import json
import requests

from vector_db import VECTOR_STORE
OLLAMA_API_URL = "http://localhost:11434/api"

def query_vectordb():
    user_question: str = input("Input your question to retrieve answers from the vector database: ")
    
    vector_store = VECTOR_STORE
    results = vector_store.similarity_search_with_score(user_question)
                
    print("RESULTS: ", results)

def query_llm(uq: str =  ""):
    if not uq:
        user_question: str = input("Input your question to retrieve answers from the LLM: ")
    else:
        user_question = uq
                
    vector_store = VECTOR_STORE
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

    return {
        "LLM_thinking": response["thinking"],
        "LLM_response": response["response"]
    }