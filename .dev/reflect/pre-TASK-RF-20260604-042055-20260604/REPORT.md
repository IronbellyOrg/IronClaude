# Reflect REPORT — UC-1 Pre-Execution Coverage/Gap Audit

- **Mode:** pre (UC-1)
- **Tier reached:** 1 (single grounded pass; rubric default STOP — no regression candidate, single domain, coverage ≥ floor)
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md`
- **Driving spec (union):** `.dev/proposals/reflect-in-task-builder.md` (Proposal 1) + `.dev/proposals/reflect-in-sc-tasklist.md` (Proposal 2) + the in-scope S4 token-set trim
- **coverage_pct:** 0.97
- **best_practice_grade:** 5 / 5
- **calibrated confidence:** 0.88
- **Date:** 2026-06-04

---

## 1. Verdict

**PASS (signed-off).** The tasklist fully covers both driving proposals' required edit-sites plus the S4 trim, at research-verified current anchors, with a drift-guard, strictly-additive discipline, a targeted regression subset, and a correctly-structured dogfood POST gate. Coverage clears the 0.90 floor. Three refinement findings below are advisory — none blocks execution.

Notably, the tasklist is **more complete than the proposals' own surface summaries**: Step 3.6 catches FIVE stage-bookkeeping blocks the Proposal-2 §6 summary collapses into "10-stage table → 11 stages," and Step 3.8 catches two additional checkpoint-cadence literal locations beyond the four invariants. A naive single-surface edit would have shipped inconsistent stage bookkeeping; this tasklist will not.

---

## 2. Coverage Map (spec delta → tasklist item)

### Proposal 1 — task-builder (§8 implementer checklist + §5/§6)

| Spec delta | Tasklist item | Status |
|---|---|---|
| Add `--spec` to Input surface (§6.3, §8.1) | Step 2.1 | ✅ Grounded |
| A.2 `spec_path` resolution priority order (§6.3) | Step 2.2 | ✅ |
| New `### A.10.7` PRE reflect gate, after A.10.6 before A.11 (§6.1) | Step 2.3 | ✅ (task corrects the proposal's stale "between A.10.5 and A.11" to "after A.10.6") |
| Pipeline-overview bullet for PRE gate (§6.1) | Step 2.4 | ✅ |
| A.9 BUILD_REQUEST `POST_REFLECT_GATE` block (§6.2) | Step 2.5 | ✅ (API-004 byte-exact guard called out) |
| New Critical Rule #19 (companion to #16, MALFORMED-on-omission) (§6.2) | Step 2.6 | ✅ |
| Output Structure frontmatter `spec_path`/`reflect_pre`/`reflect_post` (§6.1/6.3) | Step 2.7 | ✅ |
| Penultimate POST reflect item in `Phase N` example (§6.2) | Step 2.8 | ✅ |
| Validation Checklist POST-reflect guard — G-1 plain-bullet path, rf-qa.md untouched (§7-risk-5, §8) | Steps 2.9, 2.10 | ✅ (correctly avoids INV-010/merge-test break) |
| A.11 `REFLECT GATES` block + multi-track per-track row (§6.5, §7-risk-6) | Step 2.11 | ✅ |
| New `## Reflect Depth (Deterministic TCS)` section: signal table, formula, thresholds, O1-O4 (§5) | Step 2.12 | ✅ (see Finding 3 re §5.4) |
| **S4 token-set trim** to `{after Phase \d+, depends_on:}` | Steps 2.12, 2.13 | ⚠️ Covered — **see Finding 1** |
| SoT sync + verify-sync + markdownlint | Steps 2.14, 2.15 | ✅ |

### Proposal 2 — sc-tasklist (§6 surface summary + §1/§4)

