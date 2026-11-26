review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | P2 | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R3, R2 |
| L3 | open | no | single | MAJOR | FO-18 | R1 |
| L4 | open | no | single | MINOR | ARG-1 | R1 |
| L5 | open | yes | overlap | MAJOR | - | R1, R3, R2 |
| L6 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L5

#### L5.t2b-1 (F6)

- claim: The word only contradicts the docs and test edits required by Tasks 8 and 9.
- anchor: "- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`."

#### L5.t3-1 (F1)

- claim: An implementer who follows the stated text as written edits only `src/superclaude/` and does not update the plugin mirror, and that is wrong because Task 9 requires the mirror to match the changed source file byte-for-byte.
- anchor: "Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`."
- anchor2: "copy that file byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`"

#### L5.t3-1 (F2)

- claim: An implementer who follows the stated text as written creates a worktree without `--agent`, and that is wrong because the repository’s Orca rule says a hook blocks `orca worktree create` without `--agent`.
- anchor: "--comment \"sc:issue <R>#<N>\" --json`; no other `orca` or `git worktree` call"
- anchor2: "`--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call."

#### L5.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a change without the brainstorm folder, and the folder-existence acceptance criterion cannot pass because the folder is absent and no task copies it.
- anchor: "already copied into this repository and part of the change."

## Other findings

- L1 (MAJOR, open, single): Plan never states the MR --worktree flag must not exist; only --pipeline is defined.
- L2 (MAJOR, open, overlap): Plan never forbids writing pipeline.json in the worktree, which the design explicitly rejects.
- L3 (MAJOR, open, single): FO-18 as worded bans launch flags Task 6 requires; it needs the outside-launch-call scope.
- L4 (MINOR, open, single): Bad-argument exit 2 is pinned only for the preflight stage, never for later subcommands.
- L6 (MAJOR, open, single): The plan does not specify whether tracked-file and `.prev` warnings preserve `created` or `reused` status, although the source allows those warning cases with either status.

## Reviser brief

Blocking finding ids: L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
