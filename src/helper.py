import sys
import os
import textwrap
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import TokenTextSplitter, CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from src.prompt import template
from langchain.prompts import PromptTemplate
import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def file_processing(file_path):
    #load data from pdf
    loader = PyPDFLoader(file_path)
    data = loader.load()
    return data


def url_processing(url):
    loaders = UnstructuredURLLoader(urls=[url])
    data = loaders.load()
    return data

def generate_text_chunks(content):
    """Generate text chunks from either a PDF file or a URL."""
    
    if os.path.isfile(content):
        # Content is a file path
        data = file_processing(content)
    elif content.startswith("http://") or content.startswith("https://"):
        # Content is a URL
        data = url_processing(content)
    else:
        raise ValueError("Content must be a valid file path or URL.")

    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_documents(data)

def embedding(text_chunks):
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore=FAISS.from_documents(text_chunks, embeddings)

    return vectorstore


def chain_formation(vectorstore):


    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    
    )
    
    custom_prompt = PromptTemplate(
        template=template,
        input_variables=["summaries", "question"]
                                   )
    chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, 
                                                retriever= vectorstore.as_retriever(),
                                                chain_type="stuff",
                                                chain_type_kwargs={"prompt": custom_prompt}
                                                 )

    return chain


    

def ChatBot(content):
    text_chunks = generate_text_chunks(content)
    vectorstore = embedding(text_chunks)
   
    if vectorstore is None:
        raise ValueError("Vectorstore creation failed. Possibly due to embedding limits.")
    chain = chain_formation(vectorstore)
    return chain









