from ingest import ingest
from query import query_vectordb, query_llm

def main(*args):
    while True:
        user_input = int(input("Press 1 to ingest, 2 to query, 3 to get LLM response and 4 to exit: "))
        
        match user_input:
            case 1:
                ingest()
                break

            case 2:
                query_vectordb()
                break
            
            case 3:
               query_llm() 
               break
                
            case 4:
                print("Exiting")
                return

            case _:
                print("Incorrect input. Please try again")


if __name__ == "__main__":
    main()