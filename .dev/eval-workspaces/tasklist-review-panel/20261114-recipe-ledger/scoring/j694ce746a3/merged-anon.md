review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | 2.3, 3.1 | R1 |
| L2 | open | no | single | MINOR | 3.1 | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R3, R2 |
| L4 | open | no | single | MINOR | 3.2 | R1 |
| L5 | open | no | single | MINOR | 3.2 | R1 |
| L6 | open | no | single | MAJOR | - | R2 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Acceptance cannot pass with the valid gh api user line intact; fixing it breaks the claim lookup.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L3

#### L3.t2b-1 (F3)

- claim: Repo root artifacts path conflicts with edit only list and package artifacts rule.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.t3-1 (F1)

- claim: The plan requires writing the manual-check artifact outside its permitted edit locations, so the artifact criterion cannot be met while obeying the constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.t3-1 (F2)

- claim: The plan adds a second test-issue creation even though the driving document specifies one owner manual check.
- anchor: "repeat once with `--mode bug` and confirm type Bug."

#### L3.t3-1 (F3)

- claim: The plan omits the stated organization-membership visibility limitation and API-version 404 caveat from its implementation and owner-check instructions.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4"

#### L3.t4-1 (F1)

- claim: Task 12 requires writes outside the plan's permitted edit roots, so its required outputs cannot be produced while honoring the scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "the outputs are saved to `./artifacts/t12-checks.log`."

#### L3.t4-1 (F2)

- claim: The plan both applies a mode label and says exactly two things are written besides the issue, despite specifying only the issue type and field as those two things.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L3.t4-1 (F5)

- claim: Task 12 calls for one manual check but then requires a second issue check, exceeding the driving document's single test-issue check.
- anchor: "the single manual check the owner runs after merge"
- anchor2: "repeat once with `--mode bug` and confirm type Bug."

## Other findings

- L2 (MINOR, open, single): Stale line number; the row is at line 333 on disk. Byte copy makes it harmless.
- L4 (MINOR, open, single): Stale line numbers; test is at line 545 and the Will test at 580 on disk.
- L5 (MINOR, open, single): Regex pattern unnamed; a naive token scan breaks on the space in the allowed path.
- L6 (MAJOR, open, single): The plan omits the required values for the new return-contract keys: read-back values or nulls, and the missing-classification lines without their prefix.
- L7 (MAJOR, open, single): The plan requires recording the area in flags.md but never requires putting it in the pushback comment as the driving document specifies.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
