from typing import TypedDict, Dict, List


class AgentState(TypedDict):
    pdf_path: str
    user_profile: Dict
    fetched_jobs: List[Dict]
    scored_jobs: List[Dict]