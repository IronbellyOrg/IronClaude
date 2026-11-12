# Reflect report: pre-execution, Tier 2, PARTIAL (plan as reviewed: NOT READY)

Plan reviewed: `.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md` (input tree sha256 da9fb1f7...a5b9, unchanged through Wave 5)
Spec: `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (sha256 54a8dce2...c4e45, pointed to by `source.md`)
Run: Tier 2 forced by `--tier 2`; 3 reviewers (sonnet, haiku-pinned, opus), per-card blind calibration, `/sc:adversarial` debate (3 advocates, 2 rounds, invariant probe), evidence-validator.

## Verdict

The plan as written has **6 blocking defects plus 2 more found by the invariant probe**. It should not go to `/sc:implement` unedited. Every defect has a small plan edit (list in `adversarial/refactor-plan.md`). No defect needs a change of design.

## Status and honest limits

- status: partial. Three individual citations failed the evidence check (no finding was dropped), and that forces partial by the protocol.
- Calibrator diversity is degraded: all three model classes were reviewers, so no disjoint calibrator class existed.
- Reviewer 2 was pinned to haiku but called itself "OpenAI ChatGPT": its model identity is unverified (`identity_mismatch_suspected`). The gateway maps pin names to other models, so no reviewer's class is proven. This is the same open question as spike S-ID in Task 14.
- The merge was run by the orchestrator session itself (diff analysis, scoring, merge written inline; advocates and probe were real agents). The skill's dedicated debate-orchestrator and merge-executor agents were not used.
- Reviewer 1's brief was truncated at line 343 of 426, so it read Tasks 1-11 only. The executor of the plan is unknown (`executor_class_resolved: false`).
- Tier 1 card calibrated 0.50 (self-reported 0.80); the card's "unmapped" claims for Cost and Risks were partly wrong (Risks 4, 5, 11 are covered by Tasks 14, 19, 20).

## Blocking findings (Grounded; all KEPT by the evidence-validator)

- C-001 Task 10's first acceptance line needs the packaged `@reflect-pre`, which only Task 11 creates (plan:135, 140). Fix: test with a temporary template in Task 10; move the packaged check to Task 11.
- C-003 Task 8 requires byte-identical resolution output, but `panel.py:520` writes `tiers_sha256 = sha256_json(tiers)` over the whole tier object and Task 9 adds `classes` to it (plan:113, 121, 126). Fix: freeze the old tier file as a test fixture for Task 8's golden; Task 9 adds its own golden for the new packaged hash.
- C-013 Constraints say "Never use Opus ... in any new template" (plan:26) while Task 11 requires `@reflect-pre` to resolve to Opus (plan:145-146; spec:235 allows it). Fix: reword the constraint.
- C-015 The spec lists "the lint test design" as a Stage 0 deliverable (spec:408); no Stage 0 task produces it (plan:97-102, 186-194). Fix: Task 6 writes `./artifacts/lint-test-design.md`.
- C-016 Task 20 finds shadow runs by `t2_engine_effective` in the manifest, but no task writes it there (plan:212, 222, 233, 247; spec:120). Fix: Task 17 `frozen` records requested and effective engine; Task 19 passes them and adds `panel_parity`, `anchor_replaced`.
- C-017 Task 20 does not run the contract lint that the Stage 2 exit requires (plan:247-250; spec:410). Fix: Task 20 runs `panel_lint` per shadow run.
- INV-001 (HIGH) No task calls `manifest advance` for the states after `clustered`, so `publish` cannot be reached (plan:212, 233). Fix: Task 19 names each `advance` call.
- INV-007 (HIGH) `panel_parity` is true by construction because the coordinator derives both sides (plan:233). Fix: define parity as equal ordered `(persona, model id)` lists and recompute it in the exit script from the legacy card headers and `panel/resolution.json`.

## Medium findings (warnings; all fixed in the refactor plan)

C-002 (Task 14 "clean git status" cannot pass in a dirty worktree), C-004 (`resolve` re-wraps `ExclusionExhausted` at `panel.py:489-496`), C-005 (profile validator wiring, `--sequence`, Fable class), C-006 (recorded cards have mixed severity words, `deviation_class`, no plan/spec path, markdown cards), C-007 (`cluster_v2` has no input for calibration), C-008 (`section` undefined for v2 fingerprint), C-009 (Task 7 dependencies; "five" exit items but four), C-012 (judge identity field unverified), C-014 (labels before Stage 1: record Stage 0 exit as PENDING), C-018 and C-019 (judge/calibrator filter; identity mismatch response), C-020 (second cluster pass after the validator), C-021 (probe cannot separate allowlist from refusal), C-023 (EV-1 "equals" should be "at least", plus loud-fallback branch), C-024 (legacy baseline includes shadow runs), C-025 (D3 effects must be limited to the `panel` engine), INV-002 to INV-006, INV-008.

## Minor and refuted

Minor: C-010, C-011, C-022, C-027, C-028. Refuted: C-026 (manifest publish vs audit.log; spec:363 requires the temp-file publish).

## Evidence gate

36 finding clusters checked, 0 dropped. 132 distinct citations checked, 3 failed: `spec:263` for the git-status claim in C-002 (it concerns the write probes), `SKILL.md:849-890` for the unparseable-YAML claim in C-028, and `spec:587-589` in reviewer 2's header. These were not used as support. `citations_dropped: 3`.

## Recommendation

Apply the edit list in `adversarial/refactor-plan.md` to the plan, then re-review the edited plan with a fresh reviewer (fix cycle 1 of 2). Run `/sc:implement` only if that re-review has no blocking finding.

## Outcome of the refactor loop (added after the review)

- Fix cycle 1: 55 exact-match edits applied to the plan (all 20 tasks kept). Independent re-review (opus, fresh context): FAIL, 3 new blocking findings (parity could not be recomputed from card headers, Task 4 wrongly said calibration has no per-finding map, Task 2 path source) plus 2 medium and 4 minor.
- Fix cycle 2: 14 more edits. Independent re-review 2 (opus, fresh context): **PASS, no blocking finding**. Edited plan saved as `artifacts/plan-after-refactor-2.md`; diffs in `artifacts/plan-refactor.diff` (whole refactor) and `artifacts/plan-refactor-2.diff` (cycle 2).
- Follow-up candidates (medium or minor, not fixed because mediums never trigger a fix pass; the implementer should handle them with the plan text as written, and the owner may want an issue):
  - M-1 Task 19/20: which file carries the shadow card header (`model:` line) is not named; the legacy cards have `model_class` written by the orchestrator and no `model:`. Name the legacy `reviewer-cards/` files as the source for Task 20's parity recompute and never derive `model_class` from `resolution.json`.
  - M-2 Task 19: the findings block is copied to `panel/cards/` at the normalize step (step 7) before blind calibration (step 8), so Task 12 would get uncalibrated cards. Copy after calibration, or append the calibration block afterwards.
  - M-3 Tasks 12/19: finding ids are reviewer-local; `kept-ids.txt` and the calibration join need `(reviewer_id, finding_id)`, and "kept ids" has no producer (the validator does not output a per-card kept list).
  - M-4 Tasks 15/19/20: in shadow, `reviewers_resolved` from the manifest may differ from the legacy rotation actually dispatched; the lint and Task 20 could then apply two different EV-1 counts.
  - M-5 Tasks 17/20: key path of `t2_engine_effective` in the manifest is not named.
- Not applicable: Wave 7 promotion (a pre run). Remediation (Tier 3) was not requested via `--remediate`; the plan was edited by the orchestrator on the user's instruction "refactor as necessary".
