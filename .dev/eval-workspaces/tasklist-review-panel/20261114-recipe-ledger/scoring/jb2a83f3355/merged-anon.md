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
| L2 | open | no | single | MAJOR | 2.2 | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | 3.4 | R1 |
| L5 | open | no | single | MINOR | 3.2 | R1 |
| L6 | open | yes | overlap | MAJOR | - | R3, R2 |
| L7 | open | no | single | MAJOR | - | R3 |
| L8 | open | yes | single | MAJOR | - | R2 |
| L9 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 acceptance forbids the gh api user path that Task 2 keeps allowed and that the design doc still uses, so it cannot pass as written.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

### L6

#### L6.t3-1 (F1)

- claim: The plan requires a mode label and may post a pushback comment, contradicting its claim that only the issue type and Complexity field are written besides the issue itself.
- anchor: "The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Co"
- anchor2: "Pushback comment as today, then print the issue URL, the directory, every `not applied` and `not set` line."

#### L6.t3-1 (F2)

- claim: Task 12 requires writing manual-check and test-log files under `./artifacts/`, outside the explicitly allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L6.t4-1 (F2)

- claim: The plan requires writing the manual-check artifact outside its stated allowed edit paths, so the scope rule and deliverable cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L8

#### L8.t4-1 (F1)

- claim: The plan requires a pushback comment after creation while also limiting writes to the created issue to exactly two things, so both requirements cannot be met.
- anchor: "The skill writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "Pushback comment as today, then print the issue URL, the directory, every `not applied` and `not set` line"

## Other findings

- L2 (MAJOR, open, single): No task states classification_missing holds each not set line without the prefix, so the return contract can pass with wrong content.
- L3 (MINOR, open, single): Accepting two orgs path spellings weakens the source test that pins the single orgs/<owner>/issue-fields form.
- L4 (MINOR, open, single): The manual check file omits the source risks on org-only field visibility and the versioned field API default.
- L5 (MINOR, open, single): The named test sits at line 545 and the Will test at 580, not the stated 492 to 520 and 527, so a reader following line numbers lands on the wrong test.
- L7 (MAJOR, open, single): The plan does not define a `not set` reason or continuation behavior when either classification read-back command itself fails.
- L9 (MAJOR, open, single): The plan requires the return-contract keys but omits the required value semantics, including that classification_missing lists each not-set line without its prefix.

## Reviser brief

Blocking finding ids: L1, L6, L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
