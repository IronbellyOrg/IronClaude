# /sc:reflect — UC-2 Post-Execution Re-Audit: PR #144 Restoration (ddf209e4)

- **Mode:** post (UC-2) · **Tier reached:** 2 (deep, 3 heterogeneous reviewers + adversarial merge + evidence-validator)
- **Diff audited:** `4f0a60fb..ddf209e4` (restoration over the convergence head)
- **Refs:** base/canonical `54d4b4f5` · convergence head (dropped content) `4f0a60fb` · restoration under audit `ddf209e4`
- **Worktree:** `/config/workspace/IronClaude-pr144-reflect` (HEAD ddf209e4, `make sync-dev` applied)
- **Reviewers:** R1 sonnet/analyzer (conf 0.91) · R2 haiku/qa (conf 0.95) · R3 opus/refactorer (conf 0.88)
- **Calibrated confidence (inline-fallback):** **0.90**
- **Status:** success (audit-only; `--no-promote`, no remediation)

> Header note on the freshness discipline: an initial 2 KB-truncated read of the merge-test output led me to a *wrong* "all tests pass" reading; the full run (verified) shows 2 RED merge tests. All findings below are grounded on re-verified output.

---

## Verdict on the audited claim

The agent claimed **"all 44 audit-guard failures were accidental DRIFT (not intentional supersession), and zero guard tests were weakened."**

**Verdict: SUBSTANTIALLY TRUE, with one framing correction.**

- ✅ **"zero guard tests weakened" — TRUE (high confidence).** No test file was modified across `54d4b4f5 → 4f0a60fb → ddf209e4` (both diff stats empty for `tests/audit/` and `tests/skills/test_task_builder_merge.py`). The RED tests fail because they assert *superseded* behaviour, not because any assertion was loosened. `test_severity_floor_unweakened` 8/8 PASS; TEST-020 sha256 pin + byte-stability PASS.
- ⚠️ **"all 44 were DRIFT" — INACCURATE for one cluster.** The Execution Context cluster (OPTIONAL→REQUIRED + `EXECUTION CONTEXT BLOCK`→`EXECUTION_CONTEXT_INSTRUCTION`, surfacing as 2 RED merge tests) is **SUPERSESSION, not drift** (see Item 3). In *practice* the restoration handled it correctly — it did **not** restore OPTIONAL, it deferred — so the executed classification was right even though the "all drift" wording is not.

Net: the restoration did the right thing per-item, but the work is **incomplete**: the supersession leaves 2 guard tests RED that still require a test-update.

---

## Per-deviation classification

