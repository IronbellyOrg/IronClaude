review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R3 |
| L5 | open | yes | overlap | MAJOR | - | R3, R2, R1 |
| L6 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 10 AC is unpassable from the named edits alone because the design doc still has gh api user at line 157 and a repos-only rule at line 330.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L5

#### L5.t2b-1 (F7)

- claim: The manual-check artifact omits the versioned-API 2026-03-10 risk, losing the warning that a 404 may mean the wrong API version.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access)"

#### L5.t3-1 (F1)

- claim: Applying the required mode label makes three writes to the issue, contradicting the stated exact count; omitting it contradicts the goal.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."

#### L5.t3-1 (F2)

- claim: The required manual-check artifact is outside the permitted edit paths, so the plan cannot satisfy both instructions as written.
- anchor: "- Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.t4-1 (F1)

- claim: An implementer following the exactly-two-writes constraint can omit the required mode label, contradicting the goal and the label rules.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L5.t4-1 (F2)

- claim: Running the required sync changes files under `.claude/`, violating the plan's explicit prohibition on editing anything there except settings.json.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L5.t4-1 (F3)

- claim: Writing the required manual-check file under artifacts is outside the plan's permitted edit directories, so an implementer cannot satisfy both instructions.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): Kept maintainer lines use --repo <owner/repo> in the live file, so the Task 1 AC fails unless keep is read as allowing a placeholder rewrite.
- L3 (MAJOR, open, single): Task 3 states keys and the sentence but not the source 2.2 value definitions or the without-prefix rule for classification_missing.
- L4 (MAJOR, open, single): The live test definitions are at 545 and 695, so the cited numbers point the implementer at the wrong tests until the function names are used.
- L6 (MAJOR, open, single): The plan does not specify where or when to write the POST input file; writing it before the rename can leave the field POST with a stale path and prevent setting Complexity.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
