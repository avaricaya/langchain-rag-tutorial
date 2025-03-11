import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def get_reponse(query_text):
    
    # parses arguments (query)
    ##parser = argparse.ArgumentParser()
    ##parser.add_argument("query_text", type=str, help="The query text.")
    ##args = parser.parse_args()
    ##query_text = args.query_text
        
    # Prepare the DB.
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB for similar chunks
    results = db.similarity_search_with_relevance_scores(query_text, k=25)

    ##results = db.similarity_search_with_score(query_text, k=3) ## change number of pieces to the number of pieces that reach a certain relavancy threshold
    ##Can use a different method the restricts based on similarity score vs number of chunks?


    ###if len(results) == 0 or (results[0][1] < 0.5):
       ## print(f"Unable to find matching results.")
       ## return
    
    ##creates prompt for ollama
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

   ##gets ollama reponse to prompt
    model = ChatOllama(model = "llama3.1", temperature = 0.3)
    response_text = model.invoke(prompt).content

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    return(formatted_response)

