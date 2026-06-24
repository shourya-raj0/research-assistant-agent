from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent.graph import research_workflow
from app.agent.state import ResearchState

# Initialize FastAPI app
app = FastAPI(
    title="Research Assistant Agent",
    description="An AI agent that researches topics and generates structured summaries",
    version="1.0.0"
)


# ============================================================================
# Request/Response Models
# ============================================================================
class ResearchRequest(BaseModel):
    """User's research query"""
    query: str


class ResearchResponse(BaseModel):
    """Structured response from the research agent"""
    query: str
    refined_query: str
    summary: str
    key_points: list[str]
    sources: list[str]
    status: str


# ============================================================================
# Endpoints
# ============================================================================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Research a topic and return a structured summary.
    
    Input: query (user's research question)
    Output: summary, key_points, sources
    """
    
    try:
        # Validate input
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Initialize state with user query
        initial_state: ResearchState = {
            "user_query": request.query,
            "refined_query": "",
            "search_results": [],
            "summary": None,
            "key_points": None,
            "sources": None,
            "status": "pending",
            "error_message": None
        }
        
        # Run the workflow
        final_state = research_workflow.invoke(initial_state)
        
        # Check if workflow succeeded
        if final_state["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=f"Workflow error: {final_state.get('error_message', 'Unknown error')}"
            )
        
        # Build response
        response = ResearchResponse(
            query=final_state["user_query"],
            refined_query=final_state["refined_query"],
            summary=final_state["summary"] or "No summary generated",
            key_points=final_state["key_points"] or [],
            sources=final_state["sources"] or [],
            status=final_state["status"]
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# ============================================================================
# Run the app
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)