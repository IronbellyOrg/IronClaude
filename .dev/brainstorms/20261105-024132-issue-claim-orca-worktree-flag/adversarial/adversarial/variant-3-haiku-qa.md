# Variant 3 (QA): `/sc:issue --claim` Orca worktree flag — requirements specification

## 1. Summary

`/sc:issue --claim` ends at Wave 6 by printing the `next-steps.md` path, leaving the user to create a worktree by hand. This spec adds one opt-in flag, `--worktree`: after the comments are posted it creates an Orca-managed worktree for the issue, copies `.dev/issues/<N>/` into it, prints its path, and stops. No agent is launched, so ruled decision B2 ("never run a next-step command") stays intact. Without the flag every output must be byte-identical to today; worktree failure never fails the claim. Verified against the live command, skill, refs, design doc and Orca `--help` (2026-11-05).

## 2. Decisions on the open questions

### Q1. Worktree only, or also launch an agent (`--agent --prompt`)?

Decision: worktree only; never pass `--agent`, `--prompt`, `--model`, `--effort`.
Why: B2 (`docs/designs/sc-issue-command.md:27`) is ruled and an agent running the chain breaks it; repo precedent (decision D3) creates worktrees without `--agent`; it keeps three UNVERIFIED questions off the critical path (slash command via `--prompt`, agent-tab behavior, worker-contract refusal).
Rejected: a `--launch` agent flag; untestable until those answers exist, and a partial version violates B2.

### Q2. Flag name and shape

Decision: `--worktree`, boolean, claim-only, no value.
Why: one word naming the effect; mirrors the `E-CREATE-ONLY-FLAG` precedent with a new `E-CLAIM-ONLY-FLAG`. A value form adds name-validation and suffix-collision handling for no benefit.
Rejected: `--worktree [name]`, `--orca` (names the tool), `--launch` (implies an agent).

### Q3. Branch/worktree naming, base ref, parent lineage

Decision: name `issue-<N>`, branch `issue-<N>` (via `--branch`), base `origin/<B>` (`<B>` = default branch from Wave 0 step 3), `--no-parent`.
Why: `--branch` gives an exact greppable name instead of Orca's prefixed default, and dedup (Q5) keys on it; `--no-parent` makes lineage independent of where the claim runs.
Rejected: `issue-<N>-<slug>` (slugify rules for nothing; `<N>` is unique); inferred parent (caller-dependent).

### Q4. How the worktree gets `.dev/issues/<N>/`

Decision: copy `<D>` into `<worktree-path>/.dev/issues/<N>/` with `cp -r`, after creation, before printing.
Why: `next-steps.md` uses the relative input `@.dev/issues/<N>/issue-summary.md`, so a copy keeps every command runnable verbatim from the worktree root. An absolute-path rewrite changes content tests already pin; a symlink breaks tools that resolve it.
Rejected: absolute path in the prompt only; symlink.

### Q5. Duplicate detection on re-claim

Decision: after a create, write `<D>/worktree.json` (branch, path). On re-claim, read it first; if the path's `git -C <path> rev-parse --abbrev-ref HEAD` prints `issue-<N>`, reuse and re-copy. Missing record: fall back to `orca worktree list --json` matching branch `issue-<N>`.
Why: the record is one exact read; the list fallback covers a claim from another checkout. Orca's suffix on a taken name is silent and must never dedup.
Rejected: rely on Orca's suffix (silent near-duplicates); always create fresh.

### Q6. Model/effort/tier for a launched agent

Decision: not applicable; no agent is launched (Q1). Rejected: pin a tier (moot).

### Q7. Explicit version marker

Decision: none; record the change as a dated addendum in `docs/designs/sc-issue-command.md`.
Why: no primitive in `src/superclaude/` carries a version marker; adding one creates a sync surface with no reader.
Rejected: a `version:` frontmatter field (nothing consumes it; drift risk).

## 3. Functional requirements

