# Troubleshoot Report

**Target**: Agents run `orca worktree create` without `--agent`, leaving empty plain terminals.
**Type**: bug
**Tier reached**: 2
**Confidence**: 0.67
**Status**: partial
**Escalation reason**: low_confidence
**Test is wrong**: false
**Behavior is documented**: true
**Doc context card**: .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/doc-context.md
**Duration**: 2095
**Date**: 2026-11-08T02:26:08Z

---

## Summary

The reported issue is the documented behavior — a code change would regress the documented contract. Orca's `worktree create` without `--agent` always opens a plain first terminal (its help says so), and this repo's worktree rule tells agents to run exactly that bare create without saying what to do with that terminal; agents then work in the checkout from their own session, or start the work in a new tab, and the first tab is left empty. The fix is an instruction change (close the first terminal after an own-use bare create; use `--agent` for hand-offs). Status is partial: the merged fix proposal failed its sanity review on one blocking test-plan error (a pinned phrase that would not match the proposed text), so the remediation chain is not offered; a corrected proposal is below but has not been re-reviewed.

## Documentation Context

- **Relevant refs**: CLAUDE.md, src/superclaude/core/CLAUDE.md, src/superclaude/core/WORKER-CONTRACT.md, docs/designs/sc-issue-claim-pipeline-flag.md, docs/designs/sc-issue-command.md, docs/user-guide/commands.md, .dev/tasks/done/TASK-WF-revisedPlanRefac-20261102-213941/
- **Documented behavior**: Orca: a bare create "creates the worktree and its first terminal"; repo: every worktree is created through Orca, with a bare create example; core rule: new Claude sessions use `worktree create --agent` or `agent launch`. No doc says what to do with the first terminal.
- **Restrictions honored**: Orca-only creation (CLAUDE.md:307, :312); no link flags; `/sc:issue` keeps no `--agent` on create; workers keep `worker-start` (WC-13); the 12 pinned launch phrases stay.
- **Restrictions overridden**: None
- **Card path**: .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

Existing instrumentation: Claude transcripts (every Bash call) and Orca's daemon.log (each tab start, with or without a command). Gap: nothing records which caller a tab belongs to; the join is by worktree name and a gap of about 1 to 10 s. Consequence: the mechanism is directly observed in 7 worktrees; the agents' reasons are inferred from their next commands. Verdict capped at partial because discovery ran without auggie.

