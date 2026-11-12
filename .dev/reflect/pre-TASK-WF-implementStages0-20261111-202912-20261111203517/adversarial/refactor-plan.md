# Emerging consensus after Round 2 (input to the Round 2.5 invariant probe)

Plan: .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md (251 lines, 20 tasks). Proposed plan edits, by cluster, with adjudicated severity.

## Blocking
- C-001 Task 10 acceptance line 1 needs Task 11's template. Fix: Task 10 tests the exhaustion path with a temporary template written in tmp_path (tier1b fixed anchor); the packaged `@reflect-pre` assertion moves to Task 11.
- C-003 Task 8 golden vs `tiers_sha256` (panel.py:520 hashes the whole tier object; Task 9 adds `classes`). Fix: Task 8's golden is taken from a frozen copy of the current tier file stored as a test fixture (with the current `review-tiers.default.json` content), and states that `tiers_sha256` of the packaged file changes in Task 9 by design; Task 9 adds a golden for the new packaged hash.
- C-013 Constraint line "Never use Opus, Fable or Tier 0 in any new template" contradicts Task 11. Fix: reword to "Fable and Tier 0 never appear in a new template; Opus appears only in the uses the spec's 'Opus uses' section allows (the t4 slot of @reflect-pre, -enterprise)".
- C-015 "lint test design" is a Stage 0 deliverable with no Stage 0 task. Fix: Task 6 also writes `./artifacts/lint-test-design.md` from gate items 3 and 5 (assertion list, fixtures, expected failures); Task 7 exit checklist names it; Task 15 implements it.
- C-016 Task 20 reads `t2_engine_effective` and parity from a manifest nobody writes them to. Fix: Task 17 `frozen` state records `t2_engine_requested`, `t2_engine_effective`; Task 19 passes them at `manifest init`, adds `panel_parity` and `anchor_replaced` to the 9.2 list and to the manifest; Task 20 names the file and field it reads for each; Task 20 counts MALFORMED from `audit.log` rows.
- C-017 Task 20 omits the contract lint. Fix: Task 20 depends on Task 15, runs `panel_lint` per shadow run, any lint failure is FAIL, with a synthetic extra-key run proving it cannot PASS.

## Medium
- C-002 Task 14 "clean git status": replace with `git status --porcelain` identical before and after the probe window, apart from Task 14's own artifact files.
- C-004 `resolve` re-wraps `NoModelAvailable` (panel.py:489-496) and the CLI prints `str(exc)` only: Task 8 re-raises ExclusionExhausted for the fixed anchor and records skipped slots; Task 10 prints `type(exc).__name__`.
- C-005 Task 9: state that `validate_panel` runs the profile for `reflect-*` templates when a tier file is given and that `resolve` re-checks resolved ids and `launch`; `--sequence` is passed into the check; name the Fable class (`fable`).
- C-006 Task 2: card-format table (accepted shapes: yaml with severity blocking|minor, or yaml with other severity words and `deviation_class`, or markdown); plan/spec paths from the run's `artifacts/input-snapshot.yaml`; comma and semicolon ref lists split; fixed `risk` rule; other severity words counted as unconverted; unconvertible cards count against the 90% share.
- C-007 Task 3 signature gets a per-reviewer record (block, calibration map, ordinal); Task 4 says how sidecar calibration is joined and what happens when absent; Task 12 accepts `--calibration <file>` shape or an embedded `calibration:` block.
- C-008 define `section` for v2 fingerprint (empty string) and add a test.
- C-009 Task 7 depends on Tasks 4, 5, 6; "four exit items" (not five); Task 8 note.
- C-012 Task 19: record `judge_identity: unknown` and `judge_class_collision: unknown` unless sc-adversarial's return contract names a judge field; verification of that field is part of Task 19 (read sc-adversarial-protocol SKILL.md contract).
- C-014 add a labelled Plan decision: Stage 1 and 2 code is built dormant; Stage 0 exit (owner-labelled 50-pair check) is recorded PENDING in Task 7's checklist; Stage 1 entry is not claimed; merge/enable stays an owner decision.
- C-018/C-019 Task 19: assert the judge identity is not Fable or tier0 when known, add REPORT note on a collision in `<out>/panel/` notes; compare `reviewer_model_self_report` with the pin and set `identity_mismatch_suspected`; with an unverified identity the panel notes make no independence claim.
- C-020 Task 19 second `review cluster --kept <file>` call after the Wave 5 validator; define the kept-ids file the coordinator writes from the validator result.
- C-021 Task 14 probes also list their available tool names and record whether Write, Edit or Bash appears.
- C-023 Task 15 EV-1: card count >= `reviewers_resolved` (from manifest if present, else len(`reviewer_cards`)), min 2; plus the loud-fallback branch (adversarial_unavailable true + audit F-step row).
- C-024 Task 16: exclude run directories that contain `panel/manifest.json` from the legacy set; shadow input is a list of run directories; state values for `derive_verdict` args.
- C-025 Task 18: D3 effects on status and banner only for effective engine `panel`; in shadow record `t2_floor_unmet` in telemetry only.

## Minor
- C-010 Task 1 acceptance reworded to line level; decide `prior` lines. C-011 Task 11 adds reflect-lite resolution check. C-022 Task 19: brief line only when effective engine is shadow; amend reviewer-spec.md "verbatim" sentence for this one line. C-027 Task 18 creates "4.3a T2 engine selection", table inside it; baseline for byte-identity is the commit before Task 18. C-028 Task 13 lists its options; Task 15 pins a hardcoded stable key list with a test.

## Refuted
- C-026 (publish vs audit.log): spec:363 requires the temp-file publish; rows can be carried.

## Added after the Round 2.5 invariant probe (INV items, each folded into the plan edits)
- INV-001 (HIGH) Task 19 names a `superclaude review manifest advance` call after each step it runs (resolved, dispatched, collected, calibrated, clustered) and after the legacy Wave 4 and Wave 5 (debated, validated); Task 17 states shadow mode must end at `published` through the same call, with no state skipped.
- INV-007 (HIGH) `panel_parity` is defined as equal ordered `(persona, model id)` lists; `scripts/reflect_shadow_exit.py` recomputes it from the legacy reviewer card headers against `panel/resolution.json` instead of trusting the recorded boolean.
- INV-002 the second cluster pass writes `clusters_kept.json`; `clusters.json` and its manifest hash stay untouched.
- INV-003 Task 7 keeps exactly four exit items and a separate "ships" line for the lint test design.
- INV-004 Task 5 `Depends on: Task 2, Task 3`.
- INV-005 Task 5 samples `min(25, available)` per side, writes the shortfall in the sheet header; fewer than 50 rows is reported INSUFFICIENT PAIRS, not a pass.
- INV-006 Task 12 and Task 20 emit `null` / "n/a" for `cluster_agreement` with fewer than 2 valid blocks or no runs; no crash.
- INV-008 Task 20 baseline = legacy 1.8.0 pre contracts only, same `len(reviewer_cards)` EV-1 rule on both sides, n stated.