- FR-1: `/sc:issue --claim <N>` without `--worktree` MUST produce byte-identical output, files, GitHub writes and return contract to today.
- FR-2: `--worktree` MUST be claim-only; with `--create` the command MUST STOP `E-CLAIM-ONLY-FLAG` before Activation.
- FR-3: the worktree step MUST run only after Wave 6 steps 1-2 (comments posted) succeed, so an `E-POST-FAILED` STOP never leaves a worktree behind.
- FR-4: the invocation MUST be exactly the section 4 argument list, containing none of `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--issue`, `--pr`, `--reference`, `--reference-site`, `--linear-issue`, `--gitlab-issue`, `--gitlab-mr`.
- FR-5: after a create the skill MUST copy `<D>` into the worktree and MUST NOT stage or commit anything (D24 unchanged).
- FR-6: re-claiming the same issue with the flag MUST NOT create a second worktree for `<N>`.
- FR-7: any worktree failure (Orca missing, create failed, copy failed, path unparsable) MUST NOT change `status:` from `success`, MUST NOT roll back assignment or comments, and MUST emit `W-WORKTREE-FAILED` plus one remedy line.
- FR-8: the final print MUST add the worktree path and the reused/created outcome; without the flag those lines MUST NOT appear.
- FR-9: the return contract MUST add `worktree_path: <absolute path or null>` (null in create mode and on failure).
- FR-10: the skill MUST NOT run, prompt or schedule any next-step command in the worktree (B2; no agent launch).
- FR-11: primitive edits happen under `src/superclaude/` then `make sync-dev`; no installed primitive may contain a `src/superclaude/` path.

## 4. Flag contract and error codes

Flag: `--worktree` (boolean, claim-only). Valid: `--claim <N> --worktree`. With `--create`: STOP `E-CLAIM-ONLY-FLAG` ("--worktree applies to --claim only"). With `--depth|--mode|--type`: the existing `E-CREATE-ONLY-FLAG` still fires.

New warn code `W-WORKTREE-FAILED` (never a STOP). New record file `<D>/worktree.json`.

The exact create argument list (FR-4):

```bash
orca worktree create \
  --name issue-<N> \
  --branch issue-<N> \
  --base-branch origin/<B> \
  --no-parent \
  --setup run \
  --json
```

Every flag verified in `orca worktree create --help` (2026-11-05). `--repo` is omitted: Orca infers the repo from the current managed worktree (`orca worktree current --json` confirmed this checkout is managed). Duplicates: `orca worktree list --json`, match on branch `issue-<N>`.

Return contract addition (claim mode): `worktree_path: <absolute path, or null when not requested or failed>`. On failure also `W-WORKTREE-FAILED: <reason>` and a remedy line repeating the create command.

## 5. Procedure

Placement: a new **Wave 7** in `refs/claim.md`, after Wave 6 step 4; Wave 6 stays byte-identical with or without the flag. SKILL.md claim step 7 gains one Wave 7 pointer; the command file gains the Options row, STOP rule, Usage and one Example.

Steps (orchestrator, only with `--worktree`):

1. Read `<D>/worktree.json`. If it records a path whose `git -C <path> rev-parse --abbrev-ref HEAD` prints `issue-<N>`, jump to step 5 (reuse).
2. Else run `orca worktree list --json`; a row with branch `issue-<N>` is recorded in `<D>/worktree.json`; jump to step 5.
3. Run the create command. Non-zero exit or no path in the JSON: emit `W-WORKTREE-FAILED`, print the remedy, go to step 6.
4. Parse the path; write `<D>/worktree.json` as `{"branch": "issue-<N>", "path": "<abs>"}`. Orca's JSON field names are UNVERIFIED until an observed run; the parser must accept a nested `result` object.
5. Copy: `mkdir -p <worktree-path>/.dev/issues` then `cp -r <D> <worktree-path>/.dev/issues/<N>/`. Copy failure: `W-WORKTREE-FAILED` naming the error; the worktree stays.
6. Print, in order: the `next-steps.md` path (unchanged), `Worktree: <path>`, `Worktree: reused` or `created`, then the return contract.

Re-claim idempotency: steps 1-2 give at most one worktree per issue. If both lookups miss but the branch exists in git, step 3 gets Orca's numeric suffix; the run reports `created (renamed)` and records the returned branch. A deleted worktree fails step 1 and is re-created.

Fail-open: every Wave 7 failure leaves `status: success` and all Wave 6 outputs intact; only `worktree_path` and the extra lines differ.

## 6. Edge cases and failure modes

