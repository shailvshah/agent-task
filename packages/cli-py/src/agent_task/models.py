from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal, Optional, Union, Any

class GoalDict(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")
    summary: str
    outcome: Optional[str] = None
    not_: Optional[List[str]] = Field(default=None, alias="not")

GoalType = Union[str, GoalDict]

class StateAccept(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["state"]
    description: Optional[str] = None
    check: str

class AssertionAccept(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["assertion"]
    description: Optional[str] = None
    check: str

class RubricAccept(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["rubric"]
    description: Optional[str] = None
    evaluator: str
    threshold: float
    criteria: str

AcceptType = Union[StateAccept, AssertionAccept, RubricAccept]

class Constraints(BaseModel):
    model_config = ConfigDict(extra="allow")
    scope: Optional[List[str]] = None
    never: Optional[List[str]] = None
    require_approval_if: Optional[List[str]] = None

class Budget(BaseModel):
    model_config = ConfigDict(extra="allow")
    tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    wall_time_minutes: Optional[int] = None
    on_exceed: Optional[str] = None

class RollbackStep(BaseModel):
    model_config = ConfigDict(extra="allow")
    action: str
    channel: Optional[str] = None
    message: Optional[str] = None

class Rollback(BaseModel):
    model_config = ConfigDict(extra="allow")
    on_constraint_violation: Optional[str] = None
    steps: Optional[List[RollbackStep]] = None

class Meta(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    capabilities_required: Optional[List[str]] = None

class AgentTask(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")
    scheme: Optional[str] = Field(default="https://agent-task.dev/schema/v0.1.json", alias="$schema")
    version: Optional[str] = Field(default="0.1.0", alias="$version")
    goal: GoalType
    accept: List[AcceptType]
    constraints: Optional[Constraints] = None
    budget: Optional[Budget] = None
    rollback: Optional[Rollback] = None
    meta: Meta
