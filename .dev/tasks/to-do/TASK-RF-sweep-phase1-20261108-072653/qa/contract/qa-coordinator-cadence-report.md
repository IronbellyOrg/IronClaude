# QA Report: Coordinator-cadence lens (contract gate, T269)

**Date:** 2026-11-12
**Phase:** adversarial review, fix_authorization false
**Lens:** WC-16 vs `### Liveness supervision` cadence; OQ-1 reflected where `worktree ps` is named

## Findings

Verdict basis: one blocking-class finding (F1, graded MAJOR). F2 to F4 are MINOR notes.

### F1 (MAJOR): `sweep.md` tells a coordinator to run `/sc:sweep` "on every wake", with no 5-minute cap

- Evidence: `src/superclaude/commands/sweep.md:20`: "Explicit only: the coordinator runs `/sc:sweep` on every wake, or a person types it."
- Against it: `src/superclaude/core/WORKER-CONTRACT.md:277` (WC-16): "On every coordinator wake, at most once every 5 minutes, the coordinator runs "The sweep." ... and, in the same pass, runs `/sc:sweep`"; `WORKER-CONTRACT.md:110`: "at most once every 5 minutes"; DESIGN row R2 (`docs/designs/orchestrator-mode.md:716`): "on every wake, at most once every 5 minutes, beside "The sweep."".
- Why a coordinator acts wrongly: `sweep.md` is the file the coordinator loads each time it types `/sc:sweep`. It carries the rule without the cap and without the link to "The sweep.". The wait lists `heartbeat` in `--types` (`WORKER-CONTRACT.md:101`), so every worker heartbeat wakes the waiter. A coordinator following `sweep.md` runs the sweep (several Orca reads and one new report file under `.dev/sweeps/`) on every heartbeat, many times in 5 minutes, which WC-16 and line 110 forbid. The contract and the command file therefore give two different cadences for the same action.
- Not pinned: no test asserts the `sweep.md` Triggers wording (grep for `every wake` in `tests/` hits only the WC-16 pin, `tests/skills/test_worker_contract.py:177`), so nothing would catch it.
- Smallest fix: in `src/superclaude/commands/sweep.md:20` replace "the coordinator runs `/sc:sweep` on every wake" with "the coordinator runs `/sc:sweep` inside its liveness sweep pass, at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`)". Then run `make sync-dev` so the `.claude/` copy follows.

### F2 (MINOR): WC-16 says "wake"; line 110 says "wake or timeout"

- Evidence: `WORKER-CONTRACT.md:110` "After every wake or timeout"; `WORKER-CONTRACT.md:101` waits `--timeout-ms 300000`; `WORKER-CONTRACT.md:277` "On every coordinator wake" and, separately, "When a wait on Orca expires, the coordinator re-arms it."
- A coordinator that reads an expired wait as "not a wake" would re-arm and skip both sweeps, which is the silent case supervision exists for. The word "unchanged" in WC-16 points back to line 110, so a careful reader resolves it; this is an ambiguity, not a proven contradiction. The text was approved by the owner (OQ-3, 2026-11-09), so a wording change needs the owner.
- Smallest fix: "On every coordinator wake or wait timeout, at most once every 5 minutes". I tested this on a private copy: all WC-16 and liveness pins still pass (the pinned phrase `On every coordinator wake` is still a substring).

### F3 (MINOR): "a ready Task it did not create, needing ownership review" can be read as two escalation triggers

- Evidence: `WORKER-CONTRACT.md:277` list: "a ready Task it did not create, needing ownership review, a frozen plan"; `src/superclaude/cli/sweep/classify.py:245` marks every ready Task "creator not observable; needs ownership review", and `report.py:283` prints that heading for all of them.
- A coordinator could escalate every ready Task the report lists, including its own. `WORKER-CONTRACT.md:246` limits the duty to Tasks it did not create, which the coordinator knows from its run notes. Low impact (over-escalation, no unsafe action).
- Smallest fix: "a ready Task it did not create (the report lists every ready Task as needing ownership review)".

### F4 (MINOR): the cadence clause of WC-16 is not pinned

- Evidence: on a private copy with `, at most once every 5 minutes,` removed from line 277, `_check_rule` for `WC-16`, `liveness-sweep-and-states` and `liveness-ladder-and-restart` all passed. DESIGN D6 says "No new pin" (`docs/designs/orchestrator-mode.md:833`), so this is by design.
- Note only. A later edit could drop the cap and F1 would become silent.

