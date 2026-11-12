# Final Handoff: Supervised Orchestration Technical Reference

**Task:** TASK-TECHREF-orchestration-20261110-050239
**Date:** 2026-11-12
**Item:** 374. This handoff supersedes `phase-outputs/initial-handoff.md` (task item 312). Two statements in the early handoff are wrong and are corrected here: its status paragraph (it says the Phase 7 check was in its first fix round), and its reinstall step (it says `superclaude install`; see "Open items" for the right command).

## The document

- Path: `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`
- Length: 2,243 lines by `wc -l` (measured 2026-11-12 at about 18:09 UTC; the Read tool shows one more because the file ends with a blank line). That is 243 lines over the 2,000-line target the build brief set; the template's 1,800-line Heavyweight ceiling is waived in `synthesis/assembly-brief.md`, and no reviewer found padding.
- Tier: Heavyweight. Status: Draft (frontmatter). The file is not tracked or staged in git (`git status` prints `??`). To stage it: `git add docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`. I did not stage or commit it.
- Sections: 14 of 16 populated. Section 6 (State Management) and Section 7 (Component Inventory) are N/A with a reason in the section, and so is subsection 11.3. Section 11 is limits only, with no measured figures beyond the recorded speed tests.

## Where everything is (task folder `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/`)

- `research/`: 14 files. `synthesis/`: 7 files. `qa/`: 225 files at the top level plus the older `qa/spec-panel-346/` (6 files, not touched). `phase-outputs/`: both handoffs. Also `gaps-and-questions.md`, `research-notes.md`, `BUILD-REQUEST.md`.
- The task file's "Phase Gate Findings" lists every gate, its findings and its cycles. `qa/qa-final-state-consolidated.md` records the last validation.
- Git: the task folder has 155 files staged, 1 staged with a later edit, and 101 untracked; I stage the whole folder with `git add .dev/tasks` as my last step. Nothing is committed.

## How it was checked

Every review gate that ran during this execution closed PASS, except one that closed by your decision:

- Research, web research, synthesis and assembly gates: Phases 2 to 5.
- Phase 6 document lens gate: 14 blocking findings fixed. Source fidelity gate: 338 sources checked five ways, 16 blocking findings fixed. Executor gate: 11 fixed.
- Phase 7 gate on the early handoff: ended with 2 documented open findings, by your decision ("Document these issues and move in"). It is not a pass. Both are corrected here.
- Post-completion lens gate (10 reviewers): 3 blocking findings fixed. Post-completion source fidelity gate (353 sources checked five ways): 3 fixed.
- Final-state validation: four rounds. The first three each found one blocking sentence (the last found two in one clause); you authorized each fix; round 4 passed both the structure and the content review on the complete document.

One earlier review did not pass: the task builder's integrity check of the task file (2026-11-10, before this run) ended FAIL and advised halting. It was incomplete (7 of 27 structural checks verified). I read that record only at Phase 5 (my miss). You had started the run explicitly. Its three open findings were handled during the run (every source got all five fidelity checks, reviewers compared overlapping files across partitions, every fix was followed by independent verification); it is not closed as a review.

## What you can and cannot rely on

- Source-verified: what the repository's scripts, hooks, contract text, installer and tests say and do, and what the Orca development checkout and the installed Orca files say. Reviewers re-read these against the files. Only two test files were run (739 and 5 tests passed, 2026-11-11); the hook tests were read, not run.
- Documented, not observed: what Claude Code does with hooks (timeouts, order, switches that turn hooks off, hooks in subagents) comes from official documentation pages, not from a run on this host.
- Unverified (tagged `[UNVERIFIED]` in the reference): the settings of the running Orca, the signal Claude Code uses when a hook times out, whether a subagent's session id in a hook payload is the parent's, and whether a normal governed command can reach the guard's 5-second timeout on a heavily loaded host.
- Documented ceilings, not fixes: the guard recognizes the Orca CLI only under the name `orca`, the worktree hook has the same limit, and the guard fails open when a hook is stopped at its timeout.
- Moment-in-time: git and installed-copy facts are true for 2026-11-12 (about 02:48 to 18:09 UTC). Local `origin/master` is now `167184c6b`: this branch has 2 commits it lacks and lacks 27 of its commits. Re-run steps 1 and 2 of Section 15.2 before relying on those facts. Its `WORKER-CONTRACT.md` has 338 lines against 327 here, so the reference's contract line numbers hold for this branch and the installed copy only.
- No live Orca was run. Every Orca statement is source reading, not an observation of the running application.

