# Validation Report
Generated: 2026-05-13
Roadmap: `.dev/releases/current/release-split-workspace-rca/roadmap/roadmap.md`
Phases validated: 5
Agents spawned: 10 (2 per phase)
Total findings: 14 (High: 0, Medium: 7, Low: 7)

## Findings

### High Severity

None.

### Medium Severity

#### M1. T02.01 -- Verbatim message uses em-dash in source; tasklist renders double-hyphen
- **Severity**: Medium
- **Affects**: `phase-2-tasklist.md` / T02.01
- **Problem**: The roadmap source for D2.1 uses an em-dash (U+2014) in the runtime message: `"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."`. The tasklist Why field and Step 3 render the same string with `--` (double hyphen).
- **Roadmap evidence**: roadmap.md line 106.
- **Tasklist evidence**: phase-2-tasklist.md Why field and Step 3.
- **Exact fix**: Replace `--` with em-dash `—` in T02.01 Why field and Step 3 so the verbatim runtime-message wording matches the roadmap.

#### M2. T02.01 -- Acceptance criterion only checks substring, not full verbatim message
- **Severity**: Medium
- **Affects**: `phase-2-tasklist.md` / T02.01
- **Problem**: The first acceptance criterion checks only that the substring `"Move to .dev/eval-workspaces/"` appears. It does not assert that the full verbatim message (including `<name> has no SKILL.md — not a skill, must not live in .claude/skills/.`) is emitted.
- **Roadmap evidence**: roadmap.md line 106 specifies the entire message verbatim.
- **Tasklist evidence**: phase-2-tasklist.md T02.01 first AC bullet.
- **Exact fix**: Strengthen AC to assert the full verbatim string (with em-dash) appears in `make verify-sync` output.

#### M3. T02.02 -- Acceptance criterion only checks substring, not full verbatim message
- **Severity**: Medium
- **Affects**: `phase-2-tasklist.md` / T02.02
- **Problem**: The first acceptance criterion checks only the substring `"Workspace directories belong under"`. The roadmap specifies the full message: `"Workspace directories belong under \`.dev/eval-workspaces/\`, not \`.claude/skills/\`."`.
- **Roadmap evidence**: roadmap.md line 107.
- **Tasklist evidence**: phase-2-tasklist.md T02.02 first AC bullet.
- **Exact fix**: Strengthen AC to assert the entire verbatim string (including `, not \`.claude/skills/\``) appears in output.

#### M4. T04.03 -- DEP-005 SOFT dependency not explicitly enforced in checkpoint Verification/Exit Criteria
- **Severity**: Medium
- **Affects**: `phase-4-tasklist.md` / T04.03
- **Problem**: The checkpoint Verification bullet 2 only checks `make sync-dev` + `make verify-sync` exit cleanly. It does not assert that the M2-specific error messages (D2.1 context-aware + D2.2 workspace blocklist) are operational, which DEP-005 ties to M4 done-state.
- **Roadmap evidence**: roadmap.md line 84.
- **Tasklist evidence**: phase-4-tasklist.md T04.03 Verification and Exit Criteria.
- **Exact fix**: Append a DEP-005 clause to T04.03 Verification bullet 2 (preserving the exactly-3-bullets structural rule).

#### M5. T05.04 -- AC underspecified for PLANNING.md/TASK.md absence semantics
- **Severity**: Medium
- **Affects**: `phase-5-tasklist.md` / T05.04
- **Problem**: AC asserts only that `KNOWLEDGE.md` exists. It does not affirmatively check that an unexpected `PLANNING.md`/`TASK.md` match would cause failure.
- **Roadmap evidence**: roadmap.md line 146 and SC-004 line 180.
- **Tasklist evidence**: phase-5-tasklist.md T05.04 ACs.
- **Exact fix**: Add an AC asserting that any unexpected `PLANNING.md`/`TASK.md` match in the grep output FAILS the test.

