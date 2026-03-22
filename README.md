# agent.task

**A portable, framework-agnostic task contract for agentic AI.**

`agent.task` is an open-source file format and validator library that gives any AI agent a structured, machine-readable definition of:

- **What** this specific task must achieve (goal)
- **How** to verify it succeeded (acceptance criteria)
- **What** it is bounded by (constraints + budget)
- **What** to do if it fails (rollback)

```
┌─────────────────────────────────────────────────────────┐
│  MCP          → how agents connect to tools             │
│  A2A          → how agents talk to each other           │
│  AGENTS.md    → how agents behave in a project          │
│  agent.task   → what this specific task must achieve  ← │
└─────────────────────────────────────────────────────────┘
```

---

## Quickstart

```bash
# TypeScript / Node
npx @agent-task/cli init
npx @agent-task/cli validate my-task.agent.task

# Python
uvx agent-task init
uvx agent-task validate my-task.agent.task
```

## What a task contract looks like

```json
{
  "$schema": "https://agent-task.dev/schema/v0.1.json",
  "$version": "0.1.0",

  "goal": {
    "summary": "Resolve P1 incident INC0092847 — payment service down",
    "outcome": "Payment service restored, root cause documented, incident closed within 60-minute SLA.",
    "not": ["Do not restart primary DB without DBA approval"]
  },

  "accept": [
    { "type": "state",     "description": "Incident resolved in ServiceNow",
      "check": "servicenow.incident.INC0092847.state == 'resolved'" },
    { "type": "assertion", "description": "Resolved within 60-minute SLA",
      "check": "resolved_at - opened_at <= 3600" },
    { "type": "rubric",    "description": "Post-incident report is substantive",
      "evaluator": "llm", "threshold": 0.8,
      "criteria": "Report contains timeline, specific root cause, and ≥2 action items with owners." }
  ],

  "constraints": {
    "scope": ["servicenow_itsm", "datadog", "pagerduty"],
    "never": ["Modify production DB schema", "Send external comms without approval"],
    "require_approval_if": ["Fix requires production restart"]
  },

  "budget": {
    "tokens": 200000, "cost_usd": 2.00,
    "wall_time_minutes": 60, "on_exceed": "halt_and_report"
  },

  "rollback": {
    "on_constraint_violation": "halt_and_revert",
    "steps": [
      { "action": "revert_infrastructure_changes" },
      { "action": "notify", "channel": "pagerduty", "message": "Agent halted: {reason}" }
    ]
  },

  "meta": {
    "id": "snow-p1-INC0092847",
    "created_by": "now-assist-orchestrator",
    "created_at": "2026-03-21T14:23:00Z",
    "capabilities_required": ["servicenow_read_write", "datadog_read", "log_analysis"]
  }
}
```

## How it fits in the context window

```
[system prompt]        ← KV-cached, permanent — who the agent is
[AGENTS.md]            ← KV-cached, project-scoped — how it behaves
[agent.task XML]       ← per-task, ~200 tokens — what this task must achieve  ← YOU ARE HERE
[retrieved context]    ← dynamic, assembled per step
[working memory]       ← volatile, managed by context engineering
[current input]        ← per-step trigger
```

`agent.task` is injected as a structured XML block (goal + constraints + budget only).
`accept[]` and `rollback{}` are consumed by external tools — not the LLM.

## How existing tools consume it

| Tool | Reads | Does |
|---|---|---|
| LangGraph / CrewAI / AutoGen | `goal` + `constraints` | Executes the task |
| Ragas / DeepEval | `accept[]` | Evaluates whether goal was met |
| AgentGuard / OpenShell | `budget{}` | Halts agent at cost/token limit |
| Temporal / SagaLLM | `rollback{}` | Executes compensation on failure |
| AGNTCY registry | `meta.capabilities_required` | Matches task to capable agent |

## CLI commands

```bash
task init                              # scaffold interactively
task validate task.agent.task          # validate schema + semantic rules
task inject task.agent.task            # render XML for context window
task evaluate task.agent.task \
  --trace run.jsonl                    # evaluate accept[] criteria
task result task.result.json           # display result summary
```

## Schema versions

| Version | Status | Description |
|---|---|---|
| v0.1 | Current | Core 6 keys: goal, accept, constraints, budget, rollback, meta |
| v0.2 | Planned | Extensions: inputs, phases, subtasks, environment |

## Relationship to AAIF

`agent.task` is proposed as the fourth primitive in the [Agentic AI Foundation](https://aaif.io) stack alongside MCP, A2A, and AGENTS.md. See [RFC-0001](./RFC-0001-agent-task.md).

## Status

🚧 **Pre-release — v0.1.0 in active development**

- [x] Spec v0.1 (this repo)
- [x] JSON Schema
- [x] 4 enterprise example contracts
- [ ] TypeScript CLI + validator
- [ ] Python CLI + validator
- [ ] LangGraph adapter
- [ ] CrewAI adapter
- [ ] AAIF RFC submission

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). All contributions welcome.
Schema changes require an ADR in [docs/adr/](./docs/adr/).

## License

MIT — see [LICENSE](./LICENSE)
