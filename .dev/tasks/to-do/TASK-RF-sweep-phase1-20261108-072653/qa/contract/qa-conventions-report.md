# QA Report - Conventions Lens (WC-16 and pin edits)

**Date:** 2026-11-12
**Phase:** doc-qualitative (conventions lens), gate folder qa/contract
**Fix authorization:** false

## Findings

All findings are MINOR. No BLOCKING or MAJOR finding. Files read from disk now: `src/superclaude/core/WORKER-CONTRACT.md` (lines 60-64, 71-79, 99-168, 236-287), `tests/skills/test_worker_contract.py` (lines 40-268, 380-420, 765-781, 1086-1115, 1318-1338), the guide (line 991), `docs/designs/orchestrator-mode.md` (lines 684-710), `src/superclaude/commands/sweep.md` (lines 10-17). Also `git diff` of the three files and `git show HEAD:` headings of the master contract (WC-14 and WC-15 are bullets at master lines 63-64; `### WC-6.` at master line 71 is the only other `### WC-n.` heading).

Note: the WC-16 paragraph is byte-identical to DESIGN section 8 (`grep -F` of contract line 277 in `docs/designs/orchestrator-mode.md` gives 1 match; DESIGN heading at line 677). The pin positions, the list order and the extra assertion are also what DESIGN lines 686-690 and 705 prescribe. Fixes below would therefore need a DESIGN edit first.

| id | severity | evidence | what departs | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `WORKER-CONTRACT.md:277` vs `:73-79` and `:60-64` | WC-16 is one paragraph of 299 words and 17 sentences. The only other `### WC-n.` rule (WC-6) is a 77-word intro (`:73`) plus five bullets (`:75-79`); the bullet rules WC-12 to WC-15 are 52-86 words each (`:61-64`). | Split WC-16 into a short intro and bullets (loop duty; added read; escalation list; what the report never does). |
| F2 | MINOR | `WORKER-CONTRACT.md:277` vs `:91` and `:243` | Other cross-references to a section name it in double quotes with no `###` and no inner period: "Feature worktree and child worktrees" (`:91`), "After an `/sc:implement` stop" (`:243`). WC-16 writes `"The sweep." under `### Liveness supervision``. "The sweep." is a bold run-in label (`:110`), not a heading. | Write: runs the sweep in "Liveness supervision" (the paragraph that starts "The sweep."). |
| F3 | MINOR | `WORKER-CONTRACT.md:277` vs `:89`, `:23` | "Phase 1 adds this duty, not a scheduler." spells out the phase. The contract writes phases as P0/P1 (`:89` "at P0 only") and says the list changes "never per phase" (`:23`). A phase-dated sentence inside a standing rule will go stale. | Delete the sentence, or write "at P1". |
| F4 | MINOR | `WORKER-CONTRACT.md:277` vs `:76`, `:241` | `/sc:sweep` class names (`stalled`, `could not determine`) are plain text. State and outcome values elsewhere are in backticks (`unverifiable` `:76`, `succeeded` `:241`). `sweep.md:14` also writes them as plain prose, so this is arguable. | Backtick both names, or leave. |
| F5 | MINOR | `WORKER-CONTRACT.md:23`, `test_worker_contract.py:89-90`, guide `:991`; tuple `test_worker_contract.py:391-401` | The list was alphabetical (agent, git, help, issue, pm, spawn, swarm-wizard). `/sc:sweep` was put before `/sc:swarm-wizard`, but "swarm-wizard" sorts before "sweep" (a < e). In `NEVER_AS_WORKER` it was appended after `/sc:pr-submit` (`:400`), so the tuple order no longer follows the sentence order. | Order `/sc:swarm-wizard` then `/sc:sweep` in the three sentences (and in the pin). |
| F6 | MINOR | `test_worker_contract.py:173-181` vs `:130`, `:189-198` | The WC-16 pin sits under the `# Worker-session duties` comment (`:130`), between WC-15 and `heartbeats`. WC-6, the other coordinator rule, sits under `# Coordinator rules` (`:189`, `:190-198`). DESIGN `:686` prescribes this spot. | Move the entry under `# Coordinator rules` after `"WC-6"`. |
| F7 | MINOR | `test_worker_contract.py:1328-1333` | `assert "sweep" not in UNATTENDED_COMMANDS` is added to `test_load_usage_line_declares_checkpoint_and_load_is_not_converted`, so the test name no longer describes it. Every neighbouring test is single-purpose. DESIGN `:689` prescribes it. | Put it in its own short test, or rename the test. |
| F8 | MINOR | `WORKER-CONTRACT.md:277` vs `:110` | The trigger is "On every coordinator wake, at most once every 5 minutes", but the existing sweep rule says "After every wake or timeout, at most once every 5 minutes" (`:110`). Two phrasings for one trigger. | Use "After every wake or timeout" in WC-16 (the pin phrase "On every coordinator wake" would change too). |

