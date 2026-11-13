# Reviewer 3 card — refactorer lens (structure and distribution fit), shadow06

**Plan:** .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md (82 lines)
**Spec:** .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/source.md (5 lines)
**Mode:** pre-execution plan audit, read-only; codegraph not used (brief: index_state not-run-this-audit); native Read and Grep.
**Date:** 2026-11-13

## What I checked (no finding)

- **Installer list surface.** Task 3 targets `_FRESHNESS_SCRIPTS` (tasklist:61). That is the right surface. `install_hooks.py:42-97` is the single list that is copied to `~/.claude/hooks/` (`:267-268`), and `make verify-sync` requires every `src/superclaude/hooks/scripts/*.sh` to be in it (`Makefile:307-316`).
- **The Makefile claim.** "The Makefile needs no invented Python-script enumeration because the distributable entry point is .sh" (tasklist:64) is correct. `sync-dev` globs `src/superclaude/hooks/scripts/*.sh` and `*.js` (`Makefile:138-143`), and the Installer Registration check uses the same glob (`Makefile:308`).
- **hooks.json registration surface.** Appending a separate PreToolUse `matcher: "Bash"` entry keeps the existing Bash gates as they are (`src/superclaude/hooks/hooks.json:95-114`). The landed entry is at `:125-133`.
- **Preservation and idempotency are achievable.** The installer owns registrations by exact command identity, never by matcher alone (`install_hooks.py:405-422`). On upgrade it inserts in source order (`:460-473`, with the comment "launch-job-identity.sh stays last" at `:463`). So AC tasklist:65 ("Actual installer merge tests confirm preservation and idempotency") can be met on the existing merge code.
- **The fake-source fixture named in Task 3 exists.** `tests/cli/test_install_hooks.py:45` (`fake_source_hooks`) lists hook names at `:103-104`.
- **Self-location.** Task 2's source-relative self-location (tasklist:46) fits both the installed copy (`~/.claude/hooks/...`) and the project `.claude/hooks/` copy that `sync-dev` produces.
- **Prior blocked package immutability.** This is carried as a constraint (tasklist:19). No task targets `.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815`.
- **INF-001 coverage (scoped identity integration).** It is covered on the harness side:
  - Task 1 covers the kernel job identity and survival across new sessions (AC tasklist:36-37).
  - Task 2 covers the PreToolUse Bash adapter, including background calls and later session events (AC tasklist:49-50).
  - Task 4 covers real-Git human-push non-restriction (AC tasklist:77) and the reset/resume sequences (tasklist:78).
  - The launcher side is only documented; see F4.

## Findings

### F1 (MEDIUM, non-blocking, missing-requirement): Task 3's steps omit the hand-maintained plugin mirror

The Task 3 instruction lists only these steps: the `_FRESHNESS_SCRIPTS` entry, the fixture, `src/superclaude/hooks/hooks.json`, the tests, `make sync-dev` and `make verify-sync` (tasklist:61). The AC then requires distribution to "source/plugin mirror surfaces according to this checkout's real build convention" (tasklist:64).

In this checkout the plugin mirror is hand-maintained:
- `make sync-dev` writes only to `.claude/hooks/` (`Makefile:137-143`).
- A prior spec labels the plugin script copy a "hand-maintained mirror" (`.dev/codegraph-migration/specs/phase-1-removal-spec.md:251`).
- Mirror tests require the plugin copy to be byte-identical (`tests/cli/test_install_hooks.py:730-733`).

No step tells the executor to create `plugins/superclaude/hooks/scripts/launch-job-identity.sh` or to add the matching entry in `plugins/superclaude/hooks/hooks.json`. Both exist now (plugin hooks.json:95-104), so the executor found them. As a plan, though, the requirement sits only in an AC that points at an unnamed "real build convention".

### F2 (MEDIUM, non-blocking, constraint-mismatch): "do not stage mirrors" is broader than the governing constraint

Task 3 says "Run make sync-dev and make verify-sync; do not stage mirrors." (tasklist:61). The package constraint is narrower: "Never stage generated .claude mirrors." (tasklist:25).

The plugin mirror under `plugins/superclaude/hooks/` is tracked source that must be committed with the change. Read literally, the Task 3 wording also forbids staging it. Together with F1, an executor following Task 3 could leave the plugin mirror unstaged, so the would ship without the plugin copy.

### F3 (LOW, non-blocking, other): ordering hazard between Tasks 1–2 and Task 3

