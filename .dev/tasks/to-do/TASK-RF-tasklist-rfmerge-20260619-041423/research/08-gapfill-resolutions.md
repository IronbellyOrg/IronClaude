# Research: Gap-Fill Resolutions (A.8 research-gate gap-fill round 1)

**Topic type:** Gap-fill / orchestrator-resolved
**Status:** Complete
**Date:** 2026-06-19

> Resolves every finding raised by the A.8 partitioned research gate (10 agents). Each item is closed with
> the AUTHORITATIVE answer + a current-source or spec citation. Most were the zero-tolerance "any gap = FAIL"
> rule firing on items already answered by the driving spec; a few are bounded design pins made here. No
> re-research was required — every anchor was independently re-verified by the gate's evidence agents.

---

## R-1 [CRITICAL→RESOLVED] P3 `escalation_ladder_exhaust_point` vocabulary for the Stage-7 case (gap I-2)

**Finding:** the DM-003 `dedup_key` 2nd element must come from the closed vocab `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (forking it = HALT, `task-builder/SKILL.md` API-003 `API-003-exhaust-point-vocabulary-violation`). Research did not pin which value the Stage-7 case emits.

**RESOLUTION (design pin):** Stage 7's ladder is a SINGLE retry — `SKILL.md:1310` verbatim: *"Zero agent failures (if an agent fails, retry once before reporting error)."* Therefore the conformant exhaust-point for a Stage-7 validation agent that fails after its one retry is **`retry-1`** (the existing first vocabulary member). No vocabulary extension and no fork is needed — the Stage-7 single-retry ladder maps onto `retry-1` exactly. The `dedup_key` is `["<stage7_affected_task_range>", "retry-1"]`. (If a future change adds a second Stage-7 retry, `retry-2` is already available.) This keeps P3 conformant to the existing task-builder DM-003 contract verbatim.

## R-2 [MATERIAL CONTRADICTION→RESOLVED] P1 `## Execution Context` attachment SURFACE (cross-val A; completeness A)

**Finding:** R01 says per-task BODY (`SKILL.md:894-927`, mirror `phase-template.md:55-82`); R04 says INDEX-level (after `SKILL.md:707`). They cannot both ship.

