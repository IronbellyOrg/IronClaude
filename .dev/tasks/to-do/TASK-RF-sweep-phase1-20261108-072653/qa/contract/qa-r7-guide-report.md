# QA Report: routing row R7 lens (guide never-as-worker list vs WORKER-CONTRACT.md line 23)

**Date:** 2026-11-12
**Phase:** code gate, R7 lens (master-contract fidelity domain)
**fix_authorization:** false (only this report was written)

Scope: the developer-guide never-as-worker list at `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991` against `src/superclaude/core/WORKER-CONTRACT.md:23`, the revised DESIGN section 8 (`docs/designs/orchestrator-mode.md:703-707`) and row R7 (`docs/designs/orchestrator-mode.md:721`), and the evidence file `r7-check.md`.

## Findings

No BLOCKING or MAJOR finding. Two MINOR notes (never fail the gate).

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `r7-check.md:25-28` | The side-by-side table lists the eight commands before "plus" and leaves out `/sc:pr-submit`, which both lines name after "plus" (guide `:991`, contract `:23`). The full ordered sequence of nine is identical in both lines (C3), so this hides no mismatch. | Optional: add `/sc:pr-submit` as a trailing entry. |
| F2 | MINOR | guide `:991` against contract `:23` | Trailing clause wording differs: the guide says "while decision D3 keeps it off workers", the contract says "while the answer to decision D3 keeps it off workers". The same difference exists at HEAD (C5), so item 12.2 did not introduce it, and R7 asks for the command list and its order only. | None required. |

Observation, not a finding: no test reads the developer guide's list. `grep -rn 'Developer-Guide-Commands' tests` returns only `tests/docs/test_retired_docs_absent.py:26`, so R7 stays a manual check, as DESIGN row R7 says ("manual review against `WORKER-CONTRACT.md` line 23", `docs/designs/orchestrator-mode.md:721`). Only the contract side is pinned (`RULE_PHRASES["never-as-worker"]`, `tests/skills/test_worker_contract.py:86-92`).

## Evidence summary

- Order extracted from each file with `grep -o` (read from disk this run):
  - guide `:991`: `/sc:agent /sc:git /sc:help /sc:issue /sc:pm /sc:spawn /sc:sweep /sc:swarm-wizard /sc:pr-submit`
  - contract `:23`: the same nine, in the same order.
  - HEAD contract `:23` and HEAD guide `:991`: the same sequence without `/sc:sweep` (eight entries).
- Inserting `/sc:sweep` between `/sc:spawn` and `/sc:swarm-wizard` into the HEAD text of each line reproduces the current line byte for byte (`diff` printed `IDENTICAL_AFTER_SWEEP_INSERT` for both). So only `/sc:sweep` was added to either line, and nothing else on either line changed.
- `git diff --numstat` for the guide: `1 1`, one line replaced. In the contract diff, line 23 is one changed line (`-`/`+` pair); the other hunk is the WC-16 block, outside this lens.
- Contract line 23 is still a single line holding `**Never-as-worker list**` (count 1), which `_check_never_as_worker` (`tests/skills/test_worker_contract.py:775-780`) requires.
- DESIGN `:705` gives the target text of line 23. The current contract line equals the HEAD line plus the `/sc:sweep` insert, and the DESIGN text lists the commands in that same order with the same trailing sentences (compared by reading both lines).
- `r7-check.md` quotes the live guide line, the live contract line and the HEAD guide line verbatim (each matched exactly once with `grep -x -F -f`). Its table at `r7-check.md:27-28` shows the two lines side by side, with the verdict "equal" at `:30`.
- Test pins match the design (`git diff` of the test file): `NEVER_AS_WORKER` gained `"/sc:sweep"` as the ninth entry (`tests/skills/test_worker_contract.py:391-400`), the `never-as-worker` phrase at `:86-92` now includes `/sc:sweep` between `/sc:spawn` and `/sc:swarm-wizard`, the test was renamed to `test_never_as_worker_list_names_every_listed_command` (`:922`), and `assert "sweep" not in UNATTENDED_COMMANDS` was added (diff hunk at `:1331-1335`).
- Run this session: `uv run pytest tests/skills/test_worker_contract.py -q -k 'never or never_as_worker or load_usage or contract_states_rule'` gave 79 passed. `uv run ruff check` and `uv run ruff format --check` on the test file: both clean. `phase12-validation.md` (2008 passed for `tests/skills tests/core`) and `step-1.19-pytest.txt` (742 passed) agree.
- Order sensitivity of the pin, on a private `/tmp` copy only (deleted on exit; `ls /tmp/ironclaude-batch.*` printed 0 afterwards): swapping `/sc:sweep` and `/sc:swarm-wizard` makes the pinned phrase count go from 1 to 0, so a reordered contract line would fail the existing test. The guide has no such pin (observation above).
- No other guide location repeats the list: guide `:336`, `:394` and `:2203` point to the list without repeating it, and `HOW-WE-WORK.md:403` does not enumerate it. `src/superclaude/commands/sweep.md:16` says `/sc:sweep` is on the list, which is now true.

## Checks

| id | check | result |
|---|---|---|
| C1 | Guide `:991` and contract `:23` both read from disk now; both are single list lines | PASS |
| C2 | Same set of commands in guide and contract (nine each) | PASS |
| C3 | Same order in guide and contract | PASS |
| C4 | Only `/sc:sweep` added to the guide line (HEAD text plus one insert reproduces it) | PASS |
| C5 | Only `/sc:sweep` added to the contract line (same method); the pre-existing "D3" wording difference between the two lines is unchanged from HEAD | PASS (F2 note) |
| C6 | `/sc:sweep` position matches DESIGN `:705` and row R7 `:721` ("same order as section 8") | PASS |
| C7 | Guide diff is one line (1 insertion, 1 deletion) | PASS |
| C8 | `r7-check.md` quotes before, after and contract lines exactly as on disk | PASS |
| C9 | `r7-check.md` shows both lines side by side with an order verdict | PASS (F1 note) |
| C10 | Test pins (`NEVER_AS_WORKER`, `RULE_PHRASES["never-as-worker"]`, rename, `UNATTENDED_COMMANDS` assertion) match DESIGN section 8 and research/07 (d) | PASS |
| C11 | `uv run pytest` (79 selected tests), `ruff check`, `ruff format --check` | PASS |
| C12 | Mutation on a private copy (swap order) breaks the contract pin; temp copy removed | PASS |
| C13 | No other guide location repeats the list and needs the same edit | PASS |
| C14 | OQ-3 record is RESOLVED with the owner's decision (`OQ-3-GQ-11-rule-id-decision.md:3,36-39`), so steps 1.17 to 1.19 were not gated shut; OQ-1 is about `--agent-wait` and does not touch this list | PASS |

## Verdict

Verdict: PASS

Blocking count: 0

Confidence: Verified 14/14 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%
Tool engagement: Read: 9 | Grep: 2 | Glob: 1 | Bash: 8
Not checked: the WC-16 block, the other routing rows (R1 to R6, R8) and the full `tests/skills tests/core` run, which belong to other lenses.