| Spec delta | Tasklist item | Status |
|---|---|---|
| `--no-reflect` flag — command Usage block (§6) | Step 3.1 | ✅ (`--spec` correctly NOT re-added) |
| `--no-reflect` flag — command Arguments table row (§6) | Step 3.2 | ✅ |
| `--no-reflect` flag — skill `argument-hint` frontmatter (§6) | Step 3.3 | ✅ |
| New `### Stage 10.5: Pre-Reflect Sign-off`, fenced after Stage 10 (§1a, Decision B2) | Step 3.4 | ✅ (race-safety rationale preserved) |
| 10-stage table → 11 stages (table row + lead sentence) (§6) | Step 3.5 | ✅ |
| Stage bookkeeping — 5 blocks (TaskCreate count, PROSE dep-chain, Dependencies, completion lines, Tool Usage) | Step 3.6 | ✅ **(exceeds §6 summary)** |
| Checkpoint-is-last 4-invariant amendment (#6/#18/#19/#20, amend together) (Decision C1, §6) | Step 3.7 | ✅ |
| Cadence rule + End-of-Phase Checkpoint template definition (additional literal locations) | Step 3.8 | ✅ **(exceeds §6 summary)** |
| Templated POST reflect task — SKILL.md inline §6B (Sprint-CLI metadata shape) (§1b) | Step 3.9 | ✅ (13-field table, 4 ACs, 2 Validation enumerated) |
| Templated POST reflect task — mirror `phase-template.md` (§1b) | Step 3.10 | ✅ |
| Per-phase `COMPLEXITY_SCORE` formula + thresholds + overrides, `multifile` dropped (§4) | Step 3.11 | ✅ |
| Index Pre-Reflect Sign-off column + `reflect_pre_summary` — SKILL.md inline §6A (§1a) | Step 3.12 | ✅ |
| Index Pre-Reflect Sign-off column — mirror `index-template.md` (§1a) | Step 3.13 | ✅ |
| `validation/reflect-pre/`, `reflect-post/`, `depth-map.yaml` convention (§4, §6) | Step 3.14 | ✅ |
| SoT sync + verify-sync + markdownlint (4 files) | Steps 3.15, 3.16 | ✅ |

### Verification / closure (both proposals)

Baseline capture (Step 1.3), anchor drift-guard re-verify (Step 1.4), regression subset (Steps 4.1-4.2), final consolidation + FINAL_ONLY adversarial rf-qa + rf-qa-qualitative (Steps 5.1-5.2), git-scope guard (Step 5.3), dogfood POST gate (Post-Completion). All present.

**Unmapped:** only the Proposal-1 §5.4 bounded-inference refinement (Finding 3) — ambiguous scope, not in the §8 checklist.

---

## 3. Findings (advisory — none blocking)

### Finding 1 — [MEDIUM · fidelity/drift] S4 trim is a substitution, presented as a subtraction

**Evidence:** Proposal 1 §5.1 S4 row (`.dev/proposals/reflect-in-task-builder.md:111`) defines the token set as `{after Phase \d+, blockedBy:, depends on N\.\d+, after N\.\d+}`. The task (`TASK-RF-20260604-042055.md:69`, Steps 2.12/2.13) writes the trimmed set as `{after Phase \d+, depends_on:}`, describing it as "dropping `blockedBy:` and `after N\.\d+` from the proposal's 4-token form, keeping `after Phase \d+` and `depends_on:`."

The proposal's third token is `depends on N\.\d+` (a prose regex matching "depends on 5.2"), **not** `depends_on:` (the YAML frontmatter key). The task therefore does not merely *subtract* two tokens — it also *substitutes* `depends on N\.\d+` → `depends_on:`. The substitution is arguably an improvement (`depends_on:` is a real emitted MDTM frontmatter key with corpus hits; the prose `depends on N\.\d+` is unlikely to appear in MDTM bodies), but it is characterized as a pure removal.

**Impact:** Internally the task is consistent — Step 2.12 writes exactly `{after Phase \d+, depends_on:}` and Step 2.13 greps for exactly those tokens, so the task passes its own gate. But the landed S4 row will contain a token (`depends_on:`) absent from the proposal's literal §5.1 text, and a downstream POST audit comparing the landed row against the proposal verbatim would flag it.

**Recommendation:** Add one clause to Step 2.12 stating the substitution explicitly, e.g. *"S4 retains `depends_on:` (the emitted MDTM frontmatter key) in place of the proposal's prose `depends on N\.\d+`, because the prose form is not emitted into MDTM bodies — a deliberate fidelity improvement, not just a trim."* This converts a silent divergence into an Authorized-and-documented one.

### Finding 2 — [LOW-MEDIUM · coverage, accepted limitation] Dogfood POST `--spec` covers Proposal 1 only

**Evidence:** The penultimate dogfood item (`TASK-RF-20260604-042055.md:336`) surfaces `/sc:reflect --mode post … --spec .dev/proposals/reflect-in-task-builder.md`. Reflect's `--spec` is single-path. All of Phase 3 (the ~14 Proposal-2 edits) thus has no driving-spec coverage in the POST gate's UC-2 coverage signal (the diff is still audited; only the spec-coverage dimension is Proposal-1-only).

The task handles this honestly: it names the second proposal in prose, cites research G-2, and notes neither proposal is materially larger (~279 vs ~297 lines), choosing the frontmatter-consistent primary. This is a reflect-surface limitation, not a tasklist defect.

**Recommendation (operator, at POST time):** run a second `/sc:reflect --mode post --spec .dev/proposals/reflect-in-sc-tasklist.md --diff <same range>` pass, or concatenate both proposals into one combined spec doc, so the Proposal-2 half also gets spec-coverage grading.

### Finding 3 — [LOW · coverage, ambiguous scope] §5.4 bounded ±4-TCS inference + `tcs_boundary_inference` field not explicitly required

**Evidence:** Step 2.12 requires "the signal table, the formula, the threshold table, and the overrides." Proposal 1 §5.4 (the bounded ±4-of-threshold S2 inference, recorded as `tcs_boundary_inference: {applied, from, to, reason}` in the sign-off block) is part of the proposal's TCS design but is **not** in the §8 implementer checklist and **not** named by Step 2.12. An executor reproducing only table+formula+thresholds+overrides would omit §5.4 and its audit field.

**Recommendation:** Make the omission a *decision*, not an accident — either (a) add §5.4's bounded-inference paragraph + the `tcs_boundary_inference` sign-off key to Step 2.12's required content, or (b) record in Step 2.12 that §5.4 is intentionally out-of-scope for the landed section (deterministic-core only).

---

## 4. Confirmed strengths (checked, not assumed)

- **Regression subset is a justified narrowing, not a gap.** The task narrows research-04 TABLE B's `tests/skills/ -q` to just `test_task_builder_merge.py`. Grounded check: `tests/skills/` contains only that file + an unrelated `test_repo_inventory_nongit.py`; every halt/verdict/INV-010/monotonicity test lives in `tests/audit/` (run wholesale). Nothing relevant is lost. `[Grounded: ls tests/skills/, grep tests/]`
- **sc-tasklist edits have zero test-text coupling.** No test text-reads `sc-tasklist-protocol/SKILL.md` (only `tests/sprint/test_checkpoints.py`, which is fixture-synthetic and never loads the repo templates — research-04 §2). The Stage-10.5 / 11-stage / COMPLEXITY_SCORE / invariant edits break no tests. `[Grounded: grep -rln tests/, research-04:131-138]`
- **G-1 path correctly avoids the INV-010/merge break.** Steps 2.9/2.10 add the POST-reflect guard as a plain SKILL.md validation-checklist bullet, NOT a structural `TB-Add-9` in `rf-qa.md` — keeping `rf-qa.md` untouched and the "28 items" heading stable (research-04 §1/§4). Break-risk = NONE. `[Grounded: research-04:200-240]`
- **Binding memories honored:** anti-orphaning (Done last), HALT-on-human-decision dogfood item with `reflect_post: PENDING` (`feedback_human_decision_items_must_halt`, `feedback_sc_reflect_vs_inline_rfqa`), ADVERSARIAL STANCE + `fix_authorization: true` on the FINAL rf-qa gate (`feedback_rfqa_adversarial_pattern`), `/task` never `/sc:task` (`feedback-no-sctask-on-task-builder-tasklists`), never-stage-`.claude/` git-scope guard.
- **Drift discipline:** Step 1.4 re-verifies every load-bearing anchor against the LIVE files before any edit, with the proposals' own admittedly-stale line numbers superseded by research anchors.

---

## 5. Grounding Gaps

None. All findings carry `file:line` evidence re-Read this run. No `[INFERRED]`-only load-bearing claims.

---

## 6. Recommendation

**Proceed to execution.** Optionally apply the one-line Step 2.12 clarification (Finding 1) and the Step 2.12 scope decision (Finding 3) first — both are ~1-line edits to this task file, not structural changes. Carry Finding 2 forward as operator awareness for the fresh-session POST run.
