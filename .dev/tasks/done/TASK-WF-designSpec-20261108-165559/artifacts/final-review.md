# Final review

The independent reviewer returned these review sections directly because their instructions prohibit report-file writes. The executor transcribed the completed review below without changing its findings. The later delivery-manifest coverage check supersedes the reviewer's initial provisional note classification, as stated in that section.

## Task acceptance criteria

Reviewed checkout: `/home/coder/workspaces/worktrees/IronClaude/issue-441`.

Reviewed HEAD: `77a4c70fcdc2f92550bd7c79fb4b5911dcb07100`.

The supplied state digest remained unchanged: `9a61225978203be489ea6bd91ebd5ed1023175763bd4727f1d92f30990696183`.

“Met” test criteria below refer to inspected saved results, not tests rerun during this review.

| Task | Acceptance criteria and current evidence |
|---|---|
| **1. Selector output** | **AC1 met:** reason-bearing and plain unknown outputs are present at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/hooks/scripts/launch-job-identity.sh:237-260`. **AC2 met:** the plugin copy is byte-identical; corresponding output is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/plugins/superclaude/hooks/scripts/launch-job-identity.sh:258-260`. **AC3 met:** the investigation and recorded 151-test pass are in `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t1-unknown-shape.md:16-63`. |
| **2. Hook files** | **AC1 met:** both copies are executable, byte-identical, and carry the required shebang/version; current packaging assertions are at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/cli/test_install_hooks.py:1104-1115`. **AC2 met:** the current hook passed read-only shell syntax validation and contains no source-checkout path; its header is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/hooks/scripts/launch-level-pre-push.sh:1-15`. **AC3 met:** the clean-HOME result and environment limits are recorded at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t2-env-check.md:18-35`. |
| **3. Packaging and pin** | **AC1 met:** packaging, mirror, executable, shebang and hash checks exist at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/cli/test_install_hooks.py:1100-1124`; the saved full regression log includes all 49 installer tests. **AC2 met:** separate one-byte tampering of both copies, failing checks, restoration and the successful subsequent run are recorded at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t3-pin-check.md:9-13`. The current hash matches the updated pin. |
| **4. Push matrix** | **AC1 met:** protected-ref tests distinguish human success from governed refusal at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/hooks/test_launch_level_pre_push.py:441-456`; unchanged remote refs are asserted at `:390-391`. **AC2 met:** the unknown diagnostic and unchanged remote assertions are at `:394-403`; protected refusal followed by feature-branch success is checked at `:661-667`. **AC3 met:** the saved matrix results are included in `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log:834`; the real-second-uid skip has an explicit reason at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/hooks/test_launch_level_pre_push.py:670-674`. |
| **5. Direct records and commit A** | **AC1 met:** the required four suites have successful saved results at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log:834`. **AC2 met:** successful synchronization is recorded at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t3-pin-check.md:17-18`. Direct inspection of commit `e28a71719` confirms only source change-map rows 1-9 and task-package files, with no `.claude/` path. Current touched development copies also match their sources. |
| **6. Installer helpers** | **AC1 unmet, F-FINAL1:** an existing FIFO data-file entry can block indefinitely before the function can return a state. The blocking open precedes the regular-file check at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1190-1196`; the fresh-install conflict path invokes it at `:1381-1383`. **AC2 met:** the current helper parses successfully as Python; the required choices are recorded at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t6-install-choices.md:5-23`. The launched agent’s actual HOME remains explicitly unverified, not claimed observed. |
| **7. Status and launch reporting** | **AC1 unmet for the same FIFO input, F-FINAL1:** status reaches the same blocking validation through `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1243-1244`. Existing, previously noted vocabulary differences between install and status remain disclosed at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-present-unverified.md:17-20`; those historical notes are not newly treated as blockers. **AC2 met:** no current source-text match for the removed state was found; the interim hit list is preserved at that artifact’s `:22-25`, and the updated claim wording is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/refs/claim.md:127-129`. **AC3 met for absent-hook outcomes:** launch warning and switch ordering are at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1698-1705`, with successful-launch assertions at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/skills/test_issue_l2_install.py:630-636`. |
| **8. Installer tests and commit B** | **AC1 met:** the required suites have successful saved results at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log:834`. The unchanged protocol test still names the warning at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/skills/test_issue_protocol.py:481-487`; direct full-range comparison confirms that file is unchanged. **AC2 met:** the obsolete state is absent from current source text; replacement wording is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/refs/claim.md:129`. **AC3 met:** the saved synchronization result is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/retries/T8/review-3.md:13`; direct commit inspection confirms no `.claude/` path in `1090b6098`. |
| **9. Guard tokens** | **AC1 met:** the current token case is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/hooks/scripts/launch-level-guard.sh:708-713`; both copies compare equal, and all 139 token tests have successful entries in the saved regression log ending at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log:834`. **AC2 met:** the updated conflict check is recorded at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t9-u2-check.md:15`; direct comparison from A’s parent through HEAD leaves the protected guard test unchanged. |
| **10. Documentation** | **AC1 met:** current warning-only behavior and the shipped-off refusal are described at `/home/coder/workspaces/worktrees/IronClaude/issue-441/docs/designs/sc-issue-launch-level-hook.md:516`, `/home/coder/workspaces/worktrees/IronClaude/issue-441/docs/designs/sc-issue-claim-pipeline-flag.md:4`, `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/SKILL.md:92`, `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/commands/issue.md:16`, and `/home/coder/workspaces/worktrees/IronClaude/issue-441/docs/user-guide/commands.md:381`. **AC2 met:** method and measured cost are at `/home/coder/workspaces/worktrees/IronClaude/issue-441/docs/designs/sc-issue-launch-level-hook.md:617-623`; no added latency assertion was found. **AC3 met:** the saved no-new-hit and synchronization checks are recorded at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/retries/T10/review-2.md:16`. Direct current diff inspection finds no added installed-primitive source-checkout path, and touched development copies compare equal. |
| **11. Limits and commit D** | **AC1 met:** all 20 limit IDs are covered at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/final-check-retest.md:11-30`; the real-claim observation and waiting item remain pending at `:34-35`, with the owner-machine observations open at `:39-40`. **AC2 met:** commit `719e1587a` was inspected directly and contains only the allowed five non-package paths plus task files. Its saved scope record is at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/retries/T11/review-1.md:10`. |
| **12. Off refusal and final commit** | **AC1 met:** refusal, successful launch and shipped-off assertions are present at `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/skills/test_issue_l2_install.py:623-640`; the owned-hook case installs a genuine hook at `:606-616`. **AC2 met:** the saved result is **820 passed, 3 skipped**, at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log:834`; entries cover all eight required files. **AC3 remains literally unmet, with its history-count gap explicitly accepted:** `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:27-30`. Current history is A, B, stat fix, C, D, E, with E last and separate. The full protected-test comparison is empty. This acceptance does not waive F-FINAL1 or any implementation requirement. |

