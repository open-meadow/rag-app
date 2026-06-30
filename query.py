import json
import re
import requests

from vector_db import VECTOR_STORE
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3.5:4b"
VLLM_API_URL = "http://0.0.0.0:8000/v1/chat/completions"
VLLM_MODEL = "Qwen/Qwen3-0.6B"

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
                
    data_ollama = {
        "model": OLLAMA_MODEL,
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

    data_vllm = {
        "model": VLLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"""
                    You are an HR representative answering questions about your company's onboarding process from a new hire.
                    You will be give a question from the new hire.
                    Only answer from the provided context. Do not make up answers.
                        
                    ### CONTEXT
                    {context}
                """
            },
            {
                "role": "user",
                "content": user_question
            }
        ],
        "stream": False,
        # "max_tokens": 50
    }
                
    with requests.post(f"{VLLM_API_URL}", headers={"content-type": "application/json"}, json=data_vllm) as res:
        response = res.json()
    
    print("RES: ", response)

    if "thinking" in response: # if Ollama               
        llm_thinking = response["thinking"]
        llm_response = response["response"]
    else: # if vLLM
        print("LLM thinking: ", response["choices"][0]["message"]["content"])

        # combined res is in the form <think>Thinking string</think> Response
        # Need to separate thinking and response
        llm_output = response["choices"][0]["message"]["content"]
        
        llm_thinking = ""
        
        match = re.search(r"<think>(.*?)</think>(.*)", llm_output, re.DOTALL)

        if match:
            llm_thinking = match.group(1).strip()
            llm_response = match.group(2).strip()
        else:
            llm_thinking = ""
            llm_response = llm_output


    return {
            "LLM_thinking": llm_thinking,
            "LLM_response": llm_response
        }