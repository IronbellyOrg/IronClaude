issues
state=463fa144a17ea4f9e822eeb4637d74f323ec819b42979bc86c4597392b977061 (helper --print-state before and after the review; unchanged)
reviewer: fresh general-purpose Task subagent, archive-gate FINAL (refs/qa.md "Managed FINAL review"); verbatim result below

T1 ok docs/getting-started/installation.md:66 (no `update` upgrade advice), :92-94 (git and `claude` CLI required), :308 (`doctor --verbose`); the two lint errors (MD041 at :1, MD001 at :5) predate this run, are on untouched lines and are recorded at artifacts/deviations.md:7
T2 ok docs/user-guide/mcp-installation.md:106 (litellm opt-in row); "reinstalls framework files only" is gone; lint clean
T3 ok docs/getting-started/upgrading.md:85-100; installation.md:66 links upgrading.md; upgrading.md lints clean. lint/T3.log ends rc=1, but only from the same two old installation.md lines as T1. notes T3 F3.1 is all `no`, so noted
T4 ok README.md:75 (upgrading link), :98-99 (`/sc:impact`, `/sc:graph`, codegraph); no "(v4.3)"
T5 ok docs/getting-started/quick-start.md:3 (`claude` CLI), :5 (link to upgrading.md)
T6 ok `cmp` of HOW-WE-WORK.md with the plugin copy exits 0; src/superclaude/core/HOW-WE-WORK.md:3; artifacts/t6-tests.log:42 (507 passed); only line 3 changed, the level table is untouched
T7 ok docs/user-guide/commands.md:236 (`/sc:graph`), :282 (`/sc:impact`), :772 (standard depth is the default); skipped corrections are recorded at artifacts/deviations.md:26-30
T8 ok docs/user-guide/flags.md:195, :203, :247; no `--preview`; the resolved T8 F1.1 fix holds at :9
T9 ok docs/user-guide/modes.md: the AC grep returns nothing; lint clean
T10 ok docs/user-guide/agents.md:684 (the T10 F1.1 fix holds); no `/sc:focus` or Magic
T11 ok docs/user-guide/session-management.md:35-42; no "(v4.3+)"
T12 ok docs/user-guide/memory-system.md:205
T13 ok docs/user-guide/mcp-servers.md:16, :40-45; contributing-code.md:26 says Auggie needs Node 20+; no `--all-mcp` or `/sc:validate`
T14 ok docs/user-guide/freshness-hooks.md:28; no `install -f`
T15 ok docs/user-guide/brainstorm.md:17, :73 (codegraph with its fallback)
T16 ok artifacts/t16-links.txt:2-17 (all OK); my own link check finds nothing missing
T17 ok docs/user-guide/codegraph.md:1-149 (sections per A-W22); README.md:98; mcp-installation.md:60
T18 ok docs/swarm/README.md:76; command-reference.md:154; user-guide.md:100; wizard-guide.md:75; lens-catalog.md:160; these match artifacts/t18-validate-lenses.txt:1; no `--custom-prompt-dir`
T19 ok docs/guides/sprint-cli-tools-release-guide.md:74 (`--yes`) and 13 matches for `--task-parallelism`/`--yes`; no `/sc:task-unified`
T20 ok docs/guides/reflect-cli-tools-guide.md:35, :50, :252
T21 ok docs/guides/cli-portify-and-pipeline-runner-guide.md:514, :518; no "converge until"
T22 ok docs/guides/roadmap-cli-tools-release-guide.md:134; every option in artifacts/t22-roadmap-help.txt appears in the guide, and the guide adds none; the T22 F1.1 fix holds
T23 ok docs/guides/prd-skill-release-guide.md:275; the AC grep returns nothing
T24 ok docs/guides/tdd-skill-release-guide.md:271; the AC grep returns nothing
T25 ok docs/guides/suites-guide.md:58 (87 evals, 17 suites), which matches artifacts/t25-eval-list.txt (17 suites, 87 evals); no `git stash`
T26 ok src/superclaude/rules/core/changelog_maintenance.md:138-141 (`--repo <owner>/<repo>`, notes file); no `.claude/changelogs` and no src/ path; artifacts/t26-verify-sync.log ends "All components in sync"
T27 ok docs/reference/common-issues.md:18; the AC grep returns nothing
T28 ok docs/reference/troubleshooting.md:143; the AC grep returns nothing
T29 ok docs/reference/mcp-server-guide.md:34, :46 (codegraph sections kept); the AC grep returns nothing
T30 ok docs/mcp/mcp-optional-design.md:9, :52
T31 ok docs/mcp/mcp-integration-policy.md:12; no `~/.claude/superclaude/`
T32 ok docs/reference/diagnostic-reference.md:278; no `rm -rf ~/.claude`
T33 ok docs/reference/deviation-report-format.md:105; all 4 cited source paths exist
T34 ok docs/developer-guide/technical-architecture.md:33, :68, :316; no "(v4.3+)"
T35 ok docs/developer-guide/contributing-code.md:181; no `git add .`
T36 ok docs/developer-guide/testing-debugging.md; no `rm -rf ~/.claude`; the T36 F1.1 and F1.2 fixes hold
T37 ok docs/developer-guide/README.md:138; no SuperClaude-Org; every in-file anchor resolves
T38 ok docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:872; no `task-unified` or `--all-mcp`; notes T38 F1.1 and F1.2 are all `no`, so noted
T39 ok docs/dev/lens-contribution-policy.md:40; docs/dev/sync-discipline.md:15
T40 ok docs/sprint-cli-deep-dive.md:676; no `task-unified` or `v4.3.5`
T41 ok docs/swarm/operator-runbook.md:118; no M5 line in either file
T42 ok CONTRIBUTING.md:30 (`--detach`, the T42 F1.1 fix), :66 (`--repo`); KNOWLEDGE.md:257; no bare `git stash`
T43 ok docs/developer-guide/codegraph-integration.md:37-71; every cited file:line exists (bulk check); the T43 F1.1 fix holds at :55
T44 ok docs/developer-guide/session-memory.md:1; every cited file:line exists; notes T44 F1.1 is all `no`, so noted
T45 ok docs/developer-guide/review-severity-rule.md:45-49 (B1-B5), :58 (tests/skills/test_review_severity_rule.py exists); DECISIONS.md is tracked
T46 ok docs/developer-guide/release-procedure.md:61-69 (G1-G9), :50, :62, :69, :84, :91 (all `gh` lines have `--repo IronbellyOrg/IronClaude`)
T47 ok docs/developer-guide/documentation-index.md:93-96; every link target exists
T48 ok docs/testing/v5.0.0/user/D01-install-upgrade-doctor.md:8-369 (all sections; 22 of 22 steps tagged), :14 and :339 (real-HOME guard); the T48 F1.1 fix holds at :216; notes T48 F1.2 is all `no`, so noted
T49 ok D02-mcp-servers.md:96 (exit 1 cited to install_mcp.py:1422-1428 and main.py:329-331); 16 of 16 steps tagged; the post-task fix at :281 now points to MCP_Tavily.md
T50 ok D03-codegraph-graph-impact.md Steps 9-18 cover every AC item; 18 of 18 steps tagged; the :13 post-task text matches hooks.json:18,49,104
T51 ok D04-session-memory.md:103 (checks the `.gitignore` file on disk, citing save.md); 9 of 9 steps tagged; :12 post-task fix is correct
T52 ok D05-routing-core-files-issue-templates.md: 23 citations of help.md, recommend.md or core files; 16 of 16 steps tagged; the T52 F1.1 fix holds at :12; notes F1.2, F1.3, F2.1 and F2.2 are all `no`, so noted (the sandbox `gh` lines are a recorded conflict with the Constraints, artifacts/deviations.md:141)
T53 ok D06-plan-implement-review-cap.md:46; 8 HOW-WE-WORK.md, 9 troubleshoot.md and 4 pragmatic.md citations; Steps 4-9 carry `[CLAUDE-SESSION]` or `[API-LONG]`
T54 issue docs/testing/v5.0.0/user/D07-pr-submit.md:115 `gh repo view --json nameWithOwner -q .nameWithOwner` has no `--repo IronbellyOrg/IronClaude` and names no repository, which breaks the Constraint "Every `gh` command written into a doc uses `--repo IronbellyOrg/IronClaude`"; Task 46 dropped this same command for this reason (artifacts/deviations.md:134); fix: remove it and its clause at :138, or record a deviation or Ruling; chk=n,n,n,y
T55 ok D08-ccsession.md:52; 74 ccsession or CHANGELOG citations; 17 of 17 steps tagged; the T55 F1.1, F1.2 and F1.3 fixes hold; notes F2.1 is all `no`, so noted
T56 ok D09-hooks-freshness-pragmatic.md:124; 23 freshness-pre-edit.sh and 8 hooks.json citations; 24 of 24 steps tagged. Cleanup at :497 removes only the dismiss file the Tier C session created; this is disclosed at :15 and :500
T57 ok D10-sprint.md:73 (short cli/sprint citations resolve through the Source-of-truth line at :5); 17 of 17 steps tagged
T58 ok D11-roadmap-tasklist.md: 12 of 12 steps tagged, roadmap/tasklist code cited; notes F1.1-F1.3 are all `no`, so noted
T59 ok D12-reflect.md: 19 of 19 steps tagged (Step 18 at :592 carries two tags, both accurate); the T59 F1.1 and F1.2 fixes hold; notes F1.3 is all `no`, so noted
T60 ok D13-prd-portify-cleanup-audit.md:71; 15 of 15 steps tagged; Step 14 cites "as Step 9"
T61 ok D14-swarm.md:101; 18 of 18 steps tagged; notes F1.1 is all `no`, so noted
T62 ok D15-eval-harness.md: 15 of 15 steps tagged, 9 cli/eval citations; notes F1.1 is all `no`, so noted (see the paperwork line below)
T63 ok D16-init-lite-recommend-ic.md: 38 init_lite.py, recommend/ or ic citations; 21 of 21 steps tagged; notes F1.1 is all `no`, so noted
T64 ok docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md:5 (Gate line cites models.py:104,320-328); the Negative / gate check table is filled; 10 of 10 steps tagged
T65 ok docs/testing/v5.0.0/sysop/E02-ccsession-model-data-publishing.md:24 (`file://` works), checked against models.py:265-267
T66 ok artifacts/t66-links.txt:22 (TOTAL=20 MISSING=0); docs/testing/v5.0.0/README.md lints clean
constraint ok: CHANGELOG.md, docs/releases/, src/superclaude/cli, hooks and scripts are unchanged against d953b983; nothing is staged; no src/superclaude path was added to HOW-WE-WORK.md or changelog_maintenance.md; no install or issue link points at SuperClaude-Org; closing-make-test-2.log:14853 shows 14610 passed, 0 failed, and closing-smoke-pytest-2.log shows 817 passed
constraint issue: the D07-pr-submit.md:115 breach listed under T54
paperwork (not blocking): artifacts/retries/T62/notes.md:1 holds T60's start sha (756b9662…) instead of T62's (152f64b9…), so under qa.md the file counts as absent while the T62 ledger line still cites notes@…:1-2; fix line 1
prompt-template ok: all 79 prompt-*.md files match the closed qa.md template outside the seven slots (differences are only whitespace next to empty slots); every retry file except the T62 notes file has the right start sha on line 1
Self-Audit:
1. Ran markdownlint 0.38.0 over all 78 delivery files (only the two old installation.md errors), re-ran every grep AC, checked every relative link and anchor (all misses are inherited lines), and checked that every file:line citation in the new docs and the 18 guides exists.
2. Checked each guide for sections, cost tags on every step, expected-result citations and writes to the real ~/.claude; checked `gh` commands for `--repo`; checked the forbidden paths, staged files and changed files against the delivery list; checked the cited logs' outcome lines and the closing test logs.
3. Read every notes, review and repair file and checked the resolved blockers against the current text; compared all 79 saved prompts with the template using a regex; checked the start sha on line 1 of every retry file; read the orchestrator post-task fixes in D02, D03 and D04 and the hook lines they cite.

Orchestrator action after FINAL: the paperwork item was corrected (T62 notes.md line 1 now holds 152f64b9804d8ef77d6c4edc53d250c2259d9e88); the state digest above was re-read afterwards and is unchanged (notes are not part of the digest). The T54 issue is a blocking defect at the end state; per refs/managed-workspace.md step 6 the run stops E-ARCHIVE-BLOCKED and completed tasks are not reopened without an operator ruling.