**RESOLUTION (spec-authoritative — R01 is correct, R04's index placement is rejected):** The spec is explicit and binding:
- FR-RFMERGE.1 (`spec.md:174`): *"Generated phase **tasks** may carry an optional **task-level** `## Execution Context` block..."*
- §5.3 phase contract (`spec.md:585`): `emits: "optional ## Execution Context block on a phase task"`.
- The reused task-builder contract (`task-builder/SKILL.md:1066`) is a per-task-FILE body section.
→ **The block attaches to the per-phase-task BODY at Stage 4 (compute) / Stage 5 (render), anchored at `SKILL.md:894-927` (Phase File Template task body), with the source-side shape reflected in `templates/phase-template.md:55-82`.** It is NOT an index-level section. (P5 advisory, by contrast, IS index-level — see R-3; do not conflate the two surfaces.)

## R-3 [RESOLVED] P5 `## Tier Calibration Advisory` surface (confirmed, no contradiction)

**RESOLUTION:** P5 advisory is **index-level**, rendered at Stage 4, after `#### Feedback Collection Template` (`SKILL.md:820-839`, anchor ~`:839`). It reads `TASKLIST_ROOT/feedback-log.md` (`:86`, `:707`) read-only and MUST NOT mutate scored tiers (scored tiers stay a pure function of the roadmap; `SKILL.md:544-629`). Exact markdown table per `spec.md:344-350`. Min-2 matching overrides threshold; omit whole section otherwise. Ordered by ascending `T<PP>.<TT>`.

## R-4 [RESOLVED] P1 deterministic emission rule — commit to ONE rule (gap I-4)

**RESOLUTION (spec-authoritative, `spec.md:180-185` / §5.3):** The block is emitted at Stage 4 **iff the roadmap supplies ≥1 resolvable roadmap reference for that phase task**. When the roadmap supplies named "source areas", list them; when it does not, **degrade to a References-only form**. **Never** emit invented file paths; omit the block entirely when no roadmap reference resolves. Same roadmap → same block. Reuse the existing 4.1c resolve/None gate pattern (R04) rather than building a new roadmap-ref scanner.

## R-5 [RESOLVED] P4 `gate-results.txt` canonical line format — pin it (depth A; gap)

**RESOLUTION (spec-authoritative, `spec.md:304-310` FR-RFMERGE.4):** Plain UTF-8 text (NOT JSON), one check per line, then a trailing summary line. Exact format:
- per-check: `CHECK <n> PASS: <check description>` or `CHECK <n> FAIL: <offending task/file>` for checks 1–20.
- trailing: `GATE: PASS (20/20)` or `GATE: FAIL (<n> failing)`.
- Emitted to `TASKLIST_ROOT/validation/gate-results.txt` at the END of Stage 6, present **even on an all-pass gate** (it is a passthrough, not a failure log). Injected verbatim into the Stage-7 2N validation-agent prompts (inline prose block at `SKILL.md:1265-1286`, NOT `cli/tasklist/prompts.py`).

## R-6 [RESOLVED] 17-vs-20 stray + adjacent hygiene (unanimous across R01/R04/R07 + evidence agents)

**RESOLUTION:** `SKILL.md:1187` is correct ("check 1-20"); `SKILL.md:1597` stale-says *"Self-Check: all 17 checks passed"*. P4 work fixes `17`→`20` at `:1597` as a bounded, adjacent hygiene edit (do NOT rewrite unrelated text). The 20 checks = 8 Sprint-Compatibility (`:1136-1146`) + 4 Semantic (`:1149-1156`) + 8 Structural (`:1176-1185`).

## R-7 [RESOLVED] SKILL.md line count = 1631 (R01 off-by-one)

**RESOLUTION:** `wc -l` / `awk` / `od -c` all confirm **1631** lines (single trailing `\n`). R01's "cite 1632" is wrong; use **1631**. Interior anchors are unaffected (all verified correct).

## R-8 [RESOLVED] P2 Stage-10.5 NON-OVERLAP as a writable disjointness predicate (gap I-3)

**RESOLUTION:** Reduce R03's 3-lever argument to a testable predicate the builder encodes:
- **Predicate:** `set(P2_loop_findings) ∩ set(stage_10_5_reflect_pre_findings) == ∅`, where `P2_loop_findings` are the Stage-7 QA `F_k` findings re-run inside the Stages 7→9→10 bounded loop, and `stage_10_5_reflect_pre_findings` are the spec-coverage gaps produced by the per-phase `/sc:reflect --mode pre` fan-out (post-Stage-10, `SKILL.md:1460-1481`).
- **Three independent disjointness levers** (each separately sufficient): (1) different STAGE (loop confined to 7→10, fenced before 10.5 at `SKILL.md:1462`); (2) different FINDING-SOURCE (QA-gate validation findings vs reflect spec-coverage gaps); (3) different REMEDIATION OWNERSHIP (P2 re-patches via `sc:task`; Stage 10.5 reflect only AUTHORS/offers remediation, never auto-mutates phase files). The non-overlap test asserts the predicate on a fixture where both surfaces produce findings.

## R-9 [RESOLVED] P5 determinism test — avoid the whole-bundle `==` trap (gap IMPORTANT-2)

**RESOLUTION (spec NFR-RFMERGE.1, `spec.md:627`):** The advisory section legitimately VARIES with `feedback-log.md`, so a naive whole-bundle `==` test would false-RED (or pressure weakening P5). The determinism test MUST assert on the **scored-tier slice only**: "same roadmap → identical scored tiers (independent of `feedback-log.md`)". Separately assert "same roadmap + same `feedback-log.md` → identical advisory". Never assert whole-bundle byte-equality across differing feedback logs.

## R-10 [RESOLVED] Missing stay-green integration suites (gap IMPORTANT-1)

**RESOLUTION:** Add the two retained-feature audit suites the spec/TDD require stay green (`spec.md:677`, `tdd.md:865`): `tests/audit/test_inherited_verdict_freshness_inv_002.py` and `tests/audit/test_five_axes_overlay.py`, plus `tests/skills/test_task_builder_merge.py` (PR-01..PR-07) and `tests/cli/test_verify_sync_hooks.py` (V1-V7). Full stay-green set the implementation must not regress:
`uv run pytest tests/tasklist/ -v`; `uv run pytest tests/tasklist/test_prd_cli.py tests/tasklist/test_prd_prompts.py tests/tasklist/test_autowire.py -v`; `uv run pytest tests/cli/reflect/ -v`; `uv run pytest tests/skills/test_task_builder_merge.py -v`; `uv run pytest tests/audit/test_inherited_verdict_freshness_inv_002.py tests/audit/test_five_axes_overlay.py -v`; `uv run pytest tests/cli/test_verify_sync_hooks.py -v`.

## R-11 [RESOLVED] M4 source-fidelity gate applicability for the BUILDER's own task file (gap IMPORTANT-3)

**RESOLUTION (design pin):** This task READS the spec/PRD/TDD (a different format) and the generated tasklist transforms that release intent into an implementation MDTM tasklist → per MDTM I21 (transform of source material into a different format) **M4 source-fidelity is APPLICABLE to the build's own QA**. The task-builder pipeline already runs A.10.25 research-alignment + A.10.5 qualitative as the fidelity surface for the generated tasklist; additionally, the GENERATED tasklist's own per-phase QA gates need NOT each carry an M4 fidelity gate (the per-proposal phases produce code/tests, not source-transformation documents) EXCEPT where a phase emits a >500-line document — none is expected. Net: M4 is satisfied by the task-builder's own A.10.25/A.10.5 gates; per-phase QA gates in the generated tasklist use M3 lens-based sequences sized per I19/I22 (full intensity).

## R-12 [RESOLVED] Stale-token-prevention test set + `/config/.claude` (gap MINOR-2)

**RESOLUTION:** The stale-token-prevention test asserts NONE of these appear as an operative edit target / current guidance in changed source or generated output: `sc:task-unified`, `/rf:`, `.gfdoc`, `llm-workflows`, `/config/.claude`. Confirmed absent today from `src/superclaude/skills/sc-tasklist-protocol/` (grep: 0 hits for `/config/.claude`; `sc:task-unified` and `llm-workflows` and typed `StageError` are 0 hits repo-wide in operative code). Model the test on `tests/cli/prd/test_prompts.py` staleness assertions.

## R-13 [RESOLVED / carried] `--spec §22` settlement (re-affirm; precise anchor)

**RESOLUTION:** Settled exactly as R07 drafted. The `--spec` contract item lives in **spec §5.1 / §11 "Autowire-vs-roadmap-only"** (`spec.md:553-558,755`) — the "§22" label in the prompt refers to the TDD's §22 Open-Questions region but the substantive contradiction text is spec §5.1. Two parts:
1. **Bounded, behavior-preserving doc-consistency edit** to `SKILL.md:49-57`: reframe the roadmap as the PRIMARY source and `--spec`/autowired TDD/PRD as OPTIONAL supplementary inputs (the behavior already supports `--spec` at 4 sites: `:169-182`, `:246-267`, `:1297-1308`, `:1466-1471`; `argument-hint` `:9` advertises it). Changes NO runtime behavior/flags/algorithm. Use R07's verbatim replacement text.
2. **Residual Open Question (`needs_human_decision`, MUST HALT — do NOT auto-apply):** whether the maintainer instead wants to REMOVE `--spec` enrichment to make the generator genuinely roadmap-only (a larger behavior change, out of P1-P5 scope). The generated tasklist records this as a halting human-decision item, never auto-applies removal.

## R-14 [RESOLVED] Tier-classification mirror (`rules/tier-classification.md`) + sync discipline

**RESOLUTION:** The tier algorithm exists in BOTH `SKILL.md` (authoritative inline) and `rules/tier-classification.md` (human-review mirror). P5 advisory does NOT change scored tiers, so neither needs algorithm edits for P5. For any P1-P5 edit that changes `SKILL.md` prose reflected in a source-side reference (`templates/phase-template.md` for P1 shape; `rules/file-emission-rules.md` is known mirror-lagged — respect, do not propagate), update the source-side reference in `src/superclaude/...`, then run `make sync-dev` + `make verify-sync` (regenerates `.claude/` mirrors; NEVER stage `.claude/{skills,commands,agents,hooks,templates}`).

## R-15 [RESOLVED] gate-results.txt vs Stage-6 write-atomicity (gap I-7)

**RESOLUTION:** `SKILL.md:1195` requires the full in-memory bundle to pass Self-Check before ANY `Write()`. `gate-results.txt` is a VALIDATION-evidence artifact under `TASKLIST_ROOT/validation/`, emitted as part of/after the Stage-6 gate result — it is consistent with write-atomicity because it is written alongside the validated bundle (it serializes the gate that just ran), not a partial pre-validation write. The builder emits it within the Stage-6 completion, after the gate verdict is computed, before Stage-7 consumes it.

## R-16 [RESOLVED, cosmetic] DM-003 field count framing

**RESOLUTION:** The DM-003 emission record has **7 named YAML fields** (`severity`, `source`, `affected_range`, `evidence`, `recommendation`, `dedup_key`, `found_n_times`); the occasional "8 fields" framing counts the 2-element `dedup_key` tuple as two. Use "7 named fields; `dedup_key` is a 2-element list" to avoid ambiguity (`task-builder/SKILL.md:877-883`).

---

## Summary

16 findings resolved: 1 was CRITICAL (R-1 P3 exhaust-point → `retry-1`), 1 a material contradiction (R-2 P1 = task-body per spec). The remaining 13 were spec-authoritative confirmations or bounded design pins. No item required re-research; all anchors were independently re-verified by the gate's own evidence agents. The build may proceed to A.9 with these resolutions folded into the BUILD_REQUEST.
