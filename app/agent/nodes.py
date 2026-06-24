from langchain_core.messages import HumanMessage
from tavily import TavilyClient
import os
from dotenv import load_dotenv

from app.services.llm_service import get_llm_instance
from app.prompts.research_prompt import RESEARCH_REFINEMENT_PROMPT, SUMMARIZE_PROMPT
from app.agent.state import ResearchState

load_dotenv()


# ============================================================================
# NODE 1: Research Node - Refine the user query
# ============================================================================
def research_node(state: ResearchState) -> dict:
    """
    Takes the raw user query and refines it into a better search query.
    
    Input: user_query
    Output: refined_query, status
    """
    try:
        llm = get_llm_instance()
        user_query = state["user_query"]
        
        # Create the prompt with the user's question
        prompt = RESEARCH_REFINEMENT_PROMPT.format(user_query=user_query)
        
        # Call LLM to refine the query
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        
        # Extract the refined query from response
        refined_query = response.content.strip()
        
        return {
            "refined_query": refined_query,
            "status": "searching"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Research node failed: {str(e)}"
        }


# ============================================================================
# NODE 2: Search Node - Call Tavily API
# ============================================================================
def search_node(state: ResearchState) -> dict:
    """
    Takes the refined query and searches the web using Tavily.
    
    Input: refined_query
    Output: search_results, status
    """
    try:
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY not found in .env file")
        
        # Initialize Tavily client
        client = TavilyClient(api_key=tavily_api_key)
        
        # Search the web
        refined_query = state["refined_query"]
        response = client.search(query=refined_query, max_results=5)
        
        # Extract results (Tavily returns list of dicts with 'title', 'content', 'url')
        search_results = response.get("results", [])
        
        return {
            "search_results": search_results,
            "status": "summarizing"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Search node failed: {str(e)}"
        }


# ============================================================================
# NODE 3: Summarize Node - Extract insights from results
# ============================================================================
def summarize_node(state: ResearchState) -> dict:
    """
    Takes raw search results and generates a structured summary.
    
    Input: search_results
    Output: summary, key_points, sources, status
    """
    try:
        llm = get_llm_instance()
        search_results = state["search_results"]
        
        # Convert search results to readable text
        results_text = "\n\n".join([
            f"Title: {r.get('title', 'N/A')}\n"
            f"Content: {r.get('content', 'N/A')[:500]}...\n"
            f"URL: {r.get('url', 'N/A')}"
            for r in search_results
        ])
        
        # Create the prompt
        prompt = SUMMARIZE_PROMPT.format(search_results_text=results_text)
        
        # Call LLM to summarize
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])
        summary_text = response.content.strip()
        
        # Parse the structured response
        overview = extract_section(summary_text, "OVERVIEW")
        key_points = extract_key_points(summary_text)
        sources = extract_sources(summary_text, search_results)
        
        return {
            "summary": overview,
            "key_points": key_points,
            "sources": sources,
            "status": "completed"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Summarize node failed: {str(e)}"
        }


# ============================================================================
# Helper Functions to Parse LLM Output
# ============================================================================
def extract_section(text: str, section_name: str) -> str:
    """Extract a section from the LLM response"""
    try:
        # Find the section header
        start = text.find(f"{section_name}:")
        if start == -1:
            return text[:200]  # Fallback
        
        # Find the next section or end of text
        next_section = text.find("\n\n", start)
        if next_section == -1:
            return text[start + len(section_name) + 1:].strip()
        
        return text[start + len(section_name) + 1:next_section].strip()
    
    except:
        return text[:200]


def extract_key_points(text: str) -> list:
    """Extract key points from the formatted response"""
    try:
        start = text.find("KEY POINTS:")
        if start == -1:
            return []
        
        # Get section between KEY POINTS and SOURCES
        end = text.find("SOURCES:", start)
        if end == -1:
            end = len(text)
        
        section = text[start + 11:end].strip()
        
        # Split by bullet points
        points = [line.strip("- ").strip() for line in section.split("\n") if line.strip().startswith("-")]
        
        return points
    
    except:
        return []


def extract_sources(text: str, search_results: list) -> list:
    """Extract sources from both LLM response and search results"""
    try:
        sources = []
        
        # Try to get URLs from SOURCES section in LLM response
        start = text.find("SOURCES:")
        if start != -1:
            section = text[start + 8:].strip()
            urls = [line.strip() for line in section.split("\n") if line.strip().startswith("http")]
            sources.extend(urls)
        
        # Fallback: get URLs from search results
        if not sources and search_results:
            sources = [r.get("url") for r in search_results if r.get("url")]
        
        return sources[:5]  # Limit to 5 sources
    
    except:
        return [r.get("url") for r in search_results if r.get("url")][:5]
