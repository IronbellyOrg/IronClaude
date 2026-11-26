review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted> block ok true
- R3: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | - | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MINOR | - | R2 |
| L7 | open | no | single | MINOR | - | R2 |
| L8 | open | no | single | MINOR | - | R2 |
| L9 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L10 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L9

#### L9.R2 (N4)

- claim: Leaving open whether the fake gh is an importable helper or a fixture risks an import failure in pytest.
- anchor: "exposing the fake as a helper or fixture that other test files may import"

#### L9.R3 (F1)

- claim: The mandated repository-resolution fallback uses `gh repo view` without `--repo` or a `repos/` path, so the required every-line scoping assertion fails.
- anchor: "`--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing"
- anchor2: "test_set_draft_state.py also statically scans the script and asserts every `gh` line carries `--repo` or a `repos/` path"

#### L9.R1 (F1)

- claim: An implementer following the constraint literally cannot create or edit the required tests and documentation outside `src/superclaude/`.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files."
- anchor2: "Create `tests/pr_submit/test_set_draft_state.py` using a fake `gh` on `PATH`"

## Other findings

- L1 (MAJOR, open, single): The Wave 0 bullet must say the off line prints at L3, yet the same text says it carries no L3 condition and the test rejects any L3 condition; passing needs a reading of gate that the text does not fix.
- L2 (MAJOR, open, single): A failed draft call followed by a resume leaves the engage decision at HOLD(ownership_unproven), and the plan never says whether HOLD halts before edits or proceeds with a ready PR.
- L3 (MAJOR, open, single): A run that never engaged reports merge_guard released, which tells the user a release happened when the PR was never drafted.
- L4 (MAJOR, open, single): The plan does not say where a ci-n cycle id is minted, so the Wave 8 push triad and re-trigger may use a different id from the guard.
- L5 (MAJOR, open, single): Constraint 22 requires entries for git write verbs too, but this task and Tasks 7, 10 and 12 list only gh pr and gh api, so a git write-verb line would fail the classification test.
- L6 (MINOR, open, single): Task 5 consumes Task 2's event types but declares no direct dependency on Task 2.
- L7 (MINOR, open, single): git status never lists gitignored mirrors, so this clause describes output that cannot occur.
- L8 (MINOR, open, single): The pr_not_open case omits the source requirement to report the local commit target_sha.
- L10 (MINOR, open, single): The plan does not say how the test sets remote_reachable, so the landed or not_landed outcome is a flag the test chooses rather than a live result.

## Reviser brief

Blocking finding ids: L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
