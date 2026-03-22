---
name: test-equivalence
description: Runs the behavioral equivalence tests between the TypeScript and Python CLI implementations.
---

# Test Equivalence Command

You are an AI assistant orchestrating the `test-equivalence` command for the `agent.task` repository.

## Your Task
1. Execute the behavioral equivalence test script.
2. If it fails, analyze the divergence between the TypeScript JSON output and the Python JSON output.
3. Propose a fix to ensure both implementations strictly align.

## Instructions
Run the equivalence test exactly as configured in the CI pipeline:
```bash
# Ensure both packages are built
npm run build --prefix packages/cli-ts
uv sync --prefix packages/cli-py

# Iterate over fixtures and validate output matches
for fixture in tests/fixtures/valid/*.agent.task; do
  ts_out=$(node packages/cli-ts/dist/cli/index.js validate "$fixture" --json)
  py_out=$(uv run --directory packages/cli-py agent-task validate "$fixture" --json)
  if [ "$ts_out" != "$py_out" ]; then
    echo "DIVERGENCE on $fixture"
    exit 1
  fi
done
```
If there is a divergence, investigate the `packages/cli-py/src` and `packages/cli-ts/src` validation logic immediately.
