from flask import Flask, request
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils.api_response import send_api_response
from agent import root_agent
from google.genai import types
import asyncio
import json
import re
from tools.gcs import get_job_data_from_gcs

load_dotenv()

app = Flask(__name__)
session_srv = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="RAG_AnalysisAnalyzer", session_service=session_srv)

def extract_json_from_markdown(text: str) -> dict:
    # Remove Markdown-style ```json ... ``` wrapping
    cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)

@app.route("/", methods=["POST"])
def generate_insights():
    params = request.get_json()
    user_id, session_id = params["userId"], params["sessionId"]
    job_id, raw_query = params["jobId"], params["query"]
    update_query = f"For the jobId={job_id} {raw_query}"

    job_data = get_job_data_from_gcs(job_id)
    data = json.dumps(job_data["data"], indent=2)

    context = f"""
    You are analyzing transport mobility data for job ID: {job_id}. 
    Here is the full snapshot data to base your reasoning on:
    {data}
    Please now proceed to: {raw_query}
    """

    response = asyncio.run(run_agent(job_id, user_id, session_id, update_query, context))
    return send_api_response(200, response)


async def run_agent(job_id: str, user_id: str, session_id: str, query: str, context: str) -> str:

    # Optionally pre-fill session with context
    await session_srv.create_session(
        app_name="RAG_AnalysisAnalyzer",
        user_id=user_id,
        session_id=session_id,
        state={"job_id": job_id}
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text="Please generate your analysis and recommendation in valid JSON.")]
    )

    result = ""
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=new_message, context=context):
        if event.is_final_response():
            print("INNNN", event.content.parts)
            result = event.content.parts[0].text

    parsed_json = extract_json_from_markdown(result)
    return parsed_json


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8080)