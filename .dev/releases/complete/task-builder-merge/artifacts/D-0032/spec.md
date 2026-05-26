# D-0032 — T03.08 Spec: Anti-Inflation Preservation + Failure-Mode Halt

**Task:** T03.08 (Phase 3 / M3 Inherited Verdict + Self-Audit)
**Roadmap items:** R-059, R-060
**Date:** 2026-05-17
**Tier:** STRICT
**Deliverable IDs:** D-0032

---

## 1. Scope

T03.08 lands two strict-additive changes to `src/superclaude/skills/task-builder/SKILL.md`:

1. **Wire the `halt-A.10-before-A.10.5` lever** by adding a 4th branch to §A.10 "Handling the verdict" (line 1089) that HALTs the pipeline whenever rf-qa fails to emit a well-formed `VERDICT: PASS|FAIL` line. The DM-005 contract row at SKILL.md §A.10.6 (rows :1259 and :1275) already publishes this lever name; T03.08 wires the orchestrator behavior that operationalises it.
2. **Reconcile the §A.10.5 narrative** at SKILL.md line 1101 — the prior text ("omit the section and let rf-qa-qualitative fall back to its standalone behavior") contradicted the DM-005 halt directive. Replaced with text that defers to the upstream A.10 halt and explains why the consumer cannot proceed without a producer verdict (INV-019 / Self-Audit / anti-inflation anchor at `rf-qa-qualitative.md:766-775`).

T03.08 makes **zero edits** to `src/superclaude/agents/rf-qa-qualitative.md`. The byte-stability of lines 766–775 is preserved by not editing the file at all in this task.

## 2. Anti-Inflation Block Preservation (R-059)

**Anchor:** `src/superclaude/agents/rf-qa-qualitative.md:766-775`
**Baseline sha256 (pre-T03.08):** `0570c6b474686734d8a69e62adcd825d3c0b3e421ef4a12ef114703d1deec59c`
**Post-T03.08 sha256 (src + mirror):** `0570c6b474686734d8a69e62adcd825d3c0b3e421ef4a12ef114703d1deec59c` — **byte-identical**.

The 10-line range houses the Confidence Gate Protocol's **Categorize** (Step 1) and **Count** (Step 2) directives. Functionally, this block is the anti-inflation rule: it forbids UNCHECKED items from being treated as unknowns, mandates that they count as FAILURES toward the confidence denominator, and pins the formula `confidence = VERIFIED / (TOTAL − UNVERIFIABLE) × 100`. Removing or weakening any of these would let a rf-qa-qualitative run inflate PASS counts by re-classifying unchecked items as unknown — exactly the failure mode the block prevents. T03.08 preserves the block intact.

## 3. Failure-Mode Halt Wiring (R-060)

**Edit site:** SKILL.md §A.10 "Handling the verdict" block, immediately after the existing FAIL-with-unfixable-issues branch (line 1088) and immediately before the §A.10.5 heading (line 1090).

**Specification of the new 4th branch (line 1089):**
- **Trigger conditions** (any of):
  - `${TASK_DIR}qa/qa-task-validation-report.md` is absent on disk.
  - The report file exists but `grep -E '^VERDICT: (PASS|FAIL)$'` returns zero matches.
  - The report file exists and the `VERDICT:` line is present but its value is neither `PASS` nor `FAIL`.
- **Action:**
  - HALT. Do NOT spawn rf-qa-qualitative.
  - Emit a structured log line:
    - Report absent → `INV-002-no-producer-artifact halt-A.10-before-A.10.5 task=${TASK_DIR}`
    - Report present but no/malformed VERDICT → `INV-002-no-verdict-line halt-A.10-before-A.10.5 task=${TASK_DIR} report=${REPORT_PATH}`
  - Surface the failure path to the user with an instruction to re-run rf-qa.
  - On a subsequent re-run that emits a well-formed `VERDICT:` line, the orchestrator restarts from "Handling the verdict" and routes via the existing PASS / FAIL-with-fixes / FAIL-unfixable branches.
