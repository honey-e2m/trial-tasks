import os
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from bs4 import BeautifulSoup as Soup

# Initialize OpenAI
embeddings = None
llm = None

try:
    if os.environ.get("OPENAI_API_KEY"):
        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI(model="gpt-3.5-turbo")
except Exception as e:
    print(f"Warning: OpenAI not configured: {e}")

DB_PATH = "faiss_index"

def get_vector_store():
    if not embeddings:
        return None
    # Check if index exists locally
    if os.path.exists(DB_PATH):
        try:
            return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            return None
    return None

def save_vector_store(vector_store):
    vector_store.save_local(DB_PATH)

def scrape_and_ingest(url: str, depth: int = 2):
    """Scrape a URL recursively and ingest into FAISS."""
    if not embeddings:
        print("OpenAI embeddings not configured.")
        return 0
        
    print(f"Scraping {url} with depth {depth}...")
    
    loader = RecursiveUrlLoader(
        url=url, 
        max_depth=depth, 
        extractor=lambda x: Soup(x, "html.parser").text
    )
    docs = loader.load()
    
    print(f"Loaded {len(docs)} documents.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    vector_store = get_vector_store()
    
    if vector_store:
        vector_store.add_documents(splits)
    else:
        vector_store = FAISS.from_documents(splits, embeddings)
    
    save_vector_store(vector_store)
    return len(splits)

def get_answer(question: str):
    """Retrieve context and answer the question."""
    if not llm or not embeddings:
        return "OpenAI API key is not configured in the backend environment."

    vector_store = get_vector_store()
    
    if not vector_store:
        # If no vector store, just use LLM directly or return message
        # For now, let's return a message prompting to scrape
        return "I haven't ingested any content yet. Please verify the scraping layer or check if the website has been scraped."

    retriever = vector_store.as_retriever()
    
    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke(question)
