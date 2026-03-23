from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from .models import AgentTask

ContextType = TypeVar("ContextType")
MonitorType = TypeVar("MonitorType")

class BaseTaskAdapter(ABC, Generic[ContextType, MonitorType]):
    """
    Abstract Base Class for framework-specific adapters (CrewAI, LangGraph, AutoGen, Agno).
    Ensures a consistent, plug-and-play API across all major orchestrators.
    """
    
    def __init__(self, task: AgentTask):
        self.task = task

    @abstractmethod
    def get_context_injection(self) -> ContextType:
        """
        Translates the agent.task (Goal, Constraints, Budget) into the framework's native 
        prompt or task descriptor.
        Examples:
            - LangGraph: Returns a `SystemMessage`
            - CrewAI: Returns a `Task(description=...)` object
            - Agno: Returns `instructions` list
        """
        pass

    @abstractmethod
    def get_budget_monitor(self) -> MonitorType:
        """
        Returns the framework's native callback, telemetry hook, or rate-limiter 
        to enforce the task's budget (USD, tokens, wall_time).
        Examples:
            - LangGraph: Returns a `BaseCallbackHandler` that halts execution
            - CrewAI: Returns a `step_callback` hooked to iter limits
            - Agno: Plugs into run telemetry Hooks
        """
        pass

    @abstractmethod
    def evaluate_acceptance(self, final_agent_output: Any) -> bool:
        """
        Consumes the framework's native output format and evaluates it against 
        the `accept[]` criteria limits without touching the orchestrator.
        """
        pass
