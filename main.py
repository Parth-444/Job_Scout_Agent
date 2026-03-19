from agents.profile_builder import profile_building
from agents.job_fetcher import job_fetch
from agents.job_scorer import job_scoring
from agents.filter import filter_jobs
from agents.tailor_resume import tailor_resume_agent
from graph.state import AgentState
from langgraph.graph import StateGraph, START, END
import json


def main():
    workflow = StateGraph(AgentState)

    workflow.add_node("profile_builder", profile_building)
    workflow.add_node("job_fetcher", job_fetch)
    workflow.add_node("job_scorer", job_scoring)
    workflow.add_node("filter", filter_jobs)
    workflow.add_node("tailor_resume", tailor_resume_agent)

    workflow.add_edge(START, "profile_builder")
    workflow.add_edge("profile_builder", "job_fetcher")
    workflow.add_edge("job_fetcher", "job_scorer")
    workflow.add_edge("job_scorer", "filter")
    workflow.add_edge("filter", "tailor_resume")
    workflow.add_edge("tailor_resume", END)

    app = workflow.compile()

    initial_state = {
        "pdf_path": "resume1.pdf",
        "user_profile": {},
        "fetched_jobs": [],
        "scored_jobs": [],
        "top_jobs": [],
    }

    print("Starting pipeline...\n")
    result = app.invoke(initial_state)

    print("=== USER PROFILE ===")
    print(json.dumps(result["user_profile"], indent=2))
    print("\n[debug] target_roles:", result["user_profile"].get("target_roles"))
    print("[debug] location_preferences:", result["user_profile"].get("location_preferences"))

    print(f"\n=== FETCHED JOBS ({len(result['fetched_jobs'])}) ===")
    for job in result["fetched_jobs"]:
        print(f"  - {job['job_title']} at {job['employer_name']} ({job['job_location']})")

    print(f"\n=== SCORED JOBS ({len(result['scored_jobs'])}) ===")
    for job in result["scored_jobs"]:
        print(f"  - [{job.score}] {job.job_title} at {job.employer_name} — {job.reasoning[:80]}...")

    print(f"\n=== TOP JOBS AFTER FILTER ({len(result['top_jobs'])}) ===")
    for job in result["top_jobs"]:
        print(f"  - {job['job_title']} at {job['employer_name']}")
        print(f"    Apply: {job['job_apply_link']}")
        print(f"    Resume snippet: {job['tailored_resume'][:200]}...\n")


if __name__ == "__main__":
    main()
