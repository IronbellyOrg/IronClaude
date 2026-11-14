review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MINOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R3 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Artifacts output root is ambiguous against the allowed edit roots; implementer must guess package-local versus repo-root.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: Task 12 requires two artifact files outside the permitted edit paths, so the scope constraint and required deliverables cannot both be satisfied.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F3)

- claim: The candidate requires a sync that generates `.claude/` copies while forbidding edits to those generated paths.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R2 (F1)

- claim: Task 12 requires two artifacts under `./artifacts/`, outside the allowed edit paths, so the task cannot satisfy both the scope constraint and its artifact requirements.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

### L3

#### L3.R1 (F3)

- claim: POST body file directory .dev/issues/<N>/ is not required by any task or acceptance check.
- anchor: "`gh api -X POST repos/<R>/issues/<N>/issue-field-values --input <file>`"

#### L3.R3 (F2)

- claim: The prescribed mode-row wording says feature mode selects Feature, contradicting the rule that feature mode with area tests selects Test.
- anchor: "Picks the feature or bug template, the Feature or Bug issue type and the `enhancement` / `bug` label"
- anchor2: "mode `feature` with area `tests` gives Test"

## Other findings

- L2 (MINOR, open, single): Revert acceptance overstates: Task 3 third block is pinned by Task 7 updated test, not by the six new Task 8 tests alone.
- L4 (MINOR, open, single): Cited line 329 is stale (live row at 333); constraint requires re-reading live lines so this is note-only.
- L5 (MAJOR, open, single): The plan does not specify that the POST body file must be written under `.dev/issues/<N>/` after the draft directory is renamed, allowing an implementer to use a stale draft-directory path.

## Reviser brief

Blocking finding ids: L1, L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
