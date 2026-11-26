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
| L3 | open | no | single | MAJOR | - | R3 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: Verbatim keep violates the repo-flag rule; rewrite is only a guess the text allows
- anchor: "keep only the `bug` and `enhancement` lines in the maintainer block"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`"

#### L1.R1 (F2)

- claim: Artifacts write sits outside the stated edit scope; both readings are allowed
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`"
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package"

#### L1.R3 (F1)

- claim: An implementer who follows the stated text as written builds an issue with exactly two changes beyond the issue itself and omits the mode label, and that is wrong because the goal requires applying the mode label.
- anchor: "It writes exactly two things to a created issue besides the issue itself:"
- anchor2: "applies only the mode label (`bug` or `enhancement`)"

#### L1.R3 (F2)

- claim: An implementer who follows the stated text as written cannot both restrict edits to the listed directories and create the required owner manual-check file, so the acceptance criterion cannot pass without violating the scope constraint.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F1)

- claim: The required `make sync-dev` writes generated copies under `.claude/`, which the plan separately forbids editing.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R2 (F2)

- claim: Task 12 requires writing an artifact outside the plan's permitted edit paths.
- anchor: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F3)

- claim: The plan does not define a final-output reason when a type or field read-back command fails.
- anchor: "read-back with `gh api repos/<R>/issues/<N>/issue-field-values`"

## Other findings

- L2 (MINOR, open, single): Phrase is actually at line 333 and the return-contract test is at line 545, not 492 to 520; re-read rule covers it
- L3 (MAJOR, open, single): If a type or field read-back command fails, the plan does not specify a non-fatal outcome or final-output reason, so the required report <redacted> every classification it could not set is undefined.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
