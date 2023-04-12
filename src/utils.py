import os
import pinecone
import openai
import shutil
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from source import Source
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define an empty list to store Source objects
sources = []

# Define an empty list to store the embeddings
embeddings = OpenAIEmbeddings()

# Initialize the Pinecone vector store
pinecone.init(api_key = os.getenv("PINECONE_API_KEY"), 
              environment = os.getenv("PINECONE_ENVIRONMENT"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# Pass embeddings to Pinecone
# docsearch = Pinecone.from_texts([d.page_text for d in sources[0].pages], embeddings, index_name)

# Initialize the LLM
llm = OpenAI(temperature=0, openai_api_key=openai.api_key)

# Summarize sources
def summarize_sources(sources):
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(sources[0].pages)
    
    return summary

# Save the uploaded file to the specified folder and return the saved file path
def save_uploaded_file(uploaded_file, folder="data/sources"):
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Clear the existing sources directory
def clear_sources_directory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


# Create list of Source objects by extracting the pages from each uploaded file
def create_source_objects(uploaded_files):
    # Clear the existing files in the data/sources directory
    sources_directory = os.path.join("data", "sources")
    clear_sources_directory(sources_directory)

    for uploaded_file in uploaded_files:
        # Save the uploaded file to the data/sources folder
        saved_file_path = save_uploaded_file(uploaded_file)

        # Load and process the saved file
        loader = PyPDFLoader(saved_file_path)
        pages = loader.load_and_split()

        # Create a Source object
        source = Source(filename = uploaded_file.name, pages = pages)

        # Add the Source object to the sources list
        sources.append(source)

    return sources
