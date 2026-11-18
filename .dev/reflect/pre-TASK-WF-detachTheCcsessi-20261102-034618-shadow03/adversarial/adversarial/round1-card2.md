# Round 1 — Card 2 (qa)

Position summary. My card's value is traceability: I mapped every spec requirement to a task and caught the one requirement class nobody else traced — Pipeline Hardening HC1/HC5 (my F1) — plus a silent narrowing of a verification command (my F3). Both opponents read the plan's mechanics well but did not audit spec-to-plan coverage.

Steelman of Card 1. Card 1 did the deepest dependency analysis: task ordering, setsid semantics, bash 3.2 subshell compatibility, constraint contradictions. Its F1 is the same defect I found (F2) but graded medium with stronger evidence — the actual t5-checks.log:28 line proves the criterion fails without an unplanned step, where I cited only the plan text. Its F2 (unrecorded pid baseline) and F4 (pgrep cannot match the exec'd sleep) are execution-level defects my QA lens missed.

Steelman of Card 3. Card 3 is the only card that compared plan-literal instructions against HEAD code and found the isatty guard (F1): following the plan as written does not produce the landed code. That is the single sharpest plan-fidelity finding in the set, and its structural pass was rigorous even though it yielded no finding.

Strengths claimed. 1. F1 (U-002, Medium, unique): HC1/HC5 absent from matrix and tasklist — the largest coverage hole; quoted remediation-source.md:35 "HC5: off-path review required". 2. F3 (U-003, unique): T5's grep drops `SKILL_DIR / "ccsession"` silently — a narrowed acceptance check. 3. F2: verify-sync gap independently confirmed with both plan and spec refs (C-001). 4. Meetability analysis (Task 3 alone passes directly_started_shim, outlives still fails as T3 AC expects) — no other card tested satisfiability.

Weaknesses in Cards 1/3. Card 1: missed HC1/HC5 entirely; F2 rests on a single plan-text quote, thin for medium. Card 3: only two findings, no coverage audit, and labels HEAD code as "role: spec" — a citation-category error; "no defect found" after examining two hunks is a narrow search, not a clean bill.

Concessions. My self-report mismatched the pin (tier1b vs tier2), weakening my heterogeneity claim. X-001 likely resolves toward Card 1's medium — the criterion is unmeetable as written. I missed C-002 and C-005, both real. F1 may overreach: HC5 could be satisfied by this very review rather than a tasklist item.

A-001: ACCEPT. A-002: ACCEPT.
