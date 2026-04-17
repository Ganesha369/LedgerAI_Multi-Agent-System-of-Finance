from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import logging
from graph import create_ledger_graph
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ledger AI - Multi-Agent Financial System")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Semantic Cache using a Python dictionary
# In production, this would be backed by Redis
semantic_cache: Dict[str, str] = {}

class QueryRequest(BaseModel):
    query: str
    use_cache: bool = True

class QueryResponse(BaseModel):
    query: str
    report: str
    cached: bool

@app.get("/")
async def root():
    return {"message": "Ledger AI API is operational."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def analyze_financials(request: QueryRequest):
    """
    Endpoint to trigger the multi-agent financial analysis workflow.
    Includes a mock semantic cache for high-speed query reuse.
    """
    query = request.query.strip().lower()
    
    # Check Mock Semantic Cache
    if request.use_cache and query in semantic_cache:
        logger.info(f"Cache Hit for query: {query}")
        return QueryResponse(query=request.query, report=semantic_cache[query], cached=True)
    
    logger.info(f"Cache Miss for query: {query}. Executing LangGraph workflow...")
    
    try:
        # Initialize LangGraph
        ledger_graph = create_ledger_graph()
        
        # Initial State
        initial_state = {
            "query": request.query,
            "plan": [],
            "research_results": "",
            "risk_score": 0.0,
            "report": "",
            "security_audit": ""
        }
        
        # Execute Workflow
        # We take the final state from the stream
        final_state = None
        for output in ledger_graph.stream(initial_state):
            # The stream yields updates from each node
            # We'll just keep track of the latest state
            final_state = output
            
        # Extract report from the last node's output (auditor)
        # Note: LangGraph stream output format depends on how nodes return data
        # In our graph.py, nodes return dicts that update the state.
        # The final output in the stream for the last node looks like {'auditor': {...}}
        
        report_content = ""
        if final_state and 'auditor' in final_state:
            report_content = final_state['auditor'].get('report', "No report generated.")
        else:
            # Fallback if stream doesn't behave as expected in this mock
            report_content = "Workflow execution failed to produce a final report."

        # Update Cache
        semantic_cache[query] = report_content
        
        return QueryResponse(query=request.query, report=report_content, cached=False)
        
    except Exception as e:
        logger.error(f"Workflow Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.delete("/cache")
async def clear_cache():
    semantic_cache.clear()
    return {"message": "Semantic cache cleared."}

# --- ADD THIS FOR STREAMLIT ---
def run_agent_logic(user_query: str):
    """
    Direct entry point for Streamlit to bypass the FastAPI HTTP layer.
    """
    # 1. Initialize Graph
    ledger_graph = create_ledger_graph()
    
    # 2. Initial State
    initial_state = {
        "query": user_query,
        "plan": [],
        "research_results": "",
        "risk_score": 0.0,
        "report": "",
        "security_audit": ""
    }
    
    # 3. Execute Workflow (Synchronously for Streamlit simplicity)
    final_state = None
    for output in ledger_graph.stream(initial_state):
        final_state = output
        
    # 4. Extract results
    if final_state and 'auditor' in final_state:
        report = final_state['auditor'].get('report', "No report generated.")
    else:
        report = "Workflow execution failed to produce a final report."
        
    return {"output": report, "full_state": final_state}