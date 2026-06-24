from langgraph.graph import StateGraph, END
from app.agent.state import ResearchState
from app.agent.nodes import research_node, search_node, summarize_node


def create_research_graph():
    """
    Create and compile the research assistant workflow graph.
    
    Flow:
    START → research_node → search_node → summarize_node → END
    """
    
    # Create the state graph
    graph = StateGraph(ResearchState)
    
    # Add the three nodes
    graph.add_node("research", research_node)
    graph.add_node("search", search_node)
    graph.add_node("summarize", summarize_node)
    
    # Connect nodes in sequence
    graph.add_edge("research", "search")      # research → search
    graph.add_edge("search", "summarize")     # search → summarize
    graph.add_edge("summarize", END)          # summarize → end
    
    # Set entry point
    graph.set_entry_point("research")
    
    # Compile the graph
    workflow = graph.compile()
    
    return workflow


# Create the workflow instance (used by FastAPI)
research_workflow = create_research_graph()