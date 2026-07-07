# QA Report — Task Integrity (Structure + Phase Ordering Lens)

**Topic:** Reflect Tier-2 fallback model ladder — MDTM task file
**Date:** 2026-07-06
**Phase:** task-integrity
**Lens:** phase-structure
**Fix authorization:** false (report-only)
**Fix cycle:** N/A

---

## Scope

Verifying task file STRUCTURE + PHASE ORDERING per 10-point lens focus:
1. YAML frontmatter completeness/well-formedness
2. Mandatory Template-02 sections present
3. Phase dependency logic + ordering (pure helpers → controller wiring; stub → real dispatch; HALT gates real dispatch)
4. Completion items terminal ordering / anti-orphaning
5. Task Log section present
6. Item count reasonable (94 items / 6 phases)
7. Open Questions documented (incl. T1-proxy HALT PENDING)
8. Phase 6 final gate = 7 agents (3 rf-qa + 3 rf-qa-qualitative + 1 domain) report-only + single fix agent
9. TB-Add-4: item-to-item deps form a DAG
10. POST reflect item = FLAT wrapper shell-out (guard-wrapped, exit-code-consuming)

Findings appended incrementally below.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | Read L1-62. Present + non-empty: `id`(L2), `title`(L3), `status`(L6), `created_date`/`updated_date`(L9-10), `spec_path`(L18), `start_commit`(L30, 40-char SHA `d8f84f71...` = current HEAD), `executor_model_class`(L32 "sonnet"), `reflect_post`(L27 empty w/ room-comment "written back by wrapper … leave room, do NOT hand-author"). Well-formed: nested `reflect_pre` map, inline comment on empty `reflect_post` string, `depends_on: []` all valid YAML. |
| 2 | Mandatory Template-02 sections present | PASS | Read: `## Task Overview`(L66), `## Key Objectives`(L72), `## Prerequisites & Dependencies`(L83), `## Execution Context`(L100, w/ References/Source Areas/Key Constraints/Handoff Convention/Frontmatter Protocol), `## Detailed Task Instructions`(L157, Phases 1-6), `## Post-Completion Actions`(L462), `## Task Log / Notes`(L474). |
| 3 | Phase dependency logic + ordering | FAIL | Macro-ordering correct (pure engine P1 → contract P2 → controller-wiring/stub P3 → swarm/openai_compat-gated P4 → HALT/real-dispatch P5 → docs/QA P6; HALT gates real dispatch after stub work). BUT internal-consistency defect: Step 1.5 mandates fallback.py "imports cleanly with no circular import" (only `._diversity`, swarm.models), while Step 3.4 defaults `stamp: Callable = _stamp_worker_paths` — and `_stamp_worker_paths` is defined in **ensemble.py:691** (grep-confirmed), reintroducing the ensemble↔fallback cycle Phase 1/Objective #1 exists to break. See Issue #1. |
| 4 | Completion items terminal order / anti-orphaning | PARTIAL/FAIL | Internal terminal order CORRECT: POST reflect wrapper penultimate (L470), Update-to-Done last (L472), and Done is gated on POST exit 0 ("ONLY if the POST reflect gate … returned exit 0"). BUT completion items live in a separate `## Post-Completion Actions` section (L462) rather than as the final gated steps of Phase 6 — the anti-orphaning concern the lens directs me to flag. See Issue #3. |
| 5 | Task Log section present at bottom | PASS | Read L474-548: `## Task Log / Notes 📋` with `### Task Summary`, `### Open Questions`, `### Execution Log`, per-phase Findings sections (P1-P6), `### Follow-Up Items Identified`, `### Deviations from Process`. |
| 6 | Item count reasonable (94 / 6 phases) | PASS | Counted `- [ ]` items: P1=23 (1.1-1.16 + 1.G1-1.G7), P2=14 (2.1-2.7 + 2.G1-2.G7), P3=16 (3.1-3.9 + 3.G1-3.G7), P4=15 (4.1-4.8 + 4.G1-4.G7), P5=6 (5.1-5.4 + 5.G1-5.G2), P6=15 (6.1 + 6.G1-6.G11 + 6.2-6.4), Post-Completion=5. Total=94. Matches claim; reasonable for 2 new + ~8 modified + ~9 test files across 6 QA-gated phases. |
| 7 | Open Questions documented (T1-proxy HALT PENDING) | PASS | Read L498-502: `### Open Questions` present with `[HUMAN-DECISION — T1 proxy binding, resolved in Phase 5 Step 5.1]` entry, "Status at build time: PENDING confirmation by Step 5.1", correctly noting stub work (P1-4) does not depend on it. |
| 8 | Phase 6 final gate = 7 report-only agents + 1 fix | PASS | Read L423-448: 6.G2/6.G3/6.G4 = 3× rf-qa (structural lenses), 6.G5/6.G6/6.G7 = 3× rf-qa-qualitative (content lenses), 6.G8 = 1× rf-qa (verdict-honesty DOMAIN lens) = 7 report-only (`fix_authorization: false`). 6.G9 consolidate → 6.G10 exactly ONE rf-qa `fix_authorization: true` (serialized per I20) → 6.G11 verification. |
| 9 | TB-Add-4: item-to-item deps form a DAG | PASS | All references point backward: QA-gate items consume same-phase impl outputs; fix agents consume consolidated findings; verification consumes fixes; `resolve_t1_fallback_factory` created (3.5) → openai_compat arm wired (4.4) → `_T1_PROXY_BINDING` set (5.2); `build_fallback_metadata` (2.1) & `select_contributing_set` (1.9) precede `run_fallback_ladder` (3.4). No back-edge/cycle found. |
| 10 | POST reflect = flat guard-wrapped exit-code wrapper | PASS | Read L470: `if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then … exit 0; fi; superclaude reflect run <taskfile> --depth deep --fix --promote` — emits NO `--base`/`--reflect`/`--max-turns`/range/agent-spawn token; consumes exit 0→proceed, 10/11/2→Blocked+HALT; wrapper writes `reflect_post` (not hand-authored); benign exit-11 judged via `return-contract.yaml`. Not a legacy self-run subagent or human-HALT form. |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 1.5 (L176) vs Step 3.4 (L296); Objective #1 (L76) | **Circular-import reintroduced — Phase 1's fix is incomplete.** Step 3.4 defines `run_fallback_ladder(… stamp: Callable = _stamp_worker_paths …)`. A module-level default is evaluated at fallback.py load time, so fallback.py must `from .ensemble import _stamp_worker_paths`. Grep confirms `_stamp_worker_paths` is defined in **ensemble.py:691**, and Step 3.6 makes ensemble.py import `run_fallback_ladder` from fallback.py → a genuine `ensemble ↔ fallback` cycle (partial-init ImportError as written). Phase 1 / Objective #1 extract ONLY the diversity helpers to `_diversity.py`; `_stamp_worker_paths` is NOT covered. Step 1.5 explicitly mandates fallback.py "imports cleanly with no circular import (helpers come from `._diversity`, not `.ensemble`)" — Step 3.4 contradicts it. (Note: the other two defaults are safe — `dispatch_wave1`=swarm/dispatch.py:334, `normalize_wave2`=swarm/normalize.py:508, both leaf modules.) | Extend Objective #1 / Step 1.4 to ALSO relocate `_stamp_worker_paths` to a neutral module (e.g. `_diversity.py` or a new `reflect/_seams.py`) that both ensemble.py and fallback.py import; OR change Step 3.4 to avoid a module-level ensemble import (e.g. `stamp: Callable \| None = None` + lazy `from .ensemble import _stamp_worker_paths` inside the function body). Update Step 1.5's clean-import mandate to reference the chosen neutral home. |
| 2 | IMPORTANT | Steps 2.6 (L254), 4.7 (L359), 5.1 (L392), 5.2/5.3 (L395/398), 6.1 (L416) vs Handoff Convention (L130-140) + Step 1.2 (L167) | **Handoff-directory path inconsistency — writes bypass the declared convention.** The Handoff File Convention places `reviews/`, `plans/`, `reports/` UNDER `phase-outputs/`, and Step 1.2 creates them only there. But these items write to `TASK-…/reviews/…`, `TASK-…/plans/…`, `TASK-…/reports/…` (directly under the task dir — grep-confirmed on L254/359/392/395/398/416), directories Step 1.2 never creates. Only Step 2.6 says "create the `reviews/` path … if needed"; 4.7/5.1/5.2/5.3/6.1 give no create instruction, and other plans files (e.g. 1.G6 `phase-outputs/plans/phase1-fix-verdict.md`, 5.G2 `phase-outputs/plans/phase5-fix-verdict.md`) use the phase-outputs form — so the two conventions coexist inconsistently. | Pick ONE home. Either (a) route all these to `phase-outputs/{reviews,plans,reports}/` to match Step 1.2 + the convention, or (b) add `reviews/`, `plans/`, `reports/` to the list Step 1.2 creates under the task dir AND update the Handoff File Convention block to document the task-dir homes. Make every writing item's path consistent with the chosen home. |
| 3 | IMPORTANT | `## Post-Completion Actions` (L462-472) | **Completion items in a separate section (anti-orphaning), per lens item 4.** The POST reflect gate + Update-to-Done sit under `## Post-Completion Actions`, outside the Phase 6 "YOU MUST complete EVERY item … IN ORDER" discipline header. Internal terminal order is correct (POST penultimate L470, Done last L472, Done gated on POST exit 0), and the items are executable `- [ ]` checkboxes reachable at end-of-file, so orphaning risk is moderate not severe — but the lens explicitly directs flagging the separate-section form. An executor that treats "Phase 6 complete" as task-complete could skip the independent POST audit. | Fold the 5 Post-Completion items into Phase 6 as its final gated steps (after 6.4), under the same "complete EVERY item IN ORDER" header, preserving POST-penultimate / Done-last order; OR add an explicit gating header to `## Post-Completion Actions` stating these are mandatory final gated steps that MUST run after Phase 6. |
| 4 | MINOR | Step 6.G9 (L444-445) | **Consolidation Glob over-matches on repeat cycles.** 6.G9 uses Glob `qa/qa-final-*.md` to gather "all seven final QA reports". But 6.G11 writes `qa-final-verification-structural.md` + `qa-final-verification-content.md`, and 6.G9 itself writes `qa-final-consolidated-findings.md` — all match `qa-final-*.md`. On a repeat 6.G9→6.G11 cycle the Glob folds the prior cycle's verification reports and consolidated file into the new consolidation (the "fewer than seven" guard won't catch over-matching). | Narrow the Glob to the 7 lens reports (e.g. `qa-final-structural-*.md`, `qa-final-content-*.md`, `qa-final-domain-*.md`) or enumerate the 7 filenames explicitly, excluding `qa-final-verification-*` and `qa-final-consolidated-findings`. |
| 5 | MINOR | Post-Completion item 3 (L468) vs template (L476) | **"Create" vs "fill in" redundancy.** L468 instructs "Create a `### Task Summary` section at the top of `## Task Log / Notes`", but the section already exists in the template scaffold (L476-496). Executor may create a duplicate `### Task Summary`. | Reword L468 to "Fill in the existing `### Task Summary` section (L476)" rather than "Create". |

