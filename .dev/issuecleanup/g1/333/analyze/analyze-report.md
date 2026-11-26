# Crash recovery bootstrap architecture analysis

Template: /sc:analyze Behavioral Flow and Output sections.
Command: /sc:analyze src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/333/analyze

## Scope and grounding
Static architecture review of the single scanner, with its direct skill consumer and existing regression test. No source changed; no dynamic execution was performed by this command.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:01:21Z; degraded: graph:empty

The fresh graph does not index this shell file: directory discovery returned only parse_session_log.py, and the scanner outline lookup returned no indexed file. Read/Grep supplied source and references; graph caller, callee and impact evidence is unavailable for this file.

## Architecture and metrics
The scanner is 171 lines of Bash with eight helpers and a final JSON document. It gathers session paths and pipeline artifacts first, then interpolates git, sprint, task and memory summaries. Strict shell failure handling is enabled at src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:8.

The direct consumer at src/superclaude/skills/sc-crash-recovery/SKILL.md:58-79 selects investigators from this inventory. Its failure fallback at lines 134-145 continues git-state and claude-sessions while marking pipeline-artifacts and project-memory unscanned: recovery is degraded, not necessarily stopped. The scanner execution test at tests/unit/test_crash_recovery_bootstrap.py:22-47 always creates the session directory.

## Severity-rated findings
1. **Medium severity, confirmed static defect: optional session storage becomes a fatal dependency.** At src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:65-69 an absent session directory executes a bare return, preserving the failed directory check's status 1. The unconditional pipeline assignment at line 136 propagates failure under line 8's strict handling before JSON begins at line 143. New projects without session history cannot supply the inventory. The test creates the directory at tests/unit/test_crash_recovery_bootstrap.py:27-31 and misses this case.
2. **Unverified reliability risk: bounded pipelines close early.** Scanner lines 67-68 and 60-61 use head under pipefail. Producer SIGPIPE depends on volume and buffering; the historical exit 141 is not established by this static review and is not a confirmed second defect.

No security vulnerability or measured performance regression was established; those domains were not audited.

## Recommendations
Keep the small shell architecture. Make the absent-session guard return success explicitly; add a missing-session-directory JSON regression beside the existing test and cover empty/populated session directories. Exercise high-volume session and artifact lists before claiming exit 141 fixed; if confirmed, make bounded producers safe without suppressing unrelated failures. No rewrite, new dependency or adjacent cleanup is needed.

## Verification limits
Static only: runtime exit codes, high-volume SIGPIPE, timing claims and deployed installations are UNVERIFIED by this command. Paths above are relative to /home/coder/workspaces/worktrees/IronClaude/Issuecleanup. The surrounding issue review may add separately recorded runtime evidence after the command finishes.
