# /sc:reflect Report — MultiModelSwarm Phase 1 (M1)

**Mode:** post  
**Depth:** deep / Tier 2-style independent reviewer pass  
**Diff scope:** `git diff HEAD -- src/superclaude/cli/swarm tests/swarm`  
**Tasklist:** `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md`  
**Spec:** `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md`  
**Status:** **failed** — Phase 1 exit gate is not currently satisfied.

## Executive Verdict

M1 has broad implementation and test coverage, but the current worktree does **not** satisfy the Phase 1 exit gate. The audit found three high-impact regressions against explicit Phase 1 acceptance criteria:

1. The scoped Phase 1 swarm test lane fails because `tests/swarm/test_uv_enforcement.py` detects forbidden `python -m` text in swarm sources.
2. `make verify-sync` fails, so the source-of-truth / sync discipline gate is not green.
3. All 20 DM dataclasses round-trip, but runtime inspection shows they are **not frozen**, contradicting the tasklist's M1 exit requirement and the CP5 checkpoint claim.

A fourth issue is evidence-quality related: `phase-1-cp5.md` exists, but it was produced from a different worktree/branch and now contains claims that are false against the current SwarmPost worktree.

## Validation Performed

| Check | Result |
|---|---|
| `uv run pytest <Phase 1 scoped swarm tests> -q` | **FAIL** — 1 failed, 602 passed, 1 skipped |
| `uv run superclaude swarm --help` subcommand grep | **PASS** — count `8` |
| `make verify-sync` | **FAIL** — `sc-bare-review` sync drift |
| Runtime frozen-flag probe for 20 DM classes | **FAIL** — all 20 report `False` |
| Independent reviewer passes | 3 reviewers completed; findings cross-checked inline |

## Deviation Register

### F1 — UV enforcement test fails on forbidden `python -m` in swarm source

- **Class:** regression
- **Severity:** HIGH
- **Affected tasks:** T01.01, T01.06, T01.29 / AC-001
- **Evidence:** The tasklist requires the UV guard test to be green and forbids `python -m` / `pip install` in swarm sources (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md:29-37`). The roadmap repeats AC-001 as no `python -m` / `pip install` and CI rejection (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md:77-78`). The runbook states that bare `python -m …` and `pip install …` are forbidden in `src/superclaude/cli/swarm/` (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/docs/swarm/runbook.md:6-20`). Current source contains a detached-launch doc comment spelling the forbidden invocation (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:782-784`). The implementation also constructs the child argv as `sys.executable`, `-m`, `superclaude.cli.main`, `swarm`, `run` (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/commands.py:879-886`).
- **Command evidence:** `tests/swarm/test_uv_enforcement.py` failed with `Forbidden python -m usage in swarm sources`, pointing at `commands.py:782`.
- **Why regression:** An explicit AC-001 validation command now fails.
- **Recommended remediation:** Remove/replace the forbidden `python -m` wording and decide whether detached re-entry must use a UV-safe launcher (`uv run superclaude ...`) or whether T07 detached semantics need a documented exception plus updated guard test.
- **Verifier:** `uv run pytest tests/swarm/test_uv_enforcement.py -v`.

### F2 — `make verify-sync` is not green

- **Class:** regression
- **Severity:** HIGH
- **Affected tasks:** T01.05, T01.06, T01.12, T01.29 / AC-019
- **Evidence:** T01.05 requires source-of-truth discipline and `make verify-sync` passing (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md:149-181`). The M1 roadmap makes a green `make verify-sync` part of both M1 entry/exit discipline and AC-019 (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md:72-82`). T01.29 also requires `make verify-sync` passes (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md:959-964`).
- **Command evidence:** `make verify-sync` exited 2 and reported `DIFFERS: sc-bare-review` with `Only in src/superclaude/skills/sc-bare-review/: scripts`.
- **Why regression:** The current repo fails an explicit M1 gate, regardless of whether the drift is outside `src/superclaude/cli/swarm`.
- **Recommended remediation:** Restore sync before claiming M1 completion: run `make sync-dev`, inspect the generated `.claude/` mirror drift, then run `make verify-sync` again. Do not stage `.claude/` mirrors.
- **Verifier:** `make verify-sync`.

### F3 — All 20 DM dataclasses are not frozen

- **Class:** regression
- **Severity:** HIGH
- **Affected tasks:** T01.10, T01.13-T01.29 / DM-001..DM-020
- **Evidence:** The Phase 1 goal says exit requires “all 20 data models are frozen + round-trip serializable” (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md:0-3`). T01.29 repeats that all 20 DM records must be frozen and round-trip green (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md:959-964`). Current `models.py` uses a plain `@dataclass` for `JobSpec` (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/models.py:87-88`), and runtime inspection reported `__dataclass_params__.frozen == False` for all 20 DM classes. CP5 claims all 20 records are frozen (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-cp5.md:13-19`, `/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-cp5.md:40-48`).
- **Command evidence:** `uv run python -c <frozen probe>` printed `False` for JobSpec, WorkerSpec, TargetSpec, TransportSpec, PromptSpec, NormalizationSpec, OutputSpec, StatusPolicy, RuntimeSpec, LensEntry, ResolvedLensEntry, ResultContract, WorkerResult, SwarmState, EventRecord, Manifest, DoneSentinel, Artifacts, CallerInfo, and CallerMetadata.
- **Why regression:** The implementation contradicts a stated Phase 1 exit criterion and the checkpoint claim.
- **Recommended remediation:** Either make the DM dataclasses frozen (and adjust any mutation-dependent tests/helpers), or amend the tasklist/checkpoint/spec to remove the frozen requirement before declaring M1 complete.
- **Verifier:** `uv run python -c "from superclaude.cli.swarm import models; names=[...]; print([getattr(models,n).__dataclass_params__.frozen for n in names])"` and relevant pytest model lanes.

