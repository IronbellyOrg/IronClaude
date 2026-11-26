review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 3.1 | R2 |
| L2 | open | no | single | MAJOR | 2.1 | R2 |
| L3 | open | no | single | MINOR | 3.2 | R2 |
| L4 | open | yes | single | MAJOR | - | R3 |
| L5 | open | yes | overlap | CRITICAL | - | R3, R1 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | yes | single | CRITICAL | - | R1 |

## Blocking findings

### L4

#### L4.t3-1 (scope-docs)

- claim: An implementer who follows the stated text as written builds changes to the user-guide docs, and those changes are wrong because the driving document says to edit `src/superclaude/` only.
- anchor: "Edit `docs/user-guide/commands.md` and `docs/user-guide/flags.md`."

### L5

#### L5.t3-1 (scope-artifact)

- claim: An implementer cannot both obey the allowed-path restriction and write the required artifact at `./artifacts/owner-manual-check.md`, so the acceptance criterion cannot be met while following the plan.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.t4-1 (B2)

- claim: The plan requires an artifact outside its permitted edit paths, so the deliverable cannot be produced without violating the scope constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

### L7

#### L7.t4-1 (B1)

- claim: The plan prohibits editing `.claude/` while requiring `make sync-dev`, which edits those dev copies.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L1 (MAJOR, open, single): Task 11 pins line 329 but the /sc:issue row is at line 333; line 329 is the /sc:graph row, so an implementer editing at the stated line corrupts the wrong row.
- L2 (MAJOR, open, single): The relabelled to reclassified change is ordered only for the template, leaving the identical wording in refs/create.md line 36 stale and inconsistent with the rest of the protocol.
- L3 (MINOR, open, single): Stated test line numbers (492 to 520, 527, 642) do not match the live file (545, 580, 695), so an implementer going to the stated lines lands in unrelated tests.
- L6 (MAJOR, open, single): The plan names the return-contract keys but omits the required values and meanings for each field, leaving the returned classification data unspecified.

## Reviser brief

Blocking finding ids: L4, L5, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