(Full card: /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: The repo's worktree rule (CLAUDE.md:307-320) requires a bare `orca worktree create`, which by Orca's documented default opens a plain first terminal, and no instruction (project rule, installed core rule, or Orca's bundled guide) says to use or close that terminal.

**Cause class**: Other — an instruction gap; Orca behaves as documented.

**Detailed explanation**: When a create carries no agent (and no activate, setup script, default tabs or startup command), Orca's startup step seeds a terminal with no startup command (Evidence 2-3); creates with a setup script or default tabs open their tabs through a separate background path instead. The create waits for the startup step, and its reply carries no handle for the seeded terminal (Evidence 4). Of 18 hand-typed creates found in transcripts, 17 had no `--agent`: 11 were followed by the same session `cd`-ing into the checkout, and 5 handed work to another session (Evidence 7); in all 5 hand-offs the daemon log shows the agent's tab as a separate, later start, so the first tab was not reused (Evidence 6). Every one of the 7 bare-created worktrees checked has a no-command tab start within about 1 to 10 s of the create (Evidence 6). One control worktree created by `worker-start --agent claude` has no such row (Evidence 9); this control is a single case. The rule that would route hand-offs to `--agent` was added on 2026-11-06, after the hand-off creates, and is not in the installed copy on this host (Evidence 5, 8, 11). Adding `--agent` everywhere is wrong: most creates are for the agent's own use, and `/sc:issue` and supervised workers forbid it.

## Evidence

1. `CLAUDE.md:308` — "Create it with `orca worktree create --name <name>`, adding `--repo <selector>`, `--base-branch <ref>`, and" ; `CLAUDE.md:320` — `orca worktree create --name pm-agent --base-branch origin/master` (no `--agent`, no mention of the first terminal).
2. `/home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-214` — `shouldSeedWorktreePrimaryTerminal({ hasPrimarySurface: startupPaneHeld, callerProvidesSurface: callerProvidesInitialSurface(args) })` then `await ports.createTerminal(\`id:${worktree.id}\`, { surfaceOwner: false })`; `:259-269` — `callerProvidesInitialSurface` is true only for `promisedAgentChat`, or `createdWithAgent` with neither `activate` nor `runHooks` (local IronOrca checkout; equality with installed 1.4.245-aidev02 not proven). This branch runs only when no setup, default tabs or startup apply.
3. `/home/coder/workspaces/IronOrca/src/shared/worktree-first-surface.ts:2-14` — returns `!args.hasPrimarySurface && (!args.callerProvidesSurface || ...)`.
4. `/home/coder/workspaces/IronOrca/src/main/runtime/workspaces/workspace-creation.ts:209` — `} = await startRuntimeLocalWorktreeTerminals({`; `:239-290` — the reply returns a setup terminal handle only with `awaitTerminalProvisioning` and a startup terminal handle only when a startup command was spawned; no seeded-terminal handle.
5. `src/superclaude/core/CLAUDE.md:48-50` — "Use `agent launch` in an existing worktree or `worktree create --agent` for a new checkout; request `--surface terminal` when a CLI session is required. `terminal create` is for shells,".
6. Command: jq over `~/.config/orca/logs/daemon.log` (`startup-command-delivery` per worktree) → `gh-pin-latest 2026-11-01T14:08:55.817Z false 0` then `14:09:27.326Z true 70`; `orca-idle-sleep 2026-11-02T23:09:50.410Z false 0` then `23:09:56.028Z true 28`; `ci-self-hosted-runners 15:50:48.974Z false 0` then `15:50:58.432Z true 70`; `followup-notes-359-360 19:26:05.605Z false 0` then `19:26:16.164Z true 70`; `specstory-symlink-home-fix 12:10:29.242Z false 0` then `12:10:45.190Z true 70`; `install-core-stale-warning 2026-11-07T05:36:16.234Z false 0` only; `fix-flaky-parallel-thread-test 2026-11-07T20:35:31.197Z false 0` only (tier1-observation.md N8).
7. Command: jq over `~/.claude/projects/*/*.jsonl` Bash tool calls matching `orca worktree create` plus the next two calls → 18 creates, 1 with `--agent`; e.g. `955b0bcc 2026-11-07T20:35:28.903Z | orca worktree create --name fix-flaky-parallel-thread-test --base-branch origin/master ...` then `cd /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test && uv run pytest ...` (tier1-observation.md N1, N6).
8. Command: `grep -c 'Orca session launches' ~/.claude/CLAUDE.md` → `0` (mtime 2026-11-05T13:13:32Z); same grep on `src/superclaude/core/CLAUDE.md` → `1` (tier1-observation.md N12).
9. Command: jq over the issue-473-claim transcript → `orca orchestration worker-start --run run_f0e2c5772f56 ... --worktree new-top-level --name issue-473-claim ... --agent claude --json`; its daemon rows start `2026-11-07T06:08:04.272Z true 70` with no `false` row (tier1-observation.md N8, N10).
10. Command: `orca worktree create --help` → "By default this creates the worktree and its first terminal without switching the active Orca view."; no option suppresses the first terminal (tier1-observation.md N2).
11. Command: `git log -S 'Orca session launches' -- src/superclaude/core/CLAUDE.md` → `a368db4c 2026-11-06T22:19:55-05:00 fix(orca): launch Claude CLI sessions and refresh stale guides (#415)` (tier1-observation.md N13).
12. `src/superclaude/cli/install_core.py:70-72` — `if dest_file.exists() and not force:` / `skipped.append(src_file.name)` / `continue`; `src/superclaude/cli/main.py:365` — `superclaude update` calls `install_core_files(force=True)`.
13. `tests/core/test_orca_session_launch_guidance.py:14-31` — exact substring check of 12 pinned phrases within the `### Orca session launches` section of both copies.

## Proposed Fix

The diagnosis is established, but the merged proposal (adversarial/merged-output.md) is NOT ready to apply as written: its sanity review failed on blocker B-1 (self-review.md: the pinned phrase "`orca terminal close --worktree`", with backticks, does not occur in the proposed sentence). The corrected proposal below fixes B-1 and the four minor findings (M-1 to M-4). It has not been re-reviewed.

**Files to change**:
- `src/superclaude/core/CLAUDE.md` — append after the existing "Orca session launches" paragraph (ends at line 53): "A `worktree create` without `--agent` also opens a plain first terminal. If you will work in that new checkout from your current session, close it right after the create with `orca terminal close --worktree path:<path> --all`, only when you created it with no setup script (`--setup skip` or none configured), the repo opens no default tabs, and you have started nothing in it; never run this on a worktree you did not just create. To hand work to a new Claude session, use `worktree create --agent` instead of a bare create; `/sc:issue` and supervised workers keep their own launch steps."
- `src/superclaude/skills/ccsession-tag/README.md` — append the same sentence after its "Orca session launches" paragraph (ends at line 237).
- `CLAUDE.md` (project) — one bullet after line 310 with the same command and guards in short form, pointing hand-offs to "Orca session launches" in `~/.claude/CLAUDE.md`; one comment line in the example block (318-324) showing the close after the create.

**Files that MUST NOT change**:
- `/home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts` — seeding a first terminal is Orca's documented default ("creates the worktree and its first terminal"); removing it changes the contract for every Orca user and flow.
- `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` — its argv is pinned (`test_fo18_exact_commands_and_no_forbidden_flag`; `--agent` forbidden on its create, design D2); any change goes through a separate issue.

**Test to verify**:
- In `tests/core/test_orca_session_launch_guidance.py` add pinned phrases "orca terminal close --worktree" (no backticks; fixes B-1) and "worktree you did not just create" for both copies; the 12 existing phrases must still pass.
- New small test: the project CLAUDE.md worktree section contains "orca terminal close --worktree".
- `uv run pytest tests/core/test_orca_session_launch_guidance.py tests/core/test_claude_md_routing_block.py tests/skills/test_issue_orca_worktree.py -v`.
- Delivery: `make sync-dev`, `make verify-sync`; after merge, `superclaude update` (plain `install` keeps the stale ~/.claude/CLAUDE.md, Evidence 12), then `grep -c 'Orca session launches' ~/.claude/CLAUDE.md` must print 1.
- Live V-CLOSE (pending; needs a create): after a bare own-use create and the close, `orca terminal list --worktree path:<p> --json` lists no terminals and the worktree is still in `orca worktree list`.

**Apply with**: re-review the corrected text, then apply it manually or re-run `/sc:troubleshoot --fix` to enter the plan chain.

## Alternative Fixes Considered

- **Modify the code to change the documented behavior** (make Orca skip the first terminal on a bare create) — Rejected because: **This is the DANGEROUS wrong answer** — would silently break the documented contract for downstream consumers (Orca's help documents the first terminal; it is a separate repo; agents would still need an instruction).
- **Fix 1 — installed core only, no project change** (root-cause-analyst) — Rejected because: misses IronClaude sessions until a reinstall and leaves the example agents copy unchanged (debate C-001, X-002, unanimous).
- **Fix 3 — project CLAUDE.md only** (system-architect) — Rejected because: misses creates in Coder and IronOrca (1 own-use, 4 hand-offs).
- **Fix 2's list-then-close-one-handle** (quality-engineer, the merge base) — Replaced by the guarded `--all` close (debate, 2 of 3 advocates); the dissent is kept as a risk note.
- **Always pass `--agent`** — Rejected because: 11 of 17 creates are for the agent's own use, and `/sc:issue` and workers forbid it.

## Risk + Rollback

- **Likelihood of regression**: low in instruction text; the pinned-phrase test changes must keep all 12 existing phrases.
- **Test coverage of the changed code**: partial — phrase tests prove the text exists, not that agents follow it (compliance unproven).
- **Rollback**: `git revert` of the doc and test commits, then `superclaude update` again to restore the installed copy.
- `--all` stops every terminal in the worktree and removes its tabs, layouts and resume records; the guards limit it to a worktree just created for own use with no setup script and no default tabs. If the guards are misjudged, a single-handle close would bound the damage (dissent). Opening the worktree in the Orca UI later re-seeds a shell; that is user-driven.
- `superclaude update` overwrites local edits to `~/.claude/*.md`.

## Follow-up tasks

- File a backlog issue: `/sc:issue --claim`'s bare create (orca_worktree.py) followed by `agent launch` likely leaves the same empty tab (unobserved on this host). Suggested type: bug. Evidence: tier1-observation.md N11.
- Optional, separate repo: an Orca create option that skips the first terminal. Suggested type: refactor.

## Grounding Gaps

- auggie was unavailable; all discovery used Grep, Read and jq.
- Orca source citations are from the local IronOrca checkout (HEAD dc57b3d6e8); equality with installed 1.4.245-aidev02 is not proven.
- No live create was run (a mutation; re-run permission unknown): V-CLOSE is pending; V-JSON is answered from source only.
- The agents' reasoning text was not read; intent is inferred from their next commands.
- The agent-on-create control rests on one worktree (issue-473-claim, created by `worker-start --agent claude`); creates with `worktree create --agent` were not checked in the daemon log.
- The second empty tab in fix-flaky-parallel-thread-test and the Ironeye empty tab are not traced to a create (other producers, out of scope).
- The Wave 4 merged proposal failed self-review (B-1); the corrected text above was not re-reviewed. Wave 4.5 did not run.
- Adversarial scoring was done by the orchestrating session in two passes, not by independent judges.
- Evidence validation (evidence-validation.md): 16 of 16 file:line citations verified, 6 command outputs matched their captures, 0 dropped. A5 (`consensus_on_unobserved`) fired on a literal reading because one calibration declares `source_static`; it contributes partial and changes no claim, since the mechanism is observed in the daemon log. Prose corrections from the validator's notes (timing gap, control count, Evidence 2 and 4 scope, `superclaude update` citation) are applied above.

## Next Steps

- Pending fix-verification row V-CLOSE (diagnosability-tasklist.md): the fix stays unverified until, after a bare own-use create plus `orca terminal close --worktree path:<p> --all`, `orca terminal list --worktree path:<p> --json` returns zero terminals and the worktree is still listed (works), or a terminal remains / the worktree disappears (does not work). Pending: re-run permission unknown.
- V-JSON is answered from source (Evidence 4) but not observed on the installed binary.
- Core rows M-SEED, M-REUSE and M-CTRL are observed and consistent.
- Because the merged proposal failed review, Tier 3 is not offered: re-review the corrected proposal in Proposed Fix, then apply it manually or re-run with `--fix`.

## Audit

- **Hypothesis cards**: tier1-hypothesis.md, tier2-root-cause-analyst-hypothesis.md, tier2-quality-engineer-hypothesis.md, tier2-system-architect-hypothesis.md (this directory)
- **Adversarial artifacts** (Tier 2 only): .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/adversarial/ (convergence 1.0, base variant 2, status partial)
- **Self-review** (Tier 2 only): FAIL — blocker B-1 (self-review.md)
- **Task file** (Tier 3 only): none
- **Audit log**: .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/audit.log

## Pipeline Hardening Closure

HC0 not run — applicability unassessed (Wave 4 stopped on the self-review blocker before Wave 4.5).

## Addendum: re-review of the corrected proposal

Requested by the user after the report was written (outside the protocol's single sanity pass). The corrected proposal is at .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/adversarial/merged-output-corrected.md. The re-review (self-review-2.md) is PASS: blocker B-1 and minors M-1 to M-4 are resolved. Its two new minor findings (the project test's section boundary; the bullet's insertion point) are folded into the proposal. Report status stays partial because the evidence-validator's A5 contribution still applies. Tests have not been run, and live V-CLOSE is still pending.

## Addendum: owner decision supersedes the text-only fix (2026-11-08)

The owner decided: a session may not create a worktree for its own use; every worktree gets an agent; a session that creates a worktree becomes an orchestrator (or a coordinator under another orchestrator) and owns that worktree's agent(s); a human-created worktree also always needs an agent. The "close the first terminal" proposal (adversarial/merged-output-corrected.md) is therefore superseded. Replacement direction: deterministic enforcement (a PreToolUse(Bash) hook modelled on src/superclaude/hooks/scripts/block-bare-python.sh that blocks `orca worktree create` without `--agent`), an `orca_worktree.py` change for `/sc:issue`, and instruction updates, planned through `/sc:workflow`. Evidence that `--agent` on create leaves no plain tab: tier1-observation.md N10, N14. The worker-contract interplay (WC-13) is tracked in a separate issue on a sub-orchestrator/coordinator mode.
