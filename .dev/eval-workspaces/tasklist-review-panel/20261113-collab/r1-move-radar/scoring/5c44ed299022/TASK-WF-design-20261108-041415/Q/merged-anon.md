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
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | yes | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 10 cannot pass because the design doc still has `gh api user` and the old rule paragraph, neither in the change list.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "Replace the statements that labels come from a fixed set or that `type:` and `complexity:` labels are applied"

### L5

#### L5.R3 (F1)

- claim: Task 12 requires writing the owner manual check under `./artifacts/`, outside the plan’s allowed edit directories.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`. Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L5.R3 (F2)

- claim: The required sync writes generated files under `.claude/`, contradicting the instruction never to edit those files.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L5.R2 (F1)

- claim: The plan simultaneously requires a mode label and says only the issue type and Complexity field are written besides creating the issue, leaving contradictory create behavior.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

## Other findings

- L2 (MAJOR, open, single): Task 1 omits the field-and-option precondition before the POST.
- L3 (MAJOR, open, single): The listed tests check presence only, not Wave 5 order.
- L4 (MINOR, open, single): Line number drifted from 329 to 333 in the live file.

## Reviser brief

Blocking finding ids: L1, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
