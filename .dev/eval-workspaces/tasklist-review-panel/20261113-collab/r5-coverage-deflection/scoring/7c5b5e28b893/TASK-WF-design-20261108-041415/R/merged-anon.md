review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | yes | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MINOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.R2 (F1)

- claim: Constraint line 23 allows only the issue type and the Complexity write besides the issue, but Task 2 keeps the pushback comment and Task 1 keeps the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R2 (F4)

- claim: A bare ./artifacts path can be read as the project-root folder, which is outside the four allowed edit roots.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F5)

- claim: The same sentence bans editing .claude/ and orders make sync-dev, which rewrites .claude/; the ban should say hand-edit.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R3 (F1)

- claim: The plan both forbids edits under `.claude/` and requires a sync target that copies files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R3 (F2)

- claim: The required owner manual check is outside the plan's stated allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F3)

- claim: The exact-two-writes constraint contradicts the required mode label, which is another change to the created issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R1 (F1)

- claim: Task 12 requires artifact files outside the stated allowed edit locations, so an implementer cannot satisfy both the scope constraint and the required deliverables.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.R2 (F2)

- claim: Reverting Task 3 turns none of the seven listed new tests red, so the criterion cannot pass for Task 3.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L2.R2 (F3)

- claim: No regex or scanner is specified, and the path contains spaces, so the equality check depends on the regex chosen.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "Add one self-check test in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo`"

## Other findings

- L3 (MAJOR, open, single): The plan does not say what to do when the Complexity field is not single-select, though the scout records its data type.
- L4 (MINOR, open, single): Task 2 leaves the create.md Wave 2 sentence saying relabelled, so the protocol and the design doc disagree.
- L5 (MINOR, open, single): Live line numbers are 580 (Will test), 545-573 (return contract) and 695 (fork-safety example).
- L6 (MINOR, open, single): The shorthand omits --repo, which Constraint line 21 requires on every gh issue line.
- L7 (MINOR, open, single): The template already has a Type row for the area, and the plan does not say how the two rows differ.
- L8 (MAJOR, open, single): The plan does not specify whether to skip the field write when the Complexity field is not single-select, leaving behavior undefined for a data type the lookup is required to record.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
