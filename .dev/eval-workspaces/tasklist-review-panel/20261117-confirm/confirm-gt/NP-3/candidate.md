---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-authorizedNarrow-20261106-214325
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Per-job launch identity independent of the Claude controller process

Source: ./source.md
Goal: Supply the narrowly authorized job identity integration so background jobs keep their originating logical session while new ordinary work and human pushes in the same worktree remain outside launch policy. Deliver an identity foundation, not the full launch-level classifier or claim pipeline.

## Constraints

- Preserve the original blocked workflow package, its plan and its evidence. Do not manufacture its missing observations or edit its immutable acceptance criteria. This package supplies a new authorized interface for later integration.
- Human pushes remain unrestricted. Neither worktree membership, an inherited environment label nor the long-lived Claude PID selects governed work. A per-tool hook event's session identity and kernel job lifetime establish membership; Linux process start time and boot identity prevent stale PID selection.
- This is a same-user guardrail, not a hostile-user sandbox. No root daemon, cgroup administration, server-side branch policy, new model/provider or dependency is authorized. Use UV for Python. A stdlib Python body behind one distributable shell entry point is allowed by this scoped integration, superseding the earlier bash-only limit for this component only.
- Keep permission evaluation intact: return updatedInput without permissionDecision allow and preserve the entire tool_input object except the command field. Do not disable or replace existing policy hooks. Do not silently auto-approve a rewritten command.
- Scope the initial adapter to Bash tool execution, including run_in_background. Monitor and external execution surfaces must be explicitly reported unsupported unless actually integrated and tested; never claim every tool is covered. A missing per-job identity in an unsupported surface is not proof of a human.
- Use disposable local bare repositories for push tests. Never write protected refs on the real fork. No global hook installation or production activation in this running session. Source distribution and isolated harness settings are in scope.
- Preserve existing dirty design/decision artifacts and document actual behavior. Stage .dev/tasks including evidence. Never stage generated .claude mirrors. Commit/push/PR only after executor completion via the user-requested sc:pr-submit --monitor 3 on IronbellyOrg/IronClaude.

## Phase 1: Create a durable per-job process identity

## Task 1: Implement the job runner and kernel identity selector

Add the proposed standalone src/superclaude/hooks/scripts/launch-job-identity.sh and tests/hooks/test_launch_job_identity.py. Reuse the /proc stat parsing shape of src/superclaude/skills/ccsession-tag/hooks/session-name.sh and cli/sprint/recovery.py conceptually without importing package-only code from an installed primitive. The shell entry point may execute an embedded stdlib Python program through UV. Implement a private state store under the existing launch-level root with one-use launch requests and live job records. The runnable job supervisor owns a separate Linux process session and records its actual PID/start/boot/session identity before executing the requested shell command; records refer to the logical session captured at request creation, never a mutable global controller identity.

Acceptance criteria:
- A request is consumed once, validated as owned private regular data, and cannot be replayed, replaced through a symlink or used with malformed session/job identities. Failures produce plain diagnostics and no requested command side effect. No command text, credentials or environment secrets are emitted in identity diagnostics.
- The supervisor preserves command stdout, stderr and shell exit status. Its own kernel lifetime remains live while ordinary background descendants in its process session are alive, including descendants reparented after their immediate shell exits. It cleans up its own record after the job lifetime ends and reaps children. Signal behavior and the documented completion semantics are tested.
- The identity selector uses the calling process's actual kernel process-session identity, verifies the live supervisor start time and boot identity, and returns the immutable originating logical-session identity only for that job. Forged environment labels, same directory/branch and unrelated human processes do not select membership.
- Tests keep an old governed job alive while a new ordinary job is launched by the same controlling test process. The old job remains associated with its original logical session; the ordinary job and independent human process are unselected. Reused PID/start/boot mismatch, corrupt registry, root exit and explicit release have defined tested outcomes, not silent false human claims.
- Purposeful setsid/daemonization or killing the supervisor cannot be universally covered by this lightweight mechanism; document exact limits alongside the selector's unknown/ordinary outcomes, with regression cases. Do not mark deliberate detached escape as proven retained membership. Record results in ./artifacts/job-runner-tests.log.

## Phase 2: Bind actual tool executions rather than controller launches

## Task 2: Implement the governed PreToolUse Bash adapter

Depends on: Task 1

Extend src/superclaude/hooks/scripts/launch-job-identity.sh and tests/hooks/test_launch_job_identity.py with hook mode. Read the documented PreToolUse session_id, tool_use_id and tool_input fields. Only a positively governed session record in the existing launch-level store authorizes creation of a per-call one-use request. Emit hookSpecificOutput.updatedInput as a copy of the full original input with only command rewritten to the installed job runner. Use source-relative self-location so installed and project copies work. No ccsession-wide environment switch or nearest-Claude PID authority is introduced.