| # | Case | Expected behavior | Test |
|---|---|---|---|
| E1 | `--worktree` with `--create` | STOP `E-CLAIM-ONLY-FLAG` before Activation | T1 |
| E2 | `orca` not on PATH | `W-WORKTREE-FAILED`, `worktree_path: null`, success | T5 |
| E3 | Orca daemon down | As E2; stderr tail quoted | T5 |
| E4 | Create succeeds, copy fails | Warn names the error; worktree printed | T5 |
| E5 | Re-claim, record and worktree exist | No create call; `<D>` re-copied; `reused` | T3 |
| E6 | Record deleted, list finds branch | Reuse via fallback; record rewritten | T3 |
| E7 | Both lookups miss, branch taken | Suffix accepted; `created (renamed)` | T3 |
| E8 | Worktree deleted between claims | Fresh create; record replaced | T3 |
| E9 | Claim run from another worktree | `--no-parent` keeps lineage flat | T2 |
| E10 | `--worktree` with `--depth`/`--mode`/`--type` | Existing `E-CREATE-ONLY-FLAG` STOP | T1 |
| E11 | Orca infers a wrong repo | Create fails or names a foreign repo; warn | T5 |
| E12 | `E-POST-FAILED` in Wave 6, flag set | STOP before Wave 7; no worktree | T2 |
| E13 | Wave 0 branch resolution failed | Existing STOP; Wave 7 never reached | T2 |
| E14 | `.dev/issues/` absent in worktree | Created by the copy step | T4 |
| E15 | Unflagged claim after a flagged one | No Wave 7; `worktree_path: null` | T1 |

## 7. Test plan and acceptance criteria

T1-T3 are static pytest assertions; T4-T6 are observed runs recorded in the plan's verification evidence.

- T1 (`tests/commands/test_issue_command.py`, extend): Options table lists `--worktree` claim-only; STOP rules include `E-CLAIM-ONLY-FLAG`; Usage and an Example show it; no Orca link flag in the command file.
- T2 (`tests/skills/test_issue_protocol.py`, extend): `refs/claim.md` has a flag-gated Wave 7 after Wave 6's print, carrying the exact FR-4 argument list and the `W-WORKTREE-FAILED` fail-open rule; a regex over the skill matches none of `--agent\b`, `--prompt\b`, `--model\b`, `--effort\b`, `--issue\b`, `--pr\b`, `--reference`; the return contract includes `worktree_path`.
- T3 (same file): Wave 7 pins the reuse order (record, list match, create), the no-duplicate rule, and the `worktree.json` shape.
- T4 (observed): a flagged claim on a scratch issue; `orca worktree list` gains exactly one row `issue-<N>` on this fork; the printed path exists; the copied `next-steps.md` resolves its `@.dev/issues/<N>/issue-summary.md` input from the worktree root.
- T5 (observed): with `orca` hidden from PATH, a re-claim completes `status: success`, `worktree_path: null`, `W-WORKTREE-FAILED`.
- T6 (observed): repeat the flagged claim; list row count unchanged; output says reused.

Acceptance criteria: (1) unflagged claim output and `<D>` files byte-identical to a pre-change run; (2) flagged claim ends with a worktree at Orca's default location on branch `issue-<N>` from `origin/<B>`; (3) `--create --worktree` STOPs `E-CLAIM-ONLY-FLAG`; (4) Orca failure yields the warn and `status: success`; (5) the forbidden-flag regex passes; (6) `make verify-sync` passes and the `src/superclaude` grep gains no hit.
## 8. Files to change and versioning

Edits under `src/superclaude/` plus tests and docs, then `make sync-dev` and `make verify-sync`. Over 5 edits, so implementation goes through `/sc:workflow`. No version field (Q7); the design-doc addendum records the change.

| File | Change |
|---|---|
| `src/superclaude/commands/issue.md` | Options row, STOP rule, Usage, one Example, `worktree.json` in Outputs |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md` | Claim step 7 Wave 7 pointer; `worktree_path` in the return contract; `W-WORKTREE-FAILED` error row; Will/Will Not lines (Orca only; no agent launch; no link flags) |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md` | Wave 7 procedure (section 5) |
| `docs/designs/sc-issue-command.md` | Dated addendum: flag, Wave 7, the B2 reading |
| `docs/user-guide/commands.md` | `/sc:issue` row and section mention the flag |
| `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py` | T1-T3 |
| Mirrors | `make sync-dev` output only; HOW-WE-WORK row unchanged |

## 9. Risks and open items

- R1 (UNVERIFIED): `--json` field names of `worktree create` output; no worktree was created during this read-only investigation. Verify in T4; the parser accepts top-level and nested `result` shapes meanwhile.
- R2 (UNVERIFIED): whether `--setup run` runs `make sync-dev`; if not, the worktree's `.claude/` is missing and `/sc:` commands may not resolve there until the user runs it. T4 records that.
- R3 (UNVERIFIED): Orca's repo inference may resolve this repo to the upstream id (CLAUDE.md warning). FR-4 contains the blast radius; T4 checks the fork.
- R4: `worktree.json` is untracked; a claim from another machine misses it and pays the list fallback. Accepted.
- R5: the B2 reading (worktree creation is infrastructure, not a next-step command) should be confirmed in the debate; if overruled the flag dies.
- R6: Orca CLI drift makes the exact-argument pin fail loudly. Desired.
