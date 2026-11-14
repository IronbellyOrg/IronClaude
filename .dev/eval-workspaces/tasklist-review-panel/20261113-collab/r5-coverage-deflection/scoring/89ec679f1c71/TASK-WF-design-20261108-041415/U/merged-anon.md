review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The plan both forbids edits under `.claude/` and requires `make sync-dev`, which writes the source changes there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`;"
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R3 (F3)

- claim: The stated two-write limit conflicts with the required mode label unless it is narrowed to classification settings.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R3 (F4)

- claim: Task 12 describes a single check but requires creating both a feature test issue and a separate bug test issue.
- anchor: "the single manual check the owner runs after merge"

#### L1.R2 (F2)

- claim: The plan both restricts edits to the listed directories and requires writing artifacts outside them, so an implementer cannot follow both instructions.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F4)

- claim: The artifacts path sits outside the stated edit-only roots and its base directory is ambiguous.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R3 (F2)

- claim: The acceptance criterion requires removing or changing the existing `gh api user` claim lookup, which would make the design document inaccurate about how the current login is read.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

#### L2.R2 (F1)

- claim: The acceptance criterion requires removing or rewriting the existing `gh api user` lookup even though the claim flow must remain unchanged, so the criterion cannot pass while preserving claim behavior.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`gh api user -q .login`"

#### L2.R1 (F5)

- claim: The existing 'gh api user' path makes the literal check unpassable as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

## Other findings

- L3 (MAJOR, open, single): The new orgs test accepts a spelling that Task 5 forbids, so it cannot catch that break.
- L4 (MAJOR, open, single): Without the source qualifier 'for them', the check can be read as banning the bug/enhancement maintainer lines the plan keeps.
- L5 (MINOR, open, single): Stale line numbers (333 live, 545 for test_st10) are stated as fact, relying on the re-read constraint to rescue them.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
