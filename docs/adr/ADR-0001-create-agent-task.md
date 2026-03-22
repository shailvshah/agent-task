# ADR-0001: Create agent.task — a portable task contract format for agentic AI

**Status:** Accepted  
**Date:** 2026-03-21  
**Authors:** Shail Shah 
**Deciders:** Shail Shah  
**Relates to:** ADR-0002, ADR-0003, ADR-0004

---

## Context

### The problem

When an AI agent is assigned a task in 2026, there is no standard way to express:

1. What outcome the task must achieve
2. How to verify the task succeeded in machine-checkable terms
3. What the agent is bounded from doing
4. What resources the task may consume
5. What to do if the task fails or violates a constraint

Teams currently express this in:
- System prompts (invisible to external tools, unenforced, not portable, pollutes KV cache)
- AGENTS.md files (permanent project context, not per-task, not verifiable)
- Ad-hoc YAML (no schema, no validation, no shared tooling)
- Jira tickets or Slack messages (prose, completely unenforced)

### Evidence of harm

- NeurIPS 2025 analysis of 1,642 multi-agent traces: 41–87% failure rate, with unclear task specification as the top cause
- Gartner 2026: 40%+ of enterprise agentic AI projects will be cancelled by 2027, with inability to define and measure success as the primary reason
- Anthropic Agentic Coding Trends 2026: documents the INTENT→SPEC→PLAN pattern as best practice, but notes teams implement it in incompatible, non-portable ways

### What already exists

The Agentic AI Foundation (AAIF) has standardised three layers:

| Standard | Answers |
|---|---|
| MCP | What tools can this agent use? |
| A2A | How do agents communicate? |
| AGENTS.md | How should this agent behave in this project? |

None of these answer: **what must this specific task achieve, within what bounds, and how do we verify it?**

Several partial solutions exist but none are complete:
- Anthropic's internal YAML pattern: not OSS, not portable
- CrewAI `Task` object: framework-locked, no budget/rollback
- OpenAI Agents SDK guardrails: runtime enforcement only, no task definition
- arXiv Task Intent Schema: blockchain-specific, academic, no implementation

### What is needed

A portable, framework-agnostic, machine-readable file format that:
- Travels with a task, not an agent
- Is human-authored (not auto-generated — LLM test generation is unreliable per research)
- Is readable by multiple existing tools without coupling them
- Fits the existing AAIF stack without replacing any part of it
- Is minimal enough to have zero mandatory runtime dependency

## Decision

We will create `agent.task` — an open-source file format (JSON/YAML) and validator library (TypeScript + Python) for expressing task-scoped goal contracts.

### Strategic Vision (3-Phase Roadmap)

The long-term architecture of `agent.task` supports a three-pillar vision:
1. **Enterprise Readiness (OSS Plug)**: Providing strict validation, budget limits, and rollback hooks needed for enterprise compliance, easily pluggable into existing orchestrators.
2. **Standardization for Discovery**: Using the `meta.capabilities_required` field to act as the universal hook for Agent Registries to route tasks.
3. **Universal Execution Platform Agnosticism**: Cementing the schema so that *any* future platform or runner can independently execute the task using the definition, without framework "lock-in" from tools like LangGraph or CrewAI.

### What agent.task is

A single file format with six top-level keys:

```
goal         — what the task must achieve (outcome-focused, not step-focused)
accept       — verifiable acceptance criteria (assertion | state | rubric)
constraints  — scope limits, hard rules, approval gates
budget       — token/cost/time/tool hard limits per task
rollback     — compensation steps on failure or violation
meta         — id, author, timestamp, capabilities_required (discovery hook)
```

### What agent.task is NOT

- Not a new agent runtime or framework
- Not a replacement for MCP, A2A, or AGENTS.md
- Not auto-generated (human-authored, intentionally)
- Not a guarantee of enforcement (enforcement requires runtime integration)
- Not a standard until earned through adoption

### Positioning in the context window

```
[system prompt]      ← KV-cached, permanent
[AGENTS.md]          ← KV-cached, project-scoped
[agent.task XML]     ← per-task, dynamic zone, ~200 tokens, NOT cached
[retrieved context]  ← dynamic
[working memory]     ← volatile
```

`agent.task` occupies slot 3. Only `goal`, `constraints`, and `budget` are injected into the LLM context. `accept[]` and `rollback{}` are consumed by external tools only.

---

## Consequences

### Positive

- Gives teams a structured, versioned, auditable record of what a task was supposed to do
- Enables external tools (evaluators, budget enforcers, rollback engines) to read the same contract without coupling
- `meta.capabilities_required` creates a discovery hook for marketplace matching in Phase 2
- Fits the AAIF stack as a natural fourth primitive — can be proposed as RFC once adoption is established
- MIT licensed — no friction for adoption

### Negative / risks

- Adoption risk: teams already have ad-hoc patterns; switching cost exists
- Standardisation is not guaranteed — requires 50+ adopters before AAIF proposal is credible
- Enforcement gap: the file alone does not enforce anything — runtime integrations required
- LLM-as-judge rubric evaluation is probabilistic, not deterministic — cannot be the sole acceptance criterion for safety-critical tasks

### Neutral

- The step change is portability + completeness + OSS library, not the idea of task specification (which is prior art)
- agent.task is a discipline tool, not an intelligent automation layer

---

## Alternatives considered

### Alternative 1: Extend AGENTS.md with task sections

Rejected. AGENTS.md is permanent project context. Mixing per-task goal definitions into a permanent file creates context pollution, breaks KV caching, and makes task-specific criteria invisible to external tools.

### Alternative 2: Build a new runtime that includes task specification

Rejected. The problem is a specification and portability gap, not a runtime gap. Building a runtime would compete with LangGraph, Temporal, and CrewAI rather than composing with them. agent.task is a contract format, not a runtime.

### Alternative 3: Auto-generate acceptance tests from the goal

Rejected. UC San Diego/Cornell research (Dec 2025) and Meta TestGen-LLM study show LLM-generated test suites achieve recall of 0.37–0.81 on realistic datasets — insufficient for production reliability. Human-authored accept criteria with machine evaluation is the correct pattern.

### Alternative 4: Submit to AAIF before building

Rejected. Standards require demonstrated adoption. MCP succeeded because it was shipped and adopted, then standardised. agent.task must earn standardisation through adoption, not assume it through proposal.

### Alternative 5: Name it task.json

Rejected. `task.json` is already taken on npm (version 3.2.1, unrelated TypeScript library). `agent.task` fits the AAIF naming pattern (mcp, a2a, agents.md) and is available.

---

## References

- AAIF: https://aaif.io
- MCP Specification: https://spec.modelcontextprotocol.io
- AGENTS.md: https://github.com/openai/agents-md
- NeurIPS 2025 MAS failure analysis
- Gartner Agentic AI 2026 predictions
- Anthropic Agentic Coding Trends Report 2026
- arXiv 2601.04583: Open problems in agentic AI
- arXiv 2603.04746: Agent goal specification and verifiability
