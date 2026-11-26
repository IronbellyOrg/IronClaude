review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 e54e890380e234377e77d17b785d8ad7940fdadc69528f488b0c06b0ff5964f4
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R3, R2, R1 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | overlap | MAJOR | - | R3, R2 |
| L4 | open | yes | overlap | CRITICAL | - | R3, R2 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | no | single | MINOR | - | R3 |
| L7 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Master-comparison worktree command is blocked by the --agent hook, so pre-existing-failure evidence cannot be gathered.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L1.t3-1 (F2)

- claim: The required master-comparison worktree creation omits `--agent`, which the project Orca instructions require and the hook blocks without, so the specified comparison cannot run.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

#### L1.t4-1 (F1)

- claim: The specified Orca command omits required `--agent`, so the repository hook blocks creating the temporary master-comparison worktree and the check cannot run as written.
- anchor: "orca worktree create --name issue302-master-check --base-branch origin/master"

### L4

#### L4.t2b-1 (F6)

- claim: Shape reference and enumerated frontmatter disagree (example file carries category, maxTurns and permissionMode).
- anchor: "Follow the frontmatter shape of existing agents such as `src/superclaude/agents/evidence-validator.md`."

#### L4.t3-1 (F1)

- claim: A worker must create the `/sc:analyze` report from a named skill template, but the source requires the report format of `/sc:analyze` and defines no template for it, so the worker cannot satisfy both requirements.
- anchor: "every file it writes starts from the named template under `~/.claude/skills/sc-issue-protocol/templates/`"

## Other findings

- L2 (MAJOR, open, single): SKILL.md may carry only the 9 coded STOPs and omit the message-only row behaviours (closed, assigned-to-other, ClickUp continue, recommend fallback, missing label).
- L3 (MAJOR, open, overlap): Invalid CLICKUP_MAX_PAGES behaviour is left undefined, so two implementers will build scripts with different error handling.
- L5 (MINOR, open, single): Complex templates defined only as simple-plus-extra, leaving the exact position of the extra headings undetermined.
- L6 (MINOR, open, single): Docs anchor for /sc:issue is specified by analogy only, with no exact anchor string stated.
- L7 (MAJOR, open, single): The plan does not direct the implementer to use the specified feature branch before editing, leaving work on the current branch possible.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
