from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os
import shutil
import argparse


CHROMA_PATH = "chroma"
data_path = "cs_data"


def main():
    update_path()
    generate_data_store()

def update_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="The file path of the markdown.")
    args = parser.parse_args()
    data_path = args.file_path

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(data_path, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

   ## document = chunks[10]
   ## print(document.page_content)
   ## print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    first = chunks[0:200]
    print(len(chunks))
    db = Chroma.from_documents(
        first, embeddings, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