Pins that follow their neighbours (no finding): heading `### WC-16. Coordinator loop` has the same form as `### WC-6. Every retry is a new Task` (`:71`, `:275`); the pin tuple is `("WC-16", [four phrases])` with the heading text first, as in `"WC-6"` (`test_worker_contract.py:190-198`: first phrase `"WC-6. Every retry is a new Task"`); double quotes as in the neighbours; the `never-as-worker` phrase keeps the two-string implicit concatenation of the old entry and `ruff format --check` accepts it.

## Checks

| id | check | result |
|---|---|---|
| C1 | WC-16 heading form matches `### WC-6.` (number, period, sentence-case title, no trailing period) | PASS |
| C2 | WC-16 body shape and length against WC-6 and WC-12 to WC-15 | FAIL (F1, minor) |
| C3 | Cross-reference quoting against `:91` and `:243` | FAIL (F2, minor) |
| C4 | Vocabulary: phase naming and the sweep trigger wording | FAIL (F3, F8, minor) |
| C5 | Formatting of class and state names | FAIL (F4, minor) |
| C6 | WC-16 pin tuple shape, quoting, ident and first phrase against the WC-6 pin | PASS |
| C7 | WC-16 pin placement under the right section comment | FAIL (F6, minor) |
| C8 | `never-as-worker` pin keeps the old entry's string layout; ruff format accepts it | PASS |
| C9 | Order of `/sc:sweep` in the list sentences and the `NEVER_AS_WORKER` tuple | FAIL (F5, minor) |
| C10 | Test rename and the added assertion fit their neighbours | FAIL (F7, minor; rename itself PASS) |
| C11 | Tooling: `uv run ruff check` and `ruff format --check` on the test file clean; `uv run pytest tests/skills/test_worker_contract.py -q` gives 742 passed | PASS |
| C12 | Guide line 991 wording equals contract line 23 wording | PASS |
| C13 | WC-16 paragraph equals DESIGN section 8 text (`grep -F` match count 1) | PASS |
| C14 | No stale "seven commands" wording left in the contract, test or guide (`grep` no hits) | PASS |

## Self-Audit

- Inherited structural verdict: none was given in the prompt, so I did no reliance and re-checked everything myself.
- Independent checks: 12 Read calls, 7 Grep calls, 5 Bash calls (diff, word counts, DESIGN match, ruff, pytest). Not run: Tavily (no external lookup needed).
- A zero-blocking result is stated with its basis: every WC-16 claim in the lens (form, length, quoting, pins, list order) was compared line by line with WC-6, WC-12 to WC-15 and the neighbouring `RULE_PHRASES` entries; the eight departures found are style only and do not change any rule's behaviour.
- Not checked (outside the conventions lens): whether WC-16 is behaviourally right, and the `sweep.md` / skill text.
- No file other than this report was written. The only temporary file (`/tmp/wc16-line.txt`) was deleted.

Verdict: PASS
Blocking count: 0
