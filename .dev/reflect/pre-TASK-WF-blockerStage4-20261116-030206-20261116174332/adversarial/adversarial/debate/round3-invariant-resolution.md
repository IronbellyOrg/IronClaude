# Round 3 (extra round): resolution of INV-001 (HIGH) and INV-002 (MEDIUM), saved verbatim

Trigger: the invariant-probe gate blocked convergence on one HIGH-severity UNADDRESSED item (INV-001). The orchestrator re-checked the facts by Grep before the round: the S5 bullet is at `agent_template_qa.md:140`, and in the other three digest templates it sits next to S1 to S3. The three advocates answered in parallel.

## Variant 1 advocate (sonnet class)

### INV-001
Verified by Read and Grep.

**Q1 (does "the definition bullets" include S5?).**
- Stage 3 plan line 125 uses the term for three bullets: S1, S2 and the "On a CRITICAL / IMPORTANT / MINOR scale..." bullet. In `pragmatic.md` they sit at lines 225, 226 and 229, close together.
- P4:37 says "the definition bullets near line 161". In `agent_template_qa.md`, S1 and S2 are at 161-162 and the cap is at 163. S5 is at line 140, 21 lines away.
- A literal executor edits 161-163 and leaves 140. In the other three templates S5 sits next to S1 to S3, so only `agent_template_qa.md` is exposed.
- P4 never mentions S5. Grep for S5 or "CRITICAL and IMPORTANT findings are blocking" in the P4 package returns nothing.
- The spec requires the edit. Line 815 says each carrier "replaces S1, S2 and S5 (where present)". Line 737 says S5 "becomes grade by the three conditions".
- No P4 check catches it. The P4:46 grep covers only S1 and the verdict bullet. T1 compares only the fenced digest. Strict T2 looks only for the S1 sentence.
- `CRITICAL and IMPORTANT findings are blocking` is still present in all four digest templates: `agent_template_qa.md:140`, `skill_template.md:831`, `01_mdtm_template_generic_task.md:647` and `02_mdtm_template_complex_task.md:658`.

**Q2 (what goes wrong if S5 stays).**
- The QA agents generated from the template get two rules in one file. Line 140 says CRITICAL and IMPORTANT are blocking. The digest below it says blocking only under three conditions, and that IMPORTANT is "information, never the grade".
- REQ-03 settles only a conflict between the agent's instructions and the session output style, or text inside the work under review. It does not settle a conflict inside the agent's own text.
- S5 already softens itself: "grade by the definition above, not by the label, so a finding labelled IMPORTANT that is only wording is minor". That limits the damage.
- What is left is a real defect that is IMPORTANT by the template's domain definition but that nothing rests on. S5 blocks it. The digest grades it Medium. This is the case the program exists to change.
- This is a weakness in future templated agents, not a wrong result in the exit state. The digest is narrower ("only when") and comes later, so a reader can reconcile the two. Existing agents are not migrated.

### INV-002
- `spec-panel.md:461` says `artifacts` lists `improved-spec.md` when the Improve step ran, "and it is [] otherwise".
- WC-4 defines `artifacts` as "every other file written", minus ignored paths. Stage 2 plan line 102 lists the ledger when it is a tracked path.
- P4:89 adds the ledger at `<report-dir>/follow-ups.md`. It defers to WORKER-CONTRACT only for the three `follow_up_*` keys, and it leaves line 461 alone. Stage 2 does not touch spec-panel.
- A worker can follow line 461 and return `artifacts: []` while a tracked ledger exists. The `follow_up_ledger` key still carries the path, so the coordinator is not blind.
- This is a real inconsistency, but it is non-blocking.

### Final grades
- **INV-001: MEDIUM.** The worse reading is allowed by "near line 161", but it is not the only reading. Stage 3 uses "definition bullets" to include S5, and spec 815 says "where present". Nothing checks the spec requirement, so the exit state can be reached without it. Fix: add one clause to Task 1 naming the S5 bullet near line 140, plus the adjacent S5 in the other three templates. Add an acceptance grep that `CRITICAL and IMPORTANT findings are blocking` prints 0 in `src/superclaude/templates`.
- **INV-002: MEDIUM.** Fix: have Task 4 also edit the line-461 clause so `artifacts` also lists the ledger when it is a tracked path. Re-check the `artifacts`-clause pins in `tests/skills/test_worker_contract.py` before editing.

## Variant 2 advocate (haiku class)

### INV-001
Minor, not blocking. P4:37 says "the definition bullets near line 161" and "in place of the definition bullets". Stage 3:125 explicitly calls S1, S2 AND S5 "the three definition bullets"; thus that term can include S5. But the location is misleading: in agent_template_qa.md, S5 is at 140, while S1-S3 occupy 161-163. A location-led executor could leave it; a definition-led executor would replace it. Neither outcome is compelled.

The coverage weakness is verified. P4:43-49 checks "exactly one fenced digest", merge text, registry state, the S1 sentence, verdict triggers, the Rule 6 label and allow-list removal, not S5 removal. Existing severity-rule tests:196-211 explicitly assert "S5 missing"; stage 3:192 changes v2 rows to digest checks. Stage 1:223 defines T1 as fenced-body equality and T2 around "the old definition sentence or a fence opener". These do not independently catch retained S5.

