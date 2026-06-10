# sc:reflect — UC-1 Pre-Execution Audit (REPORT)

- **Mode:** pre (UC-1 coverage/gap audit)
- **Depth:** deep → Tier 2 (3 heterogeneous reviewers + blind calibration + evidence-validator gate)
- **Spec:** `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md`
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-reflect-wrapper-autofix-20260610-053000/TASK-RF-reflect-wrapper-autofix-20260610-053000.md`
- **Tier reached:** 2
- **Calibrated confidence:** 0.89
- **coverage_pct (requirements covered by intended steps):** 0.92
- **best_practice_grade:** 4 / 5
- **Citations:** total 12 · dropped 0 · inferred 2 (G3 companion-coordination, G5 frontmatter-consumption — tagged `[INFERRED]`)
- **Verdict:** **PROCEED WITH CHANGES** — requirement coverage is high and the research grounding is excellent, but there is **one HIGH-severity executability blocker (F1)** that makes Phase 1 unexecutable as written, plus two MED design/conformance issues. Fix F1 before execution; address F2/F3 in the same pass.

> **Headline:** The plan is well-built and almost completely covers the spec — but it cannot run. Phase 1.3 branches the work off `origin/master`, which **does not contain the reflect CLI at all**. Every edit phase (2–7) then operates on files that do not exist. This is the single thing that must change before `/task`.

---

## 1. Critical Findings (must resolve before execution)

### F1 — Base acquisition is structurally impossible (HIGH) 🔴

**Claim:** Phase 1 cannot produce the "canonical audit-only base." Step 1.3 runs
`git checkout -b feat/reflect-wrapper-autofix origin/master`, but the reflect CLI does not exist on `origin/master`.

**Grounded evidence (independently re-verified by the orchestrator, not reviewer-reported):**
- `git ls-tree origin/master -- src/superclaude/cli/reflect/` → **empty**. `origin/master` (`1b0264f1`) has `audit/`, `cleanup_audit/`, `roadmap/`, `sprint/`, `tasklist/`… but **no `reflect/` package** and **no reflect registration in `main.py`**.
- The audit-only base exists **only as uncommitted/staged working-tree changes** in worktree `wrapper-onto-master` (branch `feat/reflect-wrapper-onto-master`, HEAD `e97aa4fd`): `git ls-tree HEAD -- src/superclaude/cli/reflect/` is **empty** there too, and `git status` shows every reflect file as `A`/`AM` (staged, never committed). There is **no branchable commit** that contains these files.
- Tasklist Step 1.3 (`…TASK….md:163`), Step 1.4 (`…:167`).

**Consequence:** A fresh branch off `origin/master` contains zero of the five `cli/reflect/*.py` files, zero `tests/cli/reflect/` files, and an unregistered `main.py`. Step 1.4 finds **all files MISSING**; Steps 2.1/2.2/3.1/4.1/4.3 then "Read" non-existent files. Phases 2–7 cannot proceed.

**Aggravating — the guards mask the failure rather than HALT:**
- Step 1.3 failure clause (`…:163`): "If … `git checkout -b` fails, log the specific blocker … **then mark this item complete**."
- Step 1.4 failure clause (`…:167`): "If any expected file is missing … log the specific blocker … **then mark this item complete**."
- Phase Gate PG1.2 (`…:181`) *would* flag MISSING as CRITICAL, but PG1.3 (`…:185`) caps remediation at 2 cycles whose only prescribed fix is "re-create the branch off `origin/master`" — which **reproduces the empty base**. No step instructs obtaining the files from `wrapper-onto-master`.

**Suggested fix (pick one, in safety order):**
1. **Commit the staged reflect work in `wrapper-onto-master` first** (it currently has no SHA to branch from), then `git checkout -b feat/reflect-wrapper-autofix <that-commit>`.
2. Branch off `origin/master`, then import the tree: `git checkout e97aa4fd -- src/superclaude/cli/reflect/ tests/cli/reflect/ src/superclaude/cli/main.py` (note: this pulls the *committed* HEAD tree, which is also empty of reflect — so option 1 is strictly required first, OR checkout from the working tree / a stash).
3. Branch directly off `feat/reflect-wrapper-onto-master` after committing its staged work; do **not** root off `origin/master`.

Additionally: change Step 1.4's MISSING-file branch and Step 1.3's checkout-fail branch from "mark complete" to a **true HALT** (a missing base is not a loggable-and-continue condition).

> Note: this finding does **not** indict the research. All R1/R2/R3 file:line anchors were spot-checked against the files where they physically live (`wrapper-onto-master`) and **every anchor MATCHED** (see Anchor Verification, §4). The defect is solely the *base-acquisition premise*, not the per-file change points.

---

## 2. Material Findings (resolve in the same pre-execution pass)

### F2 — Apply-step return code is discarded; a failed `/task` apply is treated as a completed cycle (MED) 🟠

**Claim:** Step 4.5's loop calls `self._apply_remediation(remediation_task_path)` then increments `iteration` and re-audits, but never inspects the `rc`. Step 4.4 explicitly defines `_apply_remediation(self, …) -> int` (returns the rc), so the value exists and is dropped.

**Evidence:** Step 4.4 (`…:283-285`), Step 4.5 (`…:287-289`), FR-3 bound (`merged-requirements.md:107-111`).

**Why it matters:** If `/task <remediation>` fails (`rc != 0`), the wrapper still proceeds to re-audit and re-classify against whatever partial state the failed apply left behind. Termination is still *bounded* (the `max` cap holds), but the **state transition is semantically wrong** — an apply subprocess failure should fail-closed to a terminal HALT/BLOCKED, not be treated like a successful repair cycle. For a fail-closed wrapper this is a real hole.

**Suggested fix:** In Step 4.5, require `apply_rc == 0` before incrementing `fix_iterations`/re-auditing; on `rc != 0`, terminate fail-closed (surface the apply stdout/stderr path). Add a Step-6.5 test: `auto-fixable` + `remediation_task_path` present + apply `rc != 0` → terminal, no further audit.

### F3 — FR-5 ownership contradiction: spec says the *wrapper* forces O2 `--no-promote`; tasklist defers it to the *generator* (MED) 🟠

**Claim:** The spec and the tasklist disagree on who guarantees O2 never promotes.

**Evidence (both re-Read by the orchestrator):**
- Spec FR-5 (`merged-requirements.md:129-130`): "**O2 (per-phase): the wrapper forces `--no-promote`**."
- Tasklist U6 (`…:139`): "**NO wrapper-side O2 force** — the only wrapper-side D5 change is the default flip." Step 3.2 (`…:233-235`) implements only the default flip and explicitly forbids wrapper-side O2 detection. Contract §2/§5 puts `--no-promote` in the *generator's* O2 invocation shape.

**Why it matters:** Because `--promote` default flips to **True** (Step 3.2) and there is no per-phase adapter, FR-5's "per-phase gates do NOT promote" guarantee now rests **entirely on the generator remembering to pass `--no-promote`**. If any O2 caller omits it, the wrapper promotes-by-default with no adapter — a fail-*open* path for the exact case FR-5 wanted closed. The tasklist's resolution (U6) is internally coherent with the contract, but it silently overrides the literal FR-5 requirement.

**Suggested fix:** Make the override explicit. Either (a) reconcile the spec — change FR-5 wording to "the generator emits `--no-promote` for O2; the wrapper does not auto-detect," and record it as an authorized spec amendment; or (b) add a thin wrapper-side guard that fails-closed when promote is requested at a scope with no adapter. Decision belongs to the spec owner — surface, don't silently proceed.

---

## 3. Coverage Map (FR / NFR / AC → tasklist steps)

Requirement coverage by *intended* steps is high (**20 COVERED, 4 PARTIAL of 24 = 0.917**). Note this measures intent-to-cover; F1 means none of it executes until the base defect is fixed.

| Req | Covering step(s) | Status | Note |
|-----|------------------|--------|------|
| FR-1 auto-fix loop | 3.1, 4.5, 4.6, 6.5 | COVERED | |
| FR-2 recursion breaker | 3.3, 4.4, 6.3 | COVERED | marker guard + exact-"1" + negative controls |
| FR-3 bounded loop | 3.1, 4.5, 4.6, 6.5 | COVERED | but see F2 (apply-rc) |
| FR-4 safe-class carve-out | 4.1, 4.5, 6.4 | COVERED | classifier ordering sound (human wins) |
| FR-5 promote flip + scope | 3.2, 6.6, 7.3 | COVERED* | *see F3 ownership contradiction |
| FR-6 per-phase base | 2.2, 2.3, 3.1, 3.4, 6.7 | COVERED | precedence + de-range tested |
| FR-7 depth passthrough | 3.1, 6.9, 7.2 | COVERED | |
| FR-8 remediation_task_path field | 4.2, 5.1, 5.2, 5.4, 6.1 | COVERED | |
| FR-9 headless --remediate | 5.3 | COVERED | signal pinned as TTY-absence under `--print` (G6) |
| FR-10 preserve v1 fail-closed | 4.5, 6.5, 7.1, 7.3 | COVERED | |
| NFR-1 thinness | 4.1, 4.4, 6.8 | COVERED | guards anchored to dodge docstring FPs |
| NFR-2 bounded cost | 3.1, 4.5 | PARTIAL | G4: no step verifies the contract cost-band doc (§7) survives |
| NFR-3 termination | 3.3, 4.5, 6.3, 6.5 | COVERED | |
| NFR-4 idempotent re-verify | 4.5, 6.7 | COVERED | same `--base` reused per iteration |
| NFR-5 land-before-generators | 7.2 | PARTIAL | G3: pipx verified locally; no step coordinates/holds the companion `ReflectInTaskLists` worktree |
| AC-1 marker self-suppress | 6.3 | COVERED | |
| AC-2 drift→autofix→converge | 6.5 | COVERED | |
| AC-3 human-required HALT | 6.4, 6.5 | COVERED | |
| AC-4 non-convergence | 6.5 | COVERED | call-count arithmetic pinned |
| AC-5 O1 promote / O2 no-promote | 6.6, 7.3 | COVERED* | flag-plumbing tested (not a dir-move) |
| AC-6 base precedence / de-range | 6.7 | COVERED | |
| AC-7 emit+read remediation_task_path | 4.2, 5.1, 5.2, 6.1 | PARTIAL | G2: no dedicated emit↔read byte-for-byte test in 6.3–6.8 (deferred to PG5.3 QA) |
| AC-8 thinness + pipx | 6.8, 7.2 | COVERED | |
| AC-9 v1 fail-closed tests green | 7.1 (full suite) | PARTIAL | G1: PG6.1 AC→test mapping says "AC-1..AC-8", omitting AC-9; covered operationally by the full-suite run, not in the mapping table |

### Lower-severity gaps (traceability, not missing coverage)
- **G1 (MED→calibrated MED):** PG6.1 (`…:403`) and Step 6.9 (`…:397`) map/name only **AC-1..AC-8**. AC-9 ("all v1 fail-closed tests remain green") is covered *operationally* by the full-suite `uv run pytest tests/cli/reflect/` in 6.9/7.1, but is absent from the explicit AC→test mapping. Add AC-9 to the mapping. *(Reviewer rated HIGH; calibrated down — the coverage exists, the traceability row does not.)*
- **G2 (MED):** AC-7's emit↔read field-name agreement is the FR-1/FR-8 linchpin; PG5.3 QA cross-checks it, but no Phase-6 test directly falsifies a byte-for-byte mismatch. Consider a small integration assertion.
- **G4 (LOW):** NFR-2 cost-band doc lives in contract §7; Step 7.3 conformance checks only §§2–6 → the cost-band requirement can regress silently.
- **G5 `[INFERRED]` (LOW):** No Step 6.3–6.8 test specifically pins `executor_model_class` consumption or `reflect_post:` write-back (spec §5 frontmatter). The contract states they're consumed; the plan assumes existing config behavior rather than proving it.
- **G3 `[INFERRED]` (MED):** NFR-5's cross-worktree "hold the companion until merged+pipx" is stated as a dependency (`…:86-88`) but no step operationally gates/signals `ReflectInTaskLists`.

---

## 4. Anchor Verification (research grounding — independently confirmed)

All R1/R2/R3 file:line anchors were spot-checked against `wrapper-onto-master` where the files physically exist. **Every anchor matched.** Highlights:

| Anchor (Step) | Real location | Verdict |
|---------------|---------------|---------|
| `ReflectConfig` fields `models.py:66-81`, `promote` :76 | matches; all fields non-default ⇒ Step 2.1 append is **safe** | MATCH |
| `ReflectResult` `:98-106`, defaulted tail | matches; appended defaults valid | MATCH |
| `_resolve_base` `config.py:81-93` | matches | MATCH |
| `commands.py` options `:62-107`, tasklist arg `exists=True` `:58-61`, `reflect_group` `:39-54` | matches; group callback exists ⇒ Step 3.3 marker placement **feasible** | MATCH |
| `--promote` default False `commands.py:70-75` | matches | MATCH |
| `_halted_reason` `contract.py:304-325`; `_DEVIATION_KEYS` includes `necessary`,`drift` | matches ⇒ `classify_fix` predicate valid | MATCH |
| `runner.py` `run()` `:378-501`, ClaudeProcess `:459-468`, `env_vars=None` `:467` | matches | MATCH |
| `task_file_path` `SKILL.md:744`; 5×`1.3.0` sites 651/654/791/1627/1758; `remediation_task_path` absent | matches exactly | MATCH |
| **`origin/master` has the reflect CLI (Step 1.3 premise)** | empty tree | **WRONG → F1** |

**Confirmed-clean (no action):** dataclass field ordering (Step 2.1 safe — all existing `ReflectConfig` fields non-default), Click group-callback feasibility (Step 3.3), SoT/`.claude` staging discipline (Phase 5 + PG5.4), bootstrap-exemption (inline `/sc:reflect` POST gate, not a `superclaude reflect run` shell-out), classify_fix purity + human-wins ordering + DEGRADED/BLOCKED-never-autofixed guard, marker exact-"1" truthiness + negative controls, audit-child marker safety.

---

## 5. Best-Practice Assessment (grade 4/5)

**Strengths:** self-contained checklist items resilient to session rollover; per-phase adversarial rf-qa + rf-qa-qualitative gates with `fix_authorization:false` report-only stance; explicit fail-closed framing; anchor "re-read before editing" discipline; correct SoT (`src/` → `make sync-dev`); correct bootstrap-exemption; honors `feedback_human_decision_items_must_halt`; research anchors are uniformly accurate.

**Docked one point for:** the F1 base-acquisition planning error and its masked-continue guards (a fail-closed tasklist should HALT on a missing base, not log-and-continue), plus the unreconciled FR-5 ownership contradiction (F3).

---

## 6. Recommended pre-execution actions

1. **Fix F1 (blocking):** rewrite Step 1.3 base acquisition to obtain the reflect CLI from where it lives (commit `wrapper-onto-master`'s staged work, then branch off it — or import the tree explicitly). Make Step 1.3/1.4 missing-base branches a HALT.
2. **Fix F2:** check `_apply_remediation` rc in Step 4.5; fail-closed on `rc != 0`; add the covering test.
3. **Resolve F3:** reconcile FR-5 vs U6 — either amend the spec wording (authorized) or add a thin wrapper-side no-adapter-no-promote guard. Spec-owner decision.
4. **Tighten traceability:** add AC-9 to the PG6.1 AC→test mapping (G1); add an emit↔read field-name assertion (G2); extend Step 7.3 conformance to contract §7 cost band (G4).

---

## Appendix — method & grounding

- **Tier 2 ensemble:** 3 reviewers — coverage-completeness (sonnet/analyzer), fail-closed-safety (sonnet/qa), executability-grounding (opus/refactorer). Each grounded independently in real files.
- **Blind calibration:** reviewer self-confidence {0.87, 0.91, 0.94} re-graded against the 5-dim rubric. `calibrator_diversity: degraded` (orchestrator/opus class collides with reviewer-3/opus — disjoint set not fully satisfiable here; noted, not silently passed).
- **Evidence-validator gate:** 12 load-bearing citations; the dominant ones (F1 git state, F2/F3 line cites, G1 mapping) were re-run/re-Read by the orchestrator directly. **0 dropped.** Two soft findings tagged `[INFERRED]` (G3, G5). A zero-drop pass is treated as a flag, not a clean signal — mitigated here by orchestrator-side re-verification rather than reviewer trust.
