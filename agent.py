from google.adk.agents import Agent
from tools.gcs import get_analysis_data_from_gcs
from prompt_v2 import AGENT_INSTRUCTION, AGENT_DESCRIPTION

root_agent = Agent(
    name="analysis_insight_agent",
    model="gemini-2.5-flash-preview-05-20",
    instruction=AGENT_INSTRUCTION,
    description=AGENT_DESCRIPTION,
    tools=[get_analysis_data_from_gcs]
)