#### M6. T05.05 -- Invented prior-run comparison + tolerance requirement
- **Severity**: Medium
- **Affects**: `phase-5-tasklist.md` / T05.05
- **Problem**: Roadmap D5.5 states only "Verify no regression". The task invents a structured "prior run" comparison with tolerance classification that exceeds roadmap scope and may not be operationally achievable if no prior baseline exists.
- **Roadmap evidence**: roadmap.md line 147 (D5.5).
- **Tasklist evidence**: phase-5-tasklist.md T05.05 Deliverables, Steps 5-6, AC bullets 1-3.
- **Exact fix**: Soften ACs to require valid-output exit 0; mark prior-run comparison as conditional (N/A if no baseline).

#### M7. T05.06 -- Explicit SC-### mapping omitted; some SCs not exercised by D5.1-D5.5
- **Severity**: Medium
- **Affects**: `phase-5-tasklist.md` / T05.06
- **Problem**: Checkpoint Verification covers AC1-AC5 but does not enumerate SC-001..SC-005 individually. SC-003 (`superclaude install` clean) and SC-005 (`make verify-sync` clean after `make sync-dev`) are NOT directly exercised by T05.01-T05.05.
- **Roadmap evidence**: roadmap.md lines 177-181 (SC-001 through SC-005).
- **Tasklist evidence**: phase-5-tasklist.md T05.06 Verification + Exit Criteria + AC.
- **Exact fix**: Add a T05.06 Step instructing the checkpoint report to map each SC-001..SC-005 to evidence task(s) AND status, with explicit SC-003 (`superclaude install` in a probe clone -> no `*-workspace/` under `.claude/skills/`) and SC-005 (`make sync-dev && make verify-sync` exits 0 with no drift) sanity checks.

### Low Severity

#### L1. T01.04 -- DEP-001 not named explicitly in Exit Criteria
- **Severity**: Low
- **Affects**: `phase-1-tasklist.md` / T01.04
- **Problem**: Exit Criterion 3 paraphrases DEP-001 without naming the identifier.
- **Roadmap evidence**: roadmap.md line 80 (DEP-001).
- **Tasklist evidence**: phase-1-tasklist.md T01.04 Exit Criteria bullet 3.
- **Exact fix**: Prefix the bullet with "DEP-001 satisfied:".

#### L2. T02.02 -- Tie-breaker rule citation lacks inline rationale
- **Severity**: Low
- **Affects**: `phase-2-tasklist.md` / T02.02
- **Problem**: Notes cites "Section 4.9 tie-breaker rule 4" without inline rationale.
- **Roadmap evidence**: roadmap.md line 107.
- **Tasklist evidence**: phase-2-tasklist.md T02.02 Notes.
- **Exact fix**: Quote the rule and apply it inline (lint-architecture vs verify-sync interface-change comparison).

#### L3. T02.03 -- Step 4 invents branch-protection requirement outside roadmap scope
- **Severity**: Low
- **Affects**: `phase-2-tasklist.md` / T02.03
- **Problem**: Step 4 instructs "Set the job as a required check for PR merge". Roadmap D2.3 only requires CI to fail on drift.
- **Roadmap evidence**: roadmap.md line 108 (D2.3).
- **Tasklist evidence**: phase-2-tasklist.md T02.03 Step 4.
- **Exact fix**: Convert Step 4 to informational note (out-of-scope for this task).

#### L4. T02.03 -- AC does not explicitly assert merge-blocking semantic
- **Severity**: Low
- **Affects**: `phase-2-tasklist.md` / T02.03
- **Problem**: AC asserts workflow failure but not the PR-merge-blocking semantic directly.
- **Roadmap evidence**: roadmap.md line 108.
- **Tasklist evidence**: phase-2-tasklist.md T02.03 ACs.
- **Exact fix**: Add AC: failing required workflow status equates to a blocked merge (or repo-admin follow-up note recorded).

#### L5. T03.03 -- Unset-SKILL handling is operational addition beyond roadmap
- **Severity**: Low
- **Affects**: `phase-3-tasklist.md` / T03.03
- **Problem**: Roadmap D3.3 does not require an unset-SKILL error case; the task adds it.
- **Roadmap evidence**: roadmap.md line 122 (D3.3).
- **Tasklist evidence**: phase-3-tasklist.md T03.03 Deliverables, ACs.
- **Exact fix**: Annotate in Notes as "operational hardening beyond roadmap D3.3 scope".

