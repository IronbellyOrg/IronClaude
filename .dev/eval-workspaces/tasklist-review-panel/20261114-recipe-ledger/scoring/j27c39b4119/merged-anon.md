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
| L1 | open | no | single | MAJOR | 2.1, 2.5 | R1 |
| L2 | open | no | single | MAJOR | 3.1 | R1 |
| L3 | open | no | single | MAJOR | 2.2 | R1 |
| L4 | open | no | single | MINOR | 2.3 | R1 |
| L5 | open | yes | single | MAJOR | - | R3 |
| L6 | open | yes | single | MAJOR | - | R2 |
| L7 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L5

#### L5.t3-1 (F1)

- claim: This wording implies feature mode selects Feature even when area is `tests`, contradicting the specified rule that this case selects Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""

### L6

#### L6.t4-1 (F1)

- claim: An implementer who follows the stated text as written runs `make sync-dev` after source edits, and that is wrong because the command copies files into `.claude/`, which the same plan forbids editing.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

### L7

#### L7.t4-1 (F2)

- claim: An implementer who follows the stated text as written writes the required artifact, and that is wrong because the plan's edit-scope constraint forbids writing to `./artifacts/`.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L7.t4-1 (F3)

- claim: Task 12 labels the procedure a single manual check but directs the owner to file two issues, adding an unrequested bug-mode issue beyond the source's one feature-mode check.
- anchor: "file one test issue with `/sc:issue --create \"<short test description>\" --mode feature --type tests --depth standard`"
- anchor2: "repeat once with `--mode bug` and confirm type Bug."

## Other findings

- L1 (MAJOR, open, single): Candidate never requires writing the JSON body to .dev/issues/<N>/complexity-field.json after the rename, so an implementer may use the pre-rename path and lose the file.
- L2 (MAJOR, open, single): Task 6 drops the Q5 rule that the area is also recorded in the pushback comment, so an implementer following it omits that record.
- L3 (MAJOR, open, single): Task 3 never requires updating the return-contract text so labels_applied and labels_missing describe the mode label only, leaving the old multi-label reading in place.
- L4 (MINOR, open, single): The exception placeholder is spelled <owner> in one place and <owner of R> in another; an implementer must guess which literal to write, though the Task 8 test allows both.

## Reviser brief

Blocking finding ids: L5, L6, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
