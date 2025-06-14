from google.adk.agents import Agent
from tools.gcs import get_job_data_from_gcs
from prompt import AGENT_INSTRUCTION, AGENT_DESCRIPTION

root_agent = Agent(
    name="analysis_insight_agent",
    model="gemini-2.0-flash",
    instruction=AGENT_INSTRUCTION,
    description=AGENT_DESCRIPTION,
    tools=[get_job_data_from_gcs]
)