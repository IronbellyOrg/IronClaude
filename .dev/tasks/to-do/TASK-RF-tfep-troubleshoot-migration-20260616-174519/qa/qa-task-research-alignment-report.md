# QA Report: Task ↔ Research Alignment

**QA Mode:** task-integrity
**Lens:** task-research-alignment
**Stance:** Adversarial — assume the builder dropped or misrepresented research findings.
**Date:** 2026-06-16
**Task file:** `TASK-RF-tfep-troubleshoot-migration-20260616-174519.md`
**Research dir:** `research/` (5 files: R-001..R-005)

---

## Methodology

Cross-validate that every significant research finding has a corresponding task item, and that no
task item fabricates actions not grounded in research. Seven targeted alignment checks (A1–A7) plus a
fabrication sweep (A8). Each check cites the research anchor and the task item that consumes it.

---

## Alignment Check Matrix (A1–A7)

| # | Research anchor | Required mapping | Task item(s) | Verdict |
|---|----------------|------------------|--------------|---------|
| A1 | R-001 §B rename worklist: SKILL.md lines 172,205,206,213,215,250,253 + task.md:48 | each bare-`forensic` anchor → a rename item | 2.2(172), 2.3(205), 2.4(206), 2.5(213), 2.6(215), 2.7(250), 2.8(253), 2.9(task.md:48) + 2.1(`diagnostic_backend:` decl) | **PASS** |
| A2 | R-002 §B3: 5 missing contract fields | each → an add-row item | 4.1 `recommended_escalation`, 4.2 `tasklist_insertion_path`, 4.3 `remediation_target`, 4.4 `root_cause_summary`, 4.5 `solution_summary` | **PASS** |
| A3 | R-002 §A/§B: `--context`/`--caller` ingestion sites (Options table, Wave 0 L115, audit header) | each ingestion site → an item | 3.1 arg-hint, 3.2/3.3 Options rows, 3.4 cmd parse, 3.5 surface, 3.6 Wave0 parse(L115), 3.7 resolve substep, 3.8 STOP, 3.9 TARGET header, 3.10 SUMMARY footer | **PASS** (over-covers; all R-002 §B sites present) |
| A4 | R-005 G2 incident-rebind table (rca-verdict.md→Diagnosis, solution-verdict.md→Proposed Fix, Forensic artifacts→Diagnostic artifacts) | each row → an item | 6.1 Root cause→Diagnosis, 6.2 Solution→Proposed Fix, 6.3 Diagnostic artifacts value rebind | **PASS** |
| A5 | R-005 G1 Option-1 ownership (no `--fix`) reflected in Phase 5 dispatch | dispatch passes NO `--fix` | 5.3 dispatch line (`/sc:troubleshoot ... --depth {depth}`, explicit "pass NO `--fix`") + 5.6 inline ownership note | **PASS** |
| A6 | R-003 §2 report-template `## TFEP Consumer` block (anchor after L154, before L156) | encoded as an item | 4.9 (inserts `## TFEP Consumer` after `## Next Steps` L154, before `### Hard-stop variant` L156) | **PASS** |
| A7 | R-003 §3 verify-sync / Makefile contract | encoded as verification items | 2.10, 3.11, 5.7, 6.5, PC.2 (`make sync-dev` → `make verify-sync`, no `.claude/` staged) | **PASS** |

All seven targeted alignment checks PASS at the structural level: every significant research finding has a corresponding task item, with the line-anchors, field names, and rebind sources traced verbatim to R-001/R-002/R-003/R-005.

---

## A8 — Fabrication Sweep (adversarial: does any item reference a file/line/field NOT in research?)

**Edit-target files** — all 5 src paths the task edits (`sc-task-protocol/SKILL.md`, `commands/task.md`, `commands/troubleshoot.md`, `sc-troubleshoot-protocol/SKILL.md`, `refs/report-template.md`) are named in R-001/R-002/R-003. No fabricated file. **CLEAN.**

