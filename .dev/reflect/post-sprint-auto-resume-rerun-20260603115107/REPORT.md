# Reflection Report — UC-2 Promotion Re-Run (v4.3.5 Sprint Auto-Resume)

**Skill:** `/sc:reflect --mode post` · **Mode:** UC-2 · **Date:** 2026-06-03
**Subject:** TASK-RF-20260602-sprint-auto-resume (re-run after TASK-RF-20260603-sprint-resume-remediation)
**Tier reached:** 2 (rubric rule 4 — S_domains = code+tests+docs = 3) · **Status:** `partial`
**Promotion:** **BLOCKED** (`promotion_action: skipped`, `skip_reason: gate-failed`, condition 4)
**Output:** `.dev/reflect/post-sprint-auto-resume-rerun-20260603115107/`

## Method (heterogeneous ensemble — the value-add)

Two independent reviewers on **disjoint model classes from disjoint vendors** measured the remediated
work against the (now-amended) spec, blind to the remediation narrative; the executor class (opus) was
excluded from the reviewer pool per §7.1.

- Reviewer A — `sonnet`=gpt-5.5 (OpenAI-compat), analyzer persona → all 4 prior findings resolved/authorized, **+1 NEW regression** (`--yes` path skips plan/paths print). `recommend: no`.
- Reviewer B — `haiku`=qwen3.6-plus (Qwen), QA persona → all 4 resolved, tests non-vacuous (21/21), no new deviations. `recommend: yes`.

`t2_model_class_diversity: full` · `t2_vendor_diversity: multi`. The reviewers **disagreed**, and the
disagreement is the finding: Reviewer B audited the test suite and code-level fixes; Reviewer A also
audited the spec's visible-by-default UX control flow and caught a gap B did not probe. The orchestrator
**independently re-verified** Reviewer A's claim against `commands.py:436-471` + `design.md §7` + AC-1/FR-4.2
before weighting it. This is the protocol's core thesis in action — a single-agent (or test-focused) pass
confirmed the work; a spec-grounded independent reviewer did not.

## The four prior blockers — RESOLVED / AUTHORIZED

| Prior finding | Status now | Class | Evidence (independently verified) |
|---------------|-----------|-------|-----------------------------------|
| **F-3** drift mis-classifies same-ID material edits (was Regression) | ✅ RESOLVED | — | `drift.py:177-219` WS-hash-gated fall-through (0.9 only on WS match, else 0.5/`cosmetic_only=False`); `_annotate_git` never sets confidence (`drift.py:260-306`, NFR-3). CG-2 `test_drift_same_id_material_body_edit_low_conf` GREEN; AC-4/AC-5 non-regressed. |
| **F-2** partial paths not surfaced (was Drift) | ✅ RESOLVED | — | `models.py:111` `BoundaryReport.partial_paths`; `integrity.py:71` assigned inside `if partial_paths:` independent of `cleanup_opted_in`; `commands.py:538-539` prints. Not a term in `_verdict` (`integrity.py:329-336`, NFR-3). CG-1 GREEN. |
| **F-4** PHASE hard-crash skips prior-tail validation (was coverage gap) | ✅ RESOLVED | — | `BoundaryTask.phase` (models.py); planner `_emit_prior_tail_boundary` write-free (`planner.py:182-229`); integrity resolves transcript+deliverables under `lc.phase` (`integrity.py:120,138-145`). CG-3 positive + negative GREEN (negative genuinely STOPs). |
| **F-1 / CG-4** spec self-contradiction (was needs_human_decision) | ✅ AUTHORIZED | Authorized | Operator ruled **YES** (Ryan W, 2026-06-02). design §4(c):221 conjunct re-worded; merged-req FR-2.4:88 clarified; §7 + `_verdict` unchanged. Spec now self-consistent for the GATE verdict. |

Both reviewers + the orchestrator concur on all four. `tasklist_completion_pct: 1.0` (31/31). All 21 deterministic
resume tests + 7 e2e_real resume tests pass; full sprint suite collects 1094 tests / 0 errors (the
`invoke_haiku` collection errors were fixed in the preceding task).

## Blocking finding — NEW-R1 (Regression)

### `--yes`/CI proceed path does not print the inferred plan or partial-work paths · **Regression** · HIGH

