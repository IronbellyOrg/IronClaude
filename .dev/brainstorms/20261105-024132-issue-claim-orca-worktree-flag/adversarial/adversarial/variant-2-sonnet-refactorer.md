# Variant 2 (refactorer): `/sc:issue --claim --worktree` requirements spec

## 1. Summary

Add one boolean, claim-only flag `--worktree` to `/sc:issue`. After a claim has fully succeeded, a new Wave 7 in `claim.md` looks up an Orca worktree for the issue, creates it with `orca worktree create` only if none exists, copies `.dev/issues/<N>/` into it, and prints its path. It creates a worktree and nothing else: no agent, no prompt, no Orca link flag, so rule B2 stays literally true. Every worktree problem is a WARN and the claim stays `success`. All new logic lives in one new wave of an existing file; no new file is added.

## 2. Decisions on the open questions

### 2.1 Worktree only, or also launch an agent

- Decision: worktree only. Pass no `--agent`, `--prompt`, `--model`, `--effort`, `--surface`.
- Why: B2 (`docs/designs/sc-issue-command.md:27`) stays true with no exception. Refactor decision D3 also creates worktrees without `--agent`.
- Rejected: `--agent claude --prompt "/sc:..."`: it runs a next-step command, needs a ruled design change, and rests on unverified behavior (slash-command delivery, worker contract).

### 2.2 Flag name and shape

- Decision: `--worktree`, boolean, no value, valid with `--claim` only.
- Why: it names the result, not the tool, and an optional value would make the parser guess whether the next token is a name or the claim argument.
- Rejected: `--orca` (names the tool), `--launch` (implies an agent), `--worktree <name>` (a second naming path).

### 2.3 Branch, worktree name, base ref, parent

- Decision: name `issue-<N>`, branch `issue-<N>`, base `origin/<B>` (`<B>` from Wave 0, refreshed by the Wave 1 `git fetch origin`), `--no-parent`.
- Why: no slug means no slug code and a lookup key that survives title edits. `--no-parent` stops Orca inferring lineage from the caller's directory.
- Rejected: `issue-<N>-<slug>` (extra code, unstable key); inferred parent.

### 2.4 How the worktree gets `.dev/issues/<N>/`

- Decision: copy the files of `<D>` into `<worktree>/.dev/issues/<N>/` after Wave 6, never overwriting a file that already exists there.
- Why: `next-steps.md` uses repo-relative `@.dev/issues/<N>/...` paths, so a copy works unedited. The files stay untracked (D24). Not overwriting protects the user's notes.
- Rejected: symlink (dangling and `git add` hazards); absolute-path rewrite (a second, divergent `next-steps.md`).

### 2.5 Duplicate detection on re-claim

