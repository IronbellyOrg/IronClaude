review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok false

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The manual-check path is ambiguous between repo-root artifacts/ and the package artifacts folder, and the repo-root reading falls outside the allowed edit roots and is never staged
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R1 (F3)

- claim: The owner manual check states no close or cleanup step, so following it leaves two real test issues open on the origin repo
- anchor: "file one test issue with `/sc:issue --create \"<short test description>\" --mode feature --type tests --depth standard` on `IronbellyOrg/IronClaude`"

#### L1.R1 (F4)

- claim: The cited commit 1aa2e5c3 is absent from this checkout, so line numbers cannot be re-read from that snapshot and only the live-file fallback works
- anchor: "Line numbers named in tasks come from the issue analysis on commit `1aa2e5c3` and must be re-read in the live file before each edit."

#### L1.R1 (F6)

- claim: Read strictly, the --repo <R> rule would rewrite the maintainer label lines, which name an arbitrary target repo, to the origin repo
- anchor: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."
- anchor2: "keep only the `bug` and `enhancement` lines in the maintainer block"

#### L1.R2 (F1)

- claim: The required manual-check artifact is outside the permitted edit scope, so the plan requires a write it forbids.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

## Other findings

- L2 (MAJOR, open, single): The new test as worded can be read to require -X POST in the read-only worker agents, contradicting the kept GET-only ban on those agents
- L3 (MINOR, open, single): Task 4 lists the scout headings in a different order than create.md Wave 1 states, with no behaviour depending on the order

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