Acceptance criteria:
- Valid unbound/ordinary sessions produce no rewrite or launch-policy output. Bound Bash calls are rewritten once, preserve timeout/run_in_background/description and other fields, preserve working-directory inputs and do not set permissionDecision allow. Non-Bash tools do not silently receive a Bash rewrite.
- Foreground and background calls capture the event's original session generation; a later new session event from the same controller cannot reassign a live old job. Subagent events use the actual documented session field contract and unproven variants are explicitly refused or unsupported rather than guessed.
- Unsupported Linux/proc/dependency states, malformed bound input, command size and conflicting wrappers have defined outcomes. Requests are private and shell quoting preserves literal command content; failed startup/rejected commands do not leave an executable authorization ticket that can be replayed unnoticed.
- Runnable adapter tests exercise real subprocess execution of the emitted command, not only expected JSON. They check stdout/stderr/status, cwd/environment behavior, special characters, background lifetime and release with live children. State any changed shell completion or cwd-persistence semantics explicitly; do not call the adapter transparent without evidence.
- Record the official updatedInput contract and actual tests in ./artifacts/tool-adapter-tests.log. No production launch-level commit/push classifier is added by this task.

## Phase 3: Ship the integration through existing distribution

## Task 3: Package the identity adapter without disturbing other hooks

Depends on: Task 2

Add the new shell script to src/superclaude/cli/install_hooks.py _FRESHNESS_SCRIPTS and the fake-source fixture in tests/cli/test_install_hooks.py. Append one PreToolUse Bash registration in src/superclaude/hooks/hooks.json, retaining all current hooks. Add installer and registration assertions to tests/cli/test_install_hooks.py and tests/hooks/test_launch_job_identity.py as appropriate. Run make sync-dev and make verify-sync; do not stage mirrors.

Acceptance criteria:
- The exact executable script distributes to the normal installed hooks directory and source/plugin mirror surfaces according to this checkout's real build convention. The Makefile needs no invented Python-script enumeration because the distributable entry point is .sh.
- The new registration does not replace bare-python/freshness/user hooks or auto-approve execution. Without positively governed session state it is inert for ordinary sessions. Actual installer merge tests confirm preservation and idempotency.
- Existing tests/hooks and affected installer/sync tests pass through UV with captured output under ./artifacts/distribution-tests.log. Any unrelated failures are separated from failures involving changed files. Generated .claude contents remain unstaged.

## Phase 4: Prove the supported actor boundary and publish its contract

## Task 4: Add real-Git isolation tests and document lifecycle integration

Depends on: Task 3

Extend tests/hooks/test_launch_job_identity.py with disposable local bare-remote integration cases and an isolated observation fixture for the actual Claude hook adapter where the installed CLI permits it without global changes. Use a fixture pre-push observer that invokes the production identity selector; it may refuse protected fixture refs only after positive governed identity. This test-only policy is not installation of the full O-22 hook. Update docs/designs/sc-issue-launch-level-hook.md section 19 with the implemented job contract, source/test paths, supported lifecycle guarantees and remaining Monitor/claim integration prerequisites. Keep historical failed reviews and the prior blocked package honest. Produce ./artifacts/identity-integration-evidence.md and ./artifacts/integration-tests.log.

Acceptance criteria:
- Real Git pushes from governed job descendants to protected fixture refs are recognized and refused by the test policy, while independent human pushes in the same worktree are unselected and succeed. Assert remote ref before/after states and selector evidence, not Git status alone. Old governed background work and new ordinary work can coexist without retagging.
- Tests cover explicit request/release, new logical session IDs/reset sequence, preserved old background identity, resume binding to a new job, stale process data and deliberate detach limitations. Actual harness observations are distinguished from direct hook payload tests; no real /clear or Monitor lifecycle claim is made without observing it.
- The documented contract tells the future claim launcher how to create a governed session record and how release affects jobs. It says clearly that main claim pipeline, full classifier and production pre-push installation remain separate pending work; this scoped integration does not automatically turn the prior plan's missing AC into PASS.
- Any isolated live CLI test uses current verified flags and safe prompts/local fixtures, preserves global settings and records failures as failures. If the environment prevents an actual hook rewrite observation, report that integration blocker rather than claiming live deployment readiness.
- Evidence covers all source requirements and defines the remaining next integration step without inventing a new service. The executor performs its prescribed per-task compliance and final archive review; no extra specification review loops are added.
