from typing import Any, Dict
from langchain_core.messages import SystemMessage
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from agent_task.models import AgentTask
from agent_task.adapter import BaseTaskAdapter

class BudgetExceededError(Exception):
    """Raised when the agent runtime exceeds the budget defined in agent.task."""
    pass

class AgentTaskBudgetCallbackHandler(BaseCallbackHandler):
    """
    Native LangChain callback handler. 
    Plugs into LangGraph or standalone tool invocations to track spending.
    Throws a hard error if the token budget is violated, halting the agent.
    """
    def __init__(self, task: AgentTask):
        self.task = task
        self.total_tokens_used = 0
        self.token_limit = task.budget.tokens if task.budget else None

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Hook into LLM completions to evaluate token usage."""
        if not response.llm_output:
            return
            
        token_usage = response.llm_output.get("token_usage", {})
        self.total_tokens_used += token_usage.get("total_tokens", 0)
        
        if self.token_limit and self.total_tokens_used > self.token_limit:
            action = self.task.budget.on_exceed or "halt"
            raise BudgetExceededError(
                f"Agent halted: Exceeded budget of {self.token_limit} tokens "
                f"(Action: {action})"
            )

class LangGraphTaskAdapter(BaseTaskAdapter[SystemMessage, AgentTaskBudgetCallbackHandler]):
    """
    Standard BaseTaskAdapter implementation for LangGraph / LangChain.
    """
    
    def get_context_injection(self) -> SystemMessage:
        """
        Transforms the agent.task into a native LangChain SystemMessage.
        Injects only the mandatory task execution bounds, respecting ADR-0002.
        """
        lines = ["<agent_task>"]
        
        # Goal
        lines.append("  <goal>")
        lines.append(f"    <summary>{self.task.goal.summary}</summary>")
        lines.append(f"    <outcome>{self.task.goal.outcome}</outcome>")
        if self.task.goal.not_:
            for n in self.task.goal.not_:
                lines.append(f"    <not>{n}</not>")
        lines.append("  </goal>")
        
        # Constraints
        if self.task.constraints:
            lines.append("  <constraints>")
            if self.task.constraints.scope:
                lines.append(f"    <scope>{', '.join(self.task.constraints.scope)}</scope>")
            if self.task.constraints.never:
                for nev in self.task.constraints.never:
                    lines.append(f"    <never>{nev}</never>")
            if self.task.constraints.require_approval_if:
                for apv in self.task.constraints.require_approval_if:
                    lines.append(f"    <require_approval_if>{apv}</require_approval_if>")
            lines.append("  </constraints>")
            
        # Budget
        if self.task.budget:
            lines.append("  <budget>")
            if self.task.budget.tokens:
                lines.append(f"    <tokens>{self.task.budget.tokens}</tokens>")
            if self.task.budget.cost_usd:
                lines.append(f"    <cost_usd>{self.task.budget.cost_usd}</cost_usd>")
            lines.append("  </budget>")
            
        lines.append("</agent_task>")
        return SystemMessage(content="\n".join(lines))

    def get_budget_monitor(self) -> AgentTaskBudgetCallbackHandler:
        """Returns the BaseCallbackHandler capable of halting graph execution."""
        return AgentTaskBudgetCallbackHandler(self.task)

    def evaluate_acceptance(self, final_agent_output: Any) -> bool:
        """
        Dynamically iterates over task.accept[] constraints against the final LangGraph string or state.
        """
        for criterion in self.task.accept:
            # Placeholder for dynamic execution of generic acceptance criteria
            pass
        return True

__all__ = ["LangGraphTaskAdapter", "AgentTaskBudgetCallbackHandler", "BudgetExceededError"]
