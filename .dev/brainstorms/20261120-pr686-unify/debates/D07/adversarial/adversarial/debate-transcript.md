# Adversarial Debate Transcript (D07, topology)

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals), plus Round 2.5 invariant probe. Round 3 is not available at standard depth.
- Convergence achieved: 95.8% (23 of 24 diff points agreed by both advocates after Round 2)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 OURS, Variant 2 CLAY; each a separate agent that read the sources and checked citations)
- Full statements are not copied here; they are on disk in this folder (see below). This file records the sequence, the points and the gates.

| Round | File |
|---|---|
| 1, OURS | round-1-advocate-1-OURS.md |
| 1, CLAY | round-1-advocate-2-CLAY.md |
| 2, OURS | round-2-rebuttal-1-OURS.md |
| 2, CLAY | round-2-rebuttal-2-CLAY.md |
| 2.5 | invariant-probe.md |

## Round 1: Advocate Statements (summary)

### Variant 1 Advocate (OURS)
Position: the topology stays project-local. OURS wins C-001, C-002, C-003, C-008 and X-001; CLAY wins C-004 and parts of C-005, C-007 and C-009 as a hybrid carried into the per-project layout.
Steelman of CLAY: the issue, not the session, is the unit of control; one router under one lock; a fail-closed in-flight count; resume wake; an allow list; `route.py` is real code (603 lines, verified).
Citation checks: about 15 verified. Errors found in OURS: the paper overstates Q26 (owner-answers line 23 says "direction accepted. The naming convention is NOT decided"; Q26's layout is per scope, not one `COORD-<RepoName>`); the git lock acts at push time.
Concessions: unpushed; `.dev/coordinators/` is design only; no in-flight cap, idle end, resume wake or per-repo merge settings.
Shared assumptions: A-001 QUALIFY, A-002 ACCEPT, A-003 QUALIFY, A-004 REJECT, A-005 QUALIFY.

### Variant 2 Advocate (CLAY)
Position: CLAY should not win the topology under the weighting rule. Its real case is separable capabilities: in-flight cap, fail-closed counting, restart with resume, per-repo settings keys, org search as a pre-check.
Steelman of OURS: three owner rulings, one registration act, no `cd` workaround, real dispatcher code.
Weaknesses of OURS found with evidence: no `Coordinator` worktree exists, so `dispatch.py:279-280` returns `worktree_invalid` for every repo today; grep finds no `max_in_flight`, `in_flight` or `.dev/coordinators` in the owner's code; branch naming differs (`coordinators` vs `Coordinator`).
Citation errors found in CLAY: "owner of record" is Clay (DESIGN lines 3 and 11); PR B items are presented as mechanism though PR B does not exist.
Shared assumptions: A-001 QUALIFY, A-002 ACCEPT, A-003 QUALIFY, A-004 QUALIFY, A-005 QUALIFY.

## Round 2: Rebuttals (summary)

### Variant 1 Rebuttal (OURS)
Conceded: the Coordinator worktree is a prerequisite owned by Coder issue 516 (CLAY has an equal prerequisite: an orchestrator clone per host); the owner decided direction, not layout or names; the git create-once lock is real exclusion in design, untested (A-004 moved from REJECT to QUALIFY). Gave adoptable text for the cap, restart, per-repo keys and an org pre-check. Rejected: the 30-minute idle end, extra coordinators started by the poll, `wrong_target`, the separate repo with its allow list, the `cd` workaround.

### Variant 2 Rebuttal (CLAY)
Accepted every rejection and conceded that no part of CLAY's topology still wins (`allowed_owners` is already a list key, so two organizations is one setting; DQ4 `setup-clone` needs a named repo first). Contested the adoptable text: it drops six safety properties of DESIGN 700-718 and `route.py`: count an issue once; write `pending` before any send; an unreadable session list decides nothing; resume only for acknowledged work; bounded restarts; the cap limits new work only, not resends or resume.

## Round 2.5: Invariant Probe (summary)
Fault-finder result: 14 findings, 2 ADDRESSED, 12 UNADDRESSED (5 HIGH, 7 MEDIUM). The orchestrator spot-checked INV-001 (`_precheck` runs before `_run_child` in `dispatch.py`; the orphan sweep `record.sweep` is in the child cycle), INV-002 (`ENTRY_STATES`, `_RESETTABLE` in `record.py`), INV-004 (`launch_argv` starts agents with `--worktree path:<worktree>`) and INV-011 (`launch.py` comment "the config directory is not tamper-protected"): all four hold. HIGH items: INV-001, INV-002, INV-004, INV-005, INV-012. See invariant-probe.md.

## Scoring Matrix

Level = debate taxonomy (L1 surface, L2 structural, L3 state mechanics). Confidence is the mean of the two advocates' final figures, rounded.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | OURS | 55% | Not contested; tie rule |
| S-002 | L2 | OURS (hybrid: per-issue accounting from CLAY) | 55% | Topology by project, counting by issue (C-004 outcome) |
| C-001 | L2 | OURS | 83% | `cd <checkout>` workaround and UNVERIFIED directory premise (DESIGN line 136); origin check in OURS |
| C-002 | L3 | OURS (hybrid: per-issue state file from CLAY) | 65% | Host-local git-ignored registry (DESIGN line 863) vs shared branch; both advocates agree |
| C-003 | L2 | OURS (optional org pre-check, fail-open) | 70% | `orca repo list` verified under cron (REQ R21); org search saves calls only at scale |
| C-004 | L3 | CLAY (hybrid, with six safety properties) | 85% | No cap in OURS (grep zero hits); `route.py` count rules |
| C-005 | L3 | SPLIT: restart with guards CLAY, idle end OURS | 73% | REQ R9 requires a standing session; restart needs guards (INV-005) |
| C-006 | L2 | OURS | 73% | `CALL_CAP` is per cycle and OURS runs a cycle per repo; allow list holds 3 repos |
| C-007 | L2 | CLAY (hybrid keys) | 67% | Settings table has no home in OURS; tamper risk INV-011 |
| C-008 | L2 | OURS | 83% | Orchestrator clone per host (DESIGN 866, 893) vs REQ R17 |
| C-009 | L3 | OURS (design, untested) | 55% | Git push-time lock vs host-local `O_EXCL` |
| C-010 | L1 | OURS | 75% | Naming belongs to the owner decision (D08); tie rule |
| C-011 | L2 | OURS | 55% | Dispatcher code exists (unpushed); PR 686 has no reader |
| C-012 | L2 | OURS | 65% | `allowed_owners` is a list key (`defaults.py`) |
| X-001 | L2 | OURS | 75% | DESIGN lines 3 and 11 name Clay as "the owner"; direction only is the owner's |
| X-002 | L2 | OURS | 70% | Skip reasons exist (`SKIP_REASONS`) |
| X-003 | L2 | OURS | 65% | `issue-watch.d/<repo>.json` can hold keys |
| X-004 | L1 | OURS | 70% | The label hides many orchestrators per repo (DESIGN lines 700, 706) |
| X-005 | L1 | UNRESOLVED | 50% | `coordinators` vs `Coordinator`: an open owner decision |
| A-001 | L3 | QUALIFY (both) | n/a | One host today; spec states the git claim as the upgrade path |
| A-002 | L2 | ACCEPT (both) | n/a | Six Orca repos, three allow-listed; budget not binding |
| A-003 | L3 | QUALIFY (both) | n/a | Tag detection UNVERIFIED (U25) |
| A-004 | L3 | QUALIFY (both) | n/a | `O_EXCL` one host; git lock acts at push |
| A-005 | L3 | QUALIFY (both) | n/a | Org search fails closed at 100; pre-check must fail open |

## Convergence Assessment
- Points resolved: 23 of 24 (X-005 unresolved by design)
- Alignment: 95.8%
- Threshold: 80%
- Taxonomy coverage gate: L1 (S-001, C-010, X-004, X-005), L2 and L3 all covered: PASS
- Invariant probe gate: FAIL. Five HIGH UNADDRESSED invariants (INV-001, INV-002, INV-004, INV-005, INV-012).
- Status: BLOCKED_BY_INVARIANTS (diff-point agreement is above threshold). Standard depth has no Round 3, so the pipeline proceeds under the no-convergence path: force-select by score, record the blocking items, status partial. The recommendation must carry each blocking item as a stated requirement of the winning design (see refactor-plan.md).
- Unresolved points: X-005
- Warnings (MEDIUM, not blocking): INV-003, INV-006, INV-007, INV-008, INV-009, INV-010, INV-011
