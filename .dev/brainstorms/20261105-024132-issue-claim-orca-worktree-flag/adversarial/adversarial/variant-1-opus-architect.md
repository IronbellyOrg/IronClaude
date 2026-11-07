# Variant 1 (architect): `/sc:issue --claim --worktree`

## 1. Summary (at most 5 sentences)

`/sc:issue --claim <N> --worktree` runs today's claim unchanged (Waves 0-6), then a new Wave 7 that creates one Orca-managed worktree for the issue, or reuses an earlier one. Wave 7 lives in one ref (`refs/worktree.md`) and one standard-library script (`scripts/orca_worktree.py`), so every Orca argument, the duplicate lookup and the copy sit behind a single unit-tested seam. The worktree gets no agent, no Orca link flags, `--no-parent` and base `origin/<B>`, and receives a copy of `.dev/issues/<N>/`. Every Orca problem is a warning; the claim never fails or rolls back because of Wave 7. Without `--worktree` nothing changes, including the return contract.

## 2. Decisions on the open questions (one H3 per open question, in the seed brief's order: decision, why, rejected alternative)

### 2.1 Worktree only, or also launch an agent?

- **Decision:** worktree only. No `--agent`, `--prompt`, `--model`, `--effort` or `--surface`.
- **Why:** B2 (`docs/designs/sc-issue-command.md:27`) is ruled. A worktree is a place, not a next-step command, so it stays inside B2. Repo precedent (refactor decision D3) creates worktrees without `--agent`; whether a `/`-prefixed `--prompt` arrives as a slash command is UNVERIFIED.
- **Rejected:** `--launch` (start Claude on the first `next-steps.md` command): breaks B2 and needs a tier-to-model mapping. A later agent option would go only in the script's argument builder, after B2 is amended.

### 2.2 Flag name and shape

- **Decision:** one boolean flag, `--worktree`, claim only.
- **Why:** it names the outcome, not the vendor, so the provider can change without renaming it. With no value, the lookup key is always derived, which keeps re-claims idempotent.
- **Rejected:** `--orca` (names a tool); `--worktree [name]` (ambiguous to parse; a user-chosen name defeats the lookup); `--launch` (2.1).

### 2.3 Branch and worktree naming, base ref, lineage

