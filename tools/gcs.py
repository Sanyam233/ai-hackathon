from google.cloud import storage
import json

def get_gcs_client():
    return storage.Client()

def get_job_data_from_gcs(job_id: str) -> str:
    """
    Retrieves job-related data from a Google Cloud Storage 
    bucket based on a given job ID.
    """
    client = storage.Client()
    bucket = client.bucket("insights_agent_001")
    blob = bucket.blob(f"data/{job_id}.json")

    if not blob.exists():
        raise FileNotFoundError(f"No job data found for job_id={job_id}")

    data = blob.download_as_text()

    return {
        "jobId" : job_id,
        "data" : json.loads(data)
    }