### F4 — CP5 checkpoint evidence is stale / not valid for current SwarmPost worktree

- **Class:** regression
- **Severity:** MEDIUM
- **Affected tasks:** T01.29 / D-CP1-1
- **Evidence:** T01.29 requires `phase-1-cp5.md` as the end-of-phase checkpoint and lists validation requirements (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-tasklist.md:959-970`). The existing CP5 says it was generated in worktree `BareReview`, branch `brainstorm/t2-bare-reviewer-adjunct`, at commit `757a3824` (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-cp5.md:6-9`). It claims placeholders still echo `not yet implemented` and `make verify-sync` passes (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/tasklist/phase-1-cp5.md:40-56`), but current tests document that placeholders have been replaced by real commands (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_cli_registration.py:0-20`, `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_cli_registration.py:69-90`) and current `make verify-sync` fails.
- **Why regression:** The checkpoint artifact is no longer reliable evidence for the current worktree.
- **Recommended remediation:** Regenerate CP5 from the SwarmPost worktree after F1-F3 are resolved, with current command outputs embedded.
- **Verifier:** Compare CP5 metadata to `pwd`, `git rev-parse HEAD`, `uv run pytest tests/swarm/ -q`, and `make verify-sync`.

### F5 — LensEntry includes a later-phase `normalizer_strategy` field beyond Phase 1's DM-010 field set

- **Class:** authorized
- **Severity:** LOW
- **Affected tasks:** T01.23 / DM-010; later M2 FR-LENSREG.NS
- **Evidence:** M1 DM-010 lists 13 LensEntry fields and does not include `normalizer_strategy` (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md:95-98`). Current `LensEntry` includes `normalizer_strategy` after `recipe_name` (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/src/superclaude/cli/swarm/models.py:707-720`). The test explicitly states this is T01.23 plus T02.21 and pins a 14-field assertion (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_lensentry.py:0-20`, `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_lensentry.py:40-61`, `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/tests/swarm/test_lensentry.py:83-90`).
- **Why authorized:** The roadmap contains an M2 row for `FR-LENSREG.NS normalizer_strategy field` (`/config/workspace/IronClaude/.dev/releases/current/MultiModelSwarm/roadmap.md:149-151`). This appears to be intentional early adoption rather than a bug.
- **Impact:** Not a blocker by itself, but CP5’s older 13-field LensEntry claim is stale.
- **Recommended remediation:** Document this as authorized scope expansion in CP5/phase log so Phase 1-only audits do not flag it as unexplained drift.

### F6 — CI/test workflow does not directly enforce the UV run shape documented for swarm tests

- **Class:** drift
- **Severity:** LOW
- **Affected tasks:** T01.01 / AC-001
- **Evidence:** The runbook says to run the swarm test lane with `uv run pytest tests/swarm/ -v`, not bare `pytest tests/swarm/` (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/docs/swarm/runbook.md:13-20`). The GitHub workflow runs bare `pytest -v` and bare `pytest tests/swarm/ -m ...` after installing dependencies (`/config/workspace/IronClaude/.claude/worktrees/SwarmPost/.github/workflows/test.yml:54-61`, `/config/workspace/IronClaude/.claude/worktrees/SwarmPost/.github/workflows/test.yml:101-107`).
- **Why drift:** The workflow may still be functionally OK after UV installation, but it diverges from the documented M1 invocation discipline.
- **Recommended remediation:** Either change the workflow to `uv run pytest ...` or explicitly scope AC-001 to source/module invocations rather than CI command spelling.

## Positive Coverage Observed

- `superclaude swarm --help` resolves and lists all 8 expected subcommands.
- The Phase 1 scoped model/test lane has broad coverage: 602 passing tests in the scoped run before the UV-enforcement failure stops the lane.
- `SwarmConfig` is frozen, but the DM dataclasses in `models.py` are not.
- `LensEntry.normalizer_strategy` has a plausible later-roadmap authorization path.

## Per-Task Verdict Summary

| Task range | Verdict | Notes |
|---|---|---|
| T01.01 | failed | UV guard test fails. |
| T01.02-T01.04 | success | CLI group/help evidence passes. |
| T01.05 | failed | `make verify-sync` fails. |
| T01.06/T01.12 checkpoints | partial | Covered evidence exists but is invalidated by current failed gates. |
| T01.07-T01.11 | mostly success | Module shape/config/transport coverage observed. |
| T01.13-T01.28 | partial | Round-trip coverage passes; frozen requirement fails for all 20 DM records. |
| T01.29 | failed | CP5 stale; exit gate not satisfied. |

## Grounding Gaps

No grounding gaps remain for the findings above. All report citations were re-read during this run or backed by command output captured in this run.

## Recommended Next Actions

1. Fix AC-001 enforcement: remove forbidden `python -m` text and resolve the detached launcher’s UV-safe re-entry semantics.
2. Restore source/dev mirror sync with `make sync-dev` followed by `make verify-sync`.
3. Decide whether M1 genuinely requires frozen DM dataclasses; either freeze the 20 models or amend/regenerate Phase 1 acceptance evidence.
4. Regenerate CP5 from the current SwarmPost worktree after gates pass.

## Promotion Verdict

Promotion is **skipped / gate-failed**. M1 should not be promoted to complete while regression findings F1-F4 remain open.