Spec:790 names S5 separately; :815 requires "replaces S1, S2 and S5"; :737 says it becomes "grade by the three conditions; the label is information".

If retained, S5 would reach newly generated QA agents, not merely be data they review. Digest precedence (:205) therefore does NOT settle this same-agent conflict. Nevertheless, S5 itself says "grade by the definition above, not by the label", including the IMPORTANT-wording exception. The digest (:195-203) supplies the three conditions and says labels are "information, never the grade". Wrong blocking is possible, not demonstrated or inevitable. Under the supplied two-readings rule, this is minor ambiguity.

### INV-002
Real wording conflict, but minor under that same rule. P4:89 adds the ledger and three return keys; stage 2:102 requires the ledger in artifacts "only when it is a tracked path". The unchanged spec-panel:461 says artifacts is "[] otherwise" when Improve did not run.

A literal fixed-list reading omits an eligible ledger. However, the section first requires reading WORKER-CONTRACT; WC-4 defines artifacts as "every other file written", and P4 explicitly imports its new ledger keys. Including the ledger is therefore also supported. The ledger remains directly discoverable through follow_up_ledger; no lost ledger or necessarily wrong downstream result is established. The claimed omission depends on selecting one reading.

### Final grades
INV-001: minor. INV-002: minor. Name S5 explicitly and reconcile the artifacts sentence. Read-only review; no execution or edits.

## Variant 3 advocate (opus class)

### INV-001
Task 1 never tells the executor to replace the S5 bullet at agent_template_qa.md:140. P4:37 lists every place to edit in that file: "the definition bullets near line 161", plus lines 85, 333, 157 and 158. Line 140 is not on that list. It sits under `### Severity Ratings`, 21 lines above the "Review severity rule" block at 161 to 163. In the other three templates the S5 bullet is next to S1 to S3, so "near line X" catches it there.

Stage 3 names S5 every time it asks for this edit:
- Line 125 quotes the opening words of the third bullet ("On a CRITICAL / IMPORTANT / MINOR scale...").
- Lines 140 and 154 say "replace S1, S2 and S5".

Stage 4 never says "S5" and never quotes its sentence. Read literally, the stage 4 text points only at the block at 161, so it leaves S5 in place.

No check would catch this:
- P4:46 greps only for the S1 sentence.
- T1 compares only the fenced digest.
- Strict T2 (P4:108 and 112) looks only for the S1 sentence and the fence.
- Under the stage 3 re-pin (line 192), test_review_severity_rule.py checks `v2` rows against the digest only.

The exit state therefore fails spec line 815 ("replaces S1, S2 and S5 (where present)") and line 737.

What goes wrong: every QA agent built from this template gets two definitions of blocking in its own instructions.
- Digest (spec line 203): the label "is information, never the grade", and a real defect that nothing named rests on is Medium.
- Old S5: "CRITICAL and IMPORTANT findings are blocking ... grade by the definition above". Once the 161 block is replaced, "the definition above" can only mean the domain CRITICAL / IMPORTANT definitions at lines 137 to 139, which grade by label.

The precedence sentence (spec line 205) cannot settle this. It ranks the agent's own instructions over an output style and treats the work under review as data, but here both bullets are the agent's own instructions. So an IMPORTANT finding that nothing rests on can still fail a review and start fix cycles. That is a wrong result, not just ambiguity. The missing check could easily be met: `grep -c "CRITICAL and IMPORTANT findings are blocking"` printing 0 in each of the four templates. Its absence is a coverage gap, not a check that cannot be met.

### INV-002
The defect is real, but nothing is lost.
- spec-panel.md:461 says `artifacts` lists improved-spec.md "and it is `[]` otherwise".
- P4:89 adds `<report-dir>/follow-ups.md` and the `follow_up_ledger` key, but leaves line 461 unchanged.
- Stage 2 line 102 (WC-4) lists the ledger in `artifacts` whenever it is a tracked path.

When the report directory is tracked, the command's own text and the shared contract disagree. The coordinator still finds the file through `follow_up_ledger`, which stage 2 names as a key the coordinator reads, and the command stages nothing. No data is lost, so this is a real weakness that does not block.

### Final grades
- **INV-001: blocking.** A spec requirement (line 815) is unmet with no check to catch it, and the generated QA agents get a contradicting label rule. Fix: add "the S5 bullet near line 140 (Severity Ratings)" to Task 1's list for agent_template_qa.md, and add a check that `grep -c "CRITICAL and IMPORTANT findings are blocking"` prints 0 in all four digest templates.
- **INV-002: MEDIUM.** Fix: in Task 4, amend the Contract bullet so `artifacts` also lists `<report-dir>/follow-ups.md` when it is written and is a tracked path.

## Orchestrator ruling on INV-001 (recorded for the merge)

Grades: V1 MEDIUM, V2 minor, V3 blocking. No two advocates agree, so the point is not decided by majority of identical grades; two of three are non-blocking, and the median grade is MEDIUM. The severity rule makes a finding that needs a guess about two readings minor unless the worse reading is the only one the text allows: the text allows the better reading (stage 3 plan line 125 uses "definition bullets" for S1, S2 and S5; spec line 815), so it is not blocking. It stays above minor because nothing checks the requirement and the worse reading leaves two blocking definitions in one template. Settled grade: MEDIUM. INV-002: V1 MEDIUM, V2 minor, V3 MEDIUM: MEDIUM.