Task 1 creates `src/superclaude/hooks/scripts/launch-job-identity.sh` (tasklist:31). The plan only adds it to `_FRESHNESS_SCRIPTS` and syncs it in Task 3, which depends on Task 2 (tasklist:59-61).

Between those points, `make verify-sync` fails twice over:
- Installer Registration reports "MISSING from _FRESHNESS_SCRIPTS" (`Makefile:312-316`).
- The Hooks check reports it missing in `.claude/hooks/`.

Commits happen only after the executor finishes (tasklist:25), so this risk is limited to any per-task compliance or pre-commit run of verify-sync during Tasks 1–2. The plan does not say that the drift is expected in the meantime.

### F4 (MINOR, non-blocking, ambiguity): the "launcher" half of the spec is only documented

The spec authorizes "launcher/harness identity integration" (spec:1) through "existing hook/launcher distribution" (spec:5). In the plan:
- Only a "positively governed session record" activates the adapter (tasklist:46).
- No task makes any existing launcher write that record. Task 4 only documents how "the future claim launcher" should create it (tasklist:79).

As a result, the shipped integration has no effect for every real session until later work lands. The plan states this openly (Goal tasklist:15: "an identity foundation"). However, it does not say whether the spec's "launcher/harness" means both halves or either one, so a reader of the spec could expect a launcher-side binding.

## Findings block

```findings-v2
{"id": "F1", "severity": "MEDIUM", "blocking": false, "category": "missing-requirement", "lens": "reflect-pre", "claim": "Task 3's instruction lists only make sync-dev and src-side edits, yet its AC requires the hand-maintained plugin mirror (plugins/superclaude/hooks/scripts and plugins/superclaude/hooks/hooks.json), which make sync-dev never writes; no step names those files.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 61, "line_end": 61, "quote": "Append one PreToolUse Bash registration in src/superclaude/hooks/hooks.json, retaining all current hooks."}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 64, "line_end": 64, "quote": "The exact executable script distributes to the normal installed hooks directory and source/plugin mirror surfaces according to this checkout's real build convention."}, {"role": "spec", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/source.md", "line_start": 5, "line_end": 5, "quote": "Use existing hook/launcher distribution and no new dependencies or services."}]}
{"id": "F2", "severity": "MEDIUM", "blocking": false, "category": "constraint-mismatch", "lens": "reflect-pre", "claim": "Task 3's blanket 'do not stage mirrors' is broader than the constraint 'Never stage generated .claude mirrors' and, read literally, forbids staging the tracked plugin mirror that must ship with the change.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 61, "line_end": 61, "quote": "Run make sync-dev and make verify-sync; do not stage mirrors."}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 25, "line_end": 25, "quote": "Never stage generated .claude mirrors."}]}
{"id": "F3", "severity": "LOW", "blocking": false, "category": "other", "lens": "reflect-pre", "claim": "Task 1 adds a new src/superclaude/hooks/scripts/*.sh but its _FRESHNESS_SCRIPTS listing and sync are deferred to Task 3, so make verify-sync's Installer Registration and Hooks checks fail during Tasks 1-2 and the plan does not declare that interim drift as expected.", "citations": [{"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 31, "line_end": 31, "quote": "Add the proposed standalone src/superclaude/hooks/scripts/launch-job-identity.sh and tests/hooks/test_launch_job_identity.py."}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 59, "line_end": 61, "quote": "Add the new shell script to src/superclaude/cli/install_hooks.py _FRESHNESS_SCRIPTS and the fake-source fixture in tests/cli/test_install_hooks.py."}]}
{"id": "F4", "severity": "MINOR", "blocking": false, "category": "ambiguity", "lens": "reflect-pre", "claim": "The spec authorizes launcher/harness identity integration, but no plan task makes an existing launcher write the governed session record that activates the adapter; the launcher side is only documented, and the plan does not say whether 'launcher/harness' means both halves or either one.", "citations": [{"role": "spec", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/source.md", "line_start": 1, "line_end": 1, "quote": "authorized narrowly scoped launcher/harness identity integration so jobs retain their originating session identity across resets and background execution, without restricting human pushes."}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 46, "line_end": 46, "quote": "Only a positively governed session record in the existing launch-level store authorizes creation of a per-call one-use request."}, {"role": "plan", "path": ".dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/TASK-WF-authorizedNarrow-20261106-214325.md", "line_start": 79, "line_end": 79, "quote": "The documented contract tells the future claim launcher how to create a governed session record and how release affects jobs."}]}
```
reviewer_model_self_report: claude-gw-tier1a (Claude, 1M context)
