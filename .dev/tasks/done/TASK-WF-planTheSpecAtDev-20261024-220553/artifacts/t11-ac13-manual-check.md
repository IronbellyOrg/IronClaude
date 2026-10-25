# T11 AC-13 manual check (SPEC Section 10.2 walkthrough)

Why manual: `/sc:implement` is model-executed protocol prose; no pytest harness can drive the reviewer, fixer and parent steps without a model. `tests/skills/test_implement_severity_replay.py` checks only that the rules are consistent.

## Setup

1. Make a temp git repo with `docs/memory/README.md`, `docs/user-guide/memory-system.md` and a tracked `docs/memory/solutions_learned.jsonl`; commit it (this commit is `$start`).
2. Write a legacy one-task plan with T1 and AC T1.AC1 to T1.AC4 (the run `E` memory-docs task), and a legacy ledger holding no T1 lines.
3. Run `/sc:implement <plan>` in a fresh Claude Code session.

## Walkthrough (steer the reviews with the Section 10.1 findings)

1. A1 review fails on D1 and D2 (`false-claim=yes`). Expect `retries/T1/review-1.md` and ref `r1-1`; no ledger line. The A1 minors and notes are appended to `retries/T1/notes.md` tagged `r1-1`.
2. A2 fix pass with probes. The A2 review raises the `solutions_learned.jsonl` append (`harmful-effect=yes`, `late`) even if labelled "low".
3. Expect a probe-only entry `probe-2-1.md` for the data-write family (no `after:` lines), then `repair-2-1.md`; no `blocked` line, no `step=open`.
4. Repair re-review (fresh subagent) raises D1 sample-file and D2 `jq` (`late`). Expect `repair-2-2.md`.
5. Second re-review is clean. Expect the notes file rewritten: line 1 the `start` sha, lines 2 to m the minors and notes of `r1-1`, `r2-1`, `r2-2` whose text is still in the tree, `superseded` lines after m.

## Expected ledger (exactly two T1 lines)

```
T1: start sha=<start sha>
T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3,T1.AC4 evidence=T1.AC1@<path:line>,T1.AC2@<path:line>,T1.AC3@<path:line>,T1.AC4@<path:line>,notes@.dev/implement/<slug>/retries/T1/notes.md:1-<m> extras=lint:skip,typecheck:skip,test:skip files=docs/user-guide/memory-system.md,docs/memory/README.md
```

## Pass criteria

- T1 `complete verdict=compliant` at A2 after 4 reviews.
- `grep -c 'step=revert' progress.md` prints 0; no `retry … step=open`, no `halt`, no `Ruling:` line; no `advice-*.md` files.
- `retries/T1/notes.md` exists and the `notes@` token cites lines 1 to m.

Record the result in the PR body.