- **Rationale embedded in the branch:**
  - References the DM-005 `failure_mode: halt-A.10-before-A.10.5` lever name.
  - Cites the anti-inflation anchor at `rf-qa-qualitative.md:766-775`.
  - Cites INV-019 (Self-Audit obligation) to explain why a missing producer verdict makes consumer reliance declarations impossible by construction.

**Edit site:** SKILL.md §A.10.5 line 1101 narrative.
- **Pre-edit text** (contradicted the contract):
  > If `qa-task-validation-report.md` is missing or malformed, omit the section and let rf-qa-qualitative fall back to its standalone behavior (passthrough is an optimization, never a dependency).
- **Post-edit text** (defers to upstream A.10 halt; cites lever, INV-002, INV-010, INV-019; cites :766-775 anchor):
  > If `qa-task-validation-report.md` is missing or its `VERDICT:` line is absent/malformed, the upstream A.10 verdict gate has already HALTed per DM-005 `failure_mode: halt-A.10-before-A.10.5` (see "Handling the verdict" branch 4 above) — control never reaches this A.10.5 spawn step on that cycle, so there is no orchestrator-visible "omit the section and fall back" code path. The consumer agent (rf-qa-qualitative) retains independent standalone capability, but operationally FR-CONV.3 (PR-04 passthrough) + INV-002 (freshness) + INV-010 (dynamic enumeration) require a producer verdict for every spawn: the anti-inflation rule at `rf-qa-qualitative.md:766-775` depends on an enumerated checklist that only the producer can publish, and the Self-Audit obligation (INV-019) requires the consumer to declare which producer-PASS items it relied on (an impossible declaration when no producer verdict exists).

## 4. Strict-Additivity / Scope Confinement

- **Files touched by T03.08:** `src/superclaude/skills/task-builder/SKILL.md` (+1 added branch at L1089; 1 paragraph rewritten at L1101). Mirror sync via `make sync-dev` propagates to `.claude/skills/task-builder/SKILL.md`.
- **Files NOT touched by T03.08:** `src/superclaude/agents/rf-qa-qualitative.md` (byte-stability requirement at :766-775 is preserved by not editing the file in this task; the 70-line additive append at L820+ is from sibling tasks T03.04 / T03.10 and lives well below the :766-775 anchor).
- **DM-005 contract row at SKILL.md:1275:** UNCHANGED in T03.08. The published contract row was frozen at M1 / T01.13 and published at M2 / T02.04; T03.08 implements the lever rather than re-authoring the contract.
- **Existing 3 verdict branches** (PASS, FAIL with fixes, FAIL unfixable): unchanged.

## 5. Verification Methodology

- **Anti-inflation byte-stability:** sha256 of `sed -n '766,775p'` of both `src/` and `.claude/` copies pre/post — must equal the baseline.
- **Halt-lever wiring:** grep for the 4th branch heading + halt-lever identifier; read the branch text to confirm all three trigger conditions, structured log lines, and the rationale citations are present.
- **Missing-verdict fixture:** `D-0032/fixture-missing-verdict.sh` exercises three synthetic producer states (report absent, report present with no VERDICT, report present with VERDICT: PASS) and asserts the orchestrator's documented behavior for each.
- **Sub-agent verification:** quality-engineer sub-agent independently re-tests all claims and writes a report to `D-0032/quality-engineer-report.md`.
- **Make verify-sync:** must report `✅ All components in sync.` post-edit.

## 6. Rollback

Per phase-3-tasklist line 403 ("As stated in roadmap"): disable the PR-04 passthrough flag; fall back to independent structural re-checking. In the SKILL.md edit, the rollback action is to revert the L1089 4th branch and the L1101 paragraph to their pre-T03.08 text. The DM-005 contract row at L1275 is unchanged and so no contract-level rollback is required.

## 7. Dependencies

- Upstream: T03.04 (Self-Audit output schema + INV-019 obligation), already PASS per CP-P03-T01-T05.
- Downstream: T03.10 (rf-qa-qualitative EOF append + Self-Audit) inspects the same :766-775 byte-stability invariant from its own delta. T03.16 (MIG-003 landing migration) lands the full M3 wrapper including this halt branch.
