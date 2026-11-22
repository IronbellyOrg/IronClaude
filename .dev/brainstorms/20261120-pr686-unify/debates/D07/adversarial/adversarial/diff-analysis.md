# Diff Analysis: Topology Position Paper Comparison (D07)

Variant A = variant-1-original.md (OURS). Variant B = variant-2-original.md (CLAY).

## Metadata
- Generated: 2026-11-20
- Variants compared: 2
- Total differences found: 37
- Categories: structural (2), content (12), contradictions (5), unique (13), shared assumptions (5)
- Convergence denominator (S + C + X + A): 24

## Structural Differences

| # | Area | Variant A (OURS) | Variant B (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Section order | Abbreviation key, claim, mechanism, cited facts, cost, risk, "gets right" | Same order, but "gets right" is a list of design qualities, not a concession list | Low |
| S-002 | Organising unit | Argues from the project (one project, one coordinator, one config) | Argues from the issue (one issue, one count, one state file, one orchestrator) | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Where the session runs | In each project's `Coordinator` worktree, session `COORD-<RepoName>` (REQ R9, R10, R17) | In a workspace of the separate orchestrator repo; claim needs `cd <checkout> &&` (DESIGN ADD2, line 136) | High |
| C-002 | Where state and records live | `.dev/coordinators/` on a shared git branch; create-once claim files (Q26) | `.orchestrator/` git-ignored in the orchestrator repo: registry, per-issue state files, wakes (DESIGN line 863) | High |
| C-003 | Discovery of repos and issues | `orca repo list`, auto-generated per-repo config, one cycle per repo (REQ R5, R8, R16) | One search per (login, org), filtered by hand-kept `repos.yaml` allow list (DESIGN ADD3, 4.4) | High |
| C-004 | Concurrency and in-flight cap | One launch per sweep, per-repo day cap, claim files; no per-coordinator cap | `max_in_flight` 3, in-flight count from state files and store, extra orchestrator per repo when full (DESIGN 5.7) | High |
| C-005 | Session lifecycle | Standing session per project, restarted if stopped, checked at boot and each run (Coder 516) | Ends after 30 idle minutes; a dead one with work in flight is restarted with a resume wake (DESIGN line 710) | Medium |
| C-006 | The 65-call budget argument | Per-cycle budget is per repo, so it does not sum (REQ R5; `CALL_CAP = 35`, `github.py` line 46) | A per-repo list needs up to 65 calls against 35 (DESIGN line 137) | Medium |
| C-007 | Per-repo settings after the claim | Not specified (merge method, reviewers, role, safety files) | Table of keys per repo in `repos.yaml` (DESIGN lines 879-889) | Medium |
| C-008 | Setup burden | Nothing manual (REQ R17); Orca registration is the only act | Orchestrator repo clone and its absolute path on each host; `repos.yaml` kept by orchestrator verbs on the user's word (DESIGN lines 866, 893, 302) | High |
| C-009 | Cross-host and cross-developer exclusion | Git create-once claim file, enforced at push (Q26 proposal B) | `O_EXCL` state file on one host; claim lease comment as last layer for two hosts (DESIGN line 708) | Medium |
| C-010 | Names | `COORD-<RepoName>`, `Coordinator` (also `coordinators` branch) | `orchestrator-<short>-<n>`, ids `<short>-<n>` | Low |
| C-011 | Maturity | `dispatch.py` 479 lines, `test_dispatch.py` 31 test functions, unpushed on the owner's branch | `route.py` 603 lines in open PR 686; PR B (reader) not written; design merged by PR 681 | Medium |
| C-012 | Organisation scope | Orca-registered repos of the owner's organization; foreign-owner repos skipped (REQ R15) | Two organizations (`IronbellyOrg`, `IronbellyGroup`) through `orgs`; unlisted repos become information entries | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Who decided the topology | The owner (login `ironbelly`) decided it on 2026-11-14 and 2026-11-18 (Q26, REQ R16) | "Decided" by ruling 8 and OD8 of 2026-11-19, rulings that the analysis files attribute to `clayphi` (G-history line 42) | High |
| X-002 | "Seen but not allowed" | CLAY paper says an Orca-registered list has no equivalent. OURS has per-repo skip reasons `not_enabled`, `config_invalid`, `origin_mismatch`, `label_missing` and a first-run check that leaves a failing repo `enabled: false` (`dispatch.py` SKIP_REASONS; REQ R14, R18) | An unlisted repo is skipped and shown as an information entry (DESIGN line 891, DQ4) | Medium |
| X-003 | Where per-repo settings can live | OURS: per-repo config under `issue-watch.d/<repo>.json` already exists (REQ R16) | CLAY: they have no home in a per-repo watcher config; R15 forbids a repo list in IronClaude configuration (DESIGN line 87) | Medium |
| X-004 | "One orchestrator per repo" | OURS: the label hides that the poll starts many per repo, up to 6 new ids a day (DESIGN lines 700, 706) | CLAY: ruling 8 says one per repo, at most three issues each, and another for the same repo when full | Low |
| X-005 | Internal naming of the owner's branch | OURS paper: branch `coordinators` (exists on origin, 2026-11-14) and branch `Coordinator` (REQ R10, R20, 2026-11-18) are both its own decisions and differ | CLAY has one naming scheme, validated by `ORCHESTRATOR_ID_PATTERN` | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Create-once claim files per item on a shared branch: a lock git enforces across developers and hosts (Q26) | High |
| U-002 | A | Orca registration as the single act that adds a project; configs auto-generated; first-run check disables a failing repo (REQ R8, R18) | High |
| U-003 | A | `orca repo list` verified under cron's minimal environment (REQ R21, 6 repos) | Medium |
| U-004 | A | Per-launch origin check so a session cannot work in the wrong repository (`check_origin`, REQ R10, R13) | Medium |
| U-005 | A | Session starts in a worktree whose origin is the project: no `cd` workaround, no UNVERIFIED `/sc:issue` directory check | High |
| U-006 | B | Organization-wide search per (login, org), one call each, reply shape observed once (DESIGN line 137) | Medium |
| U-007 | B | In-flight count where a damaged state file counts as in flight (a fail-closed rule) | High |
| U-008 | B | `wrong_target` refusal: wave 0 rejects a wake addressed to another orchestrator | Medium |
| U-009 | B | Restart of a dead orchestrator that has work in flight, with a resume wake; a dead idle one is only marked ended | High |
| U-010 | B | 30-minute idle end with the re-check under lock (an issue cannot be routed to an ending orchestrator) | Medium |
| U-011 | B | Per-issue state file created with exclusive create under a name without the orchestrator id | Medium |
| U-012 | B | Per-repo settings table (merge method, release branch, reviewers, role, safety files, tiers) | Medium |
| U-013 | B | `repos.yaml` validation: unique `<short>`, bounds on `max_in_flight`, `registry_invalid` as a cycle failure | Low |

