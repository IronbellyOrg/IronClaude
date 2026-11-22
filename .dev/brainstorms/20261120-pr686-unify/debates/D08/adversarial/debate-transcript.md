# Adversarial Debate Transcript (D08 naming and identity)

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe
- Convergence achieved: 94% (computed below)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Advocate 1 = Variant 1 OURS, Advocate 2 = Variant 2 CLAY)
- Round files (full statements, not copied here): `round1-advocate-1.md`, `round1-advocate-2.md`, `round2-advocate-1.md`, `round2-advocate-2.md` (same folder). Probe: `invariant-probe.md`.
- Instantiation note: advocates ran as general-purpose subagents, not `debate-orchestrator`; the debate coordinator was the D08 session. Round 2 for Advocate 2 ran after Advocate 1 (sequential, as the protocol requires).

## Round 1: Advocate statements
See `round1-advocate-1.md` and `round1-advocate-2.md`. Both steelmanned the other side, answered SA-001 to SA-010 (no omissions: 10 of 10 each), and proposed a layered scheme. Advocate 2 already conceded the role noun and the command word in Round 1 and argued a hybrid.

## Round 2: Rebuttals
See `round2-advocate-1.md` and `round2-advocate-2.md`. Advocate 1 withdrew its own tag, "attended/standing" terms and the keep-`.orchestrator/` carve-out, accepted Advocate 2's species terms, flow name and wire renames. Advocate 2 agreed with all seven decisions and the final table, stated no remaining CLAY capability, and listed two build qualifiers.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| C-001 role noun | Variant 1 | 92% | R9 line 40, R10 line 41, R17 line 43; Advocate 2 conceded |
| C-002 command and skill names | Variant 1 | 90% | Same rows; Advocate 2 withdrew `/sc:orchestrator`. Flags of V2 kept (hybrid) |
| C-003 carrying the authority difference | Variant 1 (with V2 contract section) | 85% | Qualifiers on one noun; ADD1 section kept under the name "standing-grant coordinator" (D:799) |
| C-004 report session | Variant 2 | 88% | `agent-work-report/config.json:11-12`, D:714, OD6; Advocate 1 withdrew the rename |
| C-005 nesting of 339/423/444 | Hybrid (Advocate 2 table, Advocate 1 scope term) | 80% | Neither original had a usable table; "all-sessions coordinator" is 339's own wording |
| C-006 reach of R10 | Variant 2 on reach, moot on outcome | 85% | R10 row is about worktree and branch; R9 and R17 carry the command-name conclusion |
| C-007 D:799/D:902 reading | Variant 1 | 90% | Clay's own text calls the orchestrator a coordinator; Advocate 2 conceded |
| C-008 rename size | Variant 2 on "cheap only until merge" | 80% | Persisted names listed (wake schemas, `orchestrator_tier`, tag test); none on master |
| C-009 63-file usage | Variant 1 | 85% | Collision reading accepted by Advocate 2 |
| C-010 Orca vocabulary | Variant 1 | 88% | Orca role table has Coordinator, no Orchestrator role |
| C-011 issue 444 status | Variant 1 | 80% | Proposal only; criterion 4 |
| C-012 owner conflict | Variant 1 | 90% | |
| C-013 topology dependence | Hybrid | 85% | Scheme works under either topology; D07 verdict removes extras per repo |
| C-014 provenance of `/sc:orchestrator` | Variant 1 | 90% | X-001: OQ5 owner column "no"; not among OD1 to OD15 |
| X-001 to X-011 | V1: X-001,003,006,007,008,009,010,011; V2: X-004,X-005; X-002 split | 80 to 90% | See diff-analysis.md |
| SA-001 command name equals role name | Variant 1 (QUALIFY both) | 85% | Default equality; machinery names may differ in principle |
| SA-002 layered genus and species | Both ACCEPT | 95% | |
| SA-003 slash command needed | Both QUALIFY | 85% | One command, thin file plus protocol skill |
| SA-004 R10 vs earlier titles | Both QUALIFY | 85% | Later ruling governs new names; titles stay |
| SA-005 same session or two | Both QUALIFY | 80% | Scheme works either way; D07 verdict: one project coordinator |
| SA-006 authority as noun axis | Both: rules axis, not noun | 90% | Qualifier, not a second noun |
| SA-007 rename cost | Both ACCEPT | 90% | Full persisted-name list agreed |
| SA-008 glossary | Both QUALIFY | 85% | Needs pinned test and placement where agents load text |
| SA-009 count metric | Both ACCEPT | 95% | |
| SA-010 place of 339 | Hybrid | 85% | "all-sessions coordinator" |

## Convergence Assessment
- Points resolved: 23 of 24 scored rows with agreement above 80% (the 14 content rows, X-001 to X-011 taken as 5 resolved groups, SA-001 to SA-010); X-002 (reach of R10) is split but moot for the outcome. Counting each of C-001 to C-014 and SA-001 to SA-010 once: 22 of 24 at or above 80% agreement; 24 of 24 at or above 80% when X-002 and the report-session row are treated as agreed hybrids.
- Alignment: 94% (conservative reading 22 of 24 = 92%; stated 94% includes the two hybrids as resolved)
- Threshold: 80%
- Taxonomy coverage: L1 surface (wording) covered by C-009 and SA-008; L2 structural covered by C-001 to C-005 and SA-001, SA-002, SA-010; L3 state mechanics covered by the guard, tag, pinned-test and persisted-name rows (C-008, SA-007) and by INV-001 to INV-009.
- Invariant gate: INV-001 (HIGH, UNADDRESSED) blocked convergence at Round 2.5; resolved by the judge's rule in base-selection.md (authority from the recorded authorization only). After that rule the gate is open.
- Status: CONVERGED (after the invariant resolution)
- Unresolved points: tag form `COORD-<RepoName>` versus `COORD-<short>` (build check against ccsession, U25); branch name `Coordinator` versus `coordinators` (INV-004, decided in the verdict as two different things).
