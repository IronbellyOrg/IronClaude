# QA Report: test-pins lens (contract gate, item 12 pins)

**Topic:** the five pin edits in `tests/skills/test_worker_contract.py` for `/sc:sweep` (WC-16, never-as-worker, NEVER_AS_WORKER, renamed test, sweep assertion)
**Date:** 2026-11-12
**Phase:** task-integrity (code gate, test-pins lens)
**Fix cycle:** N/A (fix_authorization: false)

---

## Overall Verdict: PASS

No BLOCKING or MAJOR finding. All five pin edits match DESIGN section 8 (`docs/designs/orchestrator-mode.md:684-692`) and research/07 section (d). Base: `git rev-parse HEAD` is `5dc29d23b`, so `git diff HEAD` is the whole change against master. Zero findings is the result of the checks below, not a skipped review: every pin was also attacked with a mutation on a private /tmp copy (C12) and the master test file was run against the new contract (C9).

## Findings

None. Blocking count: 0.

Notes (not findings, no action):

- N1. DESIGN section 8 quotes line numbers taken on master (`RULE_PHRASES` entries :165-172 and :173, `NEVER_AS_WORKER` :382-391, the rename at :912, the load assertion at :1322). On disk they now sit at :173-181 (WC-16), :391-401, :922 and :1332 because the new lines shifted them. Section 8 says its anchors are read on master `5dc29d23`, so this is expected and is not a departure.
- N2. The DESIGN text still names the old test (`docs/designs/orchestrator-mode.md:688`) as the thing to rename. That is the instruction itself, so the hit is correct.

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | Exactly five edits, nothing else in the test file | PASS |
| C2 | `WC-16` entry: key, position, ident, four phrases | PASS |
| C3 | The four WC-16 phrases are verbatim in the contract and the heading line carries the ident | PASS |
| C4 | Exactly one `WC-14` key; no duplicate key in `RULE_PHRASES` | PASS |
| C5 | `never-as-worker` phrase names `/sc:sweep` and equals DESIGN section 8 and contract line 23 | PASS |
| C6 | `/sc:sweep` is the ninth `NEVER_AS_WORKER` entry, appended last, once | PASS |
| C7 | Test renamed, body unchanged, no stale reference to the old name | PASS |
| C8 | `sweep` assertion directly after the `load` assertion; `sweep` not in the unattended sets | PASS |
| C9 | No pin deleted or weakened (diff, master test vs new contract, test count 739 to 742) | PASS |
| C10 | `step-1.19-pytest.txt` shows the WC-16, never-as-worker and `/sc:sweep` removal cases PASSED and is newer than the edits | PASS |
| C11 | Fresh `pytest`, `ruff check`, `ruff format --check`, wider `tests/skills tests/core` | PASS |
| C12 | Mutations on private /tmp copies: every new pin detects its own removal | PASS |
| C13 | Supporting records agree (step-1.17 gate, OQ-3 gate, phase12 validation, r7 order) | PASS |

Confidence: Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 15 | Grep: 3 | Glob: 1 | Bash: 9 (read-only git/grep/stat, three pytest/ruff runs, two /tmp-copy experiments, both copies deleted)

## Evidence log

**C1. Five edits only.** `git diff HEAD -- tests/skills/test_worker_contract.py` shows five hunks: (1) `never-as-worker` phrase, (2) `WC-16` entry, (3) `NEVER_AS_WORKER` gains `"/sc:sweep"`, (4) test rename, (5) `sweep` assertion. `git diff 5dc29d23 --numstat` gives 14 added and 3 deleted lines for the test file; the 3 deleted are the two old phrase lines and the old `def` line. `HEAD` is `5dc29d23b`, so this is the diff against master.

**C2. WC-16 entry.** Read `tests/skills/test_worker_contract.py:165-189`: `"WC-15"` ends at :172, `"WC-16": ("WC-16", [` starts at :173 and ends at :181, `"heartbeats"` starts at :182. The four phrases at :176-179, in this order: `"WC-16. Coordinator loop"`, `"On every coordinator wake"`, `"it is never posted"`, `"It never stops watching on its own"`. DESIGN section 8 line 686 lists the same key, ident and four phrases in the same order. AST scan: neighbours of `WC-16` are `WC-15` and `heartbeats`.

**C3. Phrases in the contract.** `src/superclaude/core/WORKER-CONTRACT.md:275` is `### WC-16. Coordinator loop` (grep, one hit; fan-in heading :271, worked example :279). All four phrases are in the inserted paragraph (`git diff HEAD` on the contract). `_check_rule` (`tests/skills/test_worker_contract.py:765-772`) needs the ident on the first phrase's line; the heading satisfies it. A heading renamed to `WC-17` or `WC-14` in a /tmp copy fails the check (C12).

