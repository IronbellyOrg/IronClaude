review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L3

#### L3.R1 (F4)

- claim: Task 12 artifacts path is stated without disambiguation from the edit-roots.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.R2 (F2)

- claim: Task 12 requires writing an artifact outside every location permitted by constraint 19.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

### L6

#### L6.R2 (F1)

- claim: Task 12 requires running a sync that writes under `.claude/`, despite constraint 19 forbidding edits there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L1 (MAJOR, open, single): Task 10 gh api acceptance omits the user exception that Task 2 allows.
- L2 (MAJOR, open, single): Kept-verbatim maintainer lines retain the unconstrained <owner/repo> placeholder.
- L4 (MINOR, open, single): Line-number cites have drifted from the live files.
- L5 (MINOR, open, single): The orgs/ scanner rule does not state that a bare prose orgs/ token is not a path.

## Reviser brief

Blocking finding ids: L3, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
