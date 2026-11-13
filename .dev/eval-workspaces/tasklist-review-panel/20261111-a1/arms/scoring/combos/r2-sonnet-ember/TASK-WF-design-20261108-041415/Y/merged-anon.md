review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R4: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R5: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | - | R1, R2, R3, R4, R5 |
| L2 | open | no | single | MAJOR | - | R4 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R4 (F1)

- claim: The Constraints bullet allows exactly two writes to the created issue, but Task 2 requires a third write, the pushback comment.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "type read-back; field POST and read-back; pushback comment; final output"

#### L1.R4 (F2)

- claim: The named tests leave reverts of the flags-decision row, the create-review-comment wording and the create.md Wave 1 text undetected, so the acceptance cannot be met as written.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R4 (F4)

- claim: The bullet forbids editing .claude/ but requires make sync-dev, which writes .claude/, and does not say which wins.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"

#### L1.R4 (F5)

- claim: The scanner test as specified rejects the required phrase 'no other orgs/ path', and the plan names no regex that avoids it.
- anchor: "every `orgs/` path found by regex in the skill folder files and the `AGENTS` files equals"
- anchor2: "no other `orgs/` path"

#### L1.R4 (F8)

- claim: The plan does not say whether ./artifacts/ means the package artifacts folder or the project-root folder, and the Constraints bullet does not list either as an allowed write location.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R4 (F6)

- claim: Kept gh label lines still read --repo <owner/repo>, which Constraint 21 does not allow, and the plan does not require rewriting them.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R4 (F7)

- claim: The cited test line numbers are stale; the live file has these tests at 545, 586 and 701.
- anchor: "`test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` (around lines 492 to 520)"

#### L1.R4 (F9)

- claim: The self-check refers to an orgs/ scanner that the plan never asks the implementer to write.
- anchor: "feeds the `orgs/` scanner a text with `orgs/other/issue-fields`"

#### L1.R3 (F1)

- claim: The skill is told it writes only two things to the created issue, yet the create steps post a pushback comment on that issue.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every"

#### L1.R3 (F2)

- claim: The plan describes a pre-change repo; HEAD already holds the target text and tests, and the plan gives no rule for already-applied edits.
- anchor: "Remove the 11 `type: ...` labels, the 3 `complexity: ...` labels and their `gh label create` lines"
- anchor2: "change `len(blocks) == 2` to 3"

#### L1.R3 (F3)

- claim: The orgs/ scanner is never defined, and a naive scanner cannot match the spaced placeholder orgs/<owner of R>/issue-fields.
- anchor: "Add one self-check test in the style of `test_fork_safety_scan_fails_on_a_ref_without_repo` (line 642)"

#### L1.R3 (F4)

- claim: The seven listed tests leave Task 3 error rows, the Task 4 flags row and the Task 4 wording unguarded, so the acceptance check can fail for those edits.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R3 (F5)

- claim: Keeping the maintainer lines as they are leaves --repo <owner/repo> where the constraint requires <R>, and the text does not say which to do.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R3 (F6)

- claim: Writing ./artifacts outputs falls outside the four allowed trees unless new files are exempt from the edit rule, which the plan does not say.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R3 (F7)

- claim: The literal no-edit rule for .claude/ conflicts with the instruction to run make sync-dev, which writes that folder.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"
- anchor2: "never by editing `.claude/`"

#### L1.R5 (F1)

- claim: A closed reading of the two-write constraint drops the mode label and the pushback comment that Wave 5 still requires.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "mode label only; `--type` when listed; `gh issue create` and the rename; type read-back; field POST and read-back; pushback comment"

#### L1.R5 (F2)

- claim: The read-back says to treat the value as absent, but a single-select payload stores an option id in value and the option name in single_select_option.name, so a name comparison against value reports a successful Complexity write as not set.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R5 (F3)

- claim: Wave 5 as copied from source 2.1 never records option not found when the Complexity field exists but no option matches, so that failure is missing from the final output.
- anchor: "field POST and read-back; pushback comment; final output with every `not applied` and `not set` line"
- anchor2: "not set: field Complexity <value>: <reason>` with every reason listed in specification 2.4"

#### L1.R5 (F4)

- claim: The manual-check path is package-relative in one reading and the unstaged repo-root artifacts directory in the other.
- anchor: "write `./artifacts/owner-manual-check.md` in this package"

#### L1.R5 (F5)

- claim: Keeping the maintainer lines keeps `--repo <owner/repo>` rather than `--repo <R>`, and the placeholder test does not catch angle brackets.
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R1 (F1)

- claim: The constraint allows only two writes to a created issue, but Wave 5 also posts the pushback comment and applies the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "field POST and read-back; pushback comment; final output"

#### L1.R1 (F2)

- claim: The design doc keeps `gh api user -q .login` in its unchanged claim section, so the literal check fails and conflicts with Task 2's own path rule.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented"
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F3)

- claim: With the six rule tests as specified, reverting only SKILL.md (Task 3) or the flags and review-comment edits (Task 4) leaves every new test green.
- anchor: "Reverting any one of Tasks 1 to 5 in a scratch copy would turn at least one new test red"

#### L1.R1 (F4)

- claim: Tests that pin the command file and the T3 worker are never run, so a break there would go unnoticed.
- anchor: "`make verify-sync` and `make lint` exit 0 and the whole `tests/skills/test_issue_protocol.py` file passes"

#### L1.R1 (F5)

- claim: No rule says what to compare in the Complexity read-back, so a raw value-versus-name comparison can report a false failure after a successful write.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

#### L1.R1 (F7)

- claim: The scanner must skip the bare `orgs/` prose token that Tasks 2 and 5 require, and the task does not say so.
- anchor: "every `orgs/` path found by regex in the skill folder files"

#### L1.R1 (F8)

- claim: Task 12 writes into the package artifacts folder, which the edit-only-under constraint does not list.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: Task 10 cannot pass on the live design doc because gh api user remains and the check omits the user exception.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

#### L1.R2 (F2)

- claim: Task 12 writes to artifacts outside the allowed edit folders.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F3)

- claim: Task 8 allows two orgs path spellings while Task 3 requires one.
- anchor: "equals `orgs/<owner of R>/issue-fields` or `orgs/<owner>/issue-fields`"

## Other findings

- L2 (MAJOR, open, single): The plan describes the pre-change tree, which already has the new text, and gives no check for edits that are already applied.
- L3 (MAJOR, open, single): The command file's Will Not wording is not tied to the skill's exact sentence, so the agreement check the live test enforces can fail.
- L4 (MINOR, open, single): The source sentence that labels_applied and labels_missing now describe the mode label only is not carried by any task.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
