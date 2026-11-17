review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | LA-1, LA-7 | R1 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | ARG-1 | R1 |
| L6 | open | no | single | MAJOR | - | R1 |
| L7 | open | no | single | MAJOR | FO-18, ST-4 | R1 |
| L8 | open | yes | overlap | MAJOR | FO-18 | R2, R3 |
| L9 | open | yes | single | MAJOR | - | R3 |
| L10 | open | yes | single | MAJOR | IR-4, IR-7, LA-6 | R3 |
| L11 | open | yes | single | MAJOR | LA-3 | R3 |

## Blocking findings

### L8

#### L8.t3-1 (F1)

- claim: The prescribed create call omits --agent, which the project guard requires; the call is blocked, so no worktree is created and the later launch cannot run.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"
- anchor2: "`--agent`, `--prompt`, `--surface` appear only in the `orca agent launch` call."

#### L8.t4-1 (F2)

- claim: The exact create call omits `--agent`, but project instructions say a hook blocks worktree creation without it; the test also forbids adding it.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment"

### L9

#### L9.t4-1 (F1)

- claim: Bare `orca` can resolve to the GNOME screen reader outside an Orca-managed terminal, so the required preflight may run the wrong program instead of Orca.
- anchor: "preflight runs `orca status --json`"

### L10

#### L10.t4-1 (F3)

- claim: The plan requires launching without effective enforcement, allowing the agent to take actions the selected launch level is meant to restrict.
- anchor: "missing sets `W-ENFORCEMENT-ABSENT` but does not stop the launch"

### L11

#### L11.t4-1 (F4)

- claim: A timeout can leave an agent running after its pending record is removed, preventing the hook from binding and enforcing that session's level.
- anchor: "a nonzero exit, timeout or `ok` not true removes the launch record"

## Other findings

- L1 (MAJOR, open, single): A copy warning on a successful worktree cannot both be the warning field and be demoted to detail; the implementer must guess which rule wins.
- L2 (MAJOR, open, single): Source LA-7 (no launch for a failed worktree record, no pending record for none) has no candidate test, so the skill-text pin may be skipped.
- L3 (MAJOR, open, overlap): Candidate omits the required hand-command note that a hand-started agent is not hook-governed and the timeout check-Orca detail.
- L4 (MAJOR, open, single): Candidate omits not_requested for none/failed worktree, null fields on STOP, and enforcement_hook null when no agent was requested.
- L5 (MAJOR, open, single): No candidate acceptance pins bad-argument exit 2 for the worktree, prompt, and launch subcommands as source ARG-1 requires.
- L6 (MAJOR, open, single): First rule is ambiguous between first overall and first among pre-existing rules, so STOP precedence for create-only flags needs a guess.
- L7 (MAJOR, open, single): FO-18 as worded bans --agent/--prompt/--surface in any call, contradicting the launch call that requires them; source scopes it to list/create.

## Reviser brief

Blocking finding ids: L8, L9, L10, L11.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
