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
| L1 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The plan simultaneously requires applying a mode label and limits writes besides issue creation to the issue type and Complexity field, so its write-count requirement contradicts its required behavior.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R2 (F1)

- claim: The plan forbids edits under `.claude/` while requiring a sync command that writes generated files there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R2 (F2)

- claim: Task 12 requires artifact writes outside the plan’s permitted edit locations.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L1.R2 (F3)

- claim: The Task 10 criterion rejects the unchanged claim-mode `gh api user` path in the design document.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "`--claim` behaviour and text stay unchanged, including its two-block part of the return contract."

#### L1.R1 (F2)

- claim: The retained gh api user claim lookup makes the file-wide check fail unless it is read as create-scope only.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."

#### L1.R1 (F3)

- claim: Keeping the maintainer lines verbatim leaves --repo <owner/repo> instead of the required --repo <R>.
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block."
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.R1 (F5)

- claim: Task 12 writes ./artifacts/owner-manual-check.md outside the listed editable roots with no exception.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

## Other findings

- L2 (MAJOR, open, single): Changing the T3 read-only rule without updating the exact expected-text assertion in tests/skills/test_worker_contract.py leaves that existing test failing.
- L3 (MAJOR, open, single): Line 329 is the /sc:graph row in the live file, not the /sc:issue row at line 333, so a verbatim edit hits the wrong row.
- L4 (MINOR, open, single): No text states that labels_applied/labels_missing now describe the mode label only.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
