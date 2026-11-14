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
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |

## Blocking findings

### L1

#### L1.R1 (F1)

- claim: The Task 10 criterion fails on a correct design doc because the claim-mode lookup `gh api user -q .login` (docs/designs/sc-issue-command.md:157) is a gh api path that is neither repos/<R>/ nor the orgs read, and the plan's own rule keeps `user` legal.
- anchor: "Every `gh api` path in the file spells `repos/<R>/...` except the one documented `orgs/<owner of R>/issue-fields` read."
- anchor2: "every `gh api` path stays `user` or `repos/<R>/...`"

#### L1.R1 (F2)

- claim: Copying the shorthand `gh issue create ...` forms into SKILL.md or create.md without --repo turns the live fork-safety scan red.
- anchor: "add the field POST and `gh issue create ... --type <name>` to the orchestrator's write list"
- anchor2: "Every `gh issue`, `gh pr` and `gh label` line written into the skill, refs or agents carries `--repo <R>`."

#### L1.R1 (F4)

- claim: The skill also applies the mode label and posts the pushback comment, so the 'exactly two things' sentence is literally false.
- anchor: "It writes exactly two things to a created issue besides the issue itself"
- anchor2: "pushback comment; final output with every `not applied` and `not set` line"

#### L1.R1 (F5)

- claim: The source note that labels_applied and labels_missing now describe the mode label only is not carried into Task 3.
- anchor: "keep the first block key for key and the claim block unchanged"

#### L1.R1 (F7)

- claim: Task 12 writes package artifacts outside the paths the edit constraint lists, without saying they are exempt.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R3 (F1)

- claim: The plan forbids edits under `.claude/` while requiring a sync that writes development copies there.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`"
- anchor2: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`"

#### L1.R3 (F2)

- claim: The plan requires posting a pushback comment while limiting writes to the issue to exactly two items besides issue creation.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment"

#### L1.R3 (F3)

- claim: The instruction calls the owner check a single check but also directs a second run in bug mode.
- anchor: "the single manual check the owner runs after merge"

#### L1.R2 (F1)

- claim: The plan both forbids editing outside its listed directories and requires writing the manual-check artifact under `./artifacts/`.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."
- anchor2: "Then write `./artifacts/owner-manual-check.md` in this package."

#### L1.R2 (F2)

- claim: The plan requires `make sync-dev` while prohibiting edits to the `.claude/` copies that the sync updates.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

#### L1.R2 (F3)

- claim: The plan requires a mode label and a possible pushback comment in addition to the issue type and Complexity field, contradicting its exactly-two-writes limit.
- anchor: "It writes exactly two things to a created issue besides the issue itself: the issue type (through `gh issue create --type`) and the Complexity field value (through one POST)."
- anchor2: "pushback comment"

#### L1.R2 (M1)

- claim: Task 12 requires saving verification outputs to a log but does not instruct the implementer to capture them.
- anchor: "Run `make sync-dev`, then `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_issue_protocol.py -v`; fix any failure at its source in `src/superclaude/`, never by editing `.claude/`."

## Other findings

- L2 (MAJOR, open, single): The row text Task 6 asks for contains the `type: <value>` string that the same task's criterion says must be absent.
- L3 (MINOR, open, single): Live line numbers differ (HOW-WE-WORK row at 333, return-contract test at 545-573); only the constraint to re-read them keeps this harmless.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report <redacted> byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
