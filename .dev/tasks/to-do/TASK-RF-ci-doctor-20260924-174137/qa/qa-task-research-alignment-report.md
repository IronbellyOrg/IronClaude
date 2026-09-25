# Task–Research Alignment Audit

**Date:** 2026-09-24
**QA mode:** task-integrity
**Lens:** task-research-alignment
**Fix authorization:** false; read-only audit
**Verdict:** PASS (previous staged-diff omission closed; task instructions only, not execution evidence)

## Scope and source reconciliation

- `BUILD-REQUEST.md:8,11-19` authorizes task construction from completed skill-delegated research, **not execution**; `research-notes.md:9-14,21-38` covers the workflow, installer, doctor, existing test and pending remote verification. No `research/` fan-out is required.
- The observed prerequisite gap is confirmed by `.github/workflows/test.yml:195-219`: the Python-package install at lines 213-215 is immediately followed by the unchanged doctor command at lines 217-219. The diagnosis (`REPORT.md:31-52`) calls for exactly one intervening native-install step, not a doctor change. `main.py:180-198` installs skills, wires ccsession and installs hooks; `doctor.py:52-103` reports missing native artifacts. Feature spec FR-1/FR-4 (`ccsession-native-install.md:97-109,140-150`) supports that contract but does not specify the CI change.
- No current workflow edit was observed: `git diff -- .github/workflows/test.yml` was empty at audit time. This audit assesses instructions, not implementation or a post-fix CI run.

## Item-to-authorization mapping

| Task item | Authorized source and concrete check | Alignment |
|---|---|---|
| 1.1 | `BUILD-REQUEST.md:19`; `research-notes.md:37-38`. Requires separate execution approval before editing anything and names the correct worktree (`TASK...md:98-102`). | PASS |
| 2.1 | `BUILD-REQUEST.md:11,16`; `REPORT.md:46-50`; workflow lines 213-219. Exactly one named `run: |` / `superclaude install` step between package install and existing doctor; no other job or doctor edits (`TASK...md:104-108`). | PASS |
| 3.1 | `BUILD-REQUEST.md:17`; `research-notes.md:12`; existing isolated install fixture/test at `tests/cli/test_update_command.py:113-151`. Reuses test without inventing doctor coverage (`TASK...md:110-114`). | PASS |
| 3.2 | `BUILD-REQUEST.md:16-17`; FR-1/FR-4. Requires fresh external temporary HOME for pre-install fail-on-missing, install, and post-install doctor, with exit codes and artifact check (`TASK...md:116-118`). No real-HOME install is requested. | PASS |
| 3.3 | `TASK...md:120-122` now requires `git diff --cached --quiet -- .github/workflows/test.yml` before inspection and agreement between unstaged and `git diff HEAD` workflow diffs. Staged changes stop the check without unstaging user work. | PASS |
| 4.1 | `TASK...md:126-128` repeats the clean-index guard before saving `workflow.diff` and compares the saved diff against `git diff HEAD -- .github/workflows/test.yml`, blocking incomplete or empty evidence. | PASS |
| 4.2 | `TASK...md:130-132` requires the independent runner to verify the saved diff is nonempty, the staged diff is empty, and the saved contents equal `git diff HEAD` before running POST; otherwise it returns `RUN_INCOMPLETE`. | PASS |
| 4.3 | `BUILD-REQUEST.md:16,18-19`; requires completed POST and records remote doctor-check rerun as **pending** a separate authorized push, without commit/push/PR edits (`TASK...md:134-136,164-166`). | PASS |

## Previous finding — Resolved: staged workflow changes cannot be omitted

**Re-evaluation:** Step 3.3 (`TASK-RF-ci-doctor-20260924-174137.md:120-122`) stops if the staged workflow diff is nonempty, then compares the unstaged workflow diff to the complete HEAD-relative workflow diff. Step 4.1 (`:126-128`) repeats the guard and compares the saved `workflow.diff` against HEAD; Step 4.2 (`:130-132`) independently repeats both preconditions and returns `RUN_INCOMPLETE` if either fails. Thus a staged-only or mixed staged/unstaged workflow edit cannot silently disappear from the saved POST input. Stopping without unstaging preserves existing user work; these instructions do not authorize changes to the workflow during this audit. **Disposition:** CLOSED; no remaining gap for this finding.

## Authorization and truthfulness checks

- `spec_path: ""` and `reflect_pre.skip_reason: "no-spec"` (`TASK-RF-ci-doctor-20260924-174137.md:18-27`) match `BUILD-REQUEST.md:12`; the feature spec appears only in `related_docs` (`TASK...md:30-36`). POST does not pass `--spec` (`:132`).
- Task-file creation does not imply permission to execute, commit, push or alter PR state (`TASK...md:58-60,70-73,89-102,134-136`); task status remains To Do and checklist entries unchecked. No item instructs modification of `src/superclaude/cli/doctor.py`; `BUILD-REQUEST.md:11,19` and `REPORT.md:48-52` agree with this boundary.
- No instruction claims remote CI has passed: `TASK...md:60,164-166` explicitly defers the remote doctor-check rerun. The local integration test does not pretend to be a remote CI result (`research-notes.md:12,21-23`). The isolated install/doctor commands set a temporary HOME for every invocation (`TASK...md:116-118`), unlike running install against the actual HOME.

**Counts:** 1 previous gap re-evaluated across 3 validation items; 1 resolved, 0 remaining gaps. No workflow edit, staging, unstaging or execution was performed in this re-evaluation. `TASK...md` denotes `TASK-RF-ci-doctor-20260924-174137.md` in this report; `REPORT.md` denotes `.dev/troubleshoot/ci-pr236-doctor-20260924172307/REPORT.md`.
