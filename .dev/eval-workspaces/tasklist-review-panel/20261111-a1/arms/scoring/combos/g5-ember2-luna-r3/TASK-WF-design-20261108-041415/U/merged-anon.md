review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | yes | overlap | MAJOR | - | R1, R2, R3 |
| L5 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Task 10 AC cannot pass without breaking the design doc's `gh api user` lookup that Task 2 explicitly allows.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

### L4

#### L4.R1 (M3)

- claim: Task 12 writes outside the allowed edit dirs; whether package artifacts are exempt is unstated.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L4.R2 (F2)

- claim: Task 12 artifacts path is not in the edit-only list and ./ is unspecified, so the implementer must guess root versus package artifacts.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."
- anchor2: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L4.R3 (F1)

- claim: Task 12 requires files under `artifacts/`, outside the allowed edit paths, so an implementer cannot satisfy both the scope constraint and the required deliverables.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L4.R3 (F2)

- claim: The required sync copies source edits into `.claude/`, which the same plan explicitly forbids editing.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`;"

## Other findings

- L2 (MAJOR, open, overlap): Read per-file, the Task 8 test forces -X POST into the read-only T3 worker, contradicting Task 5; read collectively it is harmless.
- L3 (MAJOR, open, overlap): Read literally, the Task 1 AC deletes the two required maintainer gh label create lines; read as 'for either kind' it does not.
- L5 (MINOR, open, single): Scout Complexity field format conflates not found and lookup failed, making the exact not set reason ambiguous.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