### OQ-1 (no finding)

`worktree ps --agent-wait` appears in the contract in two places: `WORKER-CONTRACT.md:110` (the sweep runs it) and `:277` (`/sc:sweep` does not run it). The OQ-1 record (`phase-outputs/plans/OQ-1-agent-wait-decision.md:19-23, 42`) allows the command, leaves line 110 unedited, and says Phase 1 never runs the two `--agent-wait` templates. Both contract mentions agree with that. `/sc:sweep` takes `agentWait` from `worker-show` (`src/superclaude/cli/sweep/classify.py:227-230`, `probes.py:424-437`), and the two templates are in the allowlist as "allowed by R5, not called" (`probes.py:56-57`). No contract, guide or command text still says `--agent-wait` is forbidden. The older review files `docs/designs/orchestrator-mode-review-1.md:101`, `-2.md:102` and `-3.md:78` still say it is forbidden; they are dated review records, not coordinator-facing text.

## Method notes

- Files read from disk now: `WORKER-CONTRACT.md` lines 1-331 in chunks of at most 150; the contract diff (two hunks only: line 23 and the new WC-16 block); DESIGN lines 649-731; research/07 lines 94-173; OQ-1 and OQ-3 records; `step-1.17-checks.md`, `r7-check.md`, `phase12-validation.md`, tail of `step-1.19-pytest.txt`; `sweep.md` lines 1-80; `sc-sweep-protocol/SKILL.md` lines 1-60; `report.py` 25-60.
- `uv run pytest tests/skills/test_worker_contract.py -q`: 742 passed. `uv run ruff check` and `uv run ruff format --check` on the test file: clean.
- Experiment on a private `/tmp` copy of the contract (deleted afterwards, repository untouched): removing the WC-16 cadence clause passes every pin (F4); the F2 fix keeps every pin green.
- The inserted WC-16 text is byte-identical to the DESIGN block: `md5sum` of `WORKER-CONTRACT.md:277` equals that of `docs/designs/orchestrator-mode.md:679`.

## Checks

| Check | What | Result |
|---|---|---|
| C1 | WC-16 text equals the DESIGN section 8 block (md5 of contract:277 and design:679 match) | PASS |
| C2 | WC-16 cadence ("at most once every 5 minutes") equals line 110's cap | PASS |
| C3 | WC-16 says `/sc:sweep` is added beside the line 110 sweep, "unchanged", not a replacement, not a second pass, no heartbeat update | PASS |
| C4 | WC-16 trigger ("every coordinator wake") matches line 110 trigger ("every wake or timeout") | FAIL (MINOR, F2) |
| C5 | L1 carve-out in WC-16 is consistent with line 110 (costly probes only for triggered workers) and the L1 row (line 151) | PASS |
| C6 | Never-as-worker line (contract:23) matches the revised DESIGN section 8 text (design:705); only `/sc:sweep` added, term stays one line | PASS |
| C7 | No other coordinator-facing text gives a different cadence for `/sc:sweep` (contract, `sweep.md`, skill, guide, HOW-WE-WORK) | FAIL (MAJOR, F1) |
| C8 | OQ-1 reflected where the text names `worktree ps` (contract:110, contract:277, `probes.py:56-57`, `classify.py:227-230`) | PASS |
| C9 | OQ-3 decision (WC-16 id, section 8 text approved 2026-11-09) matches what was inserted; WC-14 and WC-15 untouched (diff has two hunks) | PASS |
| C10 | WC-16 escalation list matches contract:244, :246, :250, :273 and the report's ownership-review heading | FAIL (MINOR, F3) |
| C11 | Test pins and lint: 742 passed; ruff clean | PASS |
| C12 | Pin coverage of the WC-16 cadence clause | FAIL (MINOR, F4; by design D6) |
| C13 | Guide diff (line 991) adds only `/sc:sweep` in the same order as contract:23; no cadence text | PASS |
| C14 | WC-16 never lets the coordinator treat `/sc:sweep` output as a stall proof or action (WC-10, "Never on silence", contract:46, :182-192) | PASS |

Verdict: FAIL
Blocking count: 1
