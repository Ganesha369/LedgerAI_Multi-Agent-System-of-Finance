import os
import time
import random
import logging
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from agents.researcher import FinancialResearcher
from agents.analyst import AnalystAgent
from utils.risk_engine import RiskEngine
from utils.security import audit_data
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# State Definition
class AgentState(TypedDict):
    query: str
    plan: List[str]
    research_results: str
    risk_score: float
    report: str
    security_audit: str

# Node Functions
def planner_node(state: AgentState):
    """
    Node A: Planner (Gemini 3 Flash Preview Simulation).
    Outputs a step-by-step reasoning plan.
    """
    logger.info("Node A: Planner starting...")
    # Human-Like Simulation: random sleep (0.2s - 0.7s)
    time.sleep(random.uniform(0.2, 0.7))
    
    query = state['query']
    plan = [
        f"1. Research financial data for: {query}",
        "2. Evaluate risk metrics and calculate risk score.",
        "3. Synthesize findings into a professional report.",
        "4. Audit report for PII and security compliance."
    ]
    logger.info(f"Node A: Planner generated plan: {plan}")
    return {"plan": plan}

def researcher_node(state: AgentState):
    """
    Node B: Researcher (Pinecone Assistant).
    Performs search using Pinecone Assistant.
    """
    logger.info("Node B: Researcher starting...")
    researcher = FinancialResearcher()
    results = researcher.query(state['query'])
    logger.info("Node B: Researcher finished.")
    return {"research_results": results}

def analyst_node(state: AgentState):
    """
    Node C: Analyst (Synthesis).
    Combines tool outputs into a professional financial report.
    """
    logger.info("Node C: Analyst starting...")
    risk_engine = RiskEngine()
    # Simulated risk inputs
    risk_score = risk_engine.calculate_score(0.3, 0.4, 0.2)
    
    analyst = AnalystAgent()
    report_obj = analyst.synthesize(state['research_results'], risk_score)
    report_json = analyst.format_to_json(report_obj)
    
    logger.info("Node C: Analyst finished.")
    return {"risk_score": risk_score, "report": report_json}

def auditor_node(state: AgentState):
    """
    Node D: Auditor (Security).
    Scans for PII using Scikit-learn or Transformers logic.
    """
    logger.info("Node D: Auditor starting...")
    report_content = state['report']
    audited_report = audit_data(report_content)
    logger.info("Node D: Auditor finished.")
    return {"security_audit": "PASSED", "report": audited_report}

# Graph Construction
def create_ledger_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("auditor", auditor_node)

    # Define Edges (Plan-and-Execute Pattern)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "auditor")
    workflow.add_edge("auditor", END)

    # Compile Graph
    app = workflow.compile()
    logger.info("LangGraph workflow compiled successfully.")
    return app

if __name__ == "__main__":
    graph = create_ledger_graph()
    initial_state = {"query": "Q1 Tech Sector Outlook", "plan": [], "research_results": "", "risk_score": 0.0, "report": "", "security_audit": ""}
    for output in graph.stream(initial_state):
        print(output)
