import json
from pathlib import Path
from agent_task.models import AgentTask

def test_load_basic_fixture():
    fixture_path = Path(__file__).parent.parent.parent.parent / "tests" / "fixtures" / "valid" / "basic.agent.task"
    with open(fixture_path) as f:
        data = json.load(f)
    
    task = AgentTask.model_validate(data)
    assert task.meta.id == "task-12345"
    assert task.goal == "Write a python script that returns 'hello world'"
    assert task.budget.time_limit_sec == 30
    assert task.accept[0].check == "output == 'hello world'"
