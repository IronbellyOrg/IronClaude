# Prompt 04: blind scoring of Stage C specs

Use the replicate's procedure unchanged (`p19/rep/build_score.py`, `p17/score/prompt-template.md`, `p17/score/ledger-blind.json`).

1. Copy each run's final spec to a new blind id `s<N>` (continue the numbering in `p17/score/key.json`; shuffle the order with a fixed seed), write `in/s<N>.md`, the unified diff against `p17/spec-original.md` (run `diff -u` from the `score/` directory so the header paths are `in/s<N>.md`), and the prompt from the template with BOTH placeholders filled (`__SID__` and `__OUT__`). Check that every diff is non-empty before launching anything.
2. Launch one Sonnet scorer per spec (never Fable; Opus 5.5 only for the rescore below). Scorers must not be told the panel, model or arm.
3. When all are scored, rescore the two highest and the two lowest specs with Opus 5.5 using the same inputs; report agreement.
4. Write `stage-c/scores/` (the `s<N>.json` files) and `stage-c/key.json` (sid to panel and run).
Final reply: `DONE` and the count of scored specs.
