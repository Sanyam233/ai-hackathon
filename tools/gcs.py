from google.cloud import storage

def get_gcs_client():
    return storage.Client()

def get_job_data_from_gcs(job_id: str) -> str:
    client = get_gcs_client()
    bucket = client.bucket("insights_agent_001")
    blob = bucket.blob(f"data/{job_id}.json")
    return blob.download_as_text()
