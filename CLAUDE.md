# CLAUDE.md

This file provides guidance to Claude Code and other AI copilots when working with the `agent.task` repository.

## Repository Overview
`agent.task` is a portable task contract format for agentic AI. 

## Architectural Rules
### 1. Dual Implementation (Strict)
This repository contains two independent, officially supported packages:
- `packages/cli-ts` (TypeScript / Node.js)
- `packages/cli-py` (Python)

**Rule of Behavioral Equivalence:** Both implementations MUST produce byte-identical JSON outputs for any given input. Before committing any changes to schema validation, you MUST run the equivalence tests:
```bash
# This relies on tests/fixtures/valid/*.agent.task matching exactly
npm run test:equivalence
```

### 2. Schema Changes
Any new schema key, modified validation rule, or deprecated field MUST be proposed via an Architecture Decision Record (ADR).
- Use `docs/adr/ADR-0000-template.md` to scaffold a new ADR.
- Place it in `docs/adr/`.

### 3. Extensible Schemas (Pydantic / Typer)
The Python CLI relies on `Typer` and `Rich`. The Pydantic models in `agent_task.models` MUST retain `extra="allow"` ConfigDicts so frameworks can inject custom hyperparameters (e.g. `time_limit_sec`) without crashing the parser. `GoalType` MUST remain a `Union` so developers can casually pass strings.

### 4. Universal Adapter Interface
When adding new orchestrator support (LangGraph, CrewAI, Agno), you MUST implement the `BaseTaskAdapter` interface defined in `cli-py`.
Adapters act strictly as a toolkit (providing context injection, telemetry callbacks, and evaluation) and MUST NEVER wrap or dictate the user's execution graph.

## Developer Workflows (.claude)
This repository uses Claude Code developer commands (in `.claude/commands/`) to orchestrate complex maintenance tasks:
- `/test-equivalence` (Tests matching outputs between Python and TS)
- `/scaffold-adapter` (Guides building LangGraph/CrewAI adapters)

**When writing code for `agent.task`:**
- Write clean, deterministic code. 
- Do not add external LLM evaluation requirements to the schema parser. The parser only checks schema validity.
