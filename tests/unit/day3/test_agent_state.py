from company_ai.agents.state import DeepAgentState
from company_ai.models.agent import AgentTask


def test_state_accepts_tasks():

    state: DeepAgentState = {
        "goal": "Analyze sales",
        "tasks": [
            AgentTask(
                task_id="1",
                description="Get data",
            )
        ],
        "worker_results": [],
        "iteration": 0,
    }

    assert state["goal"] == "Analyze sales"
    assert len(state["tasks"]) == 1
    assert state["iteration"] == 0