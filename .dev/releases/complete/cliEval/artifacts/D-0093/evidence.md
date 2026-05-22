# D-0093 — Evidence Index

**Deliverable:** D-0093 (E9 PostToolUse Read async hook body)
**Task:** T05.14
**Date:** 2026-05-20

## Files

| Path | Description |
|---|---|
| `../../evidence/T05.14/describe-E9.txt` | `uv run superclaude eval describe --suite real --eval E9` rendering — verifies manifest shape and OQ-2 body match |
| `../../evidence/T05.14/list-with-E9.txt` | `uv run superclaude eval list --json` — verifies 17 evals enumerate under suite `real` (E1, E2.1-3, E3-E15) |
| `../../evidence/T05.14/list-default.txt` | `uv run superclaude eval list` plain output — sibling sanity check |
| `../../evidence/T05.14/expect-roundtrip.txt` | Python `Expect.from_mapping` round-trip for all 3 E9 `expects[]` rows — verifies declarative DSL resolution; also lists every eval's `requires` clause for cross-check |
| `../../evidence/T05.14/README.md` | Evidence README with AC → evidence file mapping and out-of-scope deferral notes |

## Verifier commands used

```bash
make sync-dev          # propagated src/ → .claude/
make verify-sync       # confirmed sync (PASS)
uv run superclaude eval describe --suite real --eval E9 > evidence/T05.14/describe-E9.txt
uv run superclaude eval list --json                       > evidence/T05.14/list-with-E9.txt
uv run superclaude eval list                              > evidence/T05.14/list-default.txt
uv run python -c '<round-trip script>'                    > evidence/T05.14/expect-roundtrip.txt
```

All verifier commands exited 0.

## Cross-references

- Spec: `spec.md` (this directory)
- Design rationale / notes: `notes.md` (this directory)
- Manifest target diff: `src/superclaude/cli/eval/suites/real.yaml` E9 entry
  (was: stale stub with title `installer copies skills into ~/.claude/skills`;
   now: OQ-2-frozen body)
- Sibling deliverables: D-0087 (E3), D-0088 (E4), D-0089 (E5), D-0090 (E6),
  D-0091 (E7), D-0092 (E8)
- Parent OQ-2 resolution: D-0082 §4 row E9
- Hook script: `src/superclaude/hooks/scripts/freshness-post-read.sh`
- Hook routing: `src/superclaude/hooks/hooks.json` (PostToolUse Read matcher block)
