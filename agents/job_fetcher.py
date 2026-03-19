from graph.state import AgentState
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def job_fetch(state: AgentState):
    user_profile = state["user_profile"]
    target_roles = user_profile["target_roles"]
    preferred_locations = user_profile["location_preferences"] or ["India"]

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
	"x-rapidapi-key": os.getenv("jsearch_api"),
	"x-rapidapi-host": "jsearch.p.rapidapi.com",
	"Content-Type": "application/json"
    }
    fetched_jobs = []
    for role in target_roles:
        for location in preferred_locations:
            query_string = {
                "query": f"{role} jobs in {location}",
                "num_pages": "1",
                "date_posted": "3days",
                "country": "IN"
            }
            response = requests.get(url, headers=headers, params=query_string)
            data = response.json()

            print(f"[job_fetcher] query: {query_string['query']} | status: {data.get('status')} | http: {response.status_code}")
            if data.get("status") != "OK":
                print(f"[job_fetcher] error response: {data}")

            if data.get("status") == "OK" and "data" in data:
                for job in data["data"]:
                    simplified_job = {
                        "job_id": job.get("job_id"),
                        "job_title": job.get("job_title"),
                        "employer_name": job.get("employer_name"),
                        "job_description": job.get("job_description"),
                        "job_apply_link": job.get("job_apply_link"),
                        "job_location": job.get("job_location"),
                        "job_is_remote": job.get("job_is_remote"),
                        "job_posted_human_readable": job.get("job_posted_human_readable")
                    }
                    fetched_jobs.append(simplified_job)

            #sleep to respect API rate limits
            time.sleep(1)

    return {"fetched_jobs": fetched_jobs}