- **Grounded (orchestrator-verified):** `_auto_resume` (`commands.py:436-471`) prints via `_print_resume_decision` ONLY inside the `if not assume_yes:` interactive-TTY branch (`commands.py:441`). When `assume_yes` is set (`--yes`, `SUPERCLAUDE_SPRINT_ASSUME_YES`, or `CI=1`), it returns `action="proceed"` directly at `commands.py:469-471` with **no plan print and no partial-paths print**.
- **Spec basis (contradicted):**
  - **AC-1** (`merged-requirements.md:143-144`): "bare `sprint run <index>` resumes at phase 3, **prints the plan**."
  - **FR-4.2** (`:117-122`) + **G5** (`:44`): default = "detect → **print inferred plan** → proceed"; "visible-by-default UX."
  - **design §7** (`design.md:345-346`) — the sequence the CG-4 YES ruling declared GOVERNING: `print_plan(...)` THEN `prompt (skipped: --yes / interactive assent)`. The plan prints unconditionally; only the *confirm* is skipped under `--yes`. The code skips BOTH.
- **CG-4 linkage (why this matters now):** the CG-4 YES ruling's defensibility rests on `--yes` being *informed* — its amended FR-2.4 clause is "`--yes` + **a printed partial-paths report** == explicitly assessed-and-accepted." On the `--yes`/CI path the partial-paths report is **not printed** (F-2's printer is bypassed), so the YES ruling's own informedness precondition is unmet on the very path "auto-resume as default" targets. The prior remediation's `f2-yes-ci-residual.md` leniently read this as "`--yes` intentionally proceeds" — but design §7 + AC-1 require the plan/paths to print even when the confirm is skipped.
- **Provenance note:** this behavior is pre-existing (the original auto-resume control flow), not introduced by the remediation. Under §10.4 the taxonomy classifies by spec-contradiction, not provenance — it is a Regression-class deviation against AC-1/§7/FR-4.2. The original audit folded it into F-1's "Necessary deviation + residual gap"; under the YES amendment it sharpens into a concrete AC contradiction.
- **Adjudication:** Regression (contradicts AC-1 acceptance criterion + governing §7 sequence). Forces §5.3-rule-3 escalation (satisfied — Tier 2 ran) and blocks promotion condition 4.

## Verdict

**Status: `partial`.** The remediation cleanly closed F-2/F-3/F-4 and the CG-4 spec reconciliation is sound.
But the F-1 closure is **incomplete**: the `--yes`/CI proceed path does not realize the visible-by-default
"print the plan/paths" contract (AC-1, FR-4.2, design §7), leaving the YES ruling's informedness premise
unmet on the unattended path.

```
deviation_count_by_class: { authorized: 1 (F-1 via CG-4 YES), necessary: 0, drift: 0, regression: 1 (NEW-R1) }
coverage_gaps: 0 new    citations_dropped: 0    needs_human_decision: false
regression_present: true (NEW-R1)
```

## Promotion decision (Wave 7)

**BLOCKED — `promotion_action: skipped`, `skip_reason: gate-failed`.** §14.5.2 condition 4
(`deviation_count_by_class.regression == 0`) fails (regression == 1). Conditions 1, 2 (status≠success),
3, 5a, 5b, 7, 8, 9 are otherwise satisfiable; condition 2 also fails because `status: partial`. The task
folder is NOT moved to `.dev/tasks/done/`.

**Conditions cleared by the remediation:** condition 8 (`needs_human_decision == false`) is now ✅ (CG-4
ruled). The F-3 regression and F-2 drift that blocked condition 4 at the original audit are ✅ fixed. The
**only** remaining blocker is NEW-R1.

## Remediation recommendation (specific, small)

Make the `--yes`/CI proceed path realize design §7's "print_plan then prompt(skipped)" sequence:

- In `_auto_resume` (`commands.py`), before returning `action="proceed"` at `:469-471`, call
  `_print_resume_decision(ResumeDecision(plan=plan, drift=drift, report=report, action="proceed"))` so the
  inferred plan + `report.partial_paths` print on the `--yes`/CI path (skip only the `click.confirm`).
- Add a non-interactive AC test: bare `sprint run` with `assume_yes` prints the plan + partial paths
  (asserts `phase-3-task-...-output.txt` and the plan header appear in output on the proceed path).
- Then re-run this promotion; with regression → 0 and status → success, all 9 conditions clear.

This is a ~3-line code change + 1 test. Reflect does NOT auto-fix (it surfaces); the operator applies it.

## Evidence-validator note

All load-bearing citations (`commands.py:436-471`, `design.md §7:345-346`, `merged-requirements.md
AC-1:143-144 / FR-4.2:117-122 / G5:44`, `integrity.py:_verdict`, `models.py:111`, `drift.py:177-219`,
`planner.py:182-229`) were Read this session by the orchestrator and/or corroborated across both reviewers.
`citations_dropped: 0`; the pass is non-vacuous (independent reviewer found a real, verified gap).
