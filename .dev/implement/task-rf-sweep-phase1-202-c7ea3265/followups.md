# Follow-ups to file as ONE backlog issue at the end of the run (owner instruction 2026-11-12: "If not fixable then file them as a follow-up issue and move on")

Phase 11 (cmd-skill gate, qa/cmd-skill):
- Medium: the new SKILL.md sentences at step 5 (line 27) and the stale-style paragraph (line 49) have no regression pin; reverting either gives 115 passed.
- Medium: the conjunction pins stop at conditions 1 and 3; an escape clause appended to condition 5 still passes (115 passed).
- 32 MINOR findings CMD-F5 to CMD-F36 (qa/cmd-skill/consolidated-findings-cycle0.md), among them CMD-F23 (singular "the standard error line").
- Stale pointers: step-1.15-checks.md rows S1 and S3 cite SKILL.md:49 (now :51); phase11-validation.md keeps the pre-fix 718; test-sweep-command-summary.md:19 sentence omits the framed failure pin.

Phase 12 (contract gate, qa/contract):
- 18 MINOR findings CON-F3 to CON-F20 (qa/contract/consolidated-findings-cycle0.md). Real wording weaknesses in the owner-approved WC-16 text that need owner approval to change: CON-F8 (ready Task "needing ownership review" can read as two triggers), CON-F10 ("Phase 1 adds this duty" collides with the contract's "P1"), CON-F11 (class labels "stalled" and "could not determine" read as typos), CON-F14 (no report location or failure path), CON-F15 (one 299-word paragraph), CON-F16 (cross-reference style), CON-F20 (L1 cap carve-out), CON-F12 (no sentence says a worker session never runs /sc:sweep itself).
- DESIGN row R2 (orchestrator-mode.md:716) still says "on every wake, at most once every 5 minutes"; not live text.
- step-1.17-checks.md check 5 as written prints FAIL (line-23 hunk); the appended re-run section records the adjusted passing comparisons.

Phase 13 (routing rows):
- HOW-WE-WORK.md R2 bullet (line 405, byte-equal to DESIGN row R2, pinned by plan item 13.1) says the coordinator runs /sc:sweep "on every wake"; WC-16 now says "on every coordinator wake or wait timeout" (owner-approved 2026-11-12). Same wake-versus-timeout ambiguity as CON-F2; changing it needs a DESIGN row R2 change.
- (docs gate 13.10) tests/commands/test_sweep_command.py does not pin the command file's frontmatter name, description, argument-hint or heading order, nor the 5-minute cap sentence in sweep.md; the lens text says each departure is BLOCKING but the QA agent graded it MINOR (DESIGN 7.6 Test bullet does not list them).
- (docs gate 13.18) The exempt reply of /sc:sweep keeps the mark "(not observed in Phase 1)" on the stalled (proved) and fenced counts (SKILL.md:43), but the output style pragmatic.md:23 does not mention the mark; a session following the style text alone could drop it. Align the style text in a later change. Also: the new sentence calls the `Next inspection` column an observation although its values read like instructions (report.py:43-54).
- (docs gate 13.17) 30 MINOR findings DOC-F3 to DOC-F32 (qa/docs/consolidated-findings-cycle0.md), several of which need the owner-approved WC-16 text or DESIGN-pinned guide rows to change (DOC-F9, F14, F16, F19, F26, and the WC-16 part of F15).

Phase 14:
- 12 Markdown files with embedded Python blocks fail `uv run ruff format --check src/ tests/` at the base commit already (examples/release-spec-template.md, several skill refs, two tests/roadmap fixtures); not touched by this work.
- Pre-existing or environment test failures in the full run: tests/cli/eval/test_claude_process_adapter.py (two ruff tests call `python -m ruff` but ruff is not a module in the project venv) and tests/hooks/test_launch_level_guard.py::test_speed_large_commands[1MB-big] (timing test that fails under load).
- The step 1.29 pipx output does not by itself prove which copy ran (pipx prints its own "already on your PATH" notice); the listed `sweep` subcommand exists only in the worktree build.
- (final gate 14.14) RO-1: the git seam (probes.py:296-300) does not pin `-c core.fsmonitor=false`, so a hostile repository config could run its fsmonitor hook; RO-2: transcripts are read without a regular-file check (probes.py:575, :756), so a FIFO or special file could hang the read (availability only).

- Run helper mkgf.sh: review prompts name a doubled report path (qa/final/.dev/...) and leave two blank placeholders ("( lines)", "report's own last lines read:"); reviewers found the real file anyway (seen in T316, T327, T329).

- Run records: notes.md of many tasks had a first line other than the task start sha (28 held the q0-head sha, 22 had no header line); the executor rewrote line 1 to the start sha in every such file at the final gate (content of the other lines unchanged).

## Final gate cycle 1 (items 14.24 to 14.28)
- FIN-F5 (OPEN): the header banner prints "Orca unavailable" when Orca answered; DESIGN :614 pins the literal and test_report.py WORKTREES_BANNER and test_cli_contract.py:443 pin it again. Needs an owner decision and a design edit.
- FIN-F1 (partly OPEN): Rule 4(a) stays in the code but nothing sets agent_wait now (design :481 and requirements :252 require the rule); the live capture of `worker-show` and `worktree ps --agent-wait` needs a live Orca command; nothing in the report says `working` is also never printed (SP24_LINE names only stalled and fenced; DESIGN D7 pins it).
- FIN-F7 (partly OPEN): the exempt reply still prints counts and path alone, so an exit 0 Orca outage run is not relayed there; needs pragmatic.md and the revision addendum changed. DESIGN 7.6 (:662) says step 3 takes report_path and summary only; the skill now also takes orca_available.
- FIN-F8 option (a) and FIN-F9 design-text lines: DESIGN 7.2 :511 and NFR-007 row :808; DESIGN 7.1 import list :211 lacks yaml.
- Review notes of the fix cycle: a contract with an unquoted colon and space in a value now yields an empty record with Source coverage "read" (probes.py:684), a Medium follow-up; SKILL.md:15 says "two facts"; the fix log FIN-F7 and FIN-F9 text was superseded by its repair section.

- Final gate cycle 2: FIN-F7 stays OPEN by the owner decision of 2026-11-12 (option 1); the 12 pre-existing Markdown format failures and the 2 pre-existing test_ruff_* failures (ruff not importable in the venv) remain.

- Final gate notes: DESIGN 7.6 step 3 is now at docs/designs/orchestrator-mode.md:663 (it was :662 before the owner edit of line 614); cycle-2 report notes CY2-N1 and the qualitative N-1 to N-5 (`qa/final/verify-cycle2-rf-qa.md:51`, `verify-cycle2-rf-qa-qualitative.md`) are follow-up candidates.

- Phase 2 (owner message 2026-11-12): add a preflight phase that ingests the reading list and instructions in `phase-outputs/plans/PHASE2-preflight-input.md`; FIN-F7 is not part of Phase 2 scope (it stays in the backlog issue as a documented Phase 1 limitation).
