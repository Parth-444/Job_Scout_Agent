import yaml
from agents.llm_client import llm
from typing import List
from pydantic import BaseModel
import base64
from graph.state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage

class ContactInfo(BaseModel):
    name: str
    phone: str
    email: str

class Education(BaseModel):
    degree: str
    university: str
    graduation_year: str

class Project(BaseModel):
    name: str
    description: str
    tech_stack: List[str]



class Profile(BaseModel):
    contact_info: ContactInfo
    education: Education
    skills: List
    experience_years: str
    target_roles: List
    location_preferences: List
    projects: List[Project]




def profile_building(state: AgentState):
    """This method willtake user resume
     and give it to the llm and will output a structure user profile"""

    pdf_path = state["pdf_path"]

    with open("prompts/profile_builder.yaml", "r") as f:
        p = yaml.safe_load(f)

    with open(pdf_path, "rb") as file:
        pdf_bytes = file.read()

    llm_with_structure = llm.with_structured_output(Profile)

    pdf_base64  = base64.b64encode(pdf_bytes).decode("utf-8")

    message = [
        SystemMessage(content=p["system"]),
        HumanMessage(content=[
        {
            "type": "media",
            "mime_type": "application/pdf",
            "data": pdf_base64
        },
        {
            "type": "text",
            "text": p["user"]  # no .format() needed, resume is passed as media block
        }
    ])
    ]

    response = llm_with_structure.invoke(message)

    return {"user_profile": response.model_dump()}




    