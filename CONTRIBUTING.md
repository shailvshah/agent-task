# Contributing to agent.task

Thank you for contributing. This document explains how.

## Quick start

```bash
git clone https://github.com/agent-task/agent-task
cd agent-task

# TypeScript
cd packages/cli-ts && npm install && npm run dev

# Python
cd packages/cli-py && uv sync && uv run agent-task --help
```

## What to contribute

### High priority
- Example `.agent.task` contracts for real enterprise agents (see `examples/`)
- Bug reports with minimal reproduction cases
- Adapter implementations for agent frameworks (LangGraph, CrewAI, AutoGen)

### Schema changes
All schema changes — new keys, new types, modified validation rules — require an ADR in `docs/adr/` before implementation. Use `docs/adr/ADR-NNNN-title.md` format. See existing ADRs for the template.

### Fixing bugs
Open an issue first for non-trivial changes. Small fixes (typos, test gaps) can go straight to a PR.

## Pull request process

1. Fork the repo and create a branch: `git checkout -b feat/your-feature`
2. Make changes with tests
3. Ensure both implementations pass: `npm test` (TypeScript), `uv run pytest` (Python)
4. Ensure shared fixtures pass: `npm run test:fixtures`
5. Open a PR with a clear description

## ADR process

For any decision that affects the spec, external API, or architecture:

1. Copy `docs/adr/ADR-0000-template.md` to `docs/adr/ADR-NNNN-short-title.md`
2. Fill in context, decision, consequences, alternatives
3. Submit as a PR with status "Proposed"
4. After discussion and merge, status changes to "Accepted"

## Behavioural equivalence

Both the TypeScript and Python implementations must produce identical output for all shared test fixtures. Before submitting a PR that changes validation logic or CLI output, run:

```bash
npm run test:equivalence
```

This runs both implementations against `tests/fixtures/` and diffs the output.

## Code of conduct

Be kind. Assume good faith. Focus on the work, not the person.

## License

By contributing, you agree your contributions are licensed under MIT.
