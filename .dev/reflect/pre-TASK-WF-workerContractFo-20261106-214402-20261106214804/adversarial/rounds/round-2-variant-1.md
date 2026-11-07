# Round 2: Variant 1 rebuttal (sonnet, analyzer)

Persisted by the orchestrator on receipt, 2026-11-06T22:02:55Z.

## Response to criticisms

- V2, R1-6 does not address QA-1: CONCEDED. R1-6 is a different hazard: if `artifacts` appears on an earlier Unattended line, `_artifacts_clause` (test_worker_contract.py:769-774) picks that line and the pin fails; it cannot pass wrongly. test.md:99-107 has no `artifacts` token today, so the hazard is not live. R1-6 is a P3 implementer hint.
- V2, R1-2 is a documented gap, not proven impossibility: CONCEDED IN PART. Added evidence: sc-workflow-protocol/SKILL.md:60 records only `reflect_report_path`; SKILL.md:62 forbids editing `<id>.md` after reflect; refs/return-contract.md:51 sets `report_path` to `<id>.md`; `runs.jsonl` appears in the workflow skill only at return-contract.md:52. Narrowed claim: "Task 2 arranges no way for workflow's report to name the ignored files, and WC-4's unconditional sentence (plan :30, source.md:13) then asks for it." P2 with owner note.
- V2 and V3, one defect class and one grade: CONCEDED. R1-1 P1, QA-1 P1, R1-4/R3-3 merged P2 (rule below).
- V3, clean claim too narrow: CONCEDED. `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is tracked; :72 restates WC-4; source.md:14 names a spec copy; plan :30 greps only tests/ and plugins/. Git history mixed (spec and contract changed together in cb8f2f81, f3c1ef06; not in 38eb3c58, bb2650fa; in cb8f2f81 the spec edits were at :62 and :286, not :72), so no strict co-maintenance rule; still a silent drop of a brief item. P2. The grep must exclude `.dev/orca-command-refactor/specs/history/` (nine frozen snapshots).
- V3, R1-6 cannot pass wrongly: CONCEDED.

## Updated assessment of other variants

- V2: QA-1 real; criticism "inflated" withdrawn. QA-2 P3. V2's Task 5 clean line wrong in premise (init-lite.md:92 status sentence is inside the clause read by :787-797); benign if wording avoids "failed tool run" and "on a failed run". Plan :76 names only "on a failed run"; :792 also bans "failed tool run": P3 (the test would catch it).
- V3: R3-1 valid. R3-5 stronger than credited: sc-workflow-protocol/refs/input-parse.md:16 already uses "`~/.claude/WORKER-CONTRACT.md` (rule WC-4)". R3-5's "no criterion forbids src/superclaude/" is half true: `_check_unattended_section` asserts `"src/superclaude/" not in text` for command sections (test_worker_contract.py:517); only return-contract.md is unguarded. R3-4 P3.

## New evidence

1. Correction to R1-1's fix: in SKILL.md:61 the `worker_status` text precedes `artifacts`, so it is outside `_artifacts_clause`; in init-lite.md:92 it follows and is inside. The "when the audit finished" absence check must run on the whole text or line for SKILL.md.
2. Negative-test idiom exists: `test_unattended_section_check_fails_when_token_removed` (:561-570). For QA-1 add "left out" to `UNATTENDED_EXPECT["test"]["phrases"]` (:349-353) and a clause-level assertion mirroring :799 and :808.
3. Per-task AC review is a real second guard: sc-implement-protocol/refs/qa.md:9, :27-31 (diff against each AC, path:line evidence), :49 (AC unmet when output contradicts it). R1-1 and QA-1 are both contradicted by an AC (plan :79, :69).
4. Low-value hits: sc-brainstorm-protocol/SKILL.md:388 (out of scope per plan :24); developer guide :1001-1002 (RF-1).

## Grading rule for "assertion weaker than its AC"

Take the minimal text that satisfies the planned assertion but violates the AC.
- P1: that text is the negation of the AC (the state the task exists to remove). AC review mitigates but does not lower the grade (P1 definition is test-centric).
- P2: the text meets the content but displaces it (wrong bullet or scope), or is weaker or incomplete.
- P3: the AC or assertion is vacuous and admits nothing another test would not catch.

| Finding | Wrong text admitted | Grade |
|---|---|---|
| R1-1 | init-lite.md:92 and SKILL.md:61 keep "succeeded when the audit finished" next to "exited 0" (the rule Follow-up 3 removes, source.md:24-25) | P1 |
| QA-1 | A test.md clause listing `htmlcov/` while naming WC-4 and `[]` (contradicts plan :69, source.md:19) | P1 |
| R1-4 / R3-3 | New sentence placed in WC-9; the WC-4 pointer becomes false | P2 |
| R1-3 / QA-2 / R3-2 | AC3 admits any sentence (`core/` outside AUDIT_ROOTS :1054-1058; WC-9 already has `git add` at WORKER-CONTRACT.md:41-42) | P3 |
| R1-6 | None; can only fail | P3 note |

Sensitivity: counting the AC review as a guard drops R1-1 and QA-1 to P2 and R1-4/R3-3 to P3; never split them. For QA-1 take V3's narrowing: pin "left out" + "WC-4" + `[]`; keep report-location out of per-command text.

## Updated per-point positions

| Point | Superior | Reason |
|---|---|---|
| S-001 | Tie | Shape changes no finding |
| C-001 | V1 | R1-3 names the test that reads contract lines (:573-574); P3 agreed |
| C-002 | V1/V3 tie | Same slice; merged P2 |
| C-003 | V1 | Gating P2, narrowed |
| C-004 | V2 (narrowed by V3) | QA-1 P1; pin "left out" and WC-4 |
| C-005 | V1 | R1-1 P1; SKILL.md fix needs whole-text check |
| C-006 | V3 | Spec :72; exclude specs/history/ |
| C-007 | V3 | P3 |
| C-008 | V3 | return-contract.md only (:517 guards command sections); input-parse.md:16 precedent |
| C-009 | V1 | Only card that verified exit paths |
| C-010 | Tie | Advisory, out of brief |
| X-001 | V3 (with V2's core) | Pin exclusion token; report-location stays in WC-4 |
| X-002 | V1/V3 | P3; V2 conceded |
| X-003 | V3 | Spec copy confirmed |
| A-001 | Tie | No variant states the route; owner may revise the plan between /sc:workflow and /sc:implement |
| A-002 | Tie | AC review is a second guard (qa.md:27-31); grade the class uniformly |
