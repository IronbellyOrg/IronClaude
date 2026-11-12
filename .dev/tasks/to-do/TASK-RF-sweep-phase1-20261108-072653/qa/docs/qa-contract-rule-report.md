# QA Report: Contract-rule lens (docs gate)

**Topic:** /sc:sweep phase 1, WC-16 contract rule, pins and guide lists
**Date:** 2026-11-12
**Phase:** docs gate, contract-rule lens
**Fix authorization:** false (report only)
**Reviewer prompt:** qa/docs/prompts/T292-prompt.md

## Scope and method

Reviewed from the files on disk (read or diffed in this session): `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`, `docs/designs/orchestrator-mode.md` (the revised DESIGN) section 8 and rows R1-R8 of section 9, `research/07-reanchor-contract.md`, `OQ-3-addendum-wc16-wait-timeout-decision.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, `src/superclaude/core/HOW-WE-WORK.md` (R2 only), `src/superclaude/commands/sweep.md:20`, `CHANGELOG.md:13`. Comparisons used `cmp`, `git diff` against HEAD and private copies under `/tmp` (deleted afterwards). No repository file other than this report was written. The style file, the skill and the sweep test file were not reviewed beyond running their tests (outside this lens).

## Findings

No BLOCKING or MAJOR finding. Two MINOR notes (never fail the gate):

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR (Medium, follow-up candidate) | `tests/skills/test_worker_contract.py:173-181` pins only four WC-16 phrases; a search of `tests/` for "wait timeout" and "once every 5 minutes" finds only `test_worker_contract.py:221` (the contract line 110 sweep pin) | Nothing pins WC-16's own cadence clause ("at most once every 5 minutes") or the owner-approved "or wait timeout" wording, so a later edit could drop either without a red test. DESIGN section 8 (lines 682-690) and the OQ-3 addendum (line 21) both say no test pin changes, so this is as designed. | If the owner wants it, add the two phrases to `RULE_PHRASES["WC-16"]` in a later change. No action now. |
| F2 | MINOR (note) | `src/superclaude/core/HOW-WE-WORK.md:405` says "on every wake"; `src/superclaude/core/WORKER-CONTRACT.md:277` says "on every coordinator wake or wait timeout" | The routing bullet (R2) is a shorter paraphrase of WC-16's trigger. The OQ-3 addendum (line 27) keeps R2 as written by owner decision, and R2 text equals DESIGN row R2 (C18). | None. |

## Evidence per check

- C1: `sed -n '677,679p' docs/designs/orchestrator-mode.md` and `sed -n '275,277p' src/superclaude/core/WORKER-CONTRACT.md` compared with `cmp`: `BYTE_IDENTICAL`, 1855 bytes each. The DESIGN text already carries the owner-approved "or wait timeout" opening (OQ-3 addendum line 21).
- C2: contract lines 273 (fan-in paragraph), 275 (`### WC-16. Coordinator loop`), 277 (paragraph), 279 (`### Worked example: gate hit, answer, new Task`). `git diff -U0` shows the insertion as exactly `@@ -274,0 +275,4 @@`.
- C3: whole-word search for "lock" in line 277 returns 0. The only hits for the substring are inside "blocked" and the existing term "a frozen plan" (contract line 250 defines it). No sentence freezes or locks the text.
- C4: `cmp` of line 110 and of line 151 against `git show HEAD:` for both: identical. The diff touches only two hunks (line 23 and the +4 insertion). `RULE_PHRASES["liveness-sweep-and-states"]` (test line 221 area) and its sibling pass in the full run.
- C5: `diff` of all `WC-14` lines against HEAD: identical (the chain lines moved from 289 to 293 only because of the 4 inserted lines). Removing line 23 from HEAD and lines 23 and 275-278 from the working file leaves the two files identical (`OUTSIDE_HUNKS_IDENTICAL`).
- C6: word diff of line 23: `/sc:spawn` becomes `/sc:spawn`, `/sc:sweep`; nothing else. It matches DESIGN section 8 line 705. It is still one term line (`_check_never_as_worker`, test line 775, passes).
- C7: `tests/skills/test_worker_contract.py:173-181` sits after `"WC-15": (` (165) and before `"heartbeats": (` (182), as DESIGN line 686 and research/07 line 142 require. All four phrases occur verbatim in contract lines 275 and 277.
- C8: `NEVER_AS_WORKER` (line 391) now has 9 entries, `"/sc:sweep"` at line 400.
- C9: line 922 is `test_never_as_worker_list_names_every_listed_command`; the body is `_check_never_as_worker(_contract())`, unchanged. The old name is gone from the file.
- C10: lines 1332-1333 hold the `"load"` assertion and the new `"sweep"` assertion.
- C11: lines 89-90 join to "`/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers", a substring of contract line 23; `test_contract_states_rule[never-as-worker]` passes.
- C12: `git diff -U2` of the test file has exactly five hunks (lines 87, 171, 389, 910, 1321 of the old file), one per pin in DESIGN lines 686-690; no other edit. `git diff --stat`: 17 lines changed in the test file.
- C13: `grep -c '^    "WC-14": ('` returns 1, and the same for `"WC-16": (`.
- C14: 31 top-level keys between lines 448 and 755; no `"sweep"` key; the test-file diff holds no `UNATTENDED_EXPECT` change; `_check_p2_set` asserts 31 at line 1575 and passes.
- C15: line 23 list and developer guide line 991 list (extracted and `cmp`ed): identical, `LIST_IDENTICAL`. No other copy of the list exists outside `.dev/` (the one extra copy is under `.venv/.../site-packages`, an untracked stale install).
- C16: `uv run pytest tests/core tests/commands tests/recommend tests/skills -q`: 2641 passed. `tests/skills/test_worker_contract.py` alone: 742 passed. `uv run ruff check` and `ruff format --check` on the four test files: clean.
- C17: WC-16 says `/sc:sweep` does not run `worktree ps --agent-wait` or update heartbeats. `src/superclaude/cli/sweep/probes.py:56-57` lists the listing as allowed, "not called"; a search of `src/superclaude/cli/sweep` finds no heartbeat write. The claim holds.
- C18: Owner-approved changes present: WC-16 opening "On every coordinator wake or wait timeout" (contract line 277, DESIGN line 679); `sweep.md:20` carries "inside its liveness sweep pass, at most once every 5 minutes (WC-16 ...)". R2 text in `HOW-WE-WORK.md:405` equals DESIGN row R2 (line 716) apart from the table quoting; `cmp` of `src/superclaude/core/HOW-WE-WORK.md` and the plugin copy: identical. `CHANGELOG.md:13` states WC-16 and the 5-minute cap and the never-as-worker entry.
- C19: `test_rule_check_fails_when_rule_removed` is parametrized over `RULE_PHRASES` (test line 1054) and `test_never_as_worker_check_fails_when_command_removed` over `NEVER_AS_WORKER` (line 1091), so pins 1 and 2 have negative tests with no further change.
- C20: no remaining "seven commands" or similar count wording tied to the never-as-worker list in `src`, `docs`, `tests` or `plugins`.

