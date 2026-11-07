# Reviewer 3 brief (refactorer lens)

This is a UC-1 pre-execution review: there is no diff. Audit the TASKLIST at `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md` against the SPEC (the design) at `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md`. A 'deviation' here is a place where the plan omits, contradicts, reorders or over-reaches the design, or would break an existing test or invariant. Map classes as: Authorized = plan goes beyond the design with a stated basis; Necessary = plan departs from the design for a stated, real constraint; Drift = plan omits or alters a design instruction with no rationale; Regression = plan step would break an existing test, invariant or documented rule. Ground every finding at file:line (plan lines or spec lines or repository files). Read the live repository only to verify a cited fact; do not modify anything.

Lens: Structure, task size and reviewability. Focus: can each task be implemented and reviewed alone from its text plus the Constraints? Are there dependency edges missing or too weak? Is any task too large to review?

## T1 card excerpt

```yaml
  - id: F-1
    kind: plan-sequencing
    severity_proposed: IMPORTANT
    claim: >-
      Task 1 creates scripts/orca_worktree.py but its SKILL.md files-table row is only added in Task 4;
      Task 5 creates templates/launch-prompt.md but its row is only added in Task 7. The existing test
      requires every scripts/*.py and templates/*.md on disk to be named in SKILL.md, so the existing
      suite is red between those tasks.
    evidence:
      - "tests/skills/test_issue_protocol.py:131 def test_every_named_path_exists_and_every_file_is_named"
      - "tests/skills/test_issue_protocol.py:141 assert sorted(on_disk - named) == []"
      - "plan:30 Task 1 heading (creates the script); plan:86 Task 4 adds the script table row"
      - "plan:95 Task 5 heading (creates the template); plan:130 Task 7 adds the template table row"
    recommendation: "Add the SKILL.md files-table row for the script to Task 1 and for the template to Task 5, and keep Tasks 4 and 7 for the prose edits."
  - id: F-5
    kind: reviewability
    severity_proposed: MINOR
    claim: "Task 2 packs list, four-key lookup, create, set difference, file-by-file copy and the record into one task with 17 named test cases."
    evidence:
      - "plan:45 Task 2"
    recommendation: "Optionally split copy and record (steps 5 to 7 of design 8.3) into a second task."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T06:36:50Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag projectPath=/home/coder/workspaces/worktrees/IronClaude/sc-issue-claim-pipeline-flag

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:45-65

````markdown
## Task 2: Add the worktree subcommand to orca_worktree.py

Depends on: Task 1

In `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` add `worktree --repo <R> --number <N> --base origin/<B> --source <D>`, printing `{status, path, branch, match_key, warning, detail}` with `status` one of `created`, `reused`, `failed`. Source: design section 8.3 (algorithm table steps 1 to 7, command list, record guard), merged-requirements.md sections 2.4, 2.5 and 5, and FR-15, FR-16, FR-17, FR-18, FR-20.

The commands the script runs are exactly: `git rev-parse --path-format=absolute --git-common-dir`; `git fetch origin`; `git rev-parse --verify origin/<B>`; `orca worktree list --repo path:<main> --limit 500 --json`; `orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json`; `git -C <wt> rev-parse --path-format=absolute --git-common-dir`; `git -C <wt> ls-files .dev/issues/<N>`. No other `orca` or `git worktree` call (no `git worktree add`, no `orca worktree rm`, no commit, push or stage).

Behaviour to implement and test in `tests/skills/test_issue_orca_worktree.py`, with list fixtures copied from the live `orca worktree list --json` shape (nested `result.worktrees` rows with `id`, `path`, `branch` as full refs, `comment`, `isMainWorktree`, `isArchived`; `result.truncated`; `result.hostScope.omittedHostIds`):
- List unusable (`ok` not true, `truncated` true, `omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true`), including the after-create list: a `worktree.json` record in the source directory whose path exists and shares the git-common-dir is reused with match key `record` and detail "unverified"; otherwise `failed` with `W-ORCA-LIST-FAILED` and no create call.
- Lookup over rows with `isArchived` false, key order marker (comment contains `sc:issue <R>#<N>` not followed by a digit), record, basename (`^issue-<N>(-|$)`), branch (same pattern on the last `/` segment). Hits deduplicated by row id, first key with a hit decides; one live hit is `reused`; stale hits only is `failed` with `W-WORKTREE-STALE`; two or more live hits is `failed` with `W-WORKTREE-AMBIGUOUS` listing all paths; none of these calls create.
- No hit: a missing `origin/<B>` is `failed` with `W-ORIGIN-BASE-MISSING` and no create call; a failed `git fetch origin` with the ref present continues with warning `W-ORIGIN-BASE-STALE`. After create (exit 0 or timeout) list once more and take the row-id set difference: exactly one new row whose basename matches the issue pattern is `created` and its `path` is the worktree path (never read from the create JSON); zero new rows is `failed` with `W-WORKTREE-CREATE-FAILED` ("created but not listed"); two or more is `failed` with `W-WORKTREE-AMBIGUOUS` and no copy or record; a nonzero create exit is `failed` with `W-WORKTREE-CREATE-FAILED` and the first stderr line, never retried.
- Copy the source directory into `<wt>/.dev/issues/<N>/` file by file including `analysis/`, never as one recursive directory copy: skip entirely when source and destination share a realpath; never copy `worktree.json`; skip and name a file that `git ls-files` shows as tracked; copy a missing file; skip an identical file; rename a differing untracked file to `<name>.prev` (replacing an older `.prev`), copy, and name it in `W-WORKTREE-COPY-FAILED`. A copy error or byte mismatch after copy is `failed` with `W-WORKTREE-COPY-FAILED`; a destination whose git-common-dir differs from the main checkout's is `failed` with `W-WORKTREE-STALE`.
- Only on `created` or `reused`, write `worktree.json` in the source directory as `{"path": "<absolute>", "status": "created|reused"}`, keeping any existing `launch` entry.
- The warning field holds the one code that set the status; any other problem goes in `detail`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k "FO or worktree"` passes with cases FO-1, FO-2, FO-3, FO-4, FO-6, FO-7, FO-8, FO-9, FO-10, FO-11, FO-12, FO-13, FO-14, FO-15, FO-16, FO-17 and FO-18 of design section 13 (each named in the test function name or id).
- FO-18 asserts the create argument list equals the command above exactly and that no forbidden flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`) appears in any recorded `orca` call.
- `grep -n "worktree add\|worktree rm\|git commit\|git push\|git add" src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` finds no executed command.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:110-121