## Notes, probes, reviews and saved prompts

- Read the current full plan and ledger, the relevant source-snapshot contracts, delivery-file content, saved results, and the retry notes, probes, reviews and repair record. No `step=revert` brief or superseded-prompts directory was present.
- Compared **all 20 saved prompts** against the current closed template in `/home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:322-351`. Every first line matches its task’s ledger start SHA. Every non-slot line matches after ignoring blank lines and trailing whitespace. No saved-prompt blocker remains.
- The first comparison incorrectly treated empty-slot whitespace and the separate `q0-head` commit pointer as prompt failures. Rechecking against the actual ledger start SHA and the required whitespace normalization cleared those false positives.
- Earlier config-state, hook-ownership, documentation-overclaim, measurement-description and refusal-test findings were checked against current files. Their corrected outcomes remain present. The earlier six-failure Task 7 test result is historical: later saved results cover the rewritten assertions successfully.
- Existing all-no entries are **noted**, not reopened as unmet criteria. This includes state-vocabulary differences, evidence-line drift, test-strength observations and documentation precision.
- The stat exception matches the current absolute-path, timeout-bounded call and the recorded decision at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:9-15`.
- The narrowed tamper-token case matches the recorded exception at that file’s `:21-23`; its former overbroad transport claim is corrected. The protected test remains unchanged.
- The history-count acceptance is explicitly limited at that file’s `:30` and `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/progress.md:27-28`. It is not represented here as literal five-entry compliance.

### Delivery-manifest coverage check

This check supersedes the earlier provisional classification of the malformed manifest entries as an all-no note.

All eight intended files exist, but **none appears in any well-formed `files=` token anywhere in the current ledger**. No well-formed directory token covers them either. They are therefore genuinely outside the helper’s delivery-byte digest, not merely duplicated under malformed names.

The exact malformed tokens are below. Line numbers refer to `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/progress.md`.

| Ledger line | Exact malformed token |
|---|---|
| 6 | `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t2-env-check.md notes@./artifacts/retries/T2/notes.md:1-4` |
| 10 | `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md notes@./artifacts/retries/T4/notes.md:1-6` |
| 12 | `tests/hooks/test_launch_level_pre_push_records.py notes@./artifacts/retries/T5/notes.md:1-2` |
| 14 | `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t6-smoke.py notes@./artifacts/retries/T6/notes.md:1-6` |
| 16 | `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py notes@./artifacts/retries/T7/notes.md:1-10` |
| 18 | `tests/skills/test_issue_orca_worktree.py notes@./artifacts/retries/T8/notes.md:1-9` |
| 20 | `tests/hooks/test_launch_level_guard_l2_tokens.py notes@./artifacts/retries/T9/notes.md:1-3` |
| 22 | `docs/user-guide/commands.md notes@./artifacts/retries/T10/notes.md:1-3` |

The corresponding real files absent from **every** well-formed token are:

1. `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t2-env-check.md`
2. `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t4-matrix-map.md`
3. `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/hooks/test_launch_level_pre_push_records.py`
4. `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t6-smoke.py`
5. `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t7-smoke.py`
6. `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/skills/test_issue_orca_worktree.py`
7. `/home/coder/workspaces/worktrees/IronClaude/issue-441/tests/hooks/test_launch_level_guard_l2_tokens.py`
8. `/home/coder/workspaces/worktrees/IronClaude/issue-441/docs/user-guide/commands.md`

The helper splits the ledger field only on commas at `/home/coder/.claude/skills/sc-implement-protocol/scripts/archive_workspace.py:394`. It retains each annotated string as a pathname and hashes its missing entry as `absent` at `:269-274`. The resulting manifest contains 24 real file paths and eight nonexistent annotated names. A change to any of the eight actual files above would not change this supplied delivery digest.

## Findings

### F-FINAL1: An invalid data-file FIFO can hang installation and status

**Severity:** blocking.

**Affected criteria:** T6.AC1; the shared validation path also prevents T7.AC1 from returning a status for this input.

**Current defect location:** `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1190`.

| Checklist | Answer | Anchor |
|---|---|---|
| `ac-outcome-missing` | **yes** | T6.AC1 requires the installer to “return[] one of the source §7.4 states with a reason” at `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:97`. |
| `false-claim` | no | No separate false textual claim is needed for this finding. |
| `harmful-effect` | no | The finding is a blocked operation, not an unauthorized write or deletion. |
| `quoted-constraint-breach` | no | The unmet required outcome is sufficient; no additional constraint breach is asserted. |

An existing `pre-push.launch-level` FIFO with no writer reaches `os.open(path, os.O_RDONLY | os.O_NOFOLLOW)` before the descriptor is checked for a regular file. A blocking read-only FIFO open waits for the other end, so execution never reaches `stat.S_ISREG` or returns `conflict`.

Both relevant routes are present in current code:

- Fresh installation encounters the existing data pathname and calls this validator at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1381-1383`.
- Status of an otherwise owned hook calls it at `/home/coder/workspaces/worktrees/IronClaude/issue-441/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1243-1244`.