## Checks

| id | check | result |
|---|---|---|
| C1 | WC-16 byte-identical to revised DESIGN section 8 final text | PASS |
| C2 | WC-16 sits between the fan-in paragraph and the worked example | PASS |
| C3 | WC-16 adds no lock sentence | PASS |
| C4 | Contract lines 110 and 151 not reworded | PASS |
| C5 | No existing WC-14 reference reworded; no change outside the two hunks | PASS |
| C6 | Line 23 changed only by adding `/sc:sweep` | PASS |
| C7 | Pin 1: `RULE_PHRASES["WC-16"]` content and position | PASS |
| C8 | Pin 2: `NEVER_AS_WORKER` has 9 entries with `/sc:sweep` | PASS |
| C9 | Pin 3: test renamed, body unchanged | PASS |
| C10 | Pin 4: `"sweep" not in UNATTENDED_COMMANDS` beside `"load"` | PASS |
| C11 | Pin 5: never-as-worker phrase matches new line 23 | PASS |
| C12 | Exactly five pin edits, no extra test edit | PASS |
| C13 | Only one `"WC-14"` key (and one `"WC-16"` key) | PASS |
| C14 | `UNATTENDED_EXPECT` still 31 entries, `sweep` absent | PASS |
| C15 | Developer-guide list matches line 23 | PASS |
| C16 | Tests and ruff pass (2641 passed) | PASS |
| C17 | WC-16 claims about sweep agree with the CLI | PASS |
| C18 | Owner-approved changes present; R2 and HOW-WE-WORK parity | PASS |
| C19 | Pins 1 and 2 have negative tests | PASS |
| C20 | No stale count wording for the list | PASS |

Confidence: Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 8 | Grep: 5 | Glob: 0 | Bash: 11

Self-audit: a zero-blocking result is backed by byte comparisons (`cmp`) of the rule text, HEAD comparisons of lines 110, 151 and every WC-14 line, a whole-file diff showing nothing changed outside the two hunks, and a full test run. Not checked (outside this lens): the style file, the skill text and `tests/commands/test_sweep_command.py` content.

Verdict: PASS

Blocking count: 0
