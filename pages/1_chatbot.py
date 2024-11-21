import os
import sys

import streamlit as st
from openai import OpenAI

# Data handling imports
import csv

# Utility imports
from datetime import datetime
import time

# Configuration imports
import config as cfg

deploy = cfg.deploy
if deploy:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
else:
    from dotenv import load_dotenv
    load_dotenv('.env')

# OpenAI and LangChain imports
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from fpdf import FPDF

# Define the chatbot model
chatbot_model = "gpt-3.5-turbo"

# Initialize embeddings with OpenAI's text-embedding-3-large model
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Define the persist directory for the Chroma database
persist_directory = "./chroma_db"

# Create a Chroma instance for annual and quarterly collections
jnj_vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings, collection_name='jnj')

# Function to find relevant entries from the Chroma database
def find_relevant_entries_from_chroma_db(query, selected_collection):
    if selected_collection == "JNJ":
        vectordb = jnj_vectordb

    results = vectordb.similarity_search_with_score(query, k=30)
    
    for doc, score in results:
        print(f"Similarity: {score:.3f}")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")
        print("---")

    return results

# Function to generate a GPT response
def generate_gpt_response(user_query, chroma_result, client):
    current_year = datetime.now().year
    last_quarter = 2

    combined_prompt = f"""User query: {user_query}

    You are a employee at ALCON Inc to find new inovation from different company. Generate a report on the competitors of what's they have doing. Write as long as possible, generate a comprehensive report. Add bullet points also if needed

    Please provide an augmented response considering the following related information from our database:
    {chroma_result}

    The current year is {current_year} and the last available quarter is {last_quarter}. 

    Format your response as follows:
    **Augmented Response**

    [Your augmented response here]
    """
    response = client.chat.completions.create(
        model=chatbot_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant capable of providing context-aware responses."},
            {"role": "user", "content": combined_prompt}
        ]
    )

    return response.choices[0].message.content

def log_response_time(query, response_time, is_first_prompt):
    csv_file = 'responses.csv'
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Query', 'Response Time (seconds)', 'Is First Prompt'])
        writer.writerow([datetime.now(), query, f"{response_time:.2f}", "Yes" if is_first_prompt else "No"])

def query_interface(user_query, is_first_prompt, selected_collection, client):
    start_time = time.time()

    chroma_result = find_relevant_entries_from_chroma_db(user_query, selected_collection)
    gpt_response = generate_gpt_response(user_query, str(chroma_result), client)

    logging_response_time = True
    if logging_response_time:
        end_time = time.time()
        response_time = end_time - start_time

        log_response_time(user_query, response_time, is_first_prompt)

    return gpt_response

def create_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    return pdf

def download_pdf_button(response):
    pdf = create_pdf(response)
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Download Response as PDF",
        data=pdf_output,
        file_name="chatbot_response.pdf",
        mime="application/pdf"
    )

def display_chatbot():
    st.title("💬 Chatbot")
    st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate reports abouts competitors. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    )
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if api_key:
        client = OpenAI(api_key=api_key)
        selected_collection = st.radio("Select Time Period (Will Work on other companies)", ("JNJ","RXSight", "Zeiss IOLs"))
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                safe_content = message["content"].replace('$', '\\$')
                st.markdown(safe_content, unsafe_allow_html=True)  

        response = None
        if prompt := st.chat_input("Type your question here..."):
            with st.chat_message("user"):
                safe_prompt = prompt.replace('$', '\\$')
                st.markdown(safe_prompt) 
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Thinking..."):
                is_first_prompt = len(st.session_state.messages) == 1
                response = query_interface(prompt, is_first_prompt, selected_collection, client)

            with st.chat_message("assistant"):
                safe_response = response.replace('$', '\\$')
                st.markdown(safe_response, unsafe_allow_html=True) 
            st.session_state.messages.append({"role": "assistant", "content": response})

        if response:
            download_pdf_button(response)

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    else:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")

def main():
    display_chatbot()   

if __name__ == "__main__":
    main()
