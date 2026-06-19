# Swarm run: edge-case / parser-crash hunt on demo.py

## Goal
Find weird inputs or states that would crash or break the parser in
`/tmp/swarm-wizard-probe/demo.py`.

## Lens choice
**`bare-review`** is the right fit. It fans a single prompt across N
heterogeneous reviewers and asks each to surface concrete findings with
severity + `file:line` citations + suspect-source flags, then normalizes and
merges them. That is exactly the shape of "find weird inputs/states that crash
or break my code." (`custom` and unknown lenses are rejected with EXIT_USAGE.)

The target file itself contains two seeded edge cases the review is meant to
surface:
- `add(a, b)` returns `a - b` (off-by-sign bug).
- `divide(numerator, denominator)` has no zero-division guard (`ZeroDivisionError`
  on `denominator == 0`).

## Reviewer count
Default for `bare-review` is **3** workers (`workers.count: 3` in the scaffold).
Overridable via `--reviewers N`, integer in `[2, 4]`.

## Transport
- `stub` (default) — deterministic in-process transport; emits empty findings
  tables. Good for verifying the pipeline wires end-to-end without spending
  model calls.
- `openai_compat` — routes through the T2 proxy. `~/.aienv` has the full
  contract present (`T2ProxyUrl`, `T2ProxyKey`, `T2Model01..04`,
  base `:4000/cli`), so this transport is ready for a real run that will
  actually reason about the bugs.

## What I ran (verified)
Safe dry-run with the deterministic `stub` transport:

```
uv run superclaude swarm run --lens bare-review \
  --target /tmp/swarm-wizard-probe/demo.py \
  --output /tmp/swarm-wizard-probe/out-stub \
  --transport stub
```

Result: `swarm run: dispatched job (mode=lens, workers=3, results=3)`.
Full artifact set landed under the output dir: `manifest.json`,
`execution-log.jsonl`, 3x `*.final.md` + `*.meta.json` reviewer outputs,
`merged.md`, and `return-contract.yaml`. The stub findings tables are empty by
design (no real model reasoning) — this confirms preflight → dispatch →
normalize → merge → contract all work; it does not yet surface the bugs.

## Recommended next command (real run to surface the bugs)
Switch to the live proxy transport so the reviewers actually analyze the file:

```
uv run superclaude swarm run --lens bare-review \
  --target /tmp/swarm-wizard-probe/demo.py \
  --output /tmp/swarm-wizard-probe/out-live \
  --transport openai_compat
```

Then read `merged.md` (per-reviewer findings) in the output dir; the
`return-contract.yaml` carries the `recommended_next_command` for handing the
suspect files to `/sc:adversarial`.

## RESULT
- LENS: bare-review
- REVIEWERS_DEFAULT: 3
- TRANSPORT: stub (verified) / openai_compat (configured, ready for real run)
- DRYRUN_CMD: `uv run superclaude swarm run --lens bare-review --target /tmp/swarm-wizard-probe/demo.py --output /tmp/swarm-wizard-probe/out-stub --transport stub`
- DRYRUN_VERIFIED: yes
- NEXT_CMD: `uv run superclaude swarm run --lens bare-review --target /tmp/swarm-wizard-probe/demo.py --output /tmp/swarm-wizard-probe/out-live --transport openai_compat`
- NOTES: Read demo.py (seeded off-by-sign in add + missing zero-div guard in divide). Mapped the request to the bare-review lens (findings table w/ severity + file:line + suspect flag). Confirmed default reviewers=3 via scaffold. Confirmed proxy contract present in ~/.aienv. Ran a safe stub dry-run; pipeline dispatched 3 workers and produced the full artifact set; stub tables empty by design. Real openai_compat run is the next step to actually surface the bugs.