- Decision: `orca worktree list --repo path:<T> --json`, then match a non-archived row whose `branch`, with `refs/heads/` removed, fits `(^|/)issue-<N>(-[0-9]+)?$` (a configured branch prefix and Orca's numeric suffix for a taken name are both tolerated; `issue-1` never matches `issue-12`). One match: reuse it, create nothing, still copy missing files. Several matches: WARN, create nothing.
- Why: the list fields `branch`, `path`, `isArchived` were read live; the same lookup finds the path after a create, so the unread create JSON is not relied on.
- Rejected: matching `displayName` (editable) or `--comment` text.

### 2.6 Model, effort and tier line

- Decision: none. No agent starts, so `next-steps.md` keeps its `/model` line.
- Rejected: `--model` or `--effort` (dead without `--agent`).

### 2.7 Version marker

- Decision: add `version: "1.1.0"` to the `issue.md` frontmatter only, as `brainstorm`, `reflect` and `pr-submit` do. Today's unversioned command counts as 1.0.0.
- Why: one line; `test_frontmatter_fields` checks keys one by one, so an extra key passes. `SKILL.md` has a test pinning its frontmatter.
- Rejected: versions in `SKILL.md` and every ref (drift).

## 3. Functional requirements

- FR-1 MUST: `/sc:issue --claim <N>` without `--worktree` produces the same files, comments, output and return contract as before (no new field printed).
- FR-2 MUST: `--worktree` with `--create`, or without `--claim`, STOPs `E-CLAIM-ONLY-FLAG` before Activation and before any write.
- FR-3 MUST: `--worktree` takes no value.
- FR-4 MUST: Wave 7 runs only after Wave 6 posted both comments; a STOP in Waves 0-6 means it never runs.
- FR-5 MUST: the only mutating Orca call is the one in section 4, and it contains no Orca link flag, no `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, no `--activate`.
- FR-6 MUST: before creating, run `orca worktree list` and create nothing when a matching worktree exists (section 2.5).
- FR-7 MUST: copy each file of `<D>` (and `<D>/analysis/`) into `<worktree>/.dev/issues/<N>/`, skipping files that already exist there.
- FR-8 MUST NOT: stage, commit or push anything, in either checkout.
- FR-9 MUST: any failure of FR-5 to FR-7 prints one `W-WORKTREE-*` line, leaves `status: success`, and Wave 7 ends.
- FR-10 MUST: print the worktree path before the return contract; the contract gains `worktree_path` and `worktree_status` only when `--worktree` was passed.
- FR-11 MUST NOT: edit `next-steps.md`, a comment or the issue in Wave 7.

## 4. Flag contract and error codes

Valid: `--claim <arg> --worktree`. Invalid: `--create ... --worktree` (`E-CLAIM-ONLY-FLAG`). Not an error: `--claim <arg> --worktree` on a re-claim.

| Code | Kind | Meaning |
|---|---|---|
| `E-CLAIM-ONLY-FLAG` | STOP | `--worktree` given without `--claim` ("--worktree applies to --claim only") |
| `W-WORKTREE-NO-ORCA` | WARN | `orca` not found, or `orca worktree list` exits nonzero |
| `W-WORKTREE-AMBIGUOUS` | WARN | several rows match; none created |
| `W-WORKTREE-CREATE-FAILED` | WARN | create exited nonzero or the follow-up list shows no row |
| `W-WORKTREE-COPY-FAILED` | WARN | worktree exists, a copy failed; path still printed |

Exact create call (`<T>` = `git rev-parse --show-toplevel`, `<B>` = default branch from Wave 0):

```text
orca worktree create --name issue-<N> --repo path:<T> --base-branch origin/<B> --branch issue-<N> --no-parent --json
```

Duplicate lookup: `orca worktree list --repo path:<T> --json`.

Return-contract additions (only with the flag):

```yaml
worktree_path: <absolute path or null>
worktree_status: created | reused | skipped | failed
```

## 5. Procedure

New **Wave 7: worktree (orchestrator, only with `--worktree`)**, appended after Wave 6 in `refs/claim.md`. Waves 0-6 change in one place only: Wave 6 step 4 becomes "Print the `next-steps.md` path; if `--worktree` was passed, run Wave 7; then STOP". No worker is spawned.

1. Resolve `<T>`. `command -v orca` missing: `W-WORKTREE-NO-ORCA`, status `skipped`, go to step 7.
2. Run the list call. Nonzero exit: `W-WORKTREE-NO-ORCA`. Parse the rows with the match rule of 2.5.
3. Exactly one match: path = its `path`, status `reused`, go to step 5. Several: `W-WORKTREE-AMBIGUOUS`, status `skipped`, go to step 7.
4. No match: run the create call of section 4. Nonzero exit: `W-WORKTREE-CREATE-FAILED`, status `failed`, go to step 7. Otherwise run the list call again and take the path of the matching row (no row: same WARN). Status `created`.
5. Copy missing files from `<D>` into `<path>/.dev/issues/<N>/` (create the directory). A failure: `W-WORKTREE-COPY-FAILED`, keep the path.
6. Print `Worktree: <path>` and, on `created`, one line saying the files are untracked there.
7. Print the contract with the two new fields.

Re-claim idempotency: the second run finds the row in step 3, creates nothing, and copies only missing files.

Fail-open: nothing in Wave 7 can change `status` or undo the assignment. A failed create is retried by re-running the same command.

## 6. Edge cases and failure modes

| Case | Behavior |
|---|---|
| `orca` missing or app not running | `W-WORKTREE-NO-ORCA`; claim stays `success` |
| Branch `issue-<N>` exists in git but has no Orca row | Orca adds a numeric suffix; the new row matches the rule; no error |
| Archived worktree for the issue | Ignored; a new one is created |
| `<T>` is a linked worktree | `--repo path:<T>` resolution UNVERIFIED; failure gives `W-WORKTREE-CREATE-FAILED` |
| Wave 2 STOP or Wave 6 `E-POST-FAILED` | Wave 7 never runs; a re-run with the flag continues normally |
| Create `--json` shape unknown | Path is read from the follow-up list, not from create output |
| Two parallel claims of one issue | May make two rows (section 9) |

## 7. Test plan and acceptance criteria

Static tests (pytest, no Orca, no network), following the existing issue tests:

1. `issue.md`: `--worktree` row, `E-CLAIM-ONLY-FLAG` STOP rule, `argument-hint`, `version` key, and the Will Not next-step line still present.
2. `claim.md`: Wave 7 present; the create argument list equals section 4 exactly.
3. Flag guard: no line holding `orca worktree create` in `claim.md`, `SKILL.md` or `issue.md` contains `--issue`, `--pr`, `--reference`, `--linear-issue`, `--gitlab-`, `--agent` or `--prompt`.
4. `SKILL.md` return contract lists `worktree_path` and `worktree_status`, marked "only with --worktree".
5. Existing tests (Waves 0-6 pins, the named-path inventory, the five-refs list) stay green unedited: no new ref file.

Observed run (manual, once, recorded as evidence):

- `--claim <test issue> --worktree`: `orca worktree list` shows `issue-<N>`; the printed path exists, is a git worktree on a new branch, and holds `.dev/issues/<N>/next-steps.md`.
- Run again: row count unchanged, `worktree_status: reused`.
- `--claim` alone: no Orca call, output identical to the master baseline.
- `PATH` without `orca`: `W-WORKTREE-NO-ORCA`, `status: success`.

Acceptance: items 1-5 pass in CI; the four observations are in the plan's evidence file. The user removes the test worktree.

## 8. Files to change

Edit under `src/superclaude/`, then `make sync-dev`; stage only the `src/` side.

| File | Change |
|---|---|
| `src/superclaude/commands/issue.md` | flag row, STOP rule, usage and `argument-hint`, example, Outputs line, Will list, `version` |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Wave 6 step 4 hand-off, new Wave 7 |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | claim step 8, return contract fields, error table rows, Will line |
| `docs/user-guide/commands.md` | usage and flag, section `/sc:issue` |
| `docs/designs/sc-issue-command.md` | new decision row noting B2 is unchanged and the flag is worktree-only |
| `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py` | the checks of section 7 |

No new file. `HOW-WE-WORK.md` and its plugin mirror stay unchanged (the routing row does not describe flags; confirm with `tests/core/test_how_we_work_routing_table.py`). `plugins/superclaude/` holds no `/sc:issue` copy (grep found only the HOW-WE-WORK mirror). More than five edits: go through `/sc:workflow` then `/sc:implement`.

Versioning: command frontmatter `version: "1.1.0"` only (2.7). No `pyproject.toml` bump for this change.

## 9. Risks and open items

UNVERIFIED items and how to verify them (during the manual run):

- Default worktree location today (last seen `/home/coder/workspaces/worktrees/IronClaude/<name>`). Verify: `path` field of the new row.
- Whether `--branch issue-<N>` gets a configured prefix. Verify: `branch` field of the new row. The match rule tolerates a prefix.
- Whether `--repo path:<T>` resolves from a linked worktree, and whether omitting `--setup` leaves `.claude/` populated. Verify: run from the main and from a linked checkout; `ls .claude/commands/sc` in the result.
- Whether `/sc:issue` may run in an Orca-launched tab (`~/.claude/WORKER-CONTRACT.md` not read). Verify: grep it for `sc:issue`.
- An existing IronClaude row in `orca worktree list` carries `projectId: github:superclaude-org/superclaude_framework`. No link flag is passed, but whether create contacts that project is UNVERIFIED. Verify: watch network or Orca logs on the manual run.

Risks:

- Parallel claims of one issue can create two rows (low; accepted).
- Skipping existing files means a re-claim leaves stale copies in the worktree. Accepted.
- If reviewers object to `version`, drop 2.7 with no other change.

Left out on purpose: agent launch, a `--worktree <name>` form, dry-run, auto-removal, a `--setup` choice.