---

## Confidence Gate

Checklist categorization (all 10 lens checks):
- [x] 1 Frontmatter — VERIFIED (Read L1-62)
- [x] 2 Sections — VERIFIED (Read, section headers cited)
- [x] 3 Phase ordering — VERIFIED (Read all phases + Bash grep for `_stamp_worker_paths`/`dispatch_wave1`/`normalize_wave2` definitions)
- [x] 4 Anti-orphaning — VERIFIED (Read L462-472)
- [x] 5 Task Log — VERIFIED (Read L474-548)
- [x] 6 Item count — VERIFIED (Read all phases + manual `- [ ]` count = 94)
- [x] 7 Open Questions — VERIFIED (Read L498-502)
- [x] 8 Phase 6 gate — VERIFIED (Read L423-448, enumerated 7 agents + fix)
- [x] 9 DAG — VERIFIED (Read, traced item-to-item edges)
- [x] 10 POST wrapper — VERIFIED (Read L470)

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 2 (both targeted greps for checks #3 and path-consistency)
- Note on tool minimum: the 5 Read calls are paginated reads of ONE large 548-line file (whole file covered), each span verifying multiple checks; 2 Bash greps independently verified check #3 (symbol home) and Issue #2 (path usage). No UNCHECKED or UNVERIFIABLE items.

---

## Summary

- Checks passed: 8 / 10 (checks 1, 2, 5, 6, 7, 8, 9, 10); checks 3 & 4 FAIL/PARTIAL
- Checks failed: 2 (check 3 phase-ordering internal-consistency; check 4 anti-orphaning)
- Issues found: 5 (CRITICAL: 1, IMPORTANT: 2, MINOR: 2)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Recommendations

Resolve Issue #1 (CRITICAL) before execution — as literally written, Step 3.4 produces an ImportError and negates Phase 1's headline circular-import fix. Resolve Issues #2 and #3 (IMPORTANT) to remove path ambiguity and the anti-orphaning risk. Issues #4/#5 (MINOR) are low-risk robustness/wording cleanups. All findings are report-only; a fix-authorized pass (or the task-builder) should apply them.

---

## Overall Verdict: FAIL

One CRITICAL internal-consistency defect (circular import reintroduced by Step 3.4, contradicting Step 1.5 / Objective #1) plus two IMPORTANT structural issues (handoff-path inconsistency; completion items orphaned in a separate section). Per zero-tolerance gating, any issue of any severity = FAIL. Structure and phase macro-ordering are otherwise sound (frontmatter complete, all Template-02 sections present, 94/6 item count accurate, Open Questions + T1-proxy HALT documented, Phase 6 7-agent gate correct, POST wrapper is the flat guard-wrapped exit-code form, DAG holds).

## QA Complete
