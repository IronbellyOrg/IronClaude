# PG4 Consolidated Findings (WS-B parity gate QA)

**Status: Complete**
**Consolidated verdict: PASS** (all 6 lens agents returned binary PASS; zero defects; only non-blocking observations)
**Date:** 2026-06-16

## Lens verdicts (6 agents, all `fix_authorization: false`, adversarial stance)

| # | lens | agent | verdict | report |
|---|------|-------|---------|--------|
| 1 | deletion-survivability | rf-qa | **PASS** | `qa/qa-structural-deletion-survivability-report.md` |
| 2 | CLI-driven | rf-qa | **PASS** | `qa/qa-structural-cli-driven-report.md` |
| 3 | invariant-coverage | rf-qa | **PASS** | `qa/qa-structural-invariant-coverage-report.md` |
| 4 | golden-authenticity | rf-qa-qualitative | **PASS** | `qa/qa-content-golden-authenticity-report.md` |
| 5 | prompt-parity-correctness | rf-qa-qualitative | **PASS** | `qa/qa-content-prompt-parity-report.md` |
| 6 | determinism | rf-qa-qualitative | **PASS** | `qa/qa-content-determinism-report.md` |

## Decisive evidence
- **Deletion-survivability (#1):** the agent PHYSICALLY removed `t2_normalize.py` from src + dev-mirror and re-ran the gate → **16 passed / 0 skipped**. No `skipif`, no `importlib` legacy load, no `LEGACY_SCRIPT` constant in executable code (4 `t2_` matches are docstring prose at lines 13/15/19/46). This is the migration's core safety property, proven.
- **CLI-driven (#2):** all 5 scenarios route through `_run_cli → runner.invoke(swarm_group, ["run","--lens","bare-review",...,"--transport","stub"])`; assertions read on-disk `bare-review-*.final.md` + `yaml.safe_load`'d nested `return-contract.yaml`; zero `BareReviewV1(`/`determine_status(` driving any assertion.
- **Invariant-coverage (#3):** all 5 invariants present + CLI-driven across 3 scenarios; invariant 1 is real multiset byte-equality (not substring); invariant 4 reads the CLI-emitted `caller_metadata.suspect` + `recommended_next_command` (not the lens template).
- **Golden-authenticity (#4):** re-running `SWARM_REGEN_GOLDEN=1` yielded a **byte-stable, zero-diff** golden tree (all 13 sha256s unchanged) — authentic real-legacy output, not hand-fabricated.
- **Prompt-parity (#5):** asserts ONLY `endswith(CANONICAL_INJECTION_GUARD_SENTENCE)` using the real imported symbol (177-char, non-vacuous); full prompt byte-parity correctly NOT asserted (G-2).
- **Determinism (#6):** hermetic (`--transport stub`), 3 consecutive runs identical (16 passed each); sorted-multiset body comparison is order-robust; timeout slot retry-overflow handled.

## FR-028 adjudication (the open item this gate was asked to assess)
The invariant-coverage lens (#3) explicitly adjudicated the FR-028 §7.4 salvage-promotion divergence as **(a) ACCEPTABLE — does NOT block**: driving `salvage-promoted` as 3 plain-success reviewers is the correct choice for a parity-vs-golden gate (the frozen golden IS success/M=3; body bytes are byte-identical because the `salvaged` flag never enters rendered frontmatter; the §7.4 promotion is structurally unreachable on the CLI path due to `normalize_wave2`'s shared `recipe_args`). The gap is a genuine, correctly-scoped, recipe-unit-tested HIGH source follow-up — asserting the divergent `partial`/M=2 would corrupt the gate into asserting a non-golden outcome. **PG4 concurs: not a blocker; tracked as a follow-up for the POST reflect gate (PC.5) to re-assess against the spec.**

## Non-blocking observations (NO fix applied — documented, not defects)
- **O1 (agents #2, #3):** the *golden* `return-contract.yaml` uses the legacy flat schema (`reviewers_*`, top-level `suspect`) while the *live* CLI contract uses the nested schema (`workers_*`, `caller_metadata.suspect`). **Harmless by design:** the gate never byte-compares the golden contract — only the `.md` bodies — and asserts the correct LIVE nested field names. Documented in `ws-b-golden-design.md` and `golden/README.md`.
- **O2 (agent #6):** recommendation that any future per-worker-field threading (the FR-028 fix) must exclude `elapsed_ms`/wall-clock fields or the golden byte-match becomes nondeterministic. **Captured** in the FR-028 follow-up item (determinism caveat added). No code change now — current code is correct.

## Fix cycle
**0 fix cycles required** (consolidated verdict PASS; no defects). Per PG4.4, a no-op note stands; PG4.5 verification round is skipped (no fixes to verify); proceed to PG4.6.