#### L6. T05.06 -- Loopback target not explicitly named
- **Severity**: Low
- **Affects**: `phase-5-tasklist.md` / T05.06
- **Problem**: Exit Criterion 3 says "loops back per the discovery-risk handling in the roadmap" without naming M2/M3.
- **Roadmap evidence**: roadmap.md line 149.
- **Tasklist evidence**: phase-5-tasklist.md T05.06 Exit Criterion 3.
- **Exact fix**: Name M2/M3 explicitly.

#### L7. T01.02 -- AC line-number references brittle to source-file drift
- **Severity**: Low
- **Affects**: `phase-1-tasklist.md` / T01.02
- **Problem**: AC locks to "lines 51-53 and 225-227" which is brittle if CLAUDE.md has drifted since the roadmap was written.
- **Roadmap evidence**: roadmap.md line 95.
- **Tasklist evidence**: phase-1-tasklist.md T01.02 AC bullet 3.
- **Exact fix**: Add "match by content (PLANNING/TASK references), not by line number" qualifier.

## Verification Results
Verified: 2026-05-13
Patch execution: applied inline by the tasklist-protocol orchestrator (sc:task delegation skipped because the 14 edits are deterministic Edit-tool operations with no decision logic required; rationale documented per Stage-9 short-circuit pragmatic deviation).
Findings resolved: 14/14

| Finding | Status | Notes |
|---------|--------|-------|
| M1 | RESOLVED | T02.01 Why field and Step 3 now use em-dash `—` matching roadmap line 106 verbatim (verified via grep `no SKILL.md —`). |
| M2 | RESOLVED | T02.01 AC bullet 1 now asserts full verbatim message including em-dash (verified via grep `em-dash exact`). |
| M3 | RESOLVED | T02.02 AC bullet 1 now asserts full verbatim message including `, not .claude/skills/.` clause (verified via grep on phase-2 line 96). |
| M4 | RESOLVED | T04.03 Verification bullet 2 now includes DEP-005 clause (M2 D2.1/D2.2 messages on probe inputs OR M4 waiver). Structural rule preserved (still exactly 3 Verification bullets). |
| M5 | RESOLVED | T05.04 ACs now include explicit FAIL assertion for unexpected PLANNING.md/TASK.md matches. |
| M6 | RESOLVED | T05.05 ACs 1+2 softened: valid-output exit 0 required; prior-run comparison conditional with N/A fallback when no baseline. |
| M7 | RESOLVED | T05.06 Step 2 now enumerates SC-001..SC-005 mapping with explicit SC-003 (`superclaude install` probe) and SC-005 (`make sync-dev && make verify-sync`) sanity checks. |
| L1 | RESOLVED | T01.04 Exit Criterion 3 prefixed with `DEP-001 satisfied:`. |
| L2 | RESOLVED | T02.02 Notes now includes inline tie-breaker rationale (lint-architecture vs verify-sync interface-change comparison). |
| L3 | RESOLVED | T02.03 Step 4 converted to informational out-of-scope note. |
| L4 | RESOLVED | T02.03 ACs include merge-blocking semantic with `mergeable=false` evidence OR repo-admin follow-up note. |
| L5 | RESOLVED | T03.03 Notes now annotates unset-SKILL handling as "operational hardening beyond roadmap D3.3's literal scope". |
| L6 | RESOLVED | T05.06 Exit Criterion 3 now names "M2 and/or M3" as loopback target per M5 Risk Assessment. |
| L7 | RESOLVED | T01.02 AC bullet 3 now matches by content (`PLANNING.md`/`TASK.md` references) rather than by absolute line number; original line refs retained as informational annotation. |

No regressions detected in surrounding context. No further patch cycles required. The tasklist bundle is ready for execution via `superclaude sprint run`.
