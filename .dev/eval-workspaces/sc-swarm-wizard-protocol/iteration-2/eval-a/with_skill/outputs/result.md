# sc-swarm-wizard-protocol — Eval A (with_skill) Result

## How the wizard handled the ambiguous goal

The user's goal — "look over my code... partly to catch bugs, partly to tidy it up.
Not sure how" — maps to **two lenses** in the Wave 1 interview table (`refs/interview.md` Q1):

- "Find bugs / review my code for correctness" → `bare-review`
- "Find small safe cleanups I could apply" → `refactor-find`

Per the interview rule ("If two fit equally (e.g. 'review and clean up'), **ask which
matters more rather than guessing**") and SKILL.md Wave 1 ("If two lenses fit the goal
equally, ask a disambiguating question rather than picking silently"), the wizard does
NOT silently default. It poses the tie-break question. The embedded answer
"catching bugs matters most" resolves the choice to **`bare-review`** (also the only
`stable` lens and the solid default).

Run type from the embedded answer: practice/stub first. Reviewers: default (3 for
`bare-review`). The mandatory stub dry-run (Wave 3) was executed and passed; no real
run was performed.

## Pre-flight (Wave 0 / Wave 2) — all green

- `swarm --help` reachable; flag surface matches `refs/cli-contract.md`.
- `validate-lenses`: registry OK (8 inspected, 7 validated).
- Target `/tmp/swarm-wizard-probe/demo.py` exists, 195 non-whitespace bytes (≥50 IMM-4 floor OK).
- Single input mode (`--lens`); `--target` + `--output` both supplied; reviewers=3 ∈ [2,4].

## Stub dry-run result (Wave 3) — passed

- exit 0; stdout `dispatched job (mode=lens, workers=3, results=3)`
- `.swarm-state.json` state == `terminal`; `return-contract.yaml` present
- contract `status: success`, workers 3/3 succeeded, 0 failed
- output dir: `.dev/swarm-runs/bare-review-20260619T061406/` (idempotent, fresh)
- Note: stub output is placeholder text, not real analysis — it only proves the pipeline.

---

## RESULT

- **AMBIGUITY_RECOGNIZED:** yes — the goal "catch bugs + tidy up" maps to two lenses
  (`bare-review` vs `refactor-find`); the wizard flagged the tie and resolved it by the
  interview's "ask which matters more" rule rather than guessing.
- **LENS:** `bare-review`
- **TIEBREAK_HONORED:** yes — the "catching bugs matters most" answer drove the choice to
  `bare-review` (not `refactor-find`).
- **DRYRUN_CMD:** `uv run superclaude swarm run --lens bare-review --target /tmp/swarm-wizard-probe/demo.py --output .dev/swarm-runs/bare-review-20260619T061406 --transport stub`
- **NEXT_CMD:** Real run (only after explicit go-ahead + env contract):
  `uv run superclaude swarm run --lens bare-review --target /tmp/swarm-wizard-probe/demo.py --output .dev/swarm-runs/bare-review-real-<ts> --transport openai_compat --reviewers 3 --tui`
  Then hand off the merged findings to `/sc:adversarial` (the bare-review lens's rendered
  `recommended_next_command`).
- **NOTES:** Stub dry-run green (status=success, 3/3 workers, state=terminal). No real run
  performed — user chose practice/stub first and the eval forbids a real run, so per the
  Return Contract this is effectively `status: cancelled` (declined real run after a green
  dry-run). Transport default correctly resolved to `stub` on the `--lens` path (the
  `--transport` help text claiming an openai_compat default is a known stale-doc claim).
  demo.py contains a planted sign bug (`add` returns `a - b`) and an unguarded
  zero-division in `divide`, which a real `bare-review` run is well-suited to surface.
