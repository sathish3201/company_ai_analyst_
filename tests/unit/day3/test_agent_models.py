from company_ai.models.agent import (
    AgentPlan,
    AgentStatus,
    AgentTask,
    TaskStatus,
)


def test_agent_task_defaults():

    task = AgentTask(
        task_id="1",
        description="Analyze sales",
    )

    assert task.status == TaskStatus.PENDING
    assert task.result is None
    assert task.error is None


def test_agent_plan():

    task = AgentTask(
        task_id="1",
        description="Get sales data",
    )

    plan = AgentPlan(
        goal="Analyze sales",
        tasks=[task],
    )

    assert plan.goal == "Analyze sales"
    assert len(plan.tasks) == 1


def test_agent_status():

    assert AgentStatus.CREATED.value == "created"
    assert AgentStatus.COMPLETED.value == "completed"