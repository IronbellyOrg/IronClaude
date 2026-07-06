# Troubleshoot Report — "exactly four files" doc claim wrong for resume mode

- **type:** bug (doc accuracy) · **tier_reached:** 1 · **confidence:** 0.96 · **status:** success
- **source:** PR #152 review comment r3380676999 (augmentcode[bot], severity medium)

## Summary
README "What a run emits today" and command-reference "Run artifacts" stated a successful
`swarm run --output` emits **exactly four** files and that `return-contract.yaml`/`merged.md`/
`done.json` are NOT emitted (pending M5). That is correct only for **fresh** runs. The
`--resume` path re-runs Wave 2 + Wave 3 and DOES emit those artifacts. The bot is correct;
the claim was unscoped and contradicted user-guide §8.

## Evidence (real code)
- Fresh run is dispatch-only: `run_cmd` calls `dispatch_wave1` only (`commands.py:374`); no `reduce_wave3`.
- Resume runs the reduce pipeline: `normalize_wave2` (`commands.py:1952`) then `reduce_wave3(mode=amalgamation_mode)` (`commands.py:1977`).
- `reduce_wave3` writes to disk: `return-contract.yaml` via `emit_contract` (`reduce.py:370-393`); `done.json` via emit_done_sentinel (`reduce.py:406+`); `merged.md` only when `mode == normalize+merge` (`reduce.py:290-295`); all atomic (`_atomic_write_bytes`, `reduce.py:335-354`).

## Diagnosis
Documentation defect, not a code defect. The "M5 not yet wired" statement applies to the
fresh dispatch-only path; resume already exercises the Wave 2/3 writer. `behavior_is_documented`
= false (the docs were wrong, code is correct).

## Fix applied (2-file doc scoping)
- `docs/swarm/README.md` "What a run emits today": scoped the four-file / not-emitted claim to **fresh (non-resume)** runs; added a Resume-mode note (resume emits `return-contract.yaml` + `done.json`, plus `merged.md` when `amalgamation_mode == normalize+merge`, via `reduce_wave3`).
- `docs/swarm/command-reference.md` "Run artifacts": same scoping + a `--resume emits more` paragraph.

markdownlint passes; new cross-links (user-guide §8, command-ref run-artifacts) resolve.

## Risk + rollback
Doc-only change; no code/test impact. Rollback = revert the two doc edits.
