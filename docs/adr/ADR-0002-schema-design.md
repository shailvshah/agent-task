# ADR-0002: Schema design — six core keys, optional extensions, JSON + YAML

**Status:** Accepted  
**Date:** 2026-03-21  
**Authors:** Shail Shah  
**Relates to:** ADR-0001, ADR-0003

---

## Context

Having decided to create agent.task (ADR-0001), we need to decide:

1. What keys the schema contains and which are required
2. How acceptance criteria are typed and evaluated
3. Whether to support JSON only, YAML only, or both
4. How to handle multimodal agents, long-horizon tasks, and multi-agent orchestration
5. Where the schema version boundary sits

---

## Decision

### Core schema — six top-level keys

Three required, three optional. This is the minimum viable contract.

**Required:**
- `goal` — outcome description + explicit exclusions. Required because without it, the contract has no definition of success.
- `accept` — array of verifiable criteria, minimum 1 item. Required because without it, there is no way to determine if the task succeeded.
- `meta` — id, author, timestamp, capabilities_required. Required for traceability and discovery.

**Optional:**
- `constraints` — scope limits, never rules, approval gates. Optional because some tasks have no meaningful constraints beyond the agent's built-in safeguards.
- `budget` — token/cost/time/tool limits. Optional because some execution environments handle budgets at the infrastructure level.
- `rollback` — compensation steps. Optional because not all tasks have reversible side effects.

### Accept criterion types — three, no more

```
assertion   — deterministic, code-evaluable expression. No LLM involved.
state       — system state check against external API/database.
rubric      — LLM-as-judge evaluation with explicit threshold.
```

Rationale: These three types cover the full evaluation spectrum. `assertion` and `state` are deterministic and reliable. `rubric` is probabilistic but necessary for qualitative outcomes. A fourth type (`test_run`) was considered but rejected — see Alternatives.

**Rubric limitations are explicit in the schema:**
- `threshold` is required for rubric type (no implicit defaults in safety-relevant evaluation)
- Rubric alone is never sufficient for safety-critical accept criteria — at least one `assertion` or `state` criterion must accompany any rubric for high-stakes tasks. This is a documented convention, not enforced by the schema.

### File format — JSON canonical, YAML accepted

Canonical format is JSON. Reason: JSON is unambiguous, universally parseable, and diff-friendly in git. YAML is accepted as an alias because it is more human-writable for complex contracts.

Both formats are equivalent. The validator accepts both. The canonical file extension is `.agent.task` for JSON and `.agent.task.yaml` for YAML.

### Extensions — four optional keys for v0.2

The core schema handles digital text agents completely. Four optional extension keys handle multimodal, long-horizon, and multi-agent scenarios without breaking v0.1 contracts:

```
inputs       — modality declaration (text, image, audio, video, sensor)
phases       — phased execution with per-phase budget and human review gates
subtasks     — multi-agent decomposition, each subtask is a nested contract
environment  — physical world + compliance (type, safety_class, latency_ms)
```

**Backwards compatibility rule:** A v0.1 validator MUST accept any v0.2 contract that uses only core keys. Extensions are purely additive.

### Context injection — goal + constraints + budget only

Only three of the six keys are injected into the LLM context window, serialised as XML:

- `goal` → injected (LLM must know what to achieve)
- `constraints` → injected (LLM must know what it cannot do)
- `budget` → injected (LLM must know when to stop)
- `accept[]` → NOT injected (consumed by evaluator, not LLM)
- `rollback{}` → NOT injected (consumed by rollback engine, not LLM)
- `meta` → NOT injected (tooling metadata only)

Rationale: Injecting accept criteria into the LLM context creates Goodhart's Law risk — the agent optimises to pass the criteria rather than achieve the outcome. Criteria are post-hoc verification tools, not guidance.

---

## Consequences

### Positive

- Minimal required surface (3 keys) lowers adoption barrier
- Three accept types cover the full evaluation spectrum without over-engineering
- JSON canonical format ensures deterministic parsing and git diff quality
- Extension model allows multimodal and multi-agent use cases without breaking existing contracts
- Separating injected vs non-injected keys prevents Goodhart's Law optimisation

### Negative / risks

- `check` expressions in assertion/state criteria have no defined evaluation language — implementations may diverge. This is tracked as a known open question in RFC-0001.
- Rubric evaluation is inherently probabilistic — high-stakes tasks SHOULD NOT rely solely on rubric criteria. This is a convention, not a schema enforcement.
- `.agent.task` file extension is unusual and may cause friction with editors that don't recognise it. VSCode extension planned for v0.2 milestone.

---

## Alternatives considered

### Alternative 1: Make all six keys required

Rejected. Mandatory rollback steps for a simple read-only research task add friction without value. Minimal required surface is a core design principle.

### Alternative 2: Add a `test_run` accept criterion type

Considered a fourth type that runs an actual test suite against the agent's output. Rejected because:
- LLM-generated tests are unreliable (recall 0.37–0.81 per Meta/UC San Diego research)
- Human-written test runners are framework-specific and cannot be portable
- `assertion` type with a deterministic check expression achieves the same result more simply

### Alternative 3: YAML only (more human-friendly)

Rejected. YAML has ambiguity pitfalls (Norway problem, implicit type coercion, indentation sensitivity) that make it a poor canonical format for a machine-read contract. JSON is unambiguous. YAML support as a write-friendly alias is the correct tradeoff.

### Alternative 4: Separate files per concern (goal.json, budget.json, etc.)

Rejected. The core value proposition is that one file travels with one task. Splitting into multiple files recreates the fragmentation problem agent.task is designed to solve.

### Alternative 5: Use OPA/Rego for constraint expressions

Considered for `constraints.never` and `accept[].check`. Rejected for v0.1 because Rego has a steep learning curve and would make the format inaccessible to non-specialists. Free-string expressions with runtime interpretation are accepted for now. Formalising the expression language is tracked as open question Q1 in RFC-0001.
