review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | CRITICAL | 2.3, 3.1, 3.2 | R2 |
| L2 | open | no | single | MAJOR | 2.3 | R2 |
| L3 | open | no | single | MINOR | 3.1 | R2 |
| L4 | open | no | single | MAJOR | 3.4 | R2 |
| L5 | open | no | single | MINOR | 3.1 | R2 |
| L6 | open | no | single | MAJOR | - | R3 |
| L7 | open | yes | overlap | MAJOR | - | R3, R1 |

## Blocking findings

### L7

#### L7.t3-1 (F-SCOPE)

- claim: The candidate permits documentation and plugin edits despite the source’s src-only instruction; the source also lists those files as targets, so the scope conflict needs clarification.
- anchor: "Edit only under `src/superclaude/`, `tests/`, `docs/` and `plugins/superclaude/skills/sc-recommend/refs/`."

#### L7.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds synced source copies under `.claude/`, violating the same plan's explicit prohibition on editing that directory.
- anchor: "Never edit or stage anything under `.claude/` except `.claude/settings.json`; run `make sync-dev` after the `src/superclaude/` edits."

## Other findings

- L1 (CRITICAL, open, single): Task 8 requires agents to contain -X POST while Task 5 keeps the T3 worker read only, so an agent that follows Task 8 breaks the worker write ban.
- L2 (MAJOR, open, single): Task 3 adds the same exception to the SKILL.md call rule that test_worker_contract.py pins verbatim, so that second needle also fails with no owned fix.
- L3 (MINOR, open, single): Task 4 changes only the template, leaving refs/create.md line 36 saying not silently relabelled, so the ref and template state different wording.
- L4 (MAJOR, open, single): The Task 12 artifacts path is outside the only-allowed edit set and ambiguous between the package artifacts folder and the never-staged root artifacts folder.
- L5 (MINOR, open, single): The -k selector matches function names, so the routing table and claude block mirror tests are not selected by the stated command alone.
- L6 (MAJOR, open, single): The manual-check guide directs the owner to file a second test issue even though the source requires one manual check.

## Reviser brief

Blocking finding ids: L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