The required conflict behavior for an existing differing data entry is explicit in `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md:185`. Linux documents the blocking behavior in [fifo(7)](https://man7.org/linux/man-pages/man7/fifo.7.html).

**Fix:** make opening the candidate data entry nonblocking while retaining symlink refusal and descriptor-based type/owner/mode checks. Add a bounded regression for a FIFO with no writer through both installation and status; each must promptly reject it without replacing it.

**Verification limit:** this finding is established by current control flow and documented FIFO semantics. No FIFO fixture was created and no runtime reproduction or tests were run, as instructed.

### F-FINAL2: Eight delivery files are omitted from the archive-state digest

**Severity:** blocking.

**Affected scope:** the managed FINAL/archive contract. This finding does not claim that the eight underlying task outputs are absent or that their verified contents are false.

**Current defect location:** `/home/coder/workspaces/worktrees/IronClaude/issue-441/.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/progress.md:6`, with the same defect at lines 10, 12, 14, 16, 18, 20 and 22.

| Checklist | Answer | Anchor |
|---|---|---|
| `ac-outcome-missing` | no | The intended files exist and their relevant contents were inspected. |
| `false-claim` | no | No additional false claim about their underlying task outcomes is asserted. |
| `harmful-effect` | no | These ledger entries themselves perform no write, deletion or secret exposure. |
| `quoted-constraint-breach` | **yes** | The governing archive instruction says **“list every delivery file there”**, referring to the ledger `files=` field, at `/home/coder/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:54`. |

The coverage check establishes that all eight files are omitted from every correctly parsed delivery token. This violates the explicit managed archive instruction, rather than merely producing an inaccurate citation for an otherwise verified claim. It also defeats the intended freshness comparison for those files: `/home/coder/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:56` requires a changed delivery state to invalidate the review.

**Fix:** correct the affected ledger fields so each actual delivery pathname is a separate valid token, preserving the review-note references without incorporating them into filenames. Then generate a fresh state manifest and conduct a fresh FINAL review. Do not reuse the old digest or silently treat the old review as bound to the corrected delivery set.

No ledger or delivery file was modified during this check.

## Self-Audit

- Checked current hook parsing, actor precedence, unknown diagnostics, selector reasons, source/plugin parity, hash pin, packaging, publication order, status validation, launch ordering and the refusal switch.
- Checked six commit subjects, attribution endings and changed-path scopes directly. No commit contains a `.claude/` path or an out-of-scope top-level path. Both protected comparisons are empty: the guard test and the unchanged issue-protocol test.
- Inspected all eight suites’ saved result entries: 820 passed, 3 skipped, no failed/error entries. The three skips correspond to the documented second-uid cases. These results do not exercise the newly identified data-file FIFO path.
- Current source and source-snapshot hashes match the ledger pins. The supplied state digest recomputes unchanged. Seven touched development primitive copies and all three hook plugin mirrors compare byte-identical.
- Codegraph did not index the shell hook, so bounded filesystem reads were used instead.
- No test suite, build, source edit, report-file write, commit, push or PR was performed. Read-only Python parsing, byte comparisons, searches and shell syntax validation were performed.
- Owner-machine observations, live claim checks and the launched agent’s actual HOME remain unverified as disclosed. Local remote-tracking references do not contain HEAD, but that cannot prove that no historical push ever occurred.
- Owner-acceptance provenance was inspected in the stored ledger and deviation records; this review did not independently authenticate the external conversation.

## Result

**issues**

Two blocking findings remain:

1. **F-FINAL1:** a FIFO data-file entry can block installation and status before a required state is returned.
2. **F-FINAL2:** eight actual delivery files are omitted from the managed archive-state digest.

The scoped acceptance of the six-entry history remains unchanged and does not waive either finding. Do not archive on this review.

Tests and builds were not rerun. The FIFO finding remains static analysis; the manifest-coverage finding was verified directly against the full current ledger and helper parsing.
