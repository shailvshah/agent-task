---
name: scaffold-adapter
description: Guides the AI copilot in scaffolding a new framework adapter (e.g. LangGraph, CrewAI) for agent.task.
---

# Scaffold Adapter Command

You are an AI assistant orchestrating the `scaffold-adapter` command for the `agent.task` repository.

## Your Task
Walk the developer through building a new framework adapter that safely bridges `.agent.task` contracts to external frameworks like LangGraph, CrewAI, or AutoGen.

## Instructions
1. **Identify the Framework**: Ask the user which framework they are building the adapter for.
2. **Setup Structure**:
   - For Python frameworks (LangGraph, CrewAI), create a new directory inside `packages/adapter-[framework]-py`.
   - For Node frameworks, create `packages/adapter-[framework]-ts`.
3. **Follow the BaseTaskAdapter Interface (ADR-0004)**: 
   - Adapters must be lightweight packages separate from the core CLI. 
   - The core adapter class MUST inherit from `BaseTaskAdapter` (found in `agent_task.adapter`).
   - You MUST implement the 3 standard hooks: `get_context_injection`, `get_budget_monitor`, and `evaluate_acceptance`.
   - **Crucial Rule:** NEVER wrap the user's agentic execution graph. The adapter must only supply these generic hooks for the user to invoke natively within their orchestrator's telemetry/callbacks.
4. **Context Window Injection Rules**:
   - `get_context_injection` must securely format `goal`, `constraints`, and `budget` into the LLM system prompt.
   - Do NOT inject `accept` or `rollback` directly into the prompt.
5. **Finalize**: 
   - Add a `README.md` to the new adapter package.
   - Test basic compilation/linting.
