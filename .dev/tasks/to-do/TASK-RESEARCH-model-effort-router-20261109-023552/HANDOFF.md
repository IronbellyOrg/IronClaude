# HANDOFF: issue 463 research task (read this first)

**Written:** 2026-11-15, by the executing Claude session `issue-463-1112-221823-683d`.
**Audience:** any agent or human with no prior context. You do not need the chat history; everything load-bearing is on disk and listed below.
**Branch / base:** `ironbelly/issue-463`, based on `933cf3a4f`. Worktree: `/home/coder/workspaces/worktrees/IronClaude/issue-463`.

## 1. What this is, in plain terms

GitHub issue #463 on `IronbellyOrg/IronClaude` asks whether an "intelligent model-plus-effort router" is feasible for `ccsession` (the launcher that picks which Claude model and effort level a session uses). This is a **research-only** task: produce one evidence-backed report, `RESEARCH-REPORT-model-effort-router.md`, in this folder. **No implementation is authorized.** Two things must be preserved by any future design: explicit user model/tier/effort choices, and issue #462's user-configured Coder-role default.

The research was packaged as an MDTM task file (a long checklist run by the `/task` skill's read-identify-execute-update loop). It has heavy built-in quality gates: every artifact is written stub-first, every producer is followed by an independent verifier, and each worker may read at most 1000 lines in its lifetime.

## 2. Where it stands (verified from disk on 2026-11-15)

| Piece | State |
|---|---|
| Task file `TASK-RESEARCH-model-effort-router-20261109-023552.md` | 128 checklist items: **8 done, 120 not done**. Status set to Blocked. |
| Phase 1 item 1.1 (preparation) | DONE. Needed 6 extra bootstrap items (prep digests + reconciliation, all independently PASS); inventory `qa/input-bindings.md` created. |
| Phase 1 item 1.2 (measure and allocate source) | DONE: manifest `qa/local-source-allocation.md` (now v2, 42 planned slices over 18 files, 16,719 lines). |
| Phase 1 item 1.3 (independent check of the allocation) | **HALTED.** Cycle 1: 4 of 5 topic checks FAIL (one launch failure). Manifest corrected to v2. Cycle 2: **all 5 FAIL**, 14 blocking findings. |
| Research itself (source slices, findings, synthesis, report) | **NOT STARTED.** Zero source files have been investigated. The report does not exist. |
| Code / tests / config | Untouched. No product change was made. |

## 3. Why it is halted

The task's gate rules (task file lines 136-138) say: if the failing set does not shrink between cycles, HALT with `[HALT-MONOTONICITY] |F|=<n>`. The set of failing allocation checks was {2.1, 2.2, 2.4, 2.5} in cycle 1 (2.3 never ran) and is {2.1, 2.2, 2.3, 2.4, 2.5} in cycle 2, so `[HALT-MONOTONICITY] |F|=5`. By raw finding count it went 13 to 14. Topics 2.2 and 2.4 improved (4 to 2 each); 2.1 and 2.5 did not shrink (3 to 3, 2 to 3). No regression rule fired (nothing passed in cycle 1). The executor may not continue past this halt without an owner ruling: see `OPEN-DECISIONS.md`, decision D1.

Important: the verifiers confirmed the line-coverage unions are correct. The 14 findings are about **boundaries cutting tests mid-body, estimated rather than measured context budgets, and obligations mapped to the wrong slice**. They are mechanical, not disagreements about the research design.

## 4. Reading order for a newcomer

1. This file, then `OPEN-DECISIONS.md` (the questions that need an answer, with a recommendation each).
2. `BUILD-REQUEST.md` (76 lines): the original owner request and constraints.
3. `qa/local-allocation-acceptance.md`: the ledger, including a register of all 14 open blocking findings, so you do not have to re-read five reports to fix them.
4. `qa/local-source-allocation.md`: manifest v2 (what needs correcting).
5. The five cycle-2 reports `qa/input-allocation/2.N/check-2.md` (50-78 lines each) only if you need a finding's full evidence. Cycle-1 reports are `check-1.md` beside them.
6. The task file itself is 756 KB. **Do not read it whole.** Read lines 1-60 (frontmatter and overview), 126-161 (execution rules and the allocation procedure), 162-205 (Phase 1), and the `### Execution Log` section (newest entry first; find it with a heading search). Locate items by heading text, not by line number: line numbers shift whenever items are inserted (my own dispatch briefs cite stale numbers; the producer specs for topics 2.1-2.5 are now at lines 224/226/228/230/232).

Broader context, if you need it: the issue text (`gh issue view 463 --repo IronbellyOrg/IronClaude`; always pass `--repo`), the repo `CLAUDE.md` (fork rules), the code under study at `src/superclaude/skills/ccsession-tag/` and `tests/unit/test_ccsession_*.py`. `.dev/issues/463/` exists locally and is untracked (output of the earlier issue-claim step); it is deliberately not committed.

## 5. How work is executed here (just enough to continue)

- **Loop:** `/task <task file path>` re-reads the file, finds the first unchecked `- [ ]` item, executes it, ticks it, repeats. Progress lives on disk, so a fresh session resumes safely.
- **Workers:** the executor does not research itself. It launches supervised helper workers through Orca. Run id: `run_c974cafd0eb6`. Launch with one `orca orchestration worker-start --run run_c974cafd0eb6 --spec "<pointer to a brief file>" --worktree current --agent claude --model claude-gw-tier1b --task-title "<title>" --json` per Bash call. Wait with `orca orchestration check --run run_c974cafd0eb6 --wait --types "worker_done,escalation,question" --json`; acknowledge each delivery with `--ack <delivery_id>` after reading the report from disk; release a worker only after accepting its settlement.
- **Model pin:** workers must be `claude-gw-tier1b`. That is a researcher-execution policy, **not** a product default. Verify beyond the launch receipt: `worker-show` shows `live`, and the worker's transcript under `~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/*.jsonl` records a backend model that is one of the live slot values `T1bModel01/02/03` (`printenv | grep '^T1bModel'`; on 2026-11-12 these were `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0`).
- **Briefs** for each dispatch live beside their outputs (`qa/prep-pages/dispatch-*.md`, `qa/input-allocation/2.N/dispatch-check*.md`). Reports are written stub-first with a case-sensitive `VERDICT: PASS` or `VERDICT: FAIL` line.
- **Gate limits:** at most 2 fix cycles and 3 review rounds per gate; a failure that does not shrink HALTs; each report's blocking findings count, minor ones never fail a gate. One serialized fix writer per gate.

## 6. Hazards and my own errors (disclosed so you do not repeat them)

1. **Duplicate dispatches, twice.** (a) Page-1 digest producer: a compound shell command ran `worker-start` twice; two workers interleaved edits in one file (both disclosed it; the output was independently verified PASS). (b) 2.1 allocation check, cycle 1: my first `worker-start` call exited 3 because of a `jq` print error **after** the worker had launched, and I launched it again; dispatch `ctx_866aff4bcc9c` and `ctx_e9422cf5e51f` both ran. I told the owner there was no duplicate; that was wrong. The `check-1.md` for 2.1 notes a pre-existing stub file written seconds before its writer started, which is consistent with two writers. I have not checked whether the interleaving changed that report's content; its blocking findings were the input to the v2 correction, so treat the 2.1 cycle-1 evidence as lower confidence than the others. **Rule:** one `orca` call per Bash call, no `||` fallback, never relaunch on a non-zero exit before running `orca orchestration worker-list --run run_c974cafd0eb6`.
2. **Wrong round count.** I told the owner cycle 2 was "the final permitted review round". By the task's own count only 2 of 3 reviews and 1 of 2 fix cycles are used. The halt comes from the monotonicity rule, not the cap. (The 2.4 verifier also miscounted, calling its report the third review.)
3. **Estimated, not measured, context.** Manifest v2 charges "fixed context 344/424" per slice from guesses. Verifiers flagged this repeatedly. Next version must use measured line counts of the actual brief, prompt, role and template passages.
4. **Stale line numbers in briefs** (see section 4, item 6). Locate specs by the `**2.N Reconcile ...` heading.
5. **Worker launch can fail on this machine.** Once (`ctx_31bb6d30c5db`, 2026-11-13) the worker terminal printed `/usr/local/bin/claude: ... node .../bin/claude: not found`. Environment fault, not a research finding; the retry worked.
6. **Unsettled workers.** After the previous session ended, the cycle-2 verifier dispatches (`ctx_517cf63186e2`, `ctx_e0f5890d0737`, `ctx_972d4f17fdf4`, `ctx_b0bdcfaecf72`, `ctx_1b668786b3c3`) and the cycle-1 duplicate `ctx_866aff4bcc9c` show liveness `unverifiable`; no `worker_done` was accepted for them, although each report is on disk with a verdict. "Unverifiable" is absence of proof, not proof of exit: do **not** stop/abandon/release on that alone. Check each with `orca orchestration worker-show --dispatch <id> --json`, then release only when settlement is positively established.
7. **Tool traps:** the freshness hook blocks Edit/Write on a file not Read in the last 30 minutes (Read, then retry); bare `python3` is blocked (use `jq`/`awk`/shell); chained `sleep` is blocked (use background commands); a `cd` in Bash changes later working directories (use absolute paths).

## 7. Hard constraints (carried from the task; do not violate)

- Research documentation only: no source/test/config edits, no tests run, no paid calls, no installs or package commands, no cleanup of prior artifacts.
- Never interact with `SuperClaude-Org` (no push, PR, comment, or link flags). Push only to `origin` (`IronbellyOrg/IronClaude`); every `gh` call carries `--repo IronbellyOrg/IronClaude`.
- Never stage `.claude/` mirrors or `.dev/issues/`. `.dev/tasks/` is always staged.
- Preserve every intermediate file. Preserve the earlier incident disclosure: during construction (scope-03) a UV-created `.venv`, a local package build and a 27-dependency install happened; never describe this overall run as installation-free.
- Missing evidence stays marked UNVERIFIED; the identity of "Jev" in the issue is unresolved and must not be invented.
