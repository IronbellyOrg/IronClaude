<!-- Provenance: merged from variant-1-original.md, variant-2-original.md, variant-3-original.md via sc:adversarial Mode A -->
<!-- Base: Variant 3 (reviewer-3-card, opus/refactorer) -->
<!-- Merge date: 2026-11-06 -->

# Merged Reviewer Card: pre-execution review of TASK-WF-fixIssue412SVeri-20261106-215543

## Card Metadata

<!-- Source: Base, modified (V3 header fields; source-card calibrations from debate-transcript.md Metadata) -->

- mode: pre
- base: Variant 3 (reviewer 3, opus, refactorer)
- merged from: Variant 1 (reviewer 1, sonnet, analyzer), Variant 2 (reviewer 2, haiku, qa), Variant 3
- source-card calibrated confidence: V1 0.72, V2 0.66, V3 0.68 (per card, calibrator diversity degraded on all three; not recalibrated for this merge)
- abbreviations: "plan" = `TASK-WF-fixIssue412SVeri-20261106-215543.md` (53 lines); "ius" = `src/superclaude/cli/install_user_setup.py`; "orca-discovery.md" = `artifacts/reflect-pre-20261106-215816/artifacts/orca-discovery.md`

## Verdict

<!-- Source: Base (V3) -->

- plan_verdict: PASS
- Basis: all three cards and all three advocates agree on PASS (debate-transcript.md, Convergence Assessment). The invariant probe found no HIGH item UNADDRESSED (invariant-probe.md, Summary). Every minor note below refines a verifier or an anchor. None is a plan defect.

## Blocking Findings

<!-- Source: Base (V3) -->

- blocking_findings: none

## Minor Findings

<!-- Source: Base, modified (order: R3-1, R3-2, then added notes, optional note last) -->

### R3-1: core CLAUDE.md has a verified reader outside the plan:52 regression list

