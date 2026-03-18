from graph.state import AgentState

def filter_jobs(state: AgentState):
    scored_jobs = state["scored_jobs"]

    top_jobs = [job for job in scored_jobs if job.score >= 6]

    top_jobs = sorted(top_jobs, key=lambda x: x.score, reverse=True)[:5]
    
    return {"top_jobs": top_jobs}
