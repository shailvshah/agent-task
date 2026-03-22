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
3. **Follow ADR-0003**: 
   - Adapters must be separate packages from the core CLI. Do not modify `cli-ts` or `cli-py` directly.
   - Core validation logic remains in the `cli` packages. The adapter should import the `agent-task` package and purely act as a translation layer.
4. **Context Window Injection Rules**:
   - Inject `goal`, `constraints`, and `budget` securely into the agent's context window.
   - Do NOT inject `accept` or `rollback` directly into the LLM system prompt.
5. **Finalize**: 
   - Add a `README.md` to the new adapter package.
   - Test basic compilation/linting.
