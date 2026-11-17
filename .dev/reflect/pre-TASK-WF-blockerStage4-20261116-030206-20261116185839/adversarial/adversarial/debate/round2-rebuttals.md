# Round 2: rebuttals (sequential: V1, V2, V3 advocates)

## V1 advocate (sonnet)

Response: conceded C-003 Medium (the digest can supply both strings, so the greps pass without the rewrite; detection weak, nothing unmeetable); conceded C-004 Medium (S3:177 rewrites Rule 6, S3:183 checks only "that's never minor", so `rf-qa-qualitative.md:990` heading can survive; P4:49 then halts visibly); graded C-007 Medium; moved C-009 from minor to Medium; withdrew "proves nothing" and "natural reading".

Re-check: C-001: `agent_template_qa.md:163` is the cap bullet and P4:39 puts S1/S2 "near lines 161 to 163", so folding gives 1, keeping gives 2 and halts visibly; both readings available, Medium, fix is one sentence. C-006/X-002: BRIEF:16 "Do not create any new plugin surface ... no plugin parity test (T15)", same line and Q:44, Q:83 say the owner has not confirmed removing parity; SPEC:948 lists the mirror; P4:23 and P4:129 disclose; owner-tracking item, minor. C-007: SPEC:867 row tagged [E]; SPEC:948 exit condition is "drift tests green and strict; a second audit window clear"; P4:26 and P4:135 record it; Medium. C-009: SPEC:739's mapping column says "CRITICAL: Blocking"; spec instruction partly delivered, reason unrecorded in Constraints; P4:93 narrows the always-CRITICAL sentence; Medium.

Updated grades: C-001 Medium (changed), C-003 Medium, C-004 Medium (changed), C-006 minor owner-tracking, C-007 Medium, C-008 Medium (changed, top of the range), C-009 Medium (changed), overall PASS with Medium findings.

New evidence: `agent_template_qa.md:140` is S5 apart from the 161-163 block; the cap sentence also at `agent_template_qa.md:190` and `:341` (HALT lines, unaffected by the fold); S3:177/S3:183 leave C-004 a real cross-stage gap.

## V2 advocate (haiku)

Response: withdrew blocking on C-006, C-007 and C-009; kept C-003 Medium. Acknowledged BRIEF:11-16 ("Shared design decisions ... do not reopen them", "Do not create any new plugin surface") and Q:44 ("This is not a decision to remove plugin parity"), Q:80-85 (plan author's decisions, not owner confirmation); the earlier argument treated every difference from the original spec as an undelivered requirement.

Re-check: C-006 is a recorded planning decision, owner confirmation outstanding (minor tracking item). C-007 is an explicit exclusion with an owner-facing open item (P4:26 "recorded so the exclusion is a decision"; P4:129-135), unresolved spec alignment: Medium. C-009 is a documented choice (P4:90), leaves an inconsistency with SPEC:739's narrowing instruction: Medium, blocking overstated.

Updated grades: C-001 Medium (changed: folding permitted but insufficiently explicit), C-003 Medium, C-004 Medium, C-006 minor (changed), C-007 Medium (changed), C-008 Medium, C-009 Medium (changed), overall PASS with Medium findings (changed).

## V3 advocate (opus)

Response: F1 blocking grade conceded wrong (keeping the bullet is not the only allowed reading); C-003 and C-004 raised to Medium; conceded the missed C-008 prompt lines, C-009 and two C-010 items; corrected V1: the reason for keeping "CRITICAL is blocking" is recorded at P4:90 ("because the mapping test pins them"), just not in Constraints.

Re-check: (i) C-009 Medium: SPEC:739 maps "CRITICAL: Blocking" and asks to narrow it; P4 delivers only the second half (P4:93); narrowing would change one case (a CRITICAL-labelled finding meeting none of the three conditions becomes Medium); keeping it over-blocks, bounded by the cap of 2 fix cycles, cannot cause a false PASS or data loss; the pin reason is weak (P4:98 re-pins other literals of the same test; test_review_severity_mapping.py:55); `spec-panel.md:259` then reads "grade by consequence, not by label; CRITICAL is blocking". (ii) C-008 Medium: automated_qa:125 and doc_code:206 sit in the "Anti-Hallucination & Quality Gate Standards" block beside the file-existence checklist, so they grade worker items; P4:61 says mechanical item rules stay ("and the like" can cover them); but automated_qa:125 repeats the doubt defect of principle 8 at line 20 that P4 rewrites, so the file would contradict itself; same for skill_template.md:834. (iii) C-001 Medium: nothing forces keeping the bullet; P4:39 "the bullets near lines 161 to 163" includes the line 163 cap bullet; the P4:45 check greps "HALT and escalate", which line 163 does not contain; "Do not touch any cap sentence" (P4:75) is in Task 3 and covers only its four skill files.

Updated grades: C-001 Medium; C-002 minor; C-003 Medium; C-004 Medium; C-005 minor; C-006 minor (owner-tracking); C-007 Medium (changed); C-008 Medium; C-009 Medium (changed); C-010 minor; C-011 minor; X-001 Medium; X-002 minor; X-003 Medium; S-001 PASS with Medium findings.

Not checked: the generic and complex MDTM templates' layout (taken from Round 1).
