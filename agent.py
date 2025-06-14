from google.adk.agents import Agent
from prompt import AGENT_INSTRUCTION, AGENT_DESCRIPTION
from pydantic import BaseModel, Field
from typing import Optional, List

class InsightResponse(BaseModel):
    jobId: str = Field(..., description="Unique identifier for the job the insight is based on.")
    insight: str = Field(..., description="Concise summary of key findings and recommendations.")
    recommendedHexes: Optional[List[str]] = Field(
        None, description="List of recommended hexes if multiple apply."
    )
    primaryHex: Optional[str] = Field(
        None, description="Single most relevant hex recommendation if only one applies."
    )

root_agent = Agent(
    name="analysis_insight_agent",
    model="gemini-2.0-flash",
    instruction=AGENT_INSTRUCTION,
    description=AGENT_DESCRIPTION,
    output_schema=InsightResponse,
    disallow_transfer_to_parent=True, 
    disallow_transfer_to_peers=True    
    # tools=[get_job_data_from_gcs]
)