| # | Item | Class | Verdict |
|---|------|-------|---------|
| 1 | sha256 `51725c0ffa` + recommendation em-dash + DNSP/INV-021/R-126 content restoration | **Necessary** (canonical drift-correction) | Guard-required, runtime-verified. Clean. |
| 2 | Em-dash restoration breadth | **Authorized / clean** | Surgical, not a broad ASCII revert. No deviation. |
| 3 | Execution Context OPTIONAL→REQUIRED + rename (2 RED tests) | **Necessary** (intentional design supersession) — **OPEN follow-up** | Correctly NOT reverted; tests need updating. |
| 4 | MD040 `​```text` fence additions (28) | **Authorized / clean** | Language-tag-only; no pinned block mutated. |
| 5 | `tests/audit/` base-parity | n/a | Only the known pre-existing filesystem failure. |
| + | Stale `L1079-1093` line-range pointer in 3 agent DNSP lines | **Drift (pre-existing / convergence-introduced)** | Inherited un-corrected by restoration; LOW severity. |

**Deviation counts:** authorized 0 · necessary 2 · drift 1 · regression 0.

---

## Item-by-item evidence

### Item 1 — Each restored item: genuine DRIFT or deserved a test-update? → genuine drift-correction; no misclassification

Two pins, correctly differentiated:

- **`51725c0ffa…` (COMP-006-M6, the `rf-team-lead's Fix Cycles rule` line).** GUARD-PINNED by `tests/audit/test_dnsp_all_agents_fail_bypass.py` — `test_rf_team_lead_fix_cycles_sha256_pin_present_at_every_site` (pin present at every site) + `test_fix_cycles_rule_present_and_byte_stable` (runtime hash of the live rule == fixture). Both PASS at HEAD. base=`frozen at 51725…`; convergence=`OMITTED as bridge-stage` (broke the guard); restoration=`frozen at 51725…` restored (`SKILL.md:897`). → **genuine drift correction, guard-required, runtime-verified true.**
- **`5ff2a1803b…`** pinned the INV-012 subsection that the convergence **structurally reformatted** (base mega-paragraph → condensed Path A/B/C, now at `SKILL.md:899`). Restoration left it `OMITTED as bridge-stage` — and `SKILL.md:899` documents this explicitly: *"the sha256 subsection pin from IC's version is OMITTED as a bridge-stage item; the behavioral contract is adopted."* No guard references `5ff2a`. Re-asserting the old hash over reformatted bytes would be a **false pin** → omission is correct, **not** under-restoration.
- **recommendation string:** base/restoration = `Manual review required — partition agent failed twice` (em-dash, byte-exact R-117 invariant); convergence = ASCII comma. Restoration restored the invariant form.

R1 independently spot-checked non-sha256 hunks (DNSP 7-field contract `rf-analyst.md:74`; TB-Add-2 checklist renumber `rf-qa.md:325-340`; INV-019 Reliance-Audit heading `rf-qa-qualitative.md:880`; INV-021/R-126 merge invariants `SKILL.md:901`; FR-CONV.5 halt-ordering `SKILL.md:1292-1303`) — **all genuine drift-correction / canonical hardening; none re-introduced deliberately-removed content; none weakened an assertion.**

### Item 2 — New drift / em-dash over-restoration? → CLEAN

Em-dash counts (base/convergence/restoration): rf-analyst 71/37/40 · rf-qa 134/86/88 · rf-qa-qualitative 298/209/217 · SKILL.md 348/220/250. Restoration stays **near the convergence count, far below base** → surgical, **not** a broad revert of clayphi's ASCII-ification. R3 pulled all 38 `+` em-dash lines: every one is a guard-pinned fixed string, a structural heading (`— Reliance Audit (PR-04, INV-019)`), an enum token, or verified base-canonical content dropped-by-convergence-and-restored (e.g. `SKILL.md:1521/1529`). **No arbitrary prose reversion.**

### Item 3 — The deferred call (OPTIONAL→REQUIRED): SUPERSESSION or DRIFT? → **SUPERSESSION (independent verdict)**

- The merge **test file was never modified** (base→convergence→restoration). The 2 failures are content-driven:
  - `test_skill_documents_execution_context_block` — `assert "EXECUTION CONTEXT BLOCK" in skill_text` (literal renamed to `EXECUTION_CONTEXT_INSTRUCTION`, `SKILL.md:1066`).
  - `test_execution_context_optional_and_degrades_gracefully` — `assert "OPTIONAL" in skill_text` (now `REQUIRED in every task file (except GOAL-only…)`, `SKILL.md:1229`).
- **Why supersession, not drift:** the change is coherent and intentional — (a) consistent `_INSTRUCTION` directive naming; (b) `REQUIRED` carries a documented `GOAL-only` degradation exception; (c) **the MDTM templates corroborate it**: `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1195` — *"BUILDER: Populate this section as a required build step. Every generated task file MUST have this section populated…"*, and the convergence diff **added** those template `## Execution Context` sections. SKILL.md and templates are mutually consistent.
- **No internal contradiction:** `OPTIONAL` has zero occurrences at HEAD; the lone `TB-Add-7 … INACTIVE if no Execution Context block exists` is a safety-valve for non-standard templates, not an OPTIONAL assertion.
- **Independent verdict:** this is **SUPERSESSION**. The restoration **correctly did NOT restore OPTIONAL** (its deferral of the *content revert* was the right call — reverting would undo an intentional design improvement). **However, the supersession is not fully resolved:** closing it requires updating the 2 tests, which remains an **open follow-up** (R2 stance). The restoration recognized the supersession but did not close the loop.

