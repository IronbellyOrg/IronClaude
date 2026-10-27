# D-0092 — Evidence Index

**Deliverable:** D-0092 (E8 PreToolUse serena matcher body)
**Task:** T05.13
**Date:** 2026-05-20

## Files

| Path | Description |
|---|---|
| `../../evidence/T05.13/describe-E8.txt` | `uv run superclaude eval describe --suite real --eval E8` rendering — verifies manifest shape and OQ-2 body match |
| `../../evidence/T05.13/list-with-E8.txt` | `uv run superclaude eval list --json` — verifies 17 evals enumerate under suite `real` (E1, E2.1-3, E3-E15) |
| `../../evidence/T05.13/expect-roundtrip.txt` | Python `Expect.from_mapping` round-trip for all 5 E8 `expects[]` rows — verifies declarative DSL resolution; also lists every eval's `requires` clause for cross-check |
| `../../evidence/T05.13/README.md` | Evidence README with AC → evidence file mapping and out-of-scope deferral notes |

## Verifier commands used

```bash
make sync-dev          # propagated src/ → .claude/
make verify-sync       # confirmed sync (PASS)
uv run superclaude eval describe --suite real --eval E8 > evidence/T05.13/describe-E8.txt
uv run superclaude eval list --json                       > evidence/T05.13/list-with-E8.txt
uv run python -c '<round-trip script>'                    > evidence/T05.13/expect-roundtrip.txt
```

All three verifier commands exited 0.

## Cross-references

- Spec: `spec.md` (this directory)
- Design rationale / notes: `notes.md` (this directory)
- Manifest target diff: `src/superclaude/cli/eval/suites/real.yaml` E8 entry
  (was: stale stub with title `verify-sync detects drift between src/
  and .claude/`; now: OQ-2-frozen body)
- Capability declaration: `src/superclaude/cli/eval/suites/real.yaml`
  `optional_capabilities` (added `mcp_server.serena` row)
- Sibling deliverables: D-0090 (E6 Edit), D-0091 (E7 Write)
- Parent OQ-2 resolution: D-0082 §4 row E8