**Line anchors** — spot-checked: 172/205/206/213/215/250/253/task.md:48 (R-001 §B/§D), L115/Options-48-58/TARGET-128-137/SUMMARY-446-455 (R-002 §A2/§B1/§B2/§B6), Output-Contract-41-72 (R-002 §B3), report-template Next-Steps-146-154 / Hard-stop-156 (R-003 §2), Escalation-Budget-257-261 (R-001 §C / R-003 §1A). Every line anchor is research-backed. **CLEAN.**

**Field names** — all 5 adapter fields appear verbatim in R-002 (4 hits each). The `remediation_target` enum `test|code|docs|none` is grounded in R-002 line 180 ("target = test (if test_is_wrong) / docs (if behavior_is_documented) / code (else)"). The `recommended_escalation` derivation (`status`+`tier_reached`+`confidence`) is grounded in R-002 line 178. **No fabricated field.**

**Token bands** — Step 6.4 correctly does NOT fabricate troubleshoot per-depth token bands; it instructs to drop the `~5-8K`/`~15-20K` figures rather than invent new ones, matching R-003 §4.4 ("must restate budgets against troubleshoot tiers"). **CLEAN — explicitly anti-fabrication.**

---

## Findings (ranked)

### Finding 1 — Task-authored `recommended_escalation` enum vocabulary not present in any research file [MINOR]

The enum `none|retry|escalate_depth|halt` (Steps 4.1, 4.9, 5.5, and PG4 internal-consistency lens) appears in **no** research file. R-002 line 178 confirms the field is MISSING and must be *synthesized* from `status`+`tier_reached`+`confidence`, but the specific 4-value vocabulary — in particular the tokens `retry` and `escalate_depth` — is a builder design fill, not a research-grounded mapping.

- **Why it matters (adversarial):** The original forensic consumer (R-003 L41, L140) branches on `recommended_escalation != "none"`. The builder invented `escalate_depth`/`halt` and Step 5.5 must re-map the legacy `!= "none"` re-loop branch onto them. A reviewer cannot validate the enum against any source-of-truth.
- **Mitigation already in task:** PG4 internal-consistency lens (line 422) explicitly checks the enum is "identical everywhere it appears", and Step 5.5 aligns the consumer branches. So the *internal* consistency is gated even though the *external* grounding is absent.
- **Not a blocker:** R-002/Open-Question-3 authorize ADDING net-new fields, and a new field legitimately needs a new value set. The enum is a reasonable design fill, flagged for traceability only.

### Finding 2 — Two research-named TFEP-Consumer fields (`tasklist_insertion_recommendation`, `safe_to_auto_insert`) silently dropped [MINOR]

R-003 §2 (line 94) and §5 (line 149, 160) explicitly name the fields the new `## TFEP Consumer` report block "should surface": `remediation_target`, **`tasklist_insertion_recommendation`**, **`safe_to_auto_insert`**. The task adopts `remediation_target` but the report-template block (Step 4.9) uses `tasklist_insertion_path` and omits `tasklist_insertion_recommendation` and `safe_to_auto_insert` entirely (grep: 0 occurrences in the task file).

- **Why it matters (adversarial):** R-003 §2 is a direct "should surface X" instruction; two of its three named fields have no corresponding item. On its face this is a dropped research finding.
- **Why it is defensible (not a contradiction):** R-003 §5's *adapter-contract gate* names the **actual consumer tokens** the task-protocol side reads as `tasklist_insertion_path` / `recommended_escalation` / `status` / `test_is_wrong` (L159). The builder correctly prioritized the *consumer-side* field names (what task-protocol actually parses, per R-001 §C L225 `tasklist_insertion_path`) over R-003 §2's *suggested* report-echo names. The two dropped names were R-003's own non-binding suggestions ("should surface"), superseded by the consumer contract. This is a justified reconciliation, but it is undocumented — the task never states "R-003 §2's suggested `tasklist_insertion_recommendation`/`safe_to_auto_insert` are intentionally replaced by the consumer-side `tasklist_insertion_path`."
- **Recommendation:** add a one-line note in Phase 4 preamble or Open Questions recording that R-003 §2's two suggested field names were deliberately reconciled to the consumer-side `tasklist_insertion_path` per R-003 §5, so a future reader does not read this as a dropped requirement.