### Item 4 — MD040 fence additions touched guard-pinned content? → NO (CLEAN)

28 `​```text` additions add a language tag to **opening fences only** (each fence-add line is followed by an unchanged context line; fenced bytes untouched). All sha256/byte-stability/severity-floor guard tests are green; fences balanced at HEAD. No pinned/SHA-pinned block mutated.

### Item 5 — tests/audit base-parity + remaining #144 failures → CONFIRMED

`tests/audit/` = **1 failed / 1188 passed / 1 skipped**. Sole failure = `test_invariant_preservation_NFR_6_through_10.py::TestInvariant3_PersistentArtifact::test_task_id_naming_pattern_preserved` — a `.dev/tasks/` directory-naming **filesystem/env** test, unrelated to the 4 restored files, in the known pre-existing set. **No new #144-introduced audit failure** beyond the known set (task_id_naming; tests/cli/eval/*; test_install_hooks.py; test_zero_files_analyzed teardown).

---

## New finding (validated): stale `L1079-1093` line-range pointer

The 3 agent DNSP lines (rf-analyst, rf-qa, rf-qa-qualitative) cite `SKILL.md L1079-1093` for the INV-012 cross-cycle dedup subsection. At HEAD, `SKILL.md:1079-1093` is **unrelated research-dir spawn boilerplate** (`RESEARCH DIR: ${TASK_DIR}research/…`); the real INV-012 subsection is now at **`SKILL.md:899`**. The pointer is **stale/dangling**.

**Provenance:** convergence-introduced (the `L1079-1093` text is byte-identical in the convergence `-` line and restoration `+` line, restoration.diff L22/23). The restoration rewrote that line to restore the adjacent `51725` pin but **inherited the stale L-range verbatim**. So it is a **pre-existing drift inherited un-corrected**, NOT restoration-created. LOW severity (no guard references it).

---

## Grounding gaps / dropped citations

- **Dropped (1):** Reviewer 2's MDTM-template citation path `src/superclaude/skills/task-builder/templates/…` was unfounded (no such dir). Re-grounded to the verified path `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md:1195`; the underlying claim survives. (`citations_dropped: 0` after correction — re-validated, not left dropped.)
- No open human-decision gates. The 2 follow-ups below are clear-cut recommendations.

---

## Recommendations (audit-only — not applied)

1. **Close the Item-3 supersession (REQUIRED for green CI).** Update `tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader`:
   - `test_skill_documents_execution_context_block`: `assert "EXECUTION CONTEXT BLOCK"` → `assert "EXECUTION_CONTEXT_INSTRUCTION"`.
   - `test_execution_context_optional_and_degrades_gracefully` → rename to `..._required_...`; `assert "OPTIONAL"` → `assert "REQUIRED"`; keep the `GOAL-only`/`References-only` degradation assertion.
   - Update the class docstring ("optional" → "required"). Edit `src/superclaude/skills/...` is N/A (test lives in `tests/`); edit `tests/` directly. Verify: `uv run pytest tests/skills/test_task_builder_merge.py -q`.
2. **Fix the stale pointer (LOW).** Re-point the 3 agent DNSP lines `L1079-1093` → `L899` (or replace the brittle line-range with a stable content anchor). Verify: `git -C /config/workspace/IronClaude-pr144-reflect grep -c "L1079-1093" src/superclaude/agents/`.

Both are follow-ups to the **convergence's** intentional changes — neither is a defect the restoration *created*, and neither falsifies the restoration's per-item classification.
