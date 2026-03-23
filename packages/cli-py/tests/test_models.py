import json
from pathlib import Path
from agent_task.models import AgentTask

def test_load_basic_fixture():
    fixture_path = Path(__file__).parent.parent.parent.parent / "tests" / "fixtures" / "valid" / "basic.agent.task"
    with open(fixture_path) as f:
        data = json.load(f)
    
    task = AgentTask.model_validate(data)
    assert task.meta.id == "INC009"
    assert task.goal.summary == "Resolve P1 incident"
    assert task.budget.cost_usd == 2.0
    # ensure "not" is correctly mapped to "not_"
    assert task.goal.not_ == ["Restart DB"]
