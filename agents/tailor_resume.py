from graph.state import AgentState
import yaml
from pydantic import BaseModel, Field
from agents.llm_client import llm
from langchain_core.messages import SystemMessage, HumanMessage

class TailoredResume(BaseModel):
    latex_code: str = Field(description="Raw compilable LaTeX resume code, nothing else")

def tailor_resume_agent(state: AgentState):
    
    with open("prompts/resume_tailor.yaml", "r") as f:
        p = yaml.safe_load(f)

    llm_with_structure = llm.with_structured_output(TailoredResume)

    updated_jobs = []
    for job in state["top_jobs"]:
        message = [
            SystemMessage(content=p["system"]),
            HumanMessage(content=p["user"].format(user_profile=state["user_profile"], **job))
        ]

        result = llm_with_structure.invoke(message)

        updated_jobs.append({**job, "tailored_resume": result.latex_code})

    return {"top_jobs": updated_jobs}