- **Decision:** `--name issue-<N>-<slug>`; `<slug>` is the title in lower case, runs outside `[a-z0-9]` replaced by `-`, trimmed, at most 40 characters (create mode's limit); empty slug gives `issue-<N>`. No `--branch`, so Orca applies the configured prefix (observed: worktree `bare-python-hook-357` is on `ironbelly/bare-python-hook-357`). `--base-branch origin/<B>` (`<B>` from Wave 0 step 3, fetched in Wave 1). `--no-parent`. `--repo path:<main>` (section 4).
- **Why:** issue work is independent of the worktree the claim ran in; inferred lineage would make it a child of, say, a feature worktree. Explicit `--repo` removes inference.
- **Rejected:** `--branch issue-<N>-<slug>` (drops the team prefix); omitting `--base-branch` (Orca's repo base can differ from `<B>`).

### 2.4 How the worktree gets `.dev/issues/<N>/`

- **Decision:** copy `<D>` recursively to `<worktree>/.dev/issues/<N>/`; a re-claim overwrites same-named files and leaves others alone.
- **Why:** `next-steps.md`'s repo-relative `@.dev/issues/<N>/issue-summary.md` then resolves in the worktree with no template change.
- **Rejected:** symlink (addable to git; dangles if the main checkout is cleaned); absolute paths (needs a second `next-steps.md` variant).

### 2.5 Duplicate detection on re-claim

- **Decision:** list the repo's worktrees (section 4). A row matches when its `comment` equals `sc:issue <R>#<N>`, else when its `path` basename matches `^issue-<N>(-|$)`. A match is reused and the copy refreshed. Every create passes `--comment "sc:issue <R>#<N>"`. If listing fails, nothing is created.
- **Why:** `--comment` is plain Orca metadata, not a link flag, and survives title edits that change the slug. The path fallback catches hand-made worktrees. Without a list result, no duplicate can be ruled out.
- **Rejected:** branch-name match (relies on the unverified prefix rule); Orca's `linkedIssue` (needs `--issue`, forbidden).

### 2.6 Model, effort and tier line for a launched agent

- **Decision:** none, since no agent starts. The user runs `next-steps.md`'s `/model` tier line in a session opened in the worktree.
- **Rejected:** `--model claude-gw-tier2|tier1a`; Orca takes a "provider model id", and picker-ID support is UNVERIFIED.

### 2.7 Explicit version marker

- **Decision:** `version: "1.1.0"` in the `commands/issue.md` frontmatter; the change is recorded as B16 in the design doc. No version in `SKILL.md`.
- **Why:** eight commands already carry `version:` (for example `brainstorm.md` 2.0.0); a minor bump signals an additive change. Skills have no such convention.
- **Rejected:** a second command (`/sc:issue2`), which doubles maintenance.

## 3. Functional requirements (numbered FR-1.., each testable, MUST/SHOULD)

- **FR-1** The Options table MUST gain one row: `--worktree`, mode `claim`, default off, no value.
- **FR-2** `--worktree` with `--create` MUST STOP `E-CLAIM-ONLY-FLAG` before Activation, making no external call.
- **FR-3** Without `--worktree`, no `orca` command runs, `refs/worktree.md` does not load, and output and return contract MUST equal today's.
- **FR-4** Wave 7 MUST run only after Wave 6 step 3 succeeded; any earlier STOP means no Orca call.
- **FR-5** Every Orca call MUST be made by `scripts/orca_worktree.py`; the skill never composes an `orca` command line itself.
- **FR-6** The create call MUST equal section 4's list exactly; no link flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`) and no `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--activate`, `--run-hooks`, `--setup`.
- **FR-7** A re-claim that finds a match MUST NOT call `orca worktree create`.
- **FR-8** After create or reuse, `<worktree>/.dev/issues/<N>/next-steps.md` and `issue-summary.md` MUST exist.
- **FR-9** The script MUST exit 0 for every runtime outcome, printing one JSON object; exit 2 only for bad arguments (the `clickup_claim.py` pattern).
- **FR-10** Any Orca or copy problem MUST yield a `W-` warning with claim `status: success`.
- **FR-11** Worktree return-contract fields MUST print only with `--worktree`.
- **FR-12** MUST NOT stage, commit, push, run `git worktree add`, use `EnterWorktree`, or run `orca worktree rm`.
- **FR-13** The final output SHOULD print the worktree path and "open it and run `.dev/issues/<N>/next-steps.md` there".
- **FR-14** Installed primitives MUST call `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path.

## 4. Flag contract and error codes (flag name, valid combinations, STOP/WARN codes, the exact `orca` argument list in a code block, return-contract additions)

Valid: `--claim <N> --worktree`. STOP: `--create ... --worktree` -> `E-CLAIM-ONLY-FLAG` ("--worktree applies to --claim only"); `--worktree` alone -> usage block; a value after `--worktree` -> usage block. `--claim --worktree --depth` hits the existing `E-CREATE-ONLY-FLAG` first.

Warnings (claim stays `success`; see section 6): `W-ORCA-MISSING`, `W-ORCA-LIST-FAILED`, `W-WORKTREE-CREATE-FAILED` (first stderr line; never auto-retried), `W-WORKTREE-MULTIPLE`, `W-WORKTREE-STALE`, `W-WORKTREE-COPY-FAILED`.

`<main>` is the parent of `git rev-parse --path-format=absolute --git-common-dir`, so a claim run in a linked worktree still names the main checkout.

```text
orca worktree list --repo path:<main> --limit 500 --json
orca worktree create --repo path:<main> --name issue-<N>-<slug> --base-branch origin/<B> --no-parent --comment "sc:issue <R>#<N>" --json
```

Return-contract additions, printed only with `--worktree`:

```yaml
worktree_status: created | reused | skipped | failed
worktree_path: <absolute path or null>
worktree_branch: <branch or null>
worktree_warning: <W- code or null>
```

## 5. Procedure (which Wave of claim.md the step goes in, ordered steps, re-claim idempotency, fail-open behavior)

`refs/claim.md` Wave 6 step 4 becomes: without `--worktree`, print the `next-steps.md` path and STOP (today's text); with it, run Wave 7, then print both paths and STOP. Wave 7 (new, in `refs/worktree.md`):

1. Load `refs/worktree.md`.
2. Run `uv run --no-project python "<skill base>/scripts/orca_worktree.py" --repo <R> --number <N> --title "<title from scout.md>" --base origin/<B> --source <D>` and write stdout to `<D>/worktree.json`.
3. The script checks `orca` on PATH, resolves `<main>`, lists, reuses a match or creates, takes `path` and `branch` from the create JSON (else re-lists by marker), copies `<D>` to `<path>/.dev/issues/<N>/`, and prints `{status, path, branch, name, warning, detail}`. Each `orca` call times out at 120 seconds.
4. Read `worktree.json`; print the path, the FR-13 line and the contract fields.

Idempotency: the marker makes a second claim `reused`, refreshing only the copy; a timed-out create that finished is found next time. Fail-open: no outcome changes `status` or undoes Waves 3-6.

## 6. Edge cases and failure modes (table)

| Case | Behavior |
|---|---|
| `orca` not installed | `skipped`, `W-ORCA-MISSING` |
| List fails or times out | `skipped`, `W-ORCA-LIST-FAILED`, no create |
| Create fails or times out | `failed`, `W-WORKTREE-CREATE-FAILED`; re-run reuses if it finished |
| One match | `reused`, copy refreshed |
| Several matches | reuse first marker match, else first path match; `W-WORKTREE-MULTIPLE` lists all |
| Matched path gone from disk | `failed`, `W-WORKTREE-STALE`; no create |
| Empty slug | name `issue-<N>` |
| Claim run in a linked worktree | `<main>` is still the main checkout |
| STOP before Wave 6 step 3, or `E-POST-FAILED` | no Orca call; a re-run creates it |
| Worktree copy of `next-steps.md` edited by the user | overwritten on re-claim |
| Copy fails | `W-WORKTREE-COPY-FAILED` naming both paths |

## 7. Test plan and acceptance criteria (observable)

Automated (`uv run pytest`):

- `tests/skills/test_issue_orca_worktree.py` (new): a fake `orca` on a temp PATH records argv and returns canned JSON. Pins both argv lists; no FR-6 flag; reuse (marker, path) and list failure make no create call; missing `orca` and create failure exit 0 with the right status; copy; slug rules; bad arguments exit 2.
- `tests/commands/test_issue_command.py`: six flags; `--worktree` mode `claim`; `E-CLAIM-ONLY-FLAG` in the STOP rules; `version` is `1.1.0`.
- `tests/skills/test_issue_protocol.py`: `refs/worktree.md` and the script are in the files table and exist; Will Not still names "Run any next-step command"; no FR-6 flag text in `refs/worktree.md`.

Observed (one manual run on a test issue):

- **AC-1** `orca worktree list` shows one new row with comment `sc:issue <R>#<N>` under Orca's default location (observed today: `/home/coder/workspaces/worktrees/IronClaude/`); there, `git merge-base HEAD origin/<B>` equals `git rev-parse origin/<B>`; the output prints its path.
- **AC-2** A Claude session opened there reads `@.dev/issues/<N>/next-steps.md`.
- **AC-3** A second run adds no row and reports `reused`.
- **AC-4** Without the flag: no worktree lines, no `orca` call.
- **AC-5** With `orca` off PATH, the claim succeeds with `W-ORCA-MISSING`.
- **AC-6** `--create "x" --worktree` STOPs `E-CLAIM-ONLY-FLAG` with no `gh` call.

## 8. Files to change (source paths, mirrors, docs, tests) and versioning

- `src/superclaude/commands/issue.md`: `version: "1.1.0"`, argument-hint, Usage, Options row, STOP rule, example, Boundaries (Will Not: launch an agent, pass Orca link flags).
- `src/superclaude/skills/sc-issue-protocol/SKILL.md`: files table, claim step 7, conditional contract block, error rows, Will / Will Not.
- `.../refs/claim.md` (Wave 6 step 4); new `.../refs/worktree.md` and `.../scripts/orca_worktree.py`. No template changes.
- Docs: `docs/designs/sc-issue-command.md` (B16; sections 4, 7, 14, 16), `docs/user-guide/commands.md`. If the `/sc:issue` row of `src/superclaude/core/HOW-WE-WORK.md` changes, byte-copy it to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`.
- Plugin mirror: none (`plugins/superclaude/` has no issue command or skill).
- Tests: section 7. Then `make sync-dev`, `make verify-sync`; never stage `.claude/`. Over 5 edits, so `/sc:workflow` then `/sc:implement`.

## 9. Risks and open items

1. UNVERIFIED: field names of the `orca worktree create --json` result; check on AC-1 (fallback: marker re-list).
2. UNVERIFIED: `--repo path:<main>` on create (it worked for `list` today); check on AC-1.
3. UNVERIFIED: branch = configured prefix plus `--name` (inferred from list rows); AC-1 records it.
4. UNVERIFIED: whether the repo's setup policy fills the project `.claude/` copy; installed `~/.claude/` primitives work regardless. Check with `ls <path>/.claude/commands/sc/`.
5. UNVERIFIED: Orca's behavior on a taken `--name`; surfaces as `W-WORKTREE-CREATE-FAILED`.
6. A later agent launch needs B2 amended first; only the script's argument builder changes.