### Finding 3 — `recommended_escalation != "none"` legacy re-loop branch reconciliation is under-specified [MINOR]

R-003 L41 and L140 record that the existing consumer branches on `recommended_escalation != "none"` → re-loop. Step 5.5 instructs mapping `escalate_depth`→re-loop-deeper and `halt`→FULL STOP, but the new enum also introduces `retry` (re-run at same depth, per Step 4.1), which has **no** corresponding consumer branch named in Step 5.5. The `retry` value is produced (4.1) but its consumption path is left to "make ONLY the minimal edits needed so every branch reads an existing adapter field."

- **Why it matters (adversarial):** A produced enum value (`retry`) with no explicit consumer branch is a latent producer/consumer asymmetry. Step 7.2's cross-check only verifies token *presence* of `recommended_escalation`, not that every *enum value* has a handler.
- **Not grounded as a gap in research** because research never enumerated the values; this is a second-order consequence of Finding 1.
- **Recommendation:** Step 5.5 should explicitly state where `recommended_escalation == retry` routes (same-depth re-loop), so all four produced values have a consumer.

---

## Cross-cutting confirmations

- **Report-template TFEP-consumer block (R-003 anchor after L154):** ENCODED at Step 4.9 with the exact anchor (after `## Next Steps`/L154, before `### Hard-stop variant`/L156). **Confirmed.**
- **verify-sync contract (R-003 Makefile §3):** ENCODED at every phase sync step (2.10/3.11/5.7/6.5) and the final HARD gate PC.2, each with `make sync-dev` → `make verify-sync` (exit 0) + `git status --porcelain` no-`.claude/`-staged check (CLAUDE.md ABSOLUTE RULE). **Confirmed.**
- **G1 Option-1 (no `--fix`):** dispatch (5.3) passes no `--fix` and the ownership note (5.6) restates the split. Alternative recorded as non-blocking Open Question item 2. **Confirmed faithful to R-005 G1.**
- **Freeze invariant (Change 6 / R-001 §C L185-188):** Step 5.1 is a no-edit *guard* item recording the freeze block verbatim. **Confirmed preserved.**

---

## VERDICT: PASS

All seven targeted alignment checks (A1–A7) PASS: every significant research finding maps to a corresponding task item, with line-anchors, field names, and rebind sources traced verbatim to R-001/R-002/R-003/R-005. The fabrication sweep (A8) found **no** task item referencing a file, line, or field absent from research — the only non-research token is a legitimate net-new enum vocabulary for an additively-added field, which research explicitly authorized adding.

Three MINOR findings, none blocking:
1. `recommended_escalation` enum vocabulary (`none|retry|escalate_depth|halt`) is a task-authored design fill not in research (traceability gap, internally gated by PG4).
2. R-003 §2's suggested report-block field names `tasklist_insertion_recommendation`/`safe_to_auto_insert` were reconciled away to the consumer-side `tasklist_insertion_path` without a documenting note (justified by R-003 §5, but undocumented).
3. The produced enum value `retry` has no explicitly named consumer branch in Step 5.5 (second-order consequence of Finding 1).

**Severity rollup:** 0 CRITICAL, 0 IMPORTANT, 3 MINOR. The task does NOT drop or misrepresent any significant research finding; the three findings are documentation/traceability hygiene around a legitimately-added field, not misalignment. Recommend addressing Finding 2's documenting note and Finding 3's `retry` routing before execution, but neither gates the PASS.
