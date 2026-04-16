import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="LedgerAI | Financial Agent",
    page_icon="💰",
    layout="centered"
)

# Sidebar for Status & Info
with st.sidebar:
    st.title("📊 System Status")
    st.success("Frontend: Live (Hugging Face)")
    st.info("Backend: Railway PaaS")
    st.markdown("---")
    st.markdown("### Sample Queries")
    st.code("What is the risk level for the 50k loan?")
    st.code("Summarize the ledger activities.")

# Main UI
st.title("💰 LedgerAI")
st.subheader("Multi-Agent Financial Analysis System")
st.write("Upload your ledger and get AI-powered insights using Agentic RAG.")

# --- IMPORTANT: UPDATE THIS URL AFTER DEPLOYING TO RAILWAY ---
# It should look something like: https://your-project.up.railway.app/query
BACKEND_URL = "https://your-railway-app-url.up.railway.app/query"

query = st.text_input("Ask a question about your financial data:", placeholder="e.g. Is there any discrepancy in the GST filing?")

if st.button("Run Analysis"):
    if query:
        with st.spinner("🤖 Agents are collaborating (Planner -> Researcher -> Auditor)..."):
            try:
                # Sending the query to your FastAPI backend
                response = requests.post(
                    BACKEND_URL, 
                    json={"query": query},
                    timeout=60  # Agents take time to think!
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    
                    # Display the final answer
                    st.markdown("### 📝 Final Report")
                    st.write(result.get("output", "No output provided by the agent."))
                    
                    # Display the Technical Trace (Recruiters LOVE this)
                    with st.expander("🔬 View Multi-Agent Execution Trace"):
                        st.json(result)
                        
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.info("Check if your Railway server is awake and the URL is correct.")
                    
            except Exception as e:
                st.error(f"Connection Failed: {e}")
                st.warning("Make sure you updated the BACKEND_URL in app.py with your Railway link.")
    else:
        st.warning("Please enter a question first.")

st.markdown("---")
st.caption("Built by Ganesh")
