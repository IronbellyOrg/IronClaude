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
| L1 | open | yes | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | overlap | MAJOR | - | R1, R3 |
| L3 | open | yes | overlap | MAJOR | - | R1, R2 |
| L4 | open | yes | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | no | single | MINOR | - | R1 |
| L8 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: Task 10’s path acceptance criterion rejects the existing and source-authorized `gh api user` call, so retaining claim-mode behavior makes the criterion fail.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F3)

- claim: The existing `gh api user -q .login` line is never mentioned by the task, so a literal check fails on correct pre-existing text.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

### L3

#### L3.R2 (F1)

- claim: The plan both requires applying the mode label and limits writes to exactly two things without exempting that label.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L3.R2 (F3)

- claim: Task 12 requires creating artifact files outside the plan's permitted edit paths.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L3.R1 (F1)

- claim: Task 12 writes outside the stated edit scope; the implementer must guess whether the specific instruction overrides the general constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

### L4

#### L4.R2 (F2)

- claim: The command description says feature mode selects Feature, while the plan requires feature mode with area `tests` to select Test.
- anchor: "the `--mode` row (line 41) to \"Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label\""
- anchor2: "the `--type` row (line 42) to say the area of the change, which selects issue type Test for a feature in `tests`"

## Other findings

- L2 (MAJOR, open, overlap): The proposed test checks line prefixes but not the required reason values, so omissions such as `option not found` could pass that test.
- L5 (MAJOR, open, single): The `bug` and `enhancement` maintainer `gh label create` lines are kept, so a literal no-`gh-label-create` reading fails against the plan's own retained lines.
- L6 (MINOR, open, single): The row is at line 333 in the live file, not 329; the wording still identifies it.
- L7 (MINOR, open, single): create.md keeps "not silently relabelled", so the template and the ref that posts it now use different words.
- L8 (MINOR, open, single): Written as a standalone entry, the shorthand lacks `--repo` and would fail the fork-safety scan; it must be folded into the existing `--repo <R>` entry.

## Reviser brief

Blocking finding ids: L1, L3, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
