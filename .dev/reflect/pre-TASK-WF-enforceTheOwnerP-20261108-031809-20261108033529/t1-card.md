# Tier 1 pre-execution card — TASK-WF-enforceTheOwnerP-20261108-031809

<!-- Returned by reflect-reviewer (read-only), persisted by orchestrator on receipt 2026-11-08T03:40Z. Self-reported confidence 0.8. -->

**best_practice_grade: 3/5.** Well ordered and mostly grounded; cited anchors exist; deviations documented. One under-specified core task (hook scanner), one unaddressed side effect of the `--pipeline none` decision, one internal contradiction in the CLAUDE.md edit.

## Coverage verdict
Every source requirement is covered by a task or a Constraint; no silent drop.
- Documented deviations: agent-not-with-create (FO-18, D2 kept) at plan :20; `none` no-worktree at :19.
- Unmatched INF-004, INF-026..030 are the Constraints at :19-25 (acceptable).
- INF-014, INF-015 are containment false positives: they match Tasks 3/4 by word overlap but those tasks do something different from source.md:1 scope item 2 (plan :51-64); covered only by the Constraints deviation. Record as "covered by deviation", not "matched".
- Undocumented consequence: a claim whose `agent launch` fails (`W-LAUNCH-FAILED`) leaves a worktree with no agent and no tab, breaking "every worktree gets an agent"; no task or Constraint acknowledges it.

## Feasibility spot-checks that hold
- `_FRESHNESS_SCRIPTS` at src/superclaude/cli/install_hooks.py:42, `block-bare-python.sh` at :85.
- hooks.json registrations: src/superclaude/hooks/hooks.json:91 and plugins/superclaude/hooks/hooks.json:61; `launch-job-identity.sh` at :101 and :71.
- Test anchors: tests/cli/test_install_hooks.py:102-103, :760-790; tests/unit/test_cli_install.py:139; tests/hooks/test_freshness_subagent_start_policy.py:105-114.
- `test_fo18_exact_commands_and_no_forbidden_flag` at tests/skills/test_issue_orca_worktree.py:794; three-call list :800-817.
- `NEVER_FLAGS`, `LAUNCH_ONLY_FLAGS` at tests/skills/test_issue_protocol.py:341, :349; `--terminal`, `--worktree` not forbidden.
- orca_worktree.py create block :594-613; new-row handling :614-646.
- `setup`, `defaultTabs` returned at IronOrca workspace-creation.ts:249, :270.
- `agentIdentity` optional in terminal rows (IronOrca runtime-terminal-contracts.ts:39).
- `terminal close --terminal <handle>` exists (IronOrca root-help-text-secondary.ts:72).
- commands/issue.md:43 has the "Every value creates the worktree" wording.
- core/CLAUDE.md:45-53, ccsession-tag/README.md:228-237; 12 pins at test_orca_session_launch_guidance.py:17-30.
- launch-job-identity.sh header: `updatedInput` replaces the whole input (:14-15); [INFERRED] that both hooks receive the original command.

## Findings

| id | sev | task | claim | evidence | recommended change |
|---|---|---|---|---|---|
| F1 | HIGH | 1 | Scanner reuse understated: block-bare-python.sh records only the command word and exits at first match (:130-134), returns early on `!need[o]` (:106); the new hook needs per-command argument tracking (`worktree`, `create`, `--agent`, `--help`) resetting at separators, which does not exist. | block-bare-python.sh:99-135 | Say the scanner must be extended with per-command word collection; add tests for `env X=1 orca …`, `sudo orca …`, `command orca …`, `orca … ; orca worktree create --agent x`, heredoc into a shell; list ceilings (`bash -c`, `eval`, `xargs`, `--bare`) in the header as the sibling does at :48-61. |
| F2 | MEDIUM | 4 | `none` creates no worktree, but Wave 0 still STOPs `E-ORCA-REQUIRED` when Orca is down. | claim.md:17; SKILL.md:84, :148; pin test_issue_protocol.py:325-332 | Make the Wave 0 Orca check conditional on `--pipeline` ≠ `none` (update ST-6 pin, SKILL.md Wave 0, error table), or record the decision to keep it. |
| F3 | MEDIUM | 4 | SKILL.md range wrong and other `none` statements not named: return contract SKILL.md:105-136 (Wave 7 block :123-134, `worktree_status` :126); Wave-7-runs-for-none at SKILL.md:91, :150, :170; worktree_path/branch/match_key/warning for `none` unstated; ten-key pin test_issue_protocol.py:503-514. | as cited | Name those lines; four worktree fields `null` for `none`; key list unchanged so ST-10 holds. |
| F4 | MEDIUM | 6 | CLAUDE.md:305 "give each session its own worktree" and Usage :335-337 (sessions open their own worktrees) contradict "no session creates a worktree for its own use"; Task 6 edits only :312, :320. | CLAUDE.md:305, :333-337 | Add both spots to Task 6 and the new test. |
| F5 | MEDIUM | 3 | Close-step timing and missing cases: seed awaited inside create (runtime-local-worktree-terminal-startup.ts:209-210) but tier1-observation.md:54 says CLI-reply waiting not shown; timed-out create (orca_worktree.py:611, 628) has no reply; reply is an envelope `{"ok","result":{…}}` (LAUNCH_OK at test_issue_orca_worktree.py:970), so keys sit under `result`. | as cited | Read `result.setup`/`result.defaultTabs`; timed-out or unparseable reply → `W-FIRST-TAB-LEFT`, no close; tests for both; keep Task 8 live check blocking. |
| F6 | MEDIUM | 3, 5 | Deviation leaves an agentless worktree when launch fails or the user stops after create. | plan :20; claim.md:123 | Constraint line accepting this, pointing at `W-LAUNCH-FAILED` remedy; mention in Task 5 doc note. |
| F7 | LOW | 5 | Task 5 misses sc-issue-claim-pipeline-flag.md:256, :352, :149-153, :25; §8.3 starts at :175, not ~184. | as cited | Add lines; use :175. |
| F8 | LOW | 4 | No pin in tests/commands/test_issue_command.py quotes the old `none` wording (hits :38, :76, :143, :174); test_issue_protocol.py:443 stays valid. | as cited | Drop the vacuous clause or say the task only adds a Wave 7 skip pin. |
| F9 | LOW | 2, 8 | tests/cli/test_verify_sync_hooks.py mutates/parses `_FRESHNESS_SCRIPTS` and hooks.json (:95-111), not in Task 2/8 lists; `make verify-sync` only in Task 7. | as cited | Add it and `make verify-sync` to Task 2 acceptance. |
| F10 | LOW | 8 | Humans, Codex/other agents, `claude --bare` not covered by the hook; delivery note silent. | block-bare-python.sh:61 | Add a "not covered" line to t8-delivery.md. |
| F11 | LOW | 2 | Interaction finding allowed as "test added, or the reason none is needed". | plan :42, :47 | Require one test feeding the original JSON for a bare create with launch-level state present, expecting exit 2. |

## Ordering and independence
Dependency chain sound; Task 5→4 serial order sensible (shared files). Acceptance criteria observable except F11. Hook interaction [INFERRED] until Task 2's test.

**Self-reported confidence: 0.8.** Unverified: launch-job-identity.sh ordering, Orca live tab timing.
