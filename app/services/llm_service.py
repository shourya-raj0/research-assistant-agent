import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

#Inititalizing our LLM
def get_llm():
    
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file"
        )
    
    llm = ChatGroq(
     model="llama-3.1-8b-instant",
        temperature=0.4,
        api_key=api_key,
        max_tokens=1024
    )

    return llm

llm_instance= None

def initialize_llm():
    """Initialize the LLM once at startup"""
    global llm_instance
    if llm_instance is None:
        llm_instance = get_llm()
    return llm_instance


def get_llm_instance():
    """Get the initialized LLM instance. Use this in your nodes."""
    global llm_instance
    if llm_instance is None:
        llm_instance = initialize_llm()
    return llm_instance