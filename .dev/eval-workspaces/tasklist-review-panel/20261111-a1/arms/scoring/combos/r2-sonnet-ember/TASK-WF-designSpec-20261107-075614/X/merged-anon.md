review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R4: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R5: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3, R4, R5 |
| L2 | open | no | overlap | MAJOR | - | R1, R2, R4 |
| L3 | open | no | overlap | MAJOR | - | R1, R2, R3, R4, R5 |
| L4 | open | no | single | MAJOR | - | R5 |
| L5 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R4 (F1)

- claim: An implementer who follows the stated text as written builds a new merge_guard.py and repeats the 43-R6 enum change, and X is wrong because both already exist at HEAD, so the base record describes a tree that already holds the feature.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "First record the base-commit state: run `make lint`"

#### L1.R4 (F3)

- claim: An implementer who follows the stated text as written places the Wave 6 release bullet after every pinned sentence, and X is wrong because the pinned S5a re-trigger must come after the release, so the release would run after the re-trigger.
- anchor: "are additive sentences, bullets and rows placed after, never inside, the sentences pinned by"
- anchor2: "the Wave 6 test asserts the Pre-push sentence and the Release-before-reply-resolve-re-trigger order"

#### L1.R4 (F4)

- claim: An implementer who follows Task 8 as written adds entries only for gh pr and gh api lines, and X fails test_every_write_verb_hit_is_classified when the ref has a git add, commit or push line, because WRITE_VERB_RE also matches those verbs.
- anchor: "that contains `gh pr`, `gh api` or a git write verb needs one entry"
- anchor2: "for every line of the ref that matches `gh pr` or `gh api`"

#### L1.R4 (F6)

- claim: An implementer who follows the stated text as written builds release_decision with a cycle_id argument that no row reads, and X is wrong because a zero-edit cycle can release a guard held for an earlier cycle, and the candidate does not say whether a run may continue past a held cycle.
- anchor: "release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)"

#### L1.R4 (F7)

- claim: An implementer who follows Task 11 as written must leave tests/pr_submit fully passing, and X conflicts with Task 13 only when the base record shows a pr_submit failure, since Task 13 accepts base failures.
- anchor: "`uv run pytest tests/pr_submit -q` passes in full."
- anchor2: "shows no failing test id that is absent from the base-commit record of Task 1"

#### L1.R4 (F8)

- claim: An implementer who follows constraint 19 literally edits no file outside src/superclaude, and X is wrong because Tasks 2, 5 and 13 require edits to tests and docs, and the text does not say canonical means the mirrored product files.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`"
- anchor2: "Edit `docs/user-guide/commands.md`: add"

#### L1.R4 (F9)

- claim: An implementer who follows Task 12 as written picks either the quoted or the placeholder form of the clear command, and X is wrong by the candidate's own inconsistency, since Task 8 and Task 13 give different forms while Task 12 asks for the exact one.
- anchor: "the section states default-on at monitor 3, the exact clear command"
- anchor2: "the clear command `gh pr ready <N> --repo <REPO>`"

#### L1.R4 (F10)

- claim: An implementer who follows the stated text as written expects gitignored .claude mirrors in git status output, and X cannot occur because git status never lists ignored paths, so that clause is vacuous.
- anchor: "and gitignored `.claude/` mirrors; no `.claude/` path other than `.claude/settings.json` is staged"

#### L1.R3 (F1)

- claim: A zero-edit cycle releases the PR even when an earlier held cycle's fix never reached the PR head, so the PR becomes ready without the fix.
- anchor: "`release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`"
- anchor2: "release on the confirmed push before replies and the re-trigger"

#### L1.R3 (F2)

- claim: The protocol already supplies a cycle_id to the push key and rereview_requested, and the plan does not say which id wins.
- anchor: "O1 names one single place where the guard-enabled cycle id is minted so the push triad and `rereview_requested` use the same id"

#### L1.R3 (F3)

- claim: The repository HEAD already contains the feature, so the create and change steps would overwrite existing work and the base record is taken on the built tree.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"
- anchor2: "run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit"

#### L1.R3 (F5)

- claim: Comparing only a start-text constant cannot establish byte-identity, so the pinned sentences can change in their tail without failing.
- anchor: "are asserted byte-identical by comparing the live text with string constants"
- anchor2: "the literal start text recorded in `./artifacts/pre-build-gate.md`"

#### L1.R3 (F6)

- claim: The reference names the decide and append steps but no command form, and it forbids a python fence, so the implementer must invent the invocation.
- anchor: "decide with `superclaude.pr_submit.merge_guard`, append the `draft_guard_requested` event with fsync before the call"

#### L1.R3 (F7)

- claim: Gitignored mirror paths never appear in git status --short, so the expected output list is partly unmatchable.
- anchor: "`git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/`, `.dev/` and gitignored `.claude/` mirrors"

#### L1.R5 (F3)

- claim: Resume row 4 calls release without this cycle's edit count or target commit, and an edit count of 0 releases before the head is checked.
- anchor: "each re-enter `release_decision` with `push_completed=True`"
- anchor2: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"

#### L1.R5 (F4)

- claim: A failed engage leaves release-pending without owning the draft, and a later resume at monitor level 3 falls through to no action, so the plan never keeps that resumed run from editing a mergeable pull request.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"

#### L1.R1 (F1)

- claim: resume_decision takes no target_sha, per-cycle applied_edits or cycle_id, so row 4 cannot reach RELEASE(pushed) and the Task 4 and Task 11 criteria that a landed or published push releases cannot pass.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "each re-enter `release_decision` with `push_completed=True`"

#### L1.R1 (F3)

- claim: The force-push wording rule is stated for SKILL.md lines only, but the test scans every md and sh file in the skill directory, including the new ref and script.
- anchor: "must not use wording that the forbidden-force-push line test rejects"

#### L1.R2 (F3)

- claim: guard_status is not pinned for mode off with an existing held record at ordinal 3, so the exit field can disagree with resume reporting.
- anchor: "mode `OFF` and ordinal below 3 with no record (`off`)"
- anchor2: "mode `OFF` at ordinal 3 with phase `HELD` returns `REPORT_HELD`"

## Other findings

- L2 (MAJOR, open, overlap): An implementer who follows the stated text as written builds a --read that exits 1 with ok false on a timeline-only failure, and X is wrong on the reading the checkout takes (exit 0 with ok true and complete false), because the exit list never says a timeline failure counts as a failing gh.
- L3 (MAJOR, open, overlap): An implementer who follows the stated text as written names the event draft_guard_requested in the Wave 0 bullet, and X fails a plain substring check for draft, since the candidate never defines draft gate wording.
- L4 (MAJOR, open, single): A search for 43 still hits the 42nd-43rd conflict-event comment after the enum count is corrected, so an empty-search reading of the check cannot pass.
- L5 (MINOR, open, single): Phase string values are used in acceptance but never stated, so the folded phase type is implied rather than specified.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
