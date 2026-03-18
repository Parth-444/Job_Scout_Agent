# gets job listing and user profile from state and generates a score
from graph.state import AgentState
from agents.llm_client import llm
import yaml
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage



class ScoreJob(BaseModel):
    job_id: str
    job_title: str
    employer_name: str
    job_description: str
    job_apply_link: str
    job_location: str
    score: float
    reasoning: str

def job_scoring(state: AgentState):
    llm_with_structure = llm.with_structured_output(ScoreJob)

    with open("prompts/job_scorer.yaml", "r") as f:
        p = yaml.safe_load(f)

    scored_jobs = []
    for job in state["fetched_jobs"]:
        message = [
            SystemMessage(content=p["system"]),
            HumanMessage(content=p["user"].format(job=job, user_profile=state["user_profile"]))
        ]
        result = llm_with_structure.invoke(message)
        scored_jobs.append(result)

    return {"scored_jobs": scored_jobs}