import os
from dotenv import load_dotenv
import logging
import shutil
import streamlit as st
import config as cfg
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb

# Load environment variables
deploy = cfg.deploy
if deploy:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    load_dotenv('.env')  # looks for .env in Python script directory unless path is provided
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Document locations (relative to this py file)
folder_paths = ['data']
DB_PATH = "./chroma_db"  # Centralized path for the database

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_txt_files(folders):
    """
    Process TXT files from specified folders and convert them to a list of LangChain documents.
    Each file is treated as a separate document.
    """
    all_docs = []
    for folder in folders:
        if not os.path.exists(folder):
            logging.warning(f"Folder '{folder}' does not exist.")
            continue
        
        logging.info(f"Processing folder: {folder}")
        txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
        
        for file in txt_files:
            file_path = os.path.join(folder, file)
            logging.info(f"Processing TXT file: {file_path}")
            
            # Read TXT file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = {
                "source": file
            }
            doc = Document(page_content=content, metadata=metadata)
            all_docs.append((file, doc))
            
            logging.info(f"Processed TXT file: {file}")
    
    logging.info(f"Total TXT documents created: {len(all_docs)}")
    return all_docs

def insert_into_vector_db(txt_docs):
    """
    Inserts documents into vector databases for TXT data.
    """
    try:
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model='text-embedding-3-large')

        client = chromadb.PersistentClient(path=DB_PATH)  # Use centralized DB_PATH
        
        # Process and insert TXT documents into separate collections
        for file, doc in txt_docs:
            collection_name = file.replace('.txt', '')
            collection = client.get_or_create_collection(
                name=collection_name,
                metadata={'hnsw:space': 'cosine'}
            )
            vectorstore = Chroma(
                client=client,
                collection_name=collection_name,
                embedding_function=embeddings,
            )
            vectorstore.add_documents(documents=[doc])
            logging.info(f"Inserted document from {file} into the {collection_name} vector store")
    except Exception as e:
        logging.error(f"Error inserting documents into vector store: {str(e)}")
        raise

def delete_vector_db():
    """
    Deletes all files and subdirectories inside the Chroma database directory to ensure a fresh start.
    """
    try:
        # Check if the directory exists
        if os.path.exists(DB_PATH):
            # Delete all files and subdirectories in the directory
            for filename in os.listdir(DB_PATH):
                file_path = os.path.join(DB_PATH, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    logging.info(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logging.info(f"Deleted directory: {file_path}")
            logging.info(f"All files and subdirectories in the chroma_db directory deleted: {DB_PATH}")
        else:
            logging.warning(f"Directory {DB_PATH} does not exist, no files to delete.")
    except Exception as e:
        logging.error(f"Error accessing or deleting files in chroma_db directory: {str(e)}")
        raise

def main():
    """
    Main function to process TXT files and populate the vector database.
    """
    try:
        # Delete existing vector database
        delete_vector_db()
        logging.info("Existing vector database deleted")
        
        # Process TXT files
        txt_docs = process_txt_files(folder_paths)

        # Insert documents into the vector database
        insert_into_vector_db(txt_docs)

        logging.info("Vector database population completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
