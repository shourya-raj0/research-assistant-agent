from typing import TypedDict,Optional
from pydantic import BaseModel,Field

# Pydantic models for structured outputs
class ResearchSummary(BaseModel):
    """Structured summary output from the research agent"""
    overview: str= Field(description="High level overview of the research topic")
    key_points: list[str]=Field(description="List of important findings")
    sources: list[str]= Field(description="List of source url")

class ResearchState(TypedDict):
    """
    Shared state for the research assistant workflow.
    
    Each node reads this state, processes it, and updates specific fields.
    """
    user_query: str              # Original user question
    refined_query: str           # Improved search query from LLM
    search_results: list[dict]   # Raw results from Tavily (dicts with title, content, url)
    summary: Optional[str]       # Final structured summary
    key_points: Optional[list]   # List of key findings
    sources: Optional[list]      # List of source URLs
    status: str                  # "pending", "searching", "summarizing", "completed", "error"
    error_message: Optional[str] # Error details if something fails