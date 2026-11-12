# Reviewer 2 brief — persona: qa (model class: haiku)

Mode: UC-1 pre-execution. Audit the proposed plan `.dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/TASK-WF-enforceTheOwnerP-20261108-031809.md` against its source `.dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/source.md` (repo root `/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test`). Your lens: testability and acceptance — is every acceptance criterion observable and would it catch a wrong implementation; are the named test files and line anchors real; which existing tests would break and are they listed; which edge cases (command shapes, failure paths, `--pipeline none`) have no test. You are read-only; audit with Read/Grep/Glob; run nothing.

## T1 card excerpt

(verbatim from t1-card.md)

| id | sev | task | claim | evidence | recommended change |
|---|---|---|---|---|---|
| F1 | HIGH | 1 | Scanner reuse understated: block-bare-python.sh records only the command word and exits at first match (:130-134), returns early on `!need[o]` (:106); the new hook needs per-command argument tracking (`worktree`, `create`, `--agent`, `--help`) resetting at separators, which does not exist. | block-bare-python.sh:99-135 | Say the scanner must be extended with per-command word collection; add tests for `env X=1 orca …`, `sudo orca …`, `command orca …`, `orca … ; orca worktree create --agent x`, heredoc into a shell; list ceilings (`bash -c`, `eval`, `xargs`, `--bare`) in the header as the sibling does at :48-61. |
| F2 | MEDIUM | 4 | `none` creates no worktree, but Wave 0 still STOPs `E-ORCA-REQUIRED` when Orca is down. | claim.md:17; SKILL.md:84, :148; pin test_issue_protocol.py:325-332 | Make the Wave 0 Orca check conditional on `--pipeline` ≠ `none` (update ST-6 pin, SKILL.md Wave 0, error table), or record the decision to keep it. |
| F3 | MEDIUM | 4 | SKILL.md range wrong and other `none` statements not named: return contract SKILL.md:105-136 (Wave 7 block :123-134, `worktree_status` :126); Wave-7-runs-for-none at SKILL.md:91, :150, :170; worktree_path/branch/match_key/warning for `none` unstated; ten-key pin test_issue_protocol.py:503-514. | as cited | Name those lines; four worktree fields `null` for `none`; key list unchanged so ST-10 holds. |
| F5 | MEDIUM | 3 | Reply is an envelope `{"ok","result":{…}}`, so keys sit under `result`; timed-out create (orca_worktree.py:611, 628) has no reply. | test_issue_orca_worktree.py:970 | Read `result.setup`/`result.defaultTabs`; timed-out or unparseable reply → `W-FIRST-TAB-LEFT`, no close; tests for both. |
| F8 | LOW | 4 | No pin in tests/commands/test_issue_command.py quotes the old `none` wording (hits :38, :76, :143, :174); test_issue_protocol.py:443 stays valid. | as cited | Drop the vacuous clause or say the task only adds a Wave 7 skip pin. |
| F9 | LOW | 2, 8 | tests/cli/test_verify_sync_hooks.py mutates/parses `_FRESHNESS_SCRIPTS` and hooks.json (:95-111), not in Task 2/8 lists; `make verify-sync` only in Task 7. | as cited | Add it and `make verify-sync` to Task 2 acceptance. |
| F11 | LOW | 2 | Interaction finding allowed as "test added, or the reason none is needed". | plan :42, :47 | Require one test feeding the original JSON for a bare create with launch-level state present, expecting exit 2. |

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T01:51Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test projectPath=/home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test

### Spec body (source.md, verbatim)

