# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** FR-RSR sc:reflect UC-2 reachability escalation MDTM tasklist
**Date:** 2026-06-20
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false (report only)
**Task file:** `.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/TASK-RF-uc2-reachability-20260620-025931.md`

---

## Items Reviewed

| # | Check (B2 lens) | Result | Evidence |
|---|-----------------|--------|----------|
| 1 | Every item has all B2 components (context/action/output/verification/completion gate) | PASS | 44/44 items carry context + action + output path + inline "ensuring…" verification + "mark this item as complete" gate (grep: 44/44 completion gates). |
| 2 | No item references prior-item context without restating it | PASS | Zero `see above`/`continue from previous` matches. Eval items 7.3–7.6 each RE-STATE `cases/post-small-diff-clean/` (4/4); 7.6 re-states `count-invariant-mechanism.md`. |
| 3 | Agent-spawning items (PG.2–PG.7, PG.9, PG.10) have FULLY EMBEDDED lens prompts | PASS | PG.2–PG.7 each carry a verbatim quoted adversarial lens prompt + named inputs + output verdict path; no "see SKILL.md" deferral. PG.9/PG.10 embed conditional logic + byte-exact monotonicity halt strings. |
| 4 | File paths specific; SKILL.md edit sites cite verified anchors | PASS | Re-verified vs live SKILL.md (1854 ln): §5.3 D13 :402, §6.1 step4 :463, §9.1 contract :663/:804/:1772, §10.8 :1014 / §10.9 insert :1025–1027, §17.7 item6 :1799, §9.4 :877, §0.5d :246, §9.2 :815, §5.3 row1 :390; reviewer-spec.md :25/:31/:43/:45/:47/:49; deviation-taxonomy.md :5/:56/:115/:117; pyproject :67–69. ALL match. |
| 5 | Verification criteria measurable (acceptance boxes + NFR + exit-0) | PASS | Verify items cite exact spec line ranges + 23 lettered (a)–(e) acceptance sub-criteria + named spec §6 NFR measurement methods + `make verify-sync` exit-0. No "verify it works" phrasing. |
| 6 | No batch items — 6 SKILL edits / new ref / 2 ref edits / 5 eval cases each its own item | PASS | 5 eval cases = 5 distinct items (7.2–7.6); 6 SKILL edits across 3.1/3.2/3.3/4.1/5.1/6.2; new ref = 2.1; 2 ref edits = 5.2 + 6.1; registry = 7.7. No item bundles >1 file-creation. |
| 7 | TB-Add-8: Context code-surface refs carry file:line OR evidence-absence | PASS | Every Context naming a code surface carries a research-anchored `file:line` citation; new-file/fixture items (2.1, 7.2–7.6) self-justify "create the new file". |
| 8 | TB-Add-1 (no TBD/TODO/FIXME, no title-only); TB-Add-7 (Source Areas reappear) | PASS | TBD/TODO/FIXME in item bodies = 0. No title-only items (38 `**Step**` headers each followed by full `- [ ]` body). All Source Areas reappear: runtime-surface.md ×23, reviewer-spec.md ×17, deviation-taxonomy.md ×15, evals.json ×14, coverage-mapping.md ×3, grader-extensions.md ×4, skill-snapshot ×5. |

(Detailed findings and verdict appended below.)

---

## Summary

- B2-lens checks passed: 8 / 8
- B2-lens checks failed: 0
- CRITICAL issues: 0
- IMPORTANT issues: 0
- MINOR / advisory observations: 2 (neither is a B2 self-containment defect)
- Issues fixed in-place: 0 (fix_authorization: false)

## Adversarial-Stance Disclosure

The spawn directive required hunting for ≥5 issues. I pursued that mandate hard:
re-verified every cited SKILL.md / refs / pyproject / spec / TDD anchor against the
live files, scanned for placeholder tokens, checked checkbox format, hunted for
cross-item context reliance, and hunted a field-name inconsistency
(`deviation_counts.regression` vs `deviation_count_by_class.regression`). Each
candidate defect was disproven by direct file evidence (see below). Per QA Principle 9
("a false PASS is worse than a false FAIL" — and equally, a manufactured FAIL is
dishonest), I am NOT inventing B2 defects that the evidence contradicts. The two
observations below are genuine but advisory; they are out of the B2 lens scope and do
not block the gate.

NOTE: my initial draft Items-Reviewed table pre-marked checks 5 and 8 as FAIL before
completing verification. Verification disproved both — they are PASS. The table above
reflects the verified result; this disclosure records the correction for audit honesty.

## Candidate Defects Investigated and DISPROVEN

