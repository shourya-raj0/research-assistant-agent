import streamlit as st
from app.agent.graph import research_workflow
from app.agent.state import ResearchState
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Research Assistant Agent",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 Research Assistant Agent")
st.markdown("An AI-powered research tool that searches the web and generates structured summaries.")

# Sidebar info
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This agent:
    1. Refines your query
    2. Searches the web
    3. Extracts key insights
    4. Returns structured summary
    """)
    
    st.markdown("### Tech Stack")
    st.markdown("""
    - **LangGraph** - Agent orchestration
    - **Groq** - LLM inference
    - **Tavily** - Web search
    - **Streamlit** - UI
    """)

# Check API keys
def check_api_keys():
    """Verify API keys are set"""
    groq_key = os.getenv("GROQ_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if not groq_key or not tavily_key:
        st.error("❌ API keys missing! Set GROQ_API_KEY and TAVILY_API_KEY in environment variables.")
        return False
    return True

# Main content
if not check_api_keys():
    st.stop()

# Input section
st.markdown("### 🤔 What would you like to research?")
query = st.text_input(
    "Enter your research topic:",
    placeholder="e.g., What is quantum computing?",
    label_visibility="collapsed"
)

# Research button
if st.button("🚀 Research", use_container_width=True):
    if not query.strip():
        st.error("Please enter a research topic!")
    else:
        with st.spinner("🔄 Researching..."):
            try:
                # Initialize state
                initial_state: ResearchState = {
                    "user_query": query,
                    "refined_query": "",
                    "search_results": [],
                    "summary": None,
                    "key_points": None,
                    "sources": None,
                    "status": "pending",
                    "error_message": None
                }
                
                # Run workflow
                result = research_workflow.invoke(initial_state)
                
                # Check for errors
                if result["status"] == "error":
                    st.error(f"❌ Error: {result.get('error_message', 'Unknown error')}")
                else:
                    # Display results
                    st.success("✅ Research completed!")
                    
                    # Tabs for different views
                    tab1, tab2, tab3 = st.tabs(["Summary", "Key Points", "Sources"])
                    
                    with tab1:
                        st.markdown("### 📄 Summary")
                        st.write(result.get("summary", "No summary generated"))
                    
                    with tab2:
                        st.markdown("### 🎯 Key Points")
                        key_points = result.get("key_points", [])
                        if key_points:
                            for i, point in enumerate(key_points, 1):
                                st.markdown(f"{i}. {point}")
                        else:
                            st.info("No key points extracted")
                    
                    with tab3:
                        st.markdown("### 🔗 Sources")
                        sources = result.get("sources", [])
                        if sources:
                            for url in sources:
                                st.markdown(f"- [{url}]({url})")
                        else:
                            st.info("No sources found")
                    
                    # Show metadata
                    with st.expander("📊 Details"):
                        st.markdown(f"**Original Query:** {result['user_query']}")
                        st.markdown(f"**Refined Query:** {result['refined_query']}")
                        st.markdown(f"**Status:** {result['status']}")
            
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using LangGraph + Streamlit</p>
    <p><a href='https://github.com/shourya-raj0/research-assistant-agent'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)