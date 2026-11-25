# QA Report - Source Fidelity 1 (semantic-coverage lens)

**QA phase:** source-fidelity
**Lens:** semantic-coverage
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**Source root:** /home/coder/.cache/ic-snap-20261120/master (read-only)
**Date:** 2026-11-20
**Fix authorization:** false
**Status:** Complete

---

Doc = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md` (2,436 lines, read in full). Src = `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/`. Status values: Covered / Partial / Missing / Phantom. "Partial" and "Missing" rows are all MINOR (see findings).

## Coverage table, part 1: issue_watch package

| # | Source item | Source path:line | Documented at | Result |
|---|---|---|---|---|
| 1 | cycle constants MAX_CANDIDATES..DISCOVERY_WARN (14 constants) | cli/issue_watch/cycle.py:34-47 | 11.1, 9.4 | Covered |
| 2 | MAX_LAUNCHES_PER_CYCLE (dead constant) | cycle.py:35 | 5.1.7, 11.1, 14.2.1 D-01 | Covered |
| 3 | NETWORK_FS_TYPES | cycle.py:50 | 9.1 state_dir row | Covered |
| 4 | _TOP_KEYS (8 config keys) | cycle.py:58-69 | 9.1, 13.1.2 | Covered |
| 5 | ConfigError / Config | cycle.py:81,97 | 9.1, 13.1.2 | Covered |
| 6 | fs_type_of / _read_mountinfo | cycle.py:146,178 | 9.1 (mountinfo skip rule) | Covered (names not cited) |
| 7 | load_config (strict, unknown keys, no ~) | cycle.py:195-283 | 5.1.4, 9.1 | Covered |
| 8 | check_platform (Linux only) | cycle.py:286 | 5.1.4 platform column, 14.1.1 | Covered |
| 9 | validate_approvers (O_NOFOLLOW, 1 MiB, id regex) | cycle.py:298-361 | 5.1.4, 9.1 | Covered |
| 10 | approvers_summary (mtime, entry count printed by check-config) | cycle.py:364 ; cli.py:192-198 | 5.1.4 check-config row (output not described) | Partial (F-8) |
| 11 | validate_setup | cycle.py:371 | 4.1 step 1, 9.1 | Covered |
| 12 | Clock / SystemClock | cycle.py:380,392 | 12.2 (four Protocols) | Covered |
| 13 | Deadline (240/5/120) | cycle.py:402-433 | 11.1 | Covered |
| 14 | Deps / CycleResult (probe, would_launch) | cycle.py:435,449 | 5.1.4 once row | Covered |
| 15 | resolve_exit, _PRECEDENCE (2,6,7,5,3,4), 75 only alone | cycle.py:462-482 | 5.1.1, 10.1 | Covered |
| 16 | _Skip / _Transient / _Stop | cycle.py:491-515 | 5.1.1 | Covered |
| 17 | _Cycle.run 13-step pipeline | cycle.py:682-1212 | 4.1, 5.1.1 | Covered |
| 18 | _sweep (pending_orphan, claim_not_observed) | cycle.py:777 | 4.1 step 7, 5.1.3 | Covered |
| 19 | _discover (truncated at 100, warning at 80) | cycle.py:794 | 4.1 step 8 | Covered |
| 20 | _candidates / halt after first launch step | cycle.py:812-834 | 4.1, 5.1.1.1 | Covered |
| 21 | _hit (marker window) | cycle.py:848 | 4.2 link steps 3-4 | Covered |
| 22 | _examine gates E1-E15 | cycle.py:915-961 | 5.1.1.1 | Covered |
| 23 | _reclaim (failed entry re-claim, T-12) | cycle.py:901 | 4.2 step 5 (T-12), function not named | Covered |
| 24 | _revalidate (G7, G3', G6') | cycle.py:979 | 5.1.1.2 | Covered |
| 25 | _launch order (dry-run return, probe, prompt, re-read, guards, write-ahead, launch) | cycle.py:1026-1112 | 5.1.1.2 | Covered |
| 26 | _commit / _commit_shadow | cycle.py:1116-1162 | 4.1 step 12, 5.1.1 dry-run paragraph | Covered |
| 27 | _conclude (decision lines, one cycle line) | cycle.py:1176 | 4.1 step 13, 5.1.4 audit | Covered |
| 28 | status_report fields (healthy, counts, day_cap_used, stale, retry) | cycle.py:1270-1335 | 5.1.4 status row | Covered |
| 29 | _is_stale (unknown, abandoned+pending_orphan, 86400 s) | cycle.py:1251 | 5.1.4, 11.1 | Covered |
| 30 | _retry_orca (bare orca-ide fallback) | cycle.py:1262 | 14.3.1 U-10 Q-07 | Covered |
| 31 | slo_numbers / SloNumbers (4 numbers, no caller) | cycle.py:1339-1406 | 5.1.4 SLO, 14.2.1 D-03 | Covered |
| 32 | REPO literal | github.py:37 | 1, 5.1.2, 9.4 | Covered |
| 33 | PAGE_SIZE / PAGE_CAP / CALL_CAP / RESERVED_CALLS | github.py:40-49 | 5.1.2, 11.1 | Covered |
| 34 | EVENTS_JQ / MARKER_JQ / REREAD_JQ | github.py:54-67 | 5.1.2 | Covered |
| 35 | EDITS_QUERY / PROJECT_ITEMS_QUERY (query only) | github.py:74-108 | 4.5, 5.1.2 | Covered |
| 36 | argv_user..argv_reread (G1-G7) | github.py:175-262 | 4.5, 5.1.2, 8.1 | Covered |
| 37 | _issue_arg/_page_arg/_cursor_args/_trigger_arg/_login_arg | github.py:111-172 | 13.1 symbols table | Covered |
| 38 | GH_ERROR_SIGNS, classify, Reply kinds | github.py:269-371 | 5.1.2, 10.2 | Covered |
| 39 | rate_limit_wait / retry_after / date_header / RATE_LIMIT_MAX_WAIT_S | github.py:376-431 | 5.1.2, 10.3 | Covered |
| 40 | CallBudget | github.py:437 | 5.1.2, 11.1 | Covered |
| 41 | Read kinds, DISCOVERY_BOUND | github.py:467-496 | 10.2, 11.1 | Covered |
| 42 | user/discover/events/marker_comments/edits/project_items/reread | github.py:784-934 | 5.1.2 | Covered |
| 43 | ENTRY_STATES (6) | record.py:34 | 5.1.3, 6 | Covered |
| 44 | StoreError / LockHeld / LockError / TransitionError / StateExists | record.py:40-64 | 10.1 exit rows; TransitionError in 5.1.3 | Covered |
| 45 | Entry (17 fields), StoreDoc (7 keys) | record.py:69-131 | 5.1.3, 6 | Covered |
| 46 | PendingContext | record.py:105 | not named | Partial (F-8, helper) |
| 47 | validate / migrate / MIGRATIONS (ships empty) | record.py:213-279 | 5.1.9, 12.1 | Covered |
| 48 | FileStore save (atomic, 0600, fsync) | record.py:334-378 | 5.1.3 write path | Covered |
| 49 | FileStore.lock (flock, O_NOFOLLOW, inode recheck) | record.py:380-419 | 5.1.3, 10.3 | Covered |
| 50 | MAX_ATTEMPTS / BACKOFF / LEASE / DAY_CAP_WINDOW | record.py:434-443 | 9.4, 11.1 | Covered |
| 51 | fail / backoff_elapsed (T-1..T-3) | record.py:503-535 | 5.1.3 | Covered |
| 52 | mark_pending / mark_launched / mark_unknown / mark_spawn_error (T-4..T-7) | record.py:538-625 | 5.1.3 (T-4..T-7 by trigger) | Covered |
| 53 | sweep (T-8, T-9) | record.py:627 | 5.1.3, 10.3 | Covered |
| 54 | mark_claimed (T-10..T-12) | record.py:654 | 4.2, 5.1.3 | Covered |
| 55 | prune_consumed_log / day_cap_count / consumed_log | record.py:693-705 | 5.1.3 key list, 5.1.5 day cap | Covered (function names not cited) |
| 56 | reset_entry (T-13) / reset_rate_limit | record.py:706-727 | 5.1.3, 5.1.4 reset | Covered |
| 57 | disabled_present (dead) | record.py:748 | 5.1.7, D-09 | Covered |
| 58 | init_state | record.py:753 | 5.1.4 | Covered |
| 59 | dry-run shadow (DryRunDoc, load/save, warning on reset) | record.py:805-865 | 5.1.1.2, 6 row 1e | Covered |
| 60 | ORCA_AGENT, PROMPT_PATTERN, OPERATION_ID_*, OP_UNKNOWN_TEXT | launch.py:28-47 | 5.1.3, 8.3 | Covered |
| 61 | ORIGIN_REPO / ORIGIN_MISMATCH | launch.py:50-53 | 5.1.3, 9.4 | Covered |
| 62 | LAUNCH_DETAILS (8 words, never read) | launch.py:58 | 5.1.7, 10.2, D-10 | Covered |
| 63 | build_claim_prompt / launch_argv (12 elements) / retry_argv | launch.py:84-132 | 5.1.3, 8.1 | Covered |
| 64 | find_orca (orca-ide then orca, skills list, not cached) | launch.py:163 | 5.1.3, 4.1 | Covered |
| 65 | parse_origin / check_origin | launch.py:215-251 | 4.1, 5.1.5 | Covered |
| 66 | LaunchOutcome / outcome_of / OrcaLauncher | launch.py:255-370 | 5.1.3 reply handling | Covered |
| 67 | CLAIM_MARKER / SKEW_TOLERANCE_S | predicates.py:14-17 | 4.2, 8.3, 11.1 | Covered |
| 68 | approval_of (7 rules) | predicates.py:185-234 | 4.6, 5.1.5 | Covered |
| 69 | is_intended_owner / unchanged_since / project_check | predicates.py:162-271 | 4.6, 5.1.5 | Covered |
| 70 | marker_time / marker_in_window / eligibility_order | predicates.py:274-312 | 4.1, 4.2 | Covered |
| 71 | REASON_TABLE (59 words, kinds 27/17/9/1/4/1) recounted from source | audit.py:26-102 | 5.1.6, 10.2 | Covered (counts match) |
| 72 | AuditLog.append / rotate_if_needed (5 MiB, 4 files) | audit.py:106-156 | 5.1.4, 11.1 | Covered |
| 73 | _KEYS / _TYPES / _RULES / line builders / stderr_fallback | audit.py:159-404 | 5.1.4, 5.1.9, 10.3 | Covered |
| 74 | CLI group + five verbs (once, status, check-config, init-state, reset) | cli.py:94-348 | 5.1.4, 8.2 | Covered |
| 75 | once --dry-run (prints probe, would_launch) | cli.py:111-137 | 5.1.4 | Covered |
| 76 | status --json, exit 1 when unhealthy | cli.py:164-182 | 5.1.4, 8.2 | Covered |
| 77 | reset ISSUE --forfeit-guarantee / --rate-limit (double flag ignored) | cli.py:282-348 | 5.1.4, 8.2, 14.3.1 Q-09 | Covered |
| 78 | _EXIT_* (1, 1, 2, 6, 75) and cycle_crashed path | cli.py:34-38,121-129 | 10.1 | Covered |
| 79 | build_deps | cli.py:62 | not named | Partial (F-8, helper) |
| 80 | runner: STDERR_CAP_BYTES, CommandResult, Runner, SubprocessRunner | runner.py:15-130 | 5.1 key files, 12.1 | Covered |

## Coverage table, part 2: claim command, skill, scripts, agents

| # | Source item | Source path:line | Documented at | Result |
|---|---|---|---|---|
| 81 | /sc:issue seven flags (--claim, --create, --depth, --mode, --type, --pipeline, --submit) | commands/issue.md:36-44 | 5.2 key files, 8.2 | Covered for --claim/--pipeline/--submit; Partial for --depth/--mode/--type (names only, no values, "create only") (F-1) |
| 82 | STOP rules before Activation (8 bullets, E-CREATE-ONLY-FLAG, E-CLAIM-ONLY-FLAG, E-SUBMIT-NEEDS-FULL) | issue.md:50-59 | 5.2 STOP table, 10.2 | Covered |
| 83 | Outputs table, claim row (10 files) | issue.md:80 | 5.2 local artefacts | Covered |
| 84 | Outputs table, create row (draft dir, description.md, flags.md, issue-body.md, draft-notes.md, create-review.md) | issue.md:81 | not documented | Missing (F-1) |
| 85 | Coordinator handoff paragraph for --pipeline none | issue.md:85 ; SKILL.md:140 ; refs/claim.md:96 | 2.3 row 17, 4.2 step 7, 5.4 (marked NOT BUILT, prose) | Covered |
| 86 | Activation (Skill sc:issue-protocol) | issue.md:104-110 | 2.3 row 2, 5.2 | Covered |
| 87 | SKILL.md files table (23 rows: 5 refs, 3 scripts, 15 templates) | SKILL.md:24-50 | 3 tree, 5.2 key files | Partial: counts given, create-only templates not described (F-1) |
| 88 | Worker spawn rule, tier pins, T1 to T2 fallback | SKILL.md:54-64 ; refs/tiers.md:11-52 | 5.2 worker table | Covered |
| 89 | Repository and GitHub call rules (--repo on every call, one orgs/ read) | SKILL.md:70-78 | 4.5, 5.2 | Covered |
| 90 | Claim waves 0-8 | SKILL.md:80-92 ; refs/claim.md:11-150 | 4.2, 5.2 | Covered |
| 91 | Create waves 0-5 | SKILL.md:94-103 ; refs/create.md:11-97 | 4.5 X1-X3 (writes only) | Partial (F-1) |
| 92 | Return contract: 9 base fields, 10 claim fields, 3 create fields | SKILL.md:105-150 | cited as a line range only; "ten fields" in a test row | Missing (F-2) |
| 93 | Error table (STOP codes, 12 W- codes) | SKILL.md:152-177 | 5.2, 10.2 | Covered |
| 94 | Effort and complexity rubric (4 h / 16 h / multi-subsystem), verdict current/out_of_date | refs/claim.md:58,65-73 | not documented | Missing (F-3) |
| 95 | Six default next-step chains, /model tier line, /sc:recommend goal | refs/chains.md:9-38 ; claim.md:79-80 | 5.2 cites `chains.md:9-16` as "default next-step rows"; rows not listed | Missing (F-3) |
| 96 | Plan boundary computation | refs/claim.md:82 | 5.2 level table ("up to `Plan boundary`") | Covered |
| 97 | Default level rule (bug full, simple/medium feature <=16 h full, else worktree) | refs/claim.md:81 | 5.2, 9.2 | Covered |
| 98 | labels.md mode label, issue type, Complexity field POST rules | refs/labels.md:1-67 | 4.5 X1/X2 (one-line cites) | Partial (F-1) |
| 99 | orca_worktree.py subcommands (preflight, worktree, prompt, launch, pending) | scripts/orca_worktree.py:1857-1894 | 5.2 subcommand table, 8.2 | Covered |
| 100 | --submit needs --level full (argparse exit 2) | orca_worktree.py:1900-1901 | 4.6, 5.2 | Covered |
| 101 | timeouts DEFAULT/PREFLIGHT/TERMINAL_READ, SC_ORCA_TIMEOUT | orca_worktree.py:88-91 | 5.2, 9.3, 11.1 | Covered |
| 102 | WARNING_ORDER (8 worktree codes) and REMEDY (4 launch codes) | orca_worktree.py:230-239,802-817 | 5.2, 10.2 | Covered |
| 103 | worktree lookup keys (marker, record, basename, branch), copy_issue_dir, close_first_tab | orca_worktree.py:373-622 | 5.2 worktree row | Covered |
| 104 | GOVERNED_TOOLS (23 names recounted: 14 + 9 mcp) | orca_worktree.py:841-867 | 5.2 launch step 4, 9.4 | Covered (23 matches) |
| 105 | enforcement_preflight (IR-4) | orca_worktree.py:955-1045 | 5.2, 4.3 | Covered |
| 106 | IR7_REFUSE = False | orca_worktree.py:822 | 2.3 row 12, 5.2, D-19 | Covered |
| 107 | l2_status / install_l2 / _l2_selftest / L2_DATA_NAME | orca_worktree.py:1048-1442 | 5.2, 5.3 | Covered |
| 108 | session_report (release text, layers) | orca_worktree.py:1445-1485 | 5.2 launch step 9 | Covered |
| 109 | publish_pending / cmd_pending (no production caller) | orca_worktree.py:1488-1523 | 2.3 row 10, 5.2, D-18 | Covered |
| 110 | behind_ccsession / SHIM_TITLE / SHIM_TRIES | orca_worktree.py:792-800,1551-1583 | 4.3, 5.2 launch step 8, 5.3 | Covered |
| 111 | record_launch / launch mirror / stale_prompt / cmd_launch | orca_worktree.py:1586-1834 | 5.2 launch table | Covered |
| 112 | clickup_claim.py outcomes (skipped, not_found, ambiguous, already_assigned, assigned, error reasons), env vars, one PUT | scripts/clickup_claim.py:50-58,163-242 | 4.5 C2, 8.1, 9.3, 10.2 | Covered |
| 113 | clickup_claim.py match rules github_link / title_number, `rule` field | clickup_claim.py:42-48,148-160 | not documented ("only if one task matches") | Missing (F-4) |
| 114 | origin_repo.py exit codes 1/3/4, check_claim | scripts/origin_repo.py:61-63,102-153 | 5.2, 8.2, 10.2 | Covered |
| 115 | issue-worker-t1 / t2 / t3 (model, tools, effort: low on t3) | agents/issue-worker-t{1,2,3}.md:1-10 | 5.2 worker table, 3.1 | Covered |
| 116 | templates directory (15 files) | skills/sc-issue-protocol/templates/ | 3, 5.2 (15 count; 7 named) | Partial: 8 create-side files unnamed (F-1) |

## Coverage table, part 3: hooks, installers, ccsession, contract

| # | Source item | Source path:line | Documented at | Result |
|---|---|---|---|---|
| 117 | L1 guard binding (marker regex, pending to sessions, hard link, degraded) | hooks/scripts/launch-level-guard.sh:284-385 | 4.3, 5.3 | Covered |
| 118 | typed approval regex (/sc:implement, /task) writes .ok at W | launch-level-guard.sh:347-360 | 4.3, 5.3 | Covered |
| 119 | level words W/WA/F/FS read from the session file | launch-level-guard.sh:257-273 | 1, 5.3 | Covered |
| 120 | Skill classifier (implement/task/cleanup IMPL, pr-submit SUBMIT, issue ESCAPE, empty SKILL) | launch-level-guard.sh:398-413 | 5.3 classifiers | Covered |
| 121 | Bash classifier (BIG, normalise, ESCAPE words, orca allow-list, git, gh) | launch-level-guard.sh:414-726 | 5.3 classifiers | Covered |
| 122 | G2 rule 2 (send/ask, no --to/--run/--environment/--pairing-code, 8192 B, 64 args) | launch-level-guard.sh:485,496-537 | 5.3, 8.1 | Covered |
| 123 | TAMPER token list (install_hooks, .claude, settings, hooks, pre-push, --no-verify, hookspath) | launch-level-guard.sh:439-451,760-775 | 5.3 TAMPER row | Covered (dot-segment forms :769-775 and `*.claude` word :450 not listed, F-8) |
| 124 | 18 LL block words, LL-STATE / LL-TEXT notes | launch-level-guard.sh:36-133 | 5.3, 10.2, 12.1 | Covered (counts match) |
| 125 | level grid (16 cells, 10 always-blocked classes, precedence) | launch-level-guard.sh:783-803 | 5.3 LEVEL MATRIX | Covered |
| 126 | fail-open / fail-closed, exit 0 or 2 only, ll_on_exit trap | launch-level-guard.sh:135-163,386-392,807-808 | 5.3, 10.4 | Covered |
| 127 | job identity modes hook/execute/identify/prepare/run | launch-job-identity.sh:541-582 | 5.3, 8.1 | Covered |
| 128 | identify output shapes (ordinary, released, governed, unknown+reason+record) | launch-job-identity.sh:215-260 | 5.3, 8.3, 10.2 | Covered |
| 129 | hook() rewrite via updatedInput, silent exits, exit 2 wrap failure | launch-job-identity.sh:430-505 | 5.3 job identity table | Covered |
| 130 | requests/ and jobs/ stores | launch-job-identity.sh:164-174,307-385 | 5.3 state stores, 6 | Covered |
| 131 | L2 pre-push (L2-PROTECTED/UNKNOWN exit 1, L2-MALFORMED exit 2, protected refs) | launch-level-pre-push.sh:1-208 | 5.3, 10.4 | Covered |
| 132 | hooks.json registrations (18 hook commands in 9 event/matcher groups, 192 lines, three launch-level) | hooks/hooks.json:3-190 | 8.4, 5.3 | Covered (every entry listed, timeouts match) |
| 133 | plugin hooks.json differs (no ccsession-tag, no pragmatic-subagent, async on subagent-start) | plugins/superclaude/hooks/hooks.json | 5.3, 8.4, X-27 | Covered (diff re-run, matches) |
| 134 | require-orca-worktree-agent.sh (blocks `orca worktree create` without --agent; orca_worktree.py subprocess outside it) | hooks/scripts/require-orca-worktree-agent.sh:1-61 | 3 tree, 8.4 (name only), A.2 (governed test) | Partial: what it does is not described (F-6) |
| 135 | install_hooks _FRESHNESS_SCRIPTS (launch scripts :90,93,96), merge, backup, force | cli/install_hooks.py:42-97,156-494 | 5.3 registrations, 9.2, 13.1.6 | Covered |
| 136 | install_hooks _SEED_FILES, _LEGACY_SCRIPTS, ccsession hook ownership regex | install_hooks.py:98-142 | not documented | Missing (F-6) |
| 137 | wire_ccsession (symlinks, unseed-env.py, retention.py ensure, --migrate-names) | cli/install_ccsession.py:11-161 | 8.1 one row, 5.3 | Partial: env seeding and the settings.json cleanupPeriodDays write not described (F-6) |
| 138 | unseed-env.py | skills/ccsession-tag/unseed-env.py:1-30 | 8.1 (named), 3 tree omits | Partial (F-6) |
| 139 | ccsession-orca (CCSESSION_ORIGIN, unsets NAME/ASK_TIMEOUT, passes prompt through) | ccsession-tag/ccsession-orca:198-263 | 5.3 ccsession coupling, 9.3 | Covered for launch-level relevance |
| 140 | ccsession-orca naming question, resume-like classification, tab reopen | ccsession-orca:19-40,157-191,222-236 | not described | Missing (F-6, adjacent) |
| 141 | session-start.sh / session-name.sh registrations | ccsession-tag/hooks/session-*.sh ; hooks.json:34-42,55-61,73-83 | 8.4 | Covered as registrations; behaviour (CLAUDE_SESSION_ID write) not described (F-6) |
| 142 | WORKER-CONTRACT sections 1-5 and rules WC-2..WC-16 (no WC-1, no WC-17) | core/WORKER-CONTRACT.md:9,27,49,68,299 | 5.4 | Covered (line numbers re-verified) |
| 143 | contract line 23 never-as-worker list (includes /sc:pr-submit while D3 holds) | WORKER-CONTRACT.md:23 | 5.4 line 1354 list omits /sc:pr-submit | Partial (F-5) |
| 144 | contract section 4 subsections (owes each worker, liveness, brief layout, feature worktree, git/GitHub ownership, reading a result, after /sc:implement stop, fan-in, worked example) | WORKER-CONTRACT.md:82-297 | 5.4 cites only the issue-related lines | Partial by design (F-5) |
| 145 | contract lines 242-244 (issue comments are coordinator actions; PRs only via /sc:pr-submit, never as a worker) | WORKER-CONTRACT.md:242-244 | 5.4 cites 242-243 | Covered (244 not cited, F-5) |

## Coverage table, part 4: tests (Glob of the assigned directories)

| # | Source item | Path | Appendix A row | Result |
|---|---|---|---|---|
| 146 | tests/issue_watch/*.py: 19 test modules + conftest.py + __init__.py | tests/issue_watch/ | A.1 (19 modules + conftest; __init__ empty) | Covered |
| 147 | fixtures/_assumed_shape/ (19 JSON) | tests/issue_watch/fixtures/_assumed_shape/ | A.1 last row | Covered (count 19 matches) |
| 148 | hooks: test_launch_job_identity, _level_guard, _guard_l2_tokens, _guard_registration, _guard_with_identity, _guard_worker, _level_observations, _pre_push, _pre_push_records (9) | tests/hooks/ | A.2 (9 rows) | Covered |
| 149 | hooks: test_require_orca_worktree_agent_governed.py | tests/hooks/ | A.2 (added) | Covered |
| 150 | hooks: test_require_orca_worktree_agent.py (the generic hook test, 7 test functions, 201 lines) | tests/hooks/ | not a row | Missing (F-7, outside the assigned name patterns) |
| 151 | tests/hooks/fixtures/launch_level/ (live_probe.py and fixtures) | tests/hooks/fixtures/launch_level/ | A.2 observations row mentions "nine fixtures" | Covered by reference |
| 152 | skills: test_issue_protocol, _orca_worktree, _l2_install, _repo_resolution, _worker_agents, _t1_fallback (6) + test_worker_contract + test_clickup_claim + test_model_alias_policy | tests/skills/ | A.3 (9 rows) | Covered |
| 153 | tests/commands/test_issue_command.py, tests/cli/test_issue_body_templates.py, tests/cli/test_install_hooks.py | tests/ | A.4 | Covered |
| 154 | tests/unit/test_install_ccsession.py, test_ccsession_tag.py, test_ccsession_tiers.py, tests/core/test_orca_session_launch_guidance.py | tests/ | A.4 | Covered |

## Phantom check (documented item to real source)

Every item below was documented, then traced to the snapshot. No phantom was found.

| Documented item | Traced to | Result |
|---|---|---|
| 59 reason words, kinds 27/17/9/1/4/1 | audit.py:26-102 recounted line by line | Exists, counts match |
| 5 `issue-watch` verbs, "exactly five" | cli.py:111,164,185,201,282 | Exists |
| 12-element launch argv; prompt `/sc:issue --claim <N> --pipeline none` | launch.py:92,103-116 | Exists |
| 18 LL block words | launch-level-guard.sh:42-106 (17 case arms) plus default LL-BROKEN :808 | Exists |
| 16-cell level grid, 10 always-blocked classes | launch-level-guard.sh:783-803 | Exists, matches |
| 23 GOVERNED_TOOLS | orca_worktree.py:841-867 (14 + 9) | Exists |
| 5 `orca_worktree.py` subcommands | orca_worktree.py:1863-1893 | Exists |
| 12 W- codes (8 worktree + 4 launch) | orca_worktree.py:230-239,802-817 | Exists |
| 13 STOP codes | issue.md:50-59, SKILL.md:152-177, origin_repo.py:61-63 | Exists |
| 3 identity hook exit shapes, `identify` 5 JSON shapes | launch-job-identity.sh:215-260 | Exists |
| L2 words L2-PROTECTED / L2-UNKNOWN / L2-MALFORMED, exit 1/1/2 | launch-level-pre-push.sh:191-208 | Exists |
| hooks.json 3 launch registrations, timeout 5, plugin copy diff | hooks.json:63-71,115-134; diff re-run | Exists, matches |
| WC-2..WC-16, no WC-1, no WC-17, "grant row" once (:57) | WORKER-CONTRACT.md grep | Exists |
| 3 byte-identical plugin scripts | `cmp` on all three | Identical |
| main.py:577-579, 211/219, 406/412; install_user_setup.py:36; probes.py:43; CHANGELOG.md:17 | grep and sed on the snapshot | All cited lines hold |
| `IR7_REFUSE = False` at :822, branch :1757-1758 | orca_worktree.py | Exists |
| `MAX_LAUNCHES_PER_CYCLE` defined, never read | cycle.py:35 | Exists |
| `slo_numbers` no production caller; `disabled_present` dead | cycle.py:1359 ; record.py:748 | Exists |
| 35 test function names cited in 5.2, 5.3, 12, 13, A.1-A.3 | grep of `def <name>` in 6 test files | All 35 exist |
| Absence claims (no WC-17, no COORD-, no dispatcher, no pipeline.json, no release-worker) | the doc labels these "not found in snapshot"; grep of sc-launch / launch-level terms under ccsession-tag returns zero (re-run); `sc-launch` appears only in launch-level-guard.sh and orca_worktree.py | Consistent with source |

## Findings

All findings are MINOR. No BLOCKING finding.

| ID | Severity | Document location or "absent" | Source evidence path:line | Problem | Required fix |
|---|---|---|---|---|---|
| F-1 | MINOR | absent (only 4.5 X1-X3 writes, 8.2 flag names, 5.2 file count) | commands/issue.md:36-46,81 ; skills/sc-issue-protocol/SKILL.md:94-103 ; refs/create.md:11-97 ; refs/labels.md ; templates/issue-{bug,feature}-{simple,complex}.md, description.md, flags-decision.md, draft-notes.md, create-review-comment.md | The `--create` mode (Waves 0-5, depth to worker table, flag settling, 4 body templates, Priority / Fix approach / Test plan sections, contradiction prompt, label/type/Complexity rules, `issue_type` / `complexity_field` / `classification_missing` return fields) is not described. `--depth`, `--mode`, `--type` appear as names only; their values (quick/standard/deep, feature/bug, 11 areas) are not given. The document scope (Section 1 line 65) names only the claim flow, but never says create is out of scope, and X1-X3 are documented as writes. The doc's GitHub-write list is complete, so no reader is misled about writes. | State in Section 1 scope that `--create` is out of scope except its three GitHub writes, or add a short 5.2 subsection. |
| F-2 | MINOR | 5.2 file table cites `SKILL.md:105-150` only | SKILL.md:105-150 | The return contract (9 base, 10 claim, 3 create fields, `enforcement_hook`, `launch_status`, `worktree_match_key`, null rules) is the claim's machine-readable output and is not listed. | Add the field list or one table row naming the fields. |
| F-3 | MINOR | 5.2 cites `chains.md:9-16`; rows not listed | refs/claim.md:58,65-73,79-81 ; refs/chains.md:9-38 | The effort and complexity rubric (simple up to 4 h, medium up to 16 h, complex over 16 h or multi-subsystem or security/migration), the accuracy verdict values `current` / `out_of_date`, the six default next-step chains and the `/model` tier line are not documented. They decide which worker runs Wave 4 and what a `full` agent runs. No claim in the doc is wrong because of it. | Add a short table of the rubric and the six default chains. |
| F-4 | MINOR | 4.5 C2, 8.1, 5.2 say "only if exactly one task matches" | skills/sc-issue-protocol/scripts/clickup_claim.py:42-48,148-160,208-231 | The two matching rules (issue URL in the markdown description or a custom field; `#N` token in the task name as fallback) and the `rule` field of the result are not documented. | Add the two rules to the C2 row. |
| F-5 | MINOR | 5.4 line "never-as-worker list" (1354) | core/WORKER-CONTRACT.md:23,244 | The list is shown without `/sc:pr-submit` (kept off workers while decision D3 holds), and line 244 ("PRs go only through `/sc:pr-submit --monitor 3` ... never as a worker") is not cited although the `full --submit` claim path ends in that command. The section 4 subsection headings (:82,95,202,218,230,249,260,283,291) are not enumerated; 5.4 states it covers only the issue-related lines. | Add `/sc:pr-submit` to the list sentence and cite :244 in the C5 row note. |
| F-6 | MINOR | 8.1 installers rows, 8.4 (names only), 3 tree line 396 | hooks/scripts/require-orca-worktree-agent.sh:1-61 ; cli/install_hooks.py:98-142 ; cli/install_ccsession.py:72-125 ; ccsession-tag/ccsession-orca:19-40,157-191 ; ccsession-tag/hooks/session-start.sh:20-30 | `require-orca-worktree-agent.sh` is registered and tested but never described (it blocks a bare `orca worktree create`; its own header says `orca_worktree.py`, which creates the claim worktree without `--agent`, is outside it). `install_hooks` `_SEED_FILES`, `_LEGACY_SCRIPTS` and the ccsession-hook ownership rule are absent. `wire_ccsession` also seeds `ccsession.env` and raises `cleanupPeriodDays` in `settings.json` (retention.py), which the 8.1 row does not say. `ccsession-orca` name question, resume classification and tab reopen are not described. The tree lists 4 of the 17 files in `hooks/scripts/`. | One sentence per item; or state that the unrelated hook scripts are out of scope. |
| F-7 | MINOR | Appendix A.2 | tests/hooks/test_require_orca_worktree_agent.py (7 test functions, 201 lines) | The main test of the hook whose governed companion is a row is not a row. It is outside the assigned name patterns, so this is a note, not a gap. | Add a row or leave the companion row as is. |
| F-8 | MINOR | 5.1.4 check-config row; 5.3 TAMPER row | cli.py:192-198 ; cycle.py:364 ; record.py:105 ; cli.py:62 ; launch-level-guard.sh:450,769-775 | Low-significance details: `check-config` prints `approvers_file mtime` and `entries`; `PendingContext` and `build_deps` are not named; the TAMPER list lacks the dot-segment / doubled-slash / `..` forms after `.claude` and the `*.claude` word rule. | Optional. |