<!-- Source: Base, modified (narrowed per Change #3; Invariant probe INV-016, INV-017, INV-019) -->

- id: R3-1
- claim: Task 1 edits `src/superclaude/core/CLAUDE.md` (plan:30), and one existing test reads that file with placement-sensitive assertions. The plan:52 regression list does not name that test.
- plan_ref: plan:52
- evidence:
  - `tests/core/test_codegraph_guide.py:137-174`. It reads core CLAUDE.md at line 137. The assertions at lines 149 (exactly one `| codegraph` row), 155 (one begin and one end marker), 162-166 (the `| Symbolic queries` row inside the `### Refresh-tool selection` section) and 173 (no "serena") depend on placement.
- verifier: Add `tests/core/test_codegraph_guide.py` to the Task 2 wider regression run. Do not add a `| codegraph` row or a `### ` heading inside Refresh-tool selection, and do not name serena. Also run `tests/cli/test_update_command.py` and `tests/core/test_how_we_work_routing_table.py` in the wider run (INV-019).
- limitation: `tests/core/test_how_we_work_routing_table.py` is a run-it recommendation; its assertions were not checked, so it is not a verified defect (INV-017). Potential test breakage is unverified.

### R3-2: child output must cover exit-0 safe skips, with no keyword parser

<!-- Source: Base, modified (V1 empty-output case per C-001; Invariant probe INV-005, INV-006) -->

- id: R3-2
- claim: The output relay must cover exit-0 safe skips, not only failures. No keyword parser is needed: relay the existing result fields as they are (plan:45).
- plan_ref: plan:45-51, plan:24
- evidence:
  - ius:230-263 (the `install_orca_skills` helper). With all three files present before the call, the post-call presence check passes trivially, so the success line at the end of the helper cannot prove a refresh (A-002).
  - The basis for an exit-0 skip is documented Orca help, not observed behavior: orca-discovery.md:21 (an edited or foreign copy is skipped and reported) and orca-discovery.md:25 (exit 1 only on a failed or changed location; skipped folders are warnings).
- verifier: three mocked fixtures, each a forced request with exit 0 and all three SKILL.md files present:
  - (a) Skip named on stdout. Assert that the skip text is visible and that no refresh-success claim is made.
  - (b) Skip named only on stderr. Same assertions (INV-005).
  - (c) Empty stdout and empty stderr. A presence-only success line is acceptable; "refreshed" or "updated" wording is not (INV-006).

### R1-3: Task 1 terminal-surface wording is weaker than the source

<!-- Source: V1 (R1-3, with X-001 and C-003; Invariant probe INV-018 refinement) -->

- id: R1-3
- claim: The Task 1 acceptance criterion says "explicitly distinguish" (plan:35), while the source says "use Claude (CLI), never New Terminal" (`source.md:1`). The prohibition reaches Task 1 only through its Inputs (plan:30). Static wording could therefore blur the agent terminal surface and a New Terminal shell.
- plan_ref: plan:30, plan:35
- evidence:
  - `source.md:1`
  - orca-discovery.md:12-16 (`worktree create --agent` and `agent launch` start an agent; `--surface chat|terminal` picks a surface for that launch; `terminal create` makes a terminal for shells)
- verifier: Assert that both instruction surfaces tie the terminal surface to agent creation and state that shell routes are prohibited for ccsession sessions. Refinement (INV-018): align the plan:35 acceptance-criterion wording with the source.

### INV-009: a forced run now spends the shared network deadline on Orca

<!-- Source: Invariant probe (INV-009, INV-010) -->

- id: INV-009
- claim: After the fix, every forced run probes and installs Orca. The install can use up to `_ORCA_TIMEOUT = 25` (ius:39) of `_NETWORK_BUDGET = 30` (ius:40; deadline set at ius:436), and the Orca probe has its own 10 s timeout (ius:213). `install_plugins` reports "(time limit)" when less than 2 s remains (ius:397-399). `superclaude update` always forces (`src/superclaude/cli/main.py:404`). No card weighed this cost. It is nonfatal and honestly reported.
- plan_ref: plan:45, plan:51
- evidence: ius:39, ius:40, ius:213, ius:397-399, ius:436; `src/superclaude/cli/main.py:404`
- verifier: The Task 2 evidence records the plugin step's reported outcome on a mocked forced run, and states that the `superclaude update` path now always requests the Orca install (INV-010).
- severity: verification note, not a plan defect.

### INV-011, INV-014, INV-015: keyword force argument and message accuracy (LOW)

<!-- Source: Invariant probe (INV-011, INV-014, INV-015, INV-007 refinement; A-004) -->

- id: INV-011+INV-014+INV-015
- severity: LOW
- claim: The new `force` parameter must stay compatible with a keyword-only stub. The failure messages can mislead on a forced run when the guides already exist.
- plan_ref: plan:23, plan:45, plan:50, plan:51
- evidence:
  - ius:230-232 (current signature: `home`, then `deadline`); ius:441 (the caller passes only `deadline=deadline`).
  - `tests/cli/test_update_command.py:47-51`: the stub is `lambda **kwargs`, so a positional argument would break it.
  - ius:252-256: the timeout/OSError branch says "not installed", which is wrong when the guides exist.
  - ius:258-262: the nonzero-exit branch says "installed 3/3; rerun" when all three files exist, which is ambiguous after a failed forced refresh.
  - `tests/cli/test_install_user_setup.py:307-308` asserts only the message prefix. The argv-capturing mock at `tests/cli/test_install_user_setup.py:264-287` can check the external command.
- verifier: `force` follows `deadline`, defaults to False, and is passed by keyword at ius:441. On the forced path, assert `"--force" not in command`. Pin the wording of both failure messages when the guides already exist.

### R1-1 (optional): run the routing and sync checks earlier

<!-- Source: V1 (R1-1, kept as optional per C-002) -->

- id: R1-1 (optional); claim: Task 1's routing and sync checks run in Task 2, so failures surface later; sync is part of Task 2 by design, so this is not an omission; plan_ref: plan:47, plan:52; evidence: plan:47; verifier: optionally run the routing and sync checks right after Task 1, without changing the required final scope.

## Self-Audit

<!-- Source: Base (V3) -->

### Reviewer self-audit

<!-- Source: Base (V3) -->

- One optional helper argument, plus top-level propagation and a force-gated early return, is bounded. No new abstraction or dependency is proposed.
- The plan preserves existing positional callers, the three skills, executable lookup, timeout and nonfatal behavior.
- Task 1 static checks follow existing core-document tests. Task 2 sync delivers the Task 1 README edit.
- No Orca source change, global install, commit or push is proposed.
- Reviewer 3 read its brief, one codegraph-guide source range, and bounded searches for relevant tests and plugin mirrors.

### Preservation checklist and mocked/live separation (context, not a finding)

<!-- Source: V2 (U-003, variant-2-original.md:12-14) -->

- Preservation checklist against plan:45: backward-compatible `force` argument, current executable identification, deadline, absent/failed-Orca nonfatal behavior, and the three-skill list.
- Task 2 scope as V2 listed it: forced refresh, default skip, no external `--force`, edited-copy protection, child output, nonfatal failure, compatibility, executable identification, deadlines and the three-skill list.
- Task 1 scope as V2 listed it: the global selection rule and the shell distinction, keeping the supervised worker and internal-agent boundaries.
- Mocked/live separation (plan:52): Task 2 logs keep mocked installer checks apart from actual Orca dry-run evidence. No live guide refresh or UI reproduction is claimed, and no prohibited global install is required.

## Coverage

<!-- Source: Base, modified (Change #8: lexical figure from diff-analysis.md; reviewer-judgment figure from V2) -->

- Lexical coverage: 13/21 = 0.6190 (measured). The shared Constraints at plan:19-24 are outside the matcher.
- Reviewer-judgment semantic coverage: 21/21 (V2, `variant-2-original.md:8-9`; not independently checked). This figure is not a measured coverage value and does not replace the lexical figure.

## Limitations

<!-- Source: Base, modified (V3 limitations; A-003; Invariant probe; Change #8) -->

- This review is plan-level only. Nothing was executed in this review: no tests, installs or Orca commands. The Orca text cited above comes from an earlier read-only discovery of help output (orca-discovery.md:4-7).
- Runtime incident causation is UNDETERMINED (plan:19). Nothing in this card proves Orca shell startup behavior.
- Orca's non-overwrite of edited copies (orca-discovery.md:21) and its exit-0 skip behavior (orca-discovery.md:25) are documented help. Neither was observed.
- Source-card reading scope: V1 and V2 read their briefs only; V3 did not read the full spec or the Orca help.
- Potential test breakage (R3-1) is unverified and remains a minor verification suggestion only.
- The 21/21 coverage figure is reviewer judgment; only the lexical 13/21 = 0.6190 is measured.