````markdown
## Task 6: Add the launch subcommand, the launch record and the shim check

Depends on: Task 2, Task 5

Add `launch --number <N> --source <D> --level worktree|full [--submit]` to `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` and extend `tests/skills/test_issue_orca_worktree.py`. Source: design sections 6 and 8.4, and hook design `docs/designs/sc-issue-launch-level-hook.md` IR-1, IR-2, IR-5. Output: `{status, warning, detail, terminal, launched_at, enforcement_hook, hand_command}` with `status` one of `launched`, `failed`, `already_launched`.

Behaviour: read `worktree.json` in the source directory through the record guard (path exists, git-common-dir equals the main checkout's by realpath); a missing or failing record is `failed` with `W-LAUNCH-FAILED`. A record with a `launch` entry returns `already_launched` with its `at` time and calls neither `orca` nor writes a launch record. `enforcement_status()` returns `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`; `missing` sets `W-ENFORCEMENT-ABSENT` but does not stop the launch. Publish the launch record at `$HOME/.claude/state/launch-level/pending/<nonce>` (nonce `secrets.token_hex(16)`, directories mode 0700, file mode 0600, content exactly one word `worktree`, `full` or `full-submit`, written to a temporary name and renamed to the nonce); a write error is `failed` with `W-LAUNCH-FAILED` and no launch. Then run `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json` with no `--model` and no `--effort`; a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command` (the same call without the marker). Then the ccsession shim check: take the first string value under any key named `handle` in the launch JSON by a recursive walk, call `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart (the sleep is injectable so tests run fast), and pass when `result.terminal.tail` text contains `[ccsession]` or `Session name (Enter or Ctrl+C`; no handle, an unreadable terminal or no match sets `W-LAUNCH-NOT-CCSESSION` and keeps the launch. Finally write `launch: {level, submit, at}` (UTC ISO time) into `worktree.json` whatever the shim result, and return `launched`.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_orca_worktree.py -k launch` passes with LA-1 (exact launch argument list, prompt starts with `[sc-launch:v1:` plus 32 hex characters and `] `, no leading `/`, no `--model`, no `--effort`, no link flag), LA-2 (record is a regular file of mode 0600 in a 0700 directory holding the exact word for the level, published before the launch call, same nonce in the prompt), LA-3 (failed launch removes the record; read-only store makes no launch call), LA-4 (`launch` entry gives `already_launched` with no `orca` call; the entry is written even when the shim check fails), LA-5 (shim pass on `[ccsession]` and on the question text; fail on neither, unreadable terminal, no handle), LA-6 (`installed` and `missing` hook script, launch happens in both).
- No file is created inside the worktree or the source directory by `launch` other than the `launch` entry in `worktree.json`.

````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md:139-160

````markdown
## Task 8: Amend the original design document

Depends on: Task 7

Edit `docs/designs/sc-issue-command.md`. Source: design section 2 (B2 rewritten text, P6), section 12 (change table row for this file) and `docs/designs/sc-issue-claim-pipeline-flag.md`.

Rewrite the B2 row of the section 2 table to the new text (the claim writes the summary and `next-steps.md`, creates a worktree and launches one agent; neither the skill nor the default agent runs `/sc:implement` or `/task`; `--pipeline full` lets the agent run them; `--submit` additionally lets it commit, push and run `/sc:pr-submit`; merging never happens). Add rows B16 (a worktree is created after `next-steps.md`), B17 (launch levels worktree, full, none; launch behind the ccsession shim through `orca agent launch --surface terminal`) and B18 (`--submit` turns on commit, push and `/sc:pr-submit --monitor 3`, never merges). Add a short "Amended 2026-11-07" note pointing to `docs/designs/sc-issue-claim-pipeline-flag.md` in sections 1, 4, 7, 14, 16 and 20, and add the new script, template and test file to the section 15 file list.

Acceptance criteria:
- `grep -n "B16\|B17\|B18" docs/designs/sc-issue-command.md` shows the three new rows, and the B2 row no longer says the claim "stops after writing the next-step prompt".
- The folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` exists with `merged-requirements.md`, `launch-levels-addendum.md`, `seed-brief.md`, `adversarial/` and `enrichment/`, ready to be staged with the change.

## Task 9: Update the user guide and routing guide, then sync

Depends on: Task 7

Edit `docs/user-guide/commands.md` (the `/sc:issue` section starting at its `### /sc:issue` heading and its table row), `src/superclaude/core/HOW-WE-WORK.md` (the `/sc:issue` row of the "Other commands" table) and copy that file byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. Source: design sections 1, 4 and 12.

In the user guide: update the usage lines, add the two flags with the four levels (`worktree` default stops at an approved plan, `full` implements without commit or push, `full` with `--submit` commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, `none` creates the worktree and launches no agent), state that no level merges and that Orca is required (`E-ORCA-REQUIRED`), and add examples. In the routing row replace "then stops without running them" with a statement that a claim also creates a worktree and launches an agent at the chosen level and never merges. Then run `make sync-dev`.

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` reports no difference, and `uv run pytest tests/core tests/commands tests/skills tests/recommend tests/cli/test_issue_body_templates.py -q` passes.
````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:163-215

````markdown
## 8. The script `scripts/orca_worktree.py`

Python standard library only, run as `uv run --no-project python "<skill base>/scripts/orca_worktree.py" <subcommand> ...` (the `clickup_claim.py` pattern). One JSON object on stdout. Exit 0 for every runtime outcome; exit 2 only for bad arguments (argparse). Every subprocess runs without a shell, with a timeout (120 s; `preflight` 30 s; each `terminal read` 15 s) and captured output. A timeout is a failed command, not an exception. FR-5: no other file calls `orca` or runs worktree git commands.

### 8.1 `preflight`

`orca status --json`. `{"ok": true}` when it exits 0, prints JSON with `ok: true` and `result.runtime.reachable: true`; otherwise `{"ok": false, "detail": "<first stderr line, or why the JSON failed the test>"}`. A missing `orca` binary gives the same shape (no separate code, P1).

### 8.2 `prompt`

Reads the template, keeps the `<!-- block:common -->` block plus `worktree` (when `--level worktree`) or `full` (when `--level full`), plus `submit` when `--submit` is passed, drops all other blocks and the block marker lines, replaces `<N>`, writes `--out`. `--submit` with `--level worktree` is bad arguments (exit 2). Output `{"status": "written", "path": "<out>"}`. This is rendered by code, not by the model, so the "do not run" lines cannot be dropped by a paraphrase.

### 8.3 `worktree`

Arguments `--repo <R> --number <N> --base origin/<B> --source <D>`. Output `{status, path, branch, match_key, warning, detail}` with `status` `created | reused | failed`. The algorithm is MR section 5 with AD section 4 applied; commands are MR section 4 exactly, each with a 120 s timeout:

```text
git rev-parse --path-format=absolute --git-common-dir
git fetch origin
git rev-parse --verify origin/<B>
orca worktree list --repo path:<main> --limit 500 --json
orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json
git -C <wt> rev-parse --path-format=absolute --git-common-dir
git -C <wt> ls-files .dev/issues/<N>
```

| Step | Rule | MR |
|---|---|---|
| 1 | Resolve `<main>` from the absolute git-common-dir. | 5 step 2 |
| 2 | List. Unusable (FR-15): `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true` (field names verified on a live `orca worktree list --json` on 2026-11-07). Then a `worktree.json` record that passes its guard is `reused` (key `record`, detail "unverified"); otherwise `failed`, `W-ORCA-LIST-FAILED`. | FR-15 |
| 3 | Look up among rows with `isArchived == false`, keys in order: `marker` (`comment` contains `sc:issue <R>#<N>` not followed by a digit), `record` (path in `<D>/worktree.json` passing the record guard, matched by `realpath`), `basename` (`^issue-<N>(-\|$)` on the path's basename), `branch` (same pattern on the last `/` segment of `branch`). Dedupe by row `id`; the first key with a hit decides. One live hit: `reused`. Stale hits (path missing) only: `failed`, `W-WORKTREE-STALE`. Two or more live hits: `failed`, `W-WORKTREE-AMBIGUOUS`, all paths in `detail`. None of these creates. | 2.5 |
| 4 | No hit: `origin/<B>` must resolve (else `failed`, `W-ORIGIN-BASE-MISSING`, no create); a failed `git fetch origin` with the ref present continues with `W-ORIGIN-BASE-STALE` (FR-16). Create. On exit 0 or a timeout, list once more (FR-15 applies) and take the row-id set difference: exactly one new id whose basename matches `^issue-<N>(-\|$)` is `created` (`<wt>` = that row's `path`, FR-20); zero new ids is `failed`, `W-WORKTREE-CREATE-FAILED` "created but not listed"; two or more is `failed`, `W-WORKTREE-AMBIGUOUS`, no copy, no record. A nonzero exit is `failed`, `W-WORKTREE-CREATE-FAILED` with the first stderr line; never auto-retried. | 5 step 5 |
| 5 | Copy `<D>` to `<wt>/.dev/issues/<N>/` file by file (MR 2.4): skip when source and destination share a `realpath`; exclude `worktree.json`; a file tracked in the worktree is skipped and named; a missing file is copied; an identical file is skipped; a differing untracked file is renamed to `<name>.prev` (replacing an older `.prev`), then copied and named. Never one recursive directory copy. `analysis/` is included. | 2.4 |
| 6 | Post-condition (FR-17): `<wt>` exists, its git-common-dir equals `<main>`'s by `realpath`, and every `<D>` file is byte-identical at the destination or named in a warning; else `failed` with a named warning (`W-WORKTREE-COPY-FAILED` for a copy problem, `W-WORKTREE-STALE` for a wrong common dir). | FR-17 |
| 7 | Only on `created` or `reused`, write `<D>/worktree.json` `{"path": "<absolute>", "status": "created\|reused"}`. It keeps an existing `launch` entry. It is never copied. | FR-18 |

The record guard: the path exists and its git-common-dir equals `<main>`'s, compared by `realpath`.

### 8.4 `launch`

Arguments `--number <N> --source <D> --level worktree|full [--submit]`. Output `{status, warning, detail, terminal, launched_at, enforcement_hook, hand_command}` with `status` `launched | failed | already_launched`.

| Step | Rule |
|---|---|
| 1 | Read `<D>/worktree.json` through the record guard. Missing or failing: `failed`, `W-LAUNCH-FAILED` "no usable worktree record". |
| 2 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. |
| 3 | `enforcement_hook = enforcement_status()` (section 6). `missing` sets `W-ENFORCEMENT-ABSENT` ("levels are instructions in the prompt only until the hook of #394 ships"); it does not stop the launch (default D3). |
| 4 | Write `pending/<nonce>` (section 6). A write error: `failed`, `W-LAUNCH-FAILED`, no launch. |
| 5 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. No `--model` or `--effort` (AD FR-22). A nonzero exit, a timeout, or `ok != true`: remove the pending record, `failed`, `W-LAUNCH-FAILED` with the first stderr line, and `hand_command` (the same call without the marker, with the note "an agent started by hand is not governed by the hook; re-running the claim is preferred"). A timeout may have started an agent; `detail` says to check Orca before re-running. |
| 6 | Shim check (FR-28): take the terminal handle (the first string value under a key `handle` in the launch JSON, found by a recursive walk, because the `agent launch` result shape is UNVERIFIED), then `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart. Pass when `result.terminal.tail` text holds `[ccsession]` or `Session name (Enter or Ctrl+C` (the question text of `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, check 11). No handle, no readable screen or no match: keep the launch and set `W-LAUNCH-NOT-CCSESSION` ("this agent is NOT behind the ccsession shim, or could not be verified; close it"). The pending record stays. |
| 7 | Write `launch: {level, submit, at}` (UTC ISO time) into `<D>/worktree.json`, whatever the shim result, because an agent exists. Status `launched`. |

`worktree.json` is the only file the script writes besides the copy, the pending record and the rendered prompt. It never runs `git worktree add`, `orca worktree rm`, a commit, a push or a stage (FR-12).
````

### .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:285-312

````markdown
## 12. Files to create or change

All under `src/superclaude/` unless stated. Nothing under `.claude/` is edited or staged; `make sync-dev` produces it. No `plugins/superclaude/` mirror of the issue command or skill exists (checked 2026-11-07), so none is added.

**Create**

| Path | Content |
|---|---|
| `skills/sc-issue-protocol/scripts/orca_worktree.py` | Section 8: four subcommands, stdlib only, `enforcement_status()` |
| `skills/sc-issue-protocol/templates/launch-prompt.md` | Section 9: four marked blocks |
| `tests/skills/test_issue_orca_worktree.py` | Section 13, fake `orca` on `PATH` |
| `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` | Copied in whole from the main checkout (untracked there) so it is committed with the PR; this design cites it |

**Change**

| Path | Change |
|---|---|
| `commands/issue.md` | `version: "1.1.0"`, `argument-hint`, Usage, two Options rows, three STOP rules (section 4), Examples, Outputs, Boundaries (Will, Will Not), claim paragraph (no longer "stops"; creates the worktree and launches an agent) |
| `skills/sc-issue-protocol/SKILL.md` | description and claim paragraph; files table rows for `scripts/orca_worktree.py` and `templates/launch-prompt.md`; claim steps 1, 6 and 7 (Wave 0 check, Wave 5 additions, Waves 7 and 8); claim return contract (section 10); error table rows (sections 4 and 11); Will / Will Not. Stays under 500 lines. |
| `skills/sc-issue-protocol/refs/claim.md` | Wave 0 step 3, Wave 5 additions, Wave 6 hand-off, Waves 7 and 8, final output (section 7). No new ref file. |
| `skills/sc-issue-protocol/templates/next-steps.md` | `Plan boundary: after step <K>` line |
| `core/HOW-WE-WORK.md` | the `/sc:issue` row: a claim now also creates a worktree and launches an agent at the chosen level, and never merges; then byte-copy the file to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| `docs/designs/sc-issue-command.md` | B2 row rewritten (section 2), new rows B16 to B18, and short "Amended 2026-11-07" notes in sections 1, 4, 7, 14, 16, 20 pointing to this design. Section 15's list of files gains the new script and template. |
| `docs/user-guide/commands.md` | the `/sc:issue` section: two flags, the four levels, examples, the "never merges" statement |
| `tests/commands/test_issue_command.py` | Options table pin becomes seven flags with the new values and defaults; STOP rule pins; Will Not text |
| `tests/skills/test_issue_protocol.py` | files-table pins, Wave 7 and 8 order, forbidden-flag scan, `Plan boundary` pin, prompt block pins |

Path rule: every new reference inside the primitives to another primitive uses the installed path and the script is called as `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path (FR-14). Pre-commit check: `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit.
````

## Coverage slice

| Requirement | Spec line | Status | Matched task | Ratio | Quote |
|---|---|---|---|---|---|
| INF-003 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:45 | covered | Task 6 (best Task 6) | 0.778 | The agent is started with `orca agent launch --agent claude --surface terminal`, a Claude CLI session. |
| INF-009 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:120 | covered | Task 6 (best Task 6) | 0.8 | `$HOME/.claude/state/launch-level/pending/<nonce>`. Built from path parts in the script, directories `0700`, files `0600`. |
| INF-010 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:121 | covered | Task 6 (best Task 6) | 0.778 | `secrets.token_hex(16)`: 32 lowercase hex characters, new for every launch |
| INF-012 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:123 | covered | Task 6 (best Task 6) | 0.625 | written to a temporary name that does not match the nonce pattern, then `os.rename` to `<nonce>` |
| INF-013 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:124 | covered | Task 6 (best Task 6) | 0.857 | written before `orca agent launch`; removed if the launch fails |
| INF-014 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:125 | covered | Task 6 (best Task 6) | 1.0 | `--prompt` starts with `[sc-launch:v1:<nonce>] ` |
| INF-015 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:126 | covered | Task 6 (best Task 6) | 0.778 | no launch (`W-LAUNCH-FAILED`); the claim never starts an agent whose level it could not record |
| INF-016 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:132 | covered | Task 6 (best Task 6) | 0.875 | `enforcement_hook` (contract field) is `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`. |
| INF-027 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:192 | covered | Task 2 (best Task 2) | 1.0 | Unusable (FR-15): `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true` |
| INF-028 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:193 | covered | Task 2 (best Task 2) | 0.857 | Dedupe by row `id`; the first key with a hit decides. |
| INF-029 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:194 | covered | Task 2 (best Task 2) | 1.0 | a failed `git fetch origin` with the ref present continues with `W-ORIGIN-BASE-STALE` (FR-16). |
| INF-030 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:195 | covered | Task 2 (best Task 2) | 1.0 | Never one recursive directory copy. |
| INF-031 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:195 | covered | Task 2 (best Task 2) | 0.9 | a differing untracked file is renamed to `<name>.prev` (replacing an older `.prev`), then copied and named. |
| INF-032 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:197 | covered | Task 2 (best Task 2) | 0.833 | It keeps an existing `launch` entry. It is never copied. |
| INF-033 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:207 | covered | Task 6 (best Task 6) | 1.0 | Read `<D>/worktree.json` through the record guard. |
| INF-034 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:208 | covered | Task 6 (best Task 6) | 1.0 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. |
| INF-035 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:211 | covered | Task 2 (best Task 2) | 0.6 | No `--model` or `--effort` (AD FR-22). |
| INF-036 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:212 | covered | Task 6 (best Task 6) | 1.0 | then `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart. |
| INF-037 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:213 | covered | Task 6 (best Task 6) | 0.938 | Write `launch: {level, submit, at}` (UTC ISO time) into `<D>/worktree.json`, whatever the shim result, because an agent exists. |
| INF-038 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:215 | covered | Task 2 (best Task 2) | 1.0 | It never runs `git worktree add`, `orca worktree rm`, a commit, a push or a stage (FR-12). |
| INF-041 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:283 | covered | Task 2 (best Task 2) | 0.75 | A launch is never attempted when the worktree `status` is `failed` (FR-21). |
| INF-043 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:296 | covered | Task 2 (best Task 2) | 0.667 | Copied in whole from the main checkout (untracked there) so it is committed with the PR; this design cites it |
| INF-045 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:306 | covered | Task 9 (best Task 9) | 1.0 | then byte-copy the file to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` |
| INF-046 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:307 | covered | Task 8 (best Task 8) | 0.958 | B2 row rewritten (section 2), new rows B16 to B18, and short "Amended 2026-11-07" notes in sections 1, 4, 7, 14, 16, 20 pointing to this design. |
| INF-047 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:312 | covered | Task 2 (best Task 2) | 0.636 | every new reference inside the primitives to another primitive uses the installed path and the script is called as `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path (FR-14). |
| INF-049 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:335 | covered | Task 6 (best Task 6) | 1.0 | the pending record is a regular file of mode `0600` holding exactly `worktree`, `full` or `full-submit` |
| INF-051 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:371 | covered | Task 6 (best Task 6) | 0.889 | A missing hook script is a warning (`W-ENFORCEMENT-ABSENT`), not a refusal, for every level |
| INF-053 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:382 | covered | Task 9 (best Task 9) | 0.846 | `docs/user-guide/commands.md` and the `/sc:issue` row of `HOW-WE-WORK.md` are updated in the same change |
| INF-054 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:419 | covered | Task 9 (best Task 9) | 0.8 | `make verify-sync` passes, the tests of section 13 pass, `make lint` and the pinned ruff format check pass, the `src/superclaude` path grep shows no new hit. |
| INF-055 | .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/source.md:31 | covered | Task 2 (best Task 2) | 0.6 | Running any live claim, worktree create or agent launch against a real issue. |