> Enforce the owner policy (2026-11-08): every Orca worktree gets an agent; no session creates a worktree for its own use; a session that creates a worktree becomes its orchestrator (or coordinator under another orchestrator) and owns that worktree's agent(s). Why: agents' bare `orca worktree create` (no --agent) leaves an empty plain terminal every time, because Orca seeds a plain first terminal unless the create carries an agent; 17 of 18 hand-typed creates were bare. Evidence and diagnosis: .dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/REPORT.md (see both addenda) and tier1-observation.md N1, N8, N10, N14 there. Instruction-only fixes were rejected because compliance is unproven; enforcement must be deterministic. Scope: (1) a new PreToolUse(Bash) hook, a sibling of src/superclaude/hooks/scripts/block-bare-python.sh (same decision contract: allow exit 0, block = one stderr message + exit 2, fail open), that blocks a Bash command running `orca worktree create` without `--agent` (allow `--help`) and prints the exact form `orca worktree create --name <name> --agent claude --prompt "<task>" ...`; register it in src/superclaude/hooks/hooks.json and the plugins/superclaude/hooks mirror; tests modelled on tests/hooks/test_block_bare_python.py plus tests/cli/test_install_hooks.py and tests/unit/test_cli_install.py if they enumerate hooks. (2) /sc:issue: src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py creates the worktree bare and then runs `orca agent launch`, which by the same Orca rule leaves a plain tab; change new-worktree creation so the agent comes with the create (keep `agent launch` only for an already existing worktree), keeping the launch-level pending record written before the agent starts; update docs/designs/sc-issue-claim-pipeline-flag.md design default D2 and forbidden-flag FO-18 and the pinned tests in tests/skills/test_issue_orca_worktree.py and tests/skills/test_issue_protocol.py accordingly. (3) Instructions: CLAUDE.md:307-324 worktree rule and its bare example at :320 (the hook would block it) to require --agent and state the ownership rule; src/superclaude/core/CLAUDE.md "Orca session launches" (45-53) and its copy src/superclaude/skills/ccsession-tag/README.md (228-237): add the rule while keeping the 12 phrases pinned by tests/core/test_orca_session_launch_guidance.py. Out of scope: supervised workers (worker-start already creates worktrees with an agent; WC-13 in src/superclaude/core/WORKER-CONTRACT.md is the subject of a separate sub-orchestrator/coordinator issue — do not change the worker contract here), changing Orca itself, closing existing empty tabs. Respect: Orca-only worktree creation, no Orca link flags for this repo, never hardcode src/superclaude/ paths inside installed primitives, make sync-dev + make verify-sync after edits.

### tests/hooks/test_block_bare_python.py (whole file)
(The model the new hook's tests must follow.)

### tests/cli/test_install_hooks.py:90-110, :755-805; tests/unit/test_cli_install.py:130-145; tests/hooks/test_freshness_subagent_start_policy.py:100-120; tests/cli/test_verify_sync_hooks.py:90-115
(Tests that enumerate hooks or `_FRESHNESS_SCRIPTS`.)

### tests/skills/test_issue_orca_worktree.py:790-825, :960-980; tests/skills/test_issue_protocol.py:320-375, :435-450, :500-520
(fo18 three-call pin, LAUNCH_OK envelope, NEVER_FLAGS/LAUNCH_ONLY_FLAGS, Wave 0 ST-6 pin, return-contract key pin.)

### tests/core/test_orca_session_launch_guidance.py:1-40
(The 12 pinned phrases.)

## Coverage slice

| Requirement | Matched task | Status | Note |
|---|---|---|---|
| INF-005..009 hook behaviour (block bare create, allow `--help`, print exact form) | Task 1 | covered | edge-case tests thin (F1) |
| INF-010..013 registration + enumerating tests | Task 2 | covered | F9 missing test file |
| INF-019, INF-020 pinned /sc:issue tests | Tasks 3, 4 | covered | F8, F2 pin |
| INF-021, INF-022 CLAUDE.md rule + example | Task 6 | covered | |
| INF-023..025 core/CLAUDE.md + README, 12 pins kept | Task 7 | covered | |
| INF-033, INF-034 sync-dev + verify-sync | Task 7 | covered | not in Task 2 (F9) |
