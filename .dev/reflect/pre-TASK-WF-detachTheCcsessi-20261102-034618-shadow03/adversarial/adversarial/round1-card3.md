# Round 1 — Card 3 (refactorer)

Position summary. The plan is structurally sound — subshell semantics, wait loops, setsid ordering, bash 3.2 constraints verified, no defect there — but it is not a faithful record of what landed: HEAD guards setsid with an isatty check the plan never mentions (my F1), and both opponents missed it. In a deviation audit, plan-vs-code divergence is the primary object; the meetability gaps Cards 1/2 found are secondary symptoms of the same executor improvisation.

Steelman of Card 1. The strongest process-integrity read: full T1-T5 DAG verification (Task 3 ACs correctly still failing until Task 4, setsid validity, bash 3.2, no constraint contradictions) and proof via t5-checks.log ("Drift detected! Run 'make sync-dev' to fix") that T5.AC2 is unmeetable as written, plus the unrecorded T4.AC4 pid baseline. Correct, evidenced, non-blocking.

Steelman of Card 2. The strongest traceability read: full remediation-requirement-to-task mapping, the unique catch that HC1/HC5 Pipeline Hardening items appear in neither the coverage matrix nor the plan — a real coverage hole — plus independent confirmation of the verify-sync gap and the narrowed AC2 grep.

Strengths claimed. 1. F1 (C-005) is the only plan-vs-code finding on the table: plan:52 vs proxy:1013-1020. The executor landed behavior the plan never specified. 2. F2 precisely scoped: anchors drifted but "the quoted statement text still matches". 3. The structural pass means F1/F2 are not false positives from misreading the mechanism.

C-005 response. Card 2's fixture observation supports and strengthens F1: the shim's stderr is a file, so isatty() is False in tests, guarded and unconditional setsid are indistinguishable to the plan's own ACs — the divergence is invisible to the acceptance tests, and under a real tty the landed code skips setsid entirely, a behavior no AC covers. It confirms the minor/non-blocking rating.

Weaknesses in Cards 1/2. Both validated Task 3 by test outcome alone; Card 2's meetability line ("directly_started_shim passes") holds only because the fixture's stderr is not a tty. Card 1's MAJOR on C-001 vs Card 2's MINOR (X-001): the log shows an improvised sync-dev resolved it — a Necessary deviation, so MINOR fits. Card 2's F1 partially misreads HC5: that requirement is discharged by this very audit, not a tasklist step; the HC1 half stands.

Concessions. My pin self-report mismatched (tier1b vs tier1a), same defect as Card 2. Only two findings; missed the verify-sync gap both opponents caught independently.

A-001 ACCEPT. A-002 QUALIFY — artifacts prove consequences (drift, pass counts); the plan text proves omissions; cite both, neither alone.
