# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

Fault-finder: the debate coordinator (this session), acting as an independent reader of the emerging consensus. Consensus probed: one role noun "coordinator"; command `/sc:coordinator`; skill `sc-coordinator-protocol`; species terms "person-opened coordinator" and "standing-grant coordinator"; session name and tag `COORD-<RepoName>`; Clay's flags kept; persisted wire names renamed before PR 686 merges; "orchestrator" kept only for Orca's layer, the 63 parent-session files, proper names and quotes. Evidence read: round1 and round2-advocate-1 files, diff-analysis.md, D06 and D07 VERDICT.md, master `core/CLAUDE.md:58`, `tests/core/test_orca_session_launch_guidance.py:33,36,53`, `agent-work-report/config.json:11-12`. No branch-trace.md exists for this debate; the sufficiency finding uses an inline enumeration.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | A flag-less `/sc:coordinator` means "person-opened, no grants" and grants arrive only through `--wake`, `--hourly`, `--resume`, `--take` | UNADDRESSED | HIGH | Advocate 1 R2 point (6) says the owner's R17 start from a launch prompt is "a third route". D06 verdict item 6 allows a script-started coordinator whose launch prompt cites an owner authorization. So grants can arrive with no flag, and a flag can arrive without any grant. The consensus ties authority to the command line, not to the recorded authorization. |
| INV-002 | state_variables | Session name and ccsession tag are one string, `COORD-<RepoName>`, 32 characters at most | ADDRESSED | MEDIUM | Round 2 A1 point (1): `launch.py:39` TAG_PATTERN allows uppercase, 32 characters; truncation collisions refused. D07 verdict removes extra sessions per repo, so the `-<n>` suffix is unused. Whether `COORD-<RepoName>` is a ccsession tag or only an Orca terminal name is UNVERIFIED (Coder 516 unread). |
| INV-003 | interaction_effects | Editing `core/CLAUDE.md:58` and `ccsession-tag/README.md:423` is a small text change | UNADDRESSED | MEDIUM | `tests/core/test_orca_session_launch_guidance.py:33` requires "coordinator is person-opened" in both files; line 53 requires both "orchestrator" and "coordinator" in the paragraph. D06 and D03 also edit WORKER-CONTRACT line 70 and 245 on the same sentence family. Three changes touch one pinned sentence, so order matters. |
| INV-004 | interaction_effects | The records branch `coordinators` (Q26, exists on the fork) and the working branch and worktree `Coordinator` (R10) are different things | UNADDRESSED | MEDIUM | D07 verdict item 10 hands the branch-name choice to D08. Neither advocate decided it. R10 uses `Coordinator` for the worktree where the session works; Q26 uses `coordinators` for the shared records branch. On a case-insensitive host the two differ only by a trailing "s", so they do not clash, but a reader will confuse them. |
| INV-005 | state_variables | The report session tag `coordinator` and project sessions `COORD-<RepoName>` never match the same prefix test | ADDRESSED | MEDIUM | A1 R2 point (3): no prefix consumer found in master src. UNVERIFIED for the IronFlow repo and for hooks outside src. |
| INV-006 | sufficiency_challenge | Renaming wire strings, keys and folders "before PR 686 merges" settles the naming | UNADDRESSED | MEDIUM | Enumeration of what the claim needs: (a) PR 686 is still open, so a rename lands in that PR or in a rewrite chosen by D14; (b) installed copies on other hosts keep old text until next install (FULL-REPORT section 3); (c) the design doc on master (759 uses of "orchestrator") is already merged and needs its own edit PR; (d) Clay's open PRs 689 and 690 and Clay's local branches may use the word. The consensus covers (a) only. |
| INV-007 | collection_boundaries | One coordinator per project; zero or several per repo are out of scope | ADDRESSED | LOW | D07 verdict: cap is per coordinator id, nothing starts extra sessions. Zero sessions: `worktree_invalid` until Coder 516 lands (D07 item 9). |
| INV-008 | count_divergence | Counts quoted by the advocates measure spread | ADDRESSED | LOW | Both advocates agreed in R1 and R2 to state lines, files or occurrences each time. |
| INV-009 | guard_conditions | A pinned test can enforce "orchestrator allowed only for uses (a) to (e)" | UNADDRESSED | LOW | A1 R2 point (7) marks feasibility UNVERIFIED. The 63 installed files use the word legitimately, so the test must be scoped to the new files only. |

## Summary

- **Total findings**: 9
- **ADDRESSED**: 4
- **UNADDRESSED**: 5
  - HIGH: 1 (INV-001)
  - MEDIUM: 3 (INV-003, INV-004, INV-006)
  - LOW: 1 (INV-009)

Gate: INV-001 blocks convergence until resolved. Resolution adopted by the judge in VERDICT.md (recorded in base-selection.md): authority comes only from a recorded owner authorization (the grant row or the authorization cited in the launch prompt, D06 items 6 and 7), never from the command, its flags or the session name. Flags choose what the session does; the authorization decides what it may do. INV-003, INV-004 and INV-006 become actions in the verdict. INV-009 becomes an unverified item.