**C4. One WC-14 key.** `grep -n '"WC-14"' tests/skills/test_worker_contract.py` returns :156 and :157 only (the key and its ident inside one entry). AST scan of the `RULE_PHRASES` literal: 58 keys, duplicates: none, `WC-14` count 1, `WC-16` count 1. The WC-14 entry at :156-164 is untouched (no diff hunk covers it).

**C5. never-as-worker phrase.** `tests/skills/test_worker_contract.py:86-92`: the two string literals join to `` `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers ``. DESIGN section 8 line 690 asks for `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, ``; contract line 23 (`git diff HEAD` on the contract) carries the same list. The D3 clause is kept, so the pin is wider, not weaker.

**C6. Ninth entry.** Read `:391-401`: the tuple ends `"/sc:swarm-wizard"`, `"/sc:pr-submit"`, `"/sc:sweep"`, `)`. Loaded in a /tmp script: length 9, last item `/sc:sweep`, count of `/sc:sweep` is 1. The parametrized removal test (`:1091-1100`) covers it with no further change.

**C7. Rename.** `:922` is `def test_never_as_worker_list_names_every_listed_command():` with the body `_check_never_as_worker(_contract())` unchanged. `grep -rn names_all_seven_commands` outside `.dev/` and `.venv` finds only the DESIGN instruction line (`docs/designs/orchestrator-mode.md:688`); no test, doc or config still names the old function.

**C8. Assertion.** `:1328-1333`: `assert "--checkpoint <name>" in usage` (:1331), `assert "load" not in UNATTENDED_COMMANDS` (:1332), `assert "sweep" not in UNATTENDED_COMMANDS` (:1333), inside `test_load_usage_line_declares_checkpoint_and_load_is_not_converted`. Loaded module: `sweep` is in neither `UNATTENDED_COMMANDS` nor `UNATTENDED_EXPECT`, and `len(UNATTENDED_EXPECT)` is 31.

**C9. Nothing deleted or weakened.** (a) C1 numstat. (b) I copied the master test file (`git show HEAD:...`) to a private /tmp tree, pointed it at the new contract, and ran it: 739 collected, 738 passed, 1 failed: `test_contract_states_rule[never-as-worker]`, the case DESIGN section 8 line 692 says goes red until pin 5 changes. (c) Current file collects 742 = 739 + 3 (WC-16 positive, WC-16 removal, `/sc:sweep` removal). No other count change.

**C10. Pytest log.** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.19-pytest.txt`: line 16 `test_contract_states_rule[WC-16] PASSED`; line 54 `[never-as-worker] PASSED`; line 68 `test_never_as_worker_list_names_every_listed_command PASSED`; line 374 `test_rule_check_fails_when_rule_removed[WC-16] PASSED`; line 412 same for `never-as-worker`; line 450 `test_never_as_worker_check_fails_when_command_removed[/sc:sweep] PASSED`; line 470 the load test PASSED; footer line 753 `742 passed in 1.33s`. grep for SKIPPED, XFAIL, XPASS, FAILED and ERROR finds 0; 742 lines contain PASSED. mtimes: test file 07:13:39, contract 07:12:56, log 07:13:46, so the log was written after the last edit of both files.

**C11. Fresh runs.** `uv run pytest tests/skills/test_worker_contract.py -q`: 742 passed. `uv run ruff check tests/skills/test_worker_contract.py`: All checks passed. `uv run ruff format --check`: 1 file already formatted. `uv run pytest tests/skills tests/core -q`: 2008 passed (matches `phase12-validation.md:56`).

**C12. Mutations (private copies only, deleted afterwards; no repo file written).** Run through the test module's own `_check_rule` and `_check_never_as_worker` on altered contract text: each of the four WC-16 phrases removed alone: fails; heading renamed `WC-17`: fails; heading renamed `WC-14`: fails; `/sc:sweep` removed from line 23: fails both the rule check and the list check; `/sc:sweep` moved after `/sc:pr-submit`: fails the phrase pin (order is pinned); D3 clause removed: fails. Unmutated text passes all of them.

**C13. Supporting records.** `step-1.17-checks.md:7` gate (OQ-3 RESOLVED) agrees with `phase-outputs/plans/OQ-3-GQ-11-rule-id-decision.md:3` and `:36-37` (owner approves new WC-16 and the section 8 text). Its check 2 (no extra WC-14 heading) agrees with C4. `phase12-validation.md` ruff and 2008-passed blocks agree with C11; its `src/superclaude` count of 0 in the contract matches my grep (0). `r7-check.md:27-28` lists the guide and contract lists in the same order, and `git diff HEAD` on the guide shows the one-line change at :991. OQ-1 (`OQ-1-agent-wait-decision.md`) concerns the sweep's allowlist, not these pins, and no pin touches it.

Verdict: PASS
Blocking count: 0
