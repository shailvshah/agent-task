# ADR-0003: Dual implementation — TypeScript (npx) + Python (uv/pip)

**Status:** Accepted  
**Date:** 2026-03-21  
**Authors:** Shail Shah 
**Relates to:** ADR-0001, ADR-0002

---

## Context

The agent.task spec needs a reference implementation — a validator library and CLI that developers can use immediately. We need to decide which programming language(s) to support, how to distribute them, and how to ensure behavioural equivalence between implementations.

The agentic AI ecosystem in 2026 is split:
- Agent frameworks: Python-dominant (LangGraph, CrewAI, AutoGen, LlamaIndex are all Python-first)
- Developer tooling: TypeScript/Node is dominant (VS Code extensions, CI/CD scripts, web tooling)
- Enterprise integration: both Python and TypeScript are common

---

## Decision

### Two independent, behaviourally equivalent implementations

**TypeScript** — distributed via npm as `@agent-task/cli`, runnable without install via `npx @agent-task/cli`.

**Python** — distributed via PyPI as `agent-task`, runnable without virtualenv via `uvx agent-task` or `pipx agent-task`.

Both expose identical CLI commands with identical exit codes:

| Command | TypeScript | Python |
|---|---|---|
| Scaffold | `task init` | `agent-task init` |
| Validate | `task validate [file]` | `agent-task validate [file]` |
| Inject | `task inject [file]` | `agent-task inject [file]` |
| Evaluate | `task evaluate [file] --trace [file]` | `agent-task evaluate [file] --trace [file]` |
| Result | `task result [file]` | `agent-task result [file]` |

### Technology choices

**TypeScript:**
- Schema validation: AJV v8 (industry standard JSON Schema validator, fast)
- CLI framework: Commander.js v12
- Interactive init: Inquirer.js v10
- Output formatting: Chalk v5
- Type system: Zod v3 for runtime validation beyond JSON Schema

**Python:**
- Schema validation: jsonschema v4 + Pydantic v2 models
- CLI framework: Typer (builds on Click, excellent UX)
- Output formatting: Rich (colour, tables, panels)
- Package build: Hatchling (modern, fast)
- uv compatibility: full (pyproject.toml with `[project.scripts]`)

### Distribution strategy

**TypeScript:** Published to npm under `@agent-task/cli`. The `npx @agent-task/cli` invocation requires no install. This is the zero-friction path for developers who want to validate a single file.

**Python:** Published to PyPI under `agent-task`. Supports three install paths:
- `uvx agent-task` — no install, no venv (recommended, uv must be installed)
- `pipx agent-task` — no venv, system-isolated
- `pip install agent-task` — traditional install

### SDK vs CLI-only

v0.1 ships CLI + importable SDK in both languages:

```typescript
// TypeScript SDK
import { load, validate, inject, evaluate } from '@agent-task/cli'
const contract = load('task.agent.task')
const result = validate(contract)
```

```python
# Python SDK
from agent_task import load, validate, inject, evaluate
contract = load('task.agent.task')
result = validate(contract)
```

Framework adapters (LangGraph, CrewAI, AutoGen) are separate packages in v0.2 to avoid forcing framework dependencies on users who just want the validator.

### Behavioural equivalence testing

A shared JSON test fixture file (`tests/fixtures/`) defines:
- Valid contracts that must pass validation in both implementations
- Invalid contracts with specific error messages that both must produce
- XML injection output that must be byte-identical between implementations

CI runs both implementations against the same fixtures on every PR.

---

## Consequences

### Positive

- Zero-friction entry path for both TypeScript and Python developers
- Python SDK integrates directly with LangGraph, CrewAI, AutoGen workflows
- TypeScript SDK integrates with CI/CD pipelines, VS Code extension (planned), web tooling
- Shared fixtures ensure behavioural equivalence — one spec, two implementations

### Negative / risks

- Two implementations double the maintenance burden
- Behavioural divergence risk as the schema evolves — requires disciplined fixture testing
- TypeScript `npx` cold start is slow (~2–3 seconds) for large packages — keep CLI dependencies minimal

### Neutral

- Rust was considered as a third implementation for speed but rejected for v0.1 — ecosystem reach is more important than performance at this stage
- Go was considered for a single cross-compiled binary but rejected — Python and TypeScript have far more reach in the target developer community

---

## Alternatives considered

### Alternative 1: Python only

Rejected. Agent framework developers (Python) are not the only audience. CI/CD engineers, VS Code extension developers, and web platform teams are TypeScript-first. Python-only would miss a significant adopter segment.

### Alternative 2: TypeScript only

Rejected. The agent framework ecosystem (LangGraph, CrewAI, AutoGen) is Python-first. A Python developer who wants to validate a contract inline in their agent code should be able to `from agent_task import validate` — not shell out to a Node process.

### Alternative 3: One implementation with bindings

Considered writing in Rust and generating Python/TypeScript bindings. Rejected for v0.1 — WASM/FFI adds complexity and friction. Speed is not a constraint for a validator that runs on a ~200-token JSON file.

### Alternative 4: JSON Schema only, no CLI

Rejected. A JSON Schema file alone requires developers to install and run ajv or jsonschema manually. The CLI is the zero-friction entry point that drives adoption. The schema is the standard; the CLI is the marketing.
