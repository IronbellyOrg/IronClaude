# Phase 3.11 — State File Verification

**Result: PASS**

## Checks

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| schema_version = 1 | 1 | 1 | PASS |
| tdd_file = null | null | null | PASS |
| prd_file = set (non-null) | non-null | "/Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-prd-user-auth.md" | PASS |
| input_type = "tdd" | "tdd" | "tdd" | PASS |

## Additional State Values

- `spec_file`: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-tdd-user-auth.md
- `spec_hash`: 43c9e660788020b6fd44044c413e818b66481006e1e84e4bc1955b4aad478c5b
- `agents`: opus/architect, haiku/architect
- `depth`: standard
- `last_run`: 2026-04-03T14:58:13.266185+00:00

## Step Statuses in State

| Step | Status | Attempt |
|------|--------|---------|
| extract | PASS | 1 |
| generate-opus-architect | PASS | 1 |
| generate-haiku-architect | PASS | 1 |
| diff | PASS | 1 |
| debate | PASS | 1 |
| score | PASS | 1 |
| merge | PASS | 1 |
| anti-instinct | FAIL | 1 |
| wiring-verification | PASS | 1 |

## Artifact

- File: `.dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json`