## Open items (yours to decide)

1. **Owner questions.** Section 14.3.1 holds 19 yes or no questions; 18 are open. Only the guard-name question (C6) is answered ("Record as DEFECT, create task"). The reference adopts no decision; leaving them open does not block use of the reference, and the product behavior each describes stays as it is until you decide. The ones that matter most: whether the rule "every Orca worktree gets an agent" should name the claim-flow exception, which `/sc:issue --claim` already uses (C1); and whether the installer should survive a malformed reply from Orca's skill list, which today aborts `superclaude install` at a step meant to be non-fatal (C3).
2. **The guard-name defect.** The launch-level guard (and the worktree gate, as a ceiling) recognizes the Orca CLI only as `orca`, so a session that types `orca-ide`, `orca-dev` or `orca.cmd` is not stopped. It is recorded as a defect and NOT fixed. The remediation plan `.dev/tasks/to-do/TASK-FIX-launch-guard-orca-names-20261111-235205/TASK-FIX-launch-guard-orca-names-20261111-235205.md` is an unreviewed draft (staged, not committed) with a wrong line 17 (it says `make sync-dev` refreshes the plugin mirror; it does not). Next step: have it reviewed with `/sc:workflow`, correct line 17, then run it. The guard-name probes covered `terminal send`, `agent launch` and `worker-start` only under `orca-ide`, and `worktree create` under all three names.
3. **Sub-orchestrator mode and installation.** Sub-orchestrator mode (a proposed middle layer of coordinators working under another orchestrator and above the workers) is deferred and was never shipped (issue #444 holds the question). Whether the clarified ownership wording is rolled out to installed copies is a separate step; none is claimed.
4. **Reinstall command (correction).** To refresh the installed hook scripts after a change, use `superclaude update` or `superclaude install --force`. A plain `superclaude install` skips hook scripts that already exist. Both overwrite installed core files, commands, agents, templates, hook scripts, rules and output styles with no backup, and delete and re-copy each installed skill folder; `settings.json` is backed up. Section 5.6 item 1 states this.
5. **Medium follow-up candidates** (real but non-blocking; no gate fails on them). About seven, after removing duplicates and the ones the reference already fixed:
   - The remediation plan's `make sync-dev` mirror step is wrong (item 2).
   - Section 5.6 no longer describes what the codegraph phase and the retired-MCP step remove, and the reference offers `install --force` and `update` as interchangeable refresh commands in six places although only plain `install` runs those two steps.
   - No read-only command in the reference verifies that the hooks are registered in `~/.claude/settings.json`, and `superclaude doctor` does not check hooks.
   - The reference does not describe what makes an issue launchable by the issue watcher, nor the standalone `ccsession-tag/install.sh` installer.
   - Section 10.3 rows do not say they are instruction text that no code enforces; the two recorded identity-hook runs have no date; the host settings description omits the agent hooks Orca writes; an unscoped "only" about where the guards are registered (lines 319, 983, 1496).
   - Phase 2 research grew from 1,396 to 1,706 lines through its fix cycles, past the 1,500-line review tier, and the tier was not re-checked.
   - The document has no named owner (`assigned_to` is "unassigned") and is 243 lines over its target.

## Process notes you should know

- A reviewer ran `claude --version` once against its brief (it prints a version and starts no session); no verdict uses it.
- Several fix cycles introduced a new wrong sentence in the text they replaced; each was caught by an independent re-read of the source. The last round only deleted text. This is why the final-state validation took four rounds.
- Archival candidates: none. No source document was consolidated, and nothing was moved.

## One question

Do you want me to open one GitHub issue on the fork for the Medium follow-up candidates above? I have not opened one and will not without your answer.
