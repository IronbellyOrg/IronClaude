review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 9f610e5d808c275bde4f84a63cf17ff433dad6004e81609f02e3953c7c7c9df8
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R2, R3, R1 |
| L2 | open | no | single | MINOR | - | R2 |
| L3 | open | yes | overlap | MAJOR | - | R2, R3 |

## Blocking findings

### L3

#### L3.t2b-1 (F7)

- claim: Source requires the Tool Coordination bullet to name the seven codegraph tools; the check words it as referring to the grounding rules, which is weaker than naming the tools.
- anchor: "Behavioral Flow steps 1 and 4 and the Tool Coordination section each refer to the codegraph grounding rules"

#### L3.t3-1 (F1)

- claim: The candidate allows completion with a failing named test, although the source requires all four test files to pass.
- anchor: "The four named test files pass with `uv run pytest`, or any failure is shown in `./artifacts/t2-checks.log` and is not attributable to `design.md`."

## Other findings

- L1 (MAJOR, open, overlap): Source adds that design is read-only against the index so there is no re-check after writing; candidate omits that sentence, though its one-check rule covers the same outcome.
- L2 (MINOR, open, single): Source states output gains only the Grounding line and no agent is spawned so no brief carries state; candidate relies on the goal line and omits both statements.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
