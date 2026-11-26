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
| L1 | open | yes | overlap | CRITICAL | - | R3, R2, R1 |
| L2 | open | yes | single | CRITICAL | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Task 12 requires artifacts outside the only permitted edit roots, so the scope constraint and its acceptance criteria contradict each other.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t2b-1 (F5)

- claim: The manual check omits the source 3.4 risk notes on org-members-only visibility and the versioned API header.
- anchor: "It also records the three UNVERIFIED points from the source section 3.4 (POST body, `--type` flag, silent drop without push access) and the four defaults"

#### L1.t3-1 (F1)

- claim: The plan requires a sync that writes under `.claude/` while forbidding edits there, so an implementer cannot meet both stated requirements.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

#### L1.t3-1 (F2)

- claim: Task 12 requires artifacts outside the four permitted edit roots, so the deliverables cannot be written without violating the plan’s scope constraint.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.t4-1 (F1)

- claim: The plan requires the mode label but says only the issue type and Complexity field are written to the issue.
- anchor: "The skill never creates a label, an issue type or an issue field. It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Co"

#### L1.t4-1 (F2)

- claim: Task 12 requires writing `./artifacts/owner-manual-check.md` and `./artifacts/t12-checks.log`, outside the allowed edit locations.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.t4-1 (F3)

- claim: The manual-check deliverable omits the source's caveats that field visibility is organization-member-only and that an older API version may return a non-fatal 404.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

### L2

#### L2.t2b-1 (F2)

- claim: The design document's legitimate gh api user lookup cannot pass this criterion without breaking the user path the source and Task 2 keep.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L2.t2b-1 (F3)

- claim: Two different orgs path spellings are required by different tasks, so following both literally can produce two paths and fail the exactly-one test.
- anchor: "`create.md` states the single `orgs/<owner>/issue-fields` exception and that no other `orgs/` path is allowed."
- anchor2: "The Read-only GitHub access rule names exactly one `orgs/` path, `orgs/<owner of R>/issue-fields`"

## Other findings

- L3 (MAJOR, open, single): The source requires re-running the level-table copy into CLAUDE.md; the plan replaces it with a conditional search and cites line 329 instead of the live line 333.
- L4 (MINOR, open, single): The ordered steps omit explicit option-not-found and write-failed detection, listing only the output line formats.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
