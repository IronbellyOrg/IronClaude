review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R3: report <redacted> block ok true
- R2: report <redacted> block ok true
- R1: report <redacted> block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R3 (F1)

- claim: The developer-guide instruction excludes `inherit` even though the required alias policy test permits it.
- anchor: "so it says `model:` is an alias unless the agent is an allow-listed issue worker"
- anchor2: "Define ALIASES = opus, sonnet, haiku, inherit"

#### L1.R2 (F1)

- claim: The policy test does not specify checks for model-selection forms in primitive text other than frontmatter model values and full IDs passed to model flags.
- anchor: "When a `model:` line is present in the frontmatter of a file in src/superclaude/agents/*.md, src/superclaude/skills/*/SKILL.md or src/superclaude/commands/*.md, its value is in ALIASES, except the all"

## Other findings

- L2 (MAJOR, open, single): The literal src-only wording forbids the docs and tests edits the tasks require; the tasks resolve it but the wording should say so.
- L3 (MINOR, open, single): The probe file is not present in this checkout, so the new link may dangle until the issue artefacts are tracked.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
