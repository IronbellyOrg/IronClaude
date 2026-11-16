review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MINOR | 3.2 | R3 |
| L2 | open | no | single | MINOR | 3.1 | R3 |
| L3 | open | yes | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | 2.1, 2.4, 2.5 | R2 |

## Blocking findings

### L3

#### L3.t3-1 (F1)

- claim: An implementer who follows the stated text as written runs the required sync and edits files under `.claude/`, violating the explicit prohibition.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L3.t3-1 (F2)

- claim: An implementer who follows the stated text as written must write the required manual-check artifact outside the permitted edit scope or leave a required deliverable incomplete.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L1 (MINOR, open, single): Stale line numbers; re-read instruction prevents wrong edit.
- L2 (MINOR, open, single): Stale line number; row is at line 333, re-read instruction prevents wrong edit.
- L4 (MAJOR, open, single): The create steps do not specify that a present field with no matching option must produce `not set: field Complexity <value>: option not found`.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