## Shared Assumptions

Agreement sources: both papers keep one poll or dispatcher as the only router, check the repo's origin before a launch, apply a per-repo day cap and keep configuration outside the project repository.

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|-----------|------------------|----------------|--------|--------|
| A-001 | One host runs the poll and the sessions; two hosts are a rare exception | One router | UNSTATED in OURS (one cron entry on a Coder workspace); STATED in CLAY only as the last lease layer | Decides whether a host-local registry or a shared branch is the right lock | Promoted |
| A-002 | The number of repositories served stays small (6 in Orca here, 3 in the allow list), so discovery cost is not binding | Per-repo or per-org discovery | UNSTATED in both. CLAY argues from 65 repositories, then lists 3 | Decides whether the call-budget argument matters | Promoted |
| A-003 | The live coordinator session can be found and restarted reliably by its ccsession tag or session name | Restart of a down session | CLAY marks the tag pattern UNVERIFIED (U25); OURS states "restart a stopped session" with no detection method | Decides whether restart and `wrong_target` guards work | Promoted |
| A-004 | Plain files give enough exclusion: `O_EXCL` on one host, git create-once across hosts (the git lock acts at push time, after `git pull --rebase`, not at create time) | Per-issue exclusion | UNSTATED in both; Q26 states the push flow, not the race before the push | Decides whether two coordinators can both start an issue | Promoted |
| A-005 | Discovery returns every candidate issue within the budget (no truncation, no index delay that drops one) | Poll finds assigned or board issues | CLAY states the 100-item `truncated` rule and an UNVERIFIED index delay (U8); OURS states `DISCOVERY_BOUND` only in the older design | Decides whether an assignment can be missed silently | Promoted |

## Summary
- Total structural differences: 2
- Total content differences: 12
- Total contradictions: 5
- Total unique contributions: 13
- Total shared assumptions surfaced: 5 (UNSTATED: 5, STATED: 0, CONTRADICTED: 0; A-001 to A-005 are each partly stated by one side, listed as UNSTATED because at least one variant depends on them without stating them)
- Highest-severity items: C-001, C-002, C-003, C-004, C-008, X-001
- Variants differ on 24 of the comparable items; this is well above the 10 percent threshold, so the debate runs.
