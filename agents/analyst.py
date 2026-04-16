from pydantic import BaseModel, Field
from typing import List, Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinancialMetric(BaseModel):
    name: str = Field(..., description="Name of the financial metric")
    value: float = Field(..., description="Value of the metric")
    trend: str = Field(..., description="Trend: stable, increasing, or decreasing")

class FinancialReport(BaseModel):
    summary: str = Field(..., description="Executive summary of the analysis")
    metrics: List[FinancialMetric] = Field(default_factory=list)
    risk_score: float = Field(..., description="Overall risk score (0-100)")
    recommendations: List[str] = Field(default_factory=list)
    audit_status: str = Field(default="pending", description="Status of the PII audit")

class AnalystAgent:
    """
    Analyst Agent responsible for synthesizing data into structured JSON reports.
    """
    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.model_name = model_name
        # Persona: Professional Financial Analyst
        self.system_instruction = (
            "You are a Senior Financial Analyst at Ledger AI. Your goal is to synthesize "
            "research findings and risk data into a professional, structured financial report. "
            "Ensure all outputs follow the provided JSON schema strictly."
        )

    def synthesize(self, research_data: str, risk_score: float) -> FinancialReport:
        """
        Simulates LLM synthesis of research and risk data into a Pydantic model.
        In production, this would call the Gemini API.
        """
        logger.info("AnalystAgent: Synthesizing financial report...")
        
        # Mocking LLM output for the skeleton
        # In a real scenario, we would use an LLM call with a JSON parser
        report = FinancialReport(
            summary=f"Analysis based on research: {research_data[:100]}...",
            metrics=[
                FinancialMetric(name="Profitability", value=0.85, trend="increasing"),
                FinancialMetric(name="Liquidity", value=1.2, trend="stable")
            ],
            risk_score=risk_score,
            recommendations=[
                "Diversify investment portfolio based on identified market trends.",
                "Mitigate exposure to high-volatility assets."
            ],
            audit_status="verified"
        )
        
        logger.info("AnalystAgent: Report synthesis complete.")
        return report

    def format_to_json(self, report: FinancialReport) -> str:
        return report.model_dump_json(indent=2)