## Checks performed

- Document read in full (2,436 lines, 8 Read calls).
- Source read or enumerated from the snapshot: issue_watch (8 modules, def/class/constant enumeration by Grep; cli.py:94-348, cycle.py:1225-1406, audit.py:20-110, launch.py:84-135 read), commands/issue.md (full), SKILL.md (full), refs/claim.md, create.md, chains.md, tiers.md (full or head), clickup_claim.py (full), orca_worktree.py (enumeration plus parser and GOVERNED_TOOLS), launch-level-guard.sh (1-40, 255-535, 756-808), launch-job-identity.sh (200-270, 425-582), launch-level-pre-push.sh (1-30, 100-208), require-orca-worktree-agent.sh (full), hooks.json (Grep of all keys), install_hooks.py (1-160), install_ccsession.py (full), ccsession-orca (1-60, 150-263), WORKER-CONTRACT.md (headings, lines 20-66, 23, 57, 242-244, 258 and greps), agents t1-t3 (frontmatter).
- Coverage rows enumerated: 154 (80 watcher, 36 claim, 29 hooks/installers/ccsession/contract, 9 test-directory rows), of which 133 Covered, 13 Partial (rows 10, 46, 79, 81, 87, 91, 98, 116, 134, 137, 138, 143, 144) and 8 Missing (rows 84, 92, 94, 95, 113, 136, 140, 150). Phantom: 0. Every Partial and Missing row maps to a MINOR finding F-1 to F-8.
- Test Glob of the assigned directories: 21 files in tests/issue_watch (19 modules, conftest.py, __init__.py), 9 launch-named plus 2 added plus 1 unlisted (F-7) in tests/hooks, 9 in tests/skills, 7 in commands/cli/unit/core; Appendix A row total (48) recounted and correct.
- Tool engagement (approximate counts): Read about 36 | Grep about 24 | Glob 0 (directory listings were done with read-only `ls` in Bash) | Bash 14 (read-only: wc, ls, sed, grep, cmp, diff; no write under the snapshot, none outside this report file).
- Confidence: Verified items 154 of 154 enumerated; no UNCHECKED; UNVERIFIABLE 0 (runtime behaviour is not part of this lens). Source-reading depth for orca_worktree.py bodies, the guard's git/gh classifiers (:550-755) and the identity supervisor (:267-420) was by enumeration and spot reads, not line by line; those are the areas where an undetected omission is most likely, and the detail-preservation lens covers them.

## Summary

Every CLI verb (5 issue-watch verbs, 5 orca_worktree.py subcommands, origin_repo.py, clickup_claim.py), command and flag of `/sc:issue --claim`, hook registration (18 commands), state (6 entry states, 4 guard levels), reason and block-word vocabulary (59, 18, 13 STOP, 12 W-), exit code (0-7, 75; 0/2; 0/1/2; origin 1/3/4) and every test file of the assigned Glob traces into the document with correct counts and line numbers, and nothing in the document lacks a source basis. The gaps are all in create mode, the claim output contract, the rubric and chains, ClickUp matching and installer or ccsession side details; none changes a reader's conclusion about the pipeline.

## Verdict: PASS

Status: Complete