| # | Hypothesis | Verification | Outcome |
|---|------------|--------------|---------|
| H1 | Verify items use vague "verify it works" (check 5 FAIL) | grep `verify it works\|ensure.*works$` = 0 matches; verify items cite spec line ranges + 23 lettered (a)–(e) boxes + exit-0 | DISPROVEN — measurable |
| H2 | Title-only / placeholder items (TB-Add-1 FAIL) | grep TBD/TODO/FIXME in bodies = 0; all 38 `**Step**` headers followed by full `- [ ]` body | DISPROVEN |
| H3 | Source Areas not echoed in item Contexts (TB-Add-7 FAIL) | All 7 Source Areas reappear in ≥1 item Context (counts in table row 8) | DISPROVEN |
| H4 | Field-name inconsistency: `deviation_counts.regression` (266/274) vs `deviation_count_by_class.regression` (×12) | `post-small-diff-clean/expected.yaml:6` uses `deviation_counts:` — the eval-oracle schema; contract uses `deviation_count_by_class`. Task uses the oracle form ONLY in eval-author items 7.2/7.4 and the contract form everywhere referencing SKILL.md | DISPROVEN — correct discrimination |
| H5 | Eval items 7.3–7.6 rely on 7.2 having read the template (cross-item context) | Each of 7.3/7.4/7.5/7.6 re-states `cases/post-small-diff-clean/` path; 7.6 re-states `count-invariant-mechanism.md` | DISPROVEN — self-contained |
| H6 | Anchor drift (line numbers stale vs live 1854-ln SKILL.md) | Every cited anchor re-Read and confirmed (table row 4) | DISPROVEN |

## Observations (advisory; NOT B2 defects, NOT gate-blocking)

| # | Severity | Location | Observation | Note |
|---|----------|----------|-------------|------|
| O1 | MINOR (advisory) | Steps 7.2/7.4 `expected.yaml` | The task instructs eval oracles to carry `runtime_surface_unreached` / `runtime_surface_degraded` / `deviation_counts.regression`. The `parse_yaml_simple` flat-key constraint (research 04 §3d) is correctly flagged in Step 7.1 for the *graded contract artifact* (`with_skill/outputs/contract.yaml`), but the `expected.yaml` ORACLE is a separate hand-authored file not subject to that constraint. The items keep these correctly separated. Advisory only: an executor should not conflate the oracle `expected.yaml` schema with the graded `contract.yaml` flat-key schema. The task already states this distinction in 7.1; no change needed. | Out of B2 lens scope (this is grader-mechanism clarity, not self-containment). |
| O2 | MINOR (advisory) | Step 7.1 | Step 7.1 is a "DECIDE and DOCUMENT" item whose primary concrete output is `plans/count-invariant-mechanism.md` (a decision record), with a *conditional* secondary action (extend grader.py only if scalar approach infeasible). It is self-contained (has context + action + output + verification + gate) and is NOT a standalone-context item — it produces a real artifact and gates a real decision. Advisory: this is the one item whose code-modifying action is conditional; an executor must record the chosen path explicitly so 7.6's count-invariant assertion has a defined target. The item already mandates this ("write this decision and the exact emitted-YAML artifact target path"). | Satisfies B2; flagged only because conditional-action items deserve executor attention. |

## Confidence Gate

**Step 1–4 computation (B2 lens = 8 checks):**

- [x] Check 1 VERIFIED — grep 44/44 completion gates; per-item structure read across all phases
- [x] Check 2 VERIFIED — grep `see above`/`previous item` = 0; 7.3–7.6 path-restatement confirmed
- [x] Check 3 VERIFIED — PG.2–PG.7 read directly; verbatim embedded lens prompts confirmed
- [x] Check 4 VERIFIED — every cited anchor re-Read against live files (Bash sed + grep)
- [x] Check 5 VERIFIED — verify-item prose read; lettered boxes + spec line ranges + exit-0 confirmed
- [x] Check 6 VERIFIED — item-to-deliverable mapping read across Phases 2–7
- [x] Check 7 VERIFIED — Context paragraphs read; file:line / new-file justification confirmed
- [x] Check 8 VERIFIED — grep TBD/TODO/FIXME = 0; Source-Area echo counts computed

TOTAL = 8 | VERIFIED = 8 | UNVERIFIABLE = 0 | UNCHECKED = 0
confidence = 8 / (8 - 0) * 100 = **100.0%**

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 7
  (Tool-engagement note: Grep-class verifications were executed inside Bash `grep`
  invocations rather than the Grep tool. Combined Read+Bash = 11 ≥ 8 checklist items;
  every Bash call mapped to a specific check — anchor verification, placeholder scan,
  Source-Area cross-validation, completion-gate count, field-name hunt.)
- No web research performed (all claims are local-source-truth; Tavily not required).

## Recommendations

- PASS — this task file is cleared on the B2 self-containment lens. No remediation required.
- Advisory for the executor (not a gate condition): treat Step 7.1's grader-mechanism
  decision as load-bearing for Steps 7.2/7.6 — record the chosen path (precomputed
  `count_invariant_holds` scalar vs grader extension) explicitly, since 7.6's
  count-invariant assertion target depends on it.

---

## VERDICT: PASS

All 8 B2 self-containment lens checks pass with 100% computed confidence. Every checklist
item is self-contained (context + action + output + inline verification + completion gate),
no item relies on un-restated prior-item context, all agent-spawning items embed their full
lens prompts, all file paths are specific, every cited SKILL.md / refs / spec / TDD / pyproject
anchor re-verified against the live files, no batch items, no placeholders, and all Execution
Context Source Areas reappear in item Contexts. Six candidate defects were hunted and
disproven by direct file evidence; two MINOR advisory observations are noted but are outside
the B2 lens and do not block the gate.

## QA Complete
