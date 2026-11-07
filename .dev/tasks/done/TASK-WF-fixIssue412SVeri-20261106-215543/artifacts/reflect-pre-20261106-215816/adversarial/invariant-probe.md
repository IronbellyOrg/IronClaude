# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Source: `rounds/round-2-5-fault-finder.md`, written by the fault-finder agent. Scope is plan-level only, and nothing was executed. "ius" means `src/superclaude/cli/install_user_setup.py`, and "plan" means `TASK-WF-fixIssue412SVeri-20261106-215543.md`.

The orchestrator re-read the code and test citations used below before carrying them forward:
- ius:39-40, 204-221, 230-263, 397-399 and 434-444
- `main.py` call sites 236, 365, 384 and 404 (grep)
- `tests/cli/test_install_user_setup.py:260-308`
- `tests/cli/test_update_command.py:44-53`

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | With force=False, the all-present early return survives: no Orca calls. | ADDRESSED | NONE | ius:236-237; plan:45, plan:50; existing test `tests/cli/test_install_user_setup.py:288-294` asserts `not calls`. |
| INV-002 | state_variables | The enclosing force reaches the helper (today ius:441 drops it). | ADDRESSED | NONE | plan:45, plan:50; callers `main.py:236` (user force) and `main.py:404` (`force=True`). The propagation test is new work the plan already requires. |
| INV-003 | guard_conditions | On a forced run with all files present, the presence check (ius:257-258) passes trivially, so ius:263 does not prove a refresh. | ADDRESSED | NONE (LOW refinement) | A-002 3/3; plan:24, plan:45; the R3-2 verifier. Refinement: keep ius:263 as a presence statement; add no "refreshed"/"updated" wording. |
| INV-004 | guard_conditions | An exit-0 safe skip reported on stdout is relayed, not replaced by a success summary. | ADDRESSED | NONE | plan:45, plan:51; `orca-discovery.md:21`, `:25`; R3-2 fixture. |
| INV-005 | guard_conditions | A skip or warning written only to stderr is also relayed. | UNADDRESSED | MEDIUM | The plan text covers it (plan:45, "stdout/stderr"). The only agreed fixture puts the skip on stdout, so an implementation that relays stdout only would pass. Add a stderr-only exit-0 fixture with three files present. |
| INV-006 | sufficiency_challenge | Forced run, exit 0, empty output, three files present: the summary does not claim a refresh. | UNADDRESSED | MEDIUM | V1's empty-output case was merged into C-001, but no card fixes the expected result. Expectation: a presence-only line is acceptable; "refreshed"/"updated" wording is not. |
| INV-007 | guard_conditions | The external command never gains `--force`, and this is testable. | ADDRESSED | NONE (LOW refinement) | plan:23, plan:50; the argv-capturing mock in `tests/cli/test_install_user_setup.py:264-287`. Refinement: assert `"--force" not in command` on the forced path. |
| INV-008 | guard_conditions | IronClaude never rewrites an existing edited guide. | ADDRESSED | NONE | plan:50. No IronClaude skill shares the three Orca names, so `install_all_skills(force=True)` (`main.py:384`) cannot overwrite them. Orca's own non-overwrite is documented, not observed (plan:52). |
| INV-009 | state_variables | The shared network deadline still serves `install_plugins` when force=True. | UNADDRESSED | MEDIUM | Every forced run now probes Orca (ius:204-221, 10 s probe timeout, not bounded by the deadline) and installs, using up to `_ORCA_TIMEOUT = 25` (ius:39) of `_NETWORK_BUDGET = 30` (ius:40, ius:436). Plugins report "(time limit)" when less than 2 s remains (ius:397-399). `update` always forces (`main.py:404`). Nonfatal and reported, so not HIGH. |
| INV-010 | interaction_effects | The behavior change on `superclaude update` is intended and visible. | UNADDRESSED | LOW | `main.py:404`. Neither the plan nor any card names the update path. |
| INV-011 | interaction_effects | The new `force` parameter is backward-compatible. | UNADDRESSED | LOW | Signature at ius:230-232. The stub in `tests/cli/test_update_command.py:47-51` is `lambda **kwargs`, so `force` must come after `deadline`, default to False, and be passed by keyword at ius:441. |
| INV-012 | collection_boundaries | One or two of the three files are present. | ADDRESSED | NONE | ius:236 falls through regardless of force; the warning at ius:258-262 applies; plan:51. |
| INV-013 | collection_boundaries | Forced run where Orca updates two guides and skips one: the count stays 3/3, so only the relayed text shows the skip. | ADDRESSED | NONE | plan:45, plan:51; R3-2 mechanism. |
| INV-014 | count_divergence | The nonzero-exit message is accurate when all three files exist. | UNADDRESSED | LOW | ius:258-262 prints "installed 3/3; rerun", which is ambiguous after a failed forced refresh. plan:51 "accurately reported"; no verifier pins the wording. |
| INV-015 | state_variables | The timeout/OSError message is accurate when guides exist. | UNADDRESSED | LOW | ius:252-256 says "not installed", which is wrong when the guides exist. The existing test asserts only the prefix (`tests/cli/test_install_user_setup.py:307-308`). |
| INV-016 | interaction_effects | The Task 1 edit to core CLAUDE.md keeps `tests/core/test_codegraph_guide.py` green. | ADDRESSED | NONE (LOW refinement) | Assertions at lines 149, 155, 162-166 and 173. Do not add a `\| codegraph` row or a `### ` heading inside Refresh-tool selection, and do not name serena or codegraph_explore. R3-1/C-004 3/3. |
| INV-017 | interaction_effects | The other core-doc readers stay green. | UNADDRESSED | LOW | `tests/core/test_how_we_work_routing_table.py` refers to core/CLAUDE.md (line 5); its assertions were not checked. |
| INV-018 | sufficiency_challenge | The guidance says "never New Terminal" for ccsession sessions, not only "distinguish". | ADDRESSED | NONE (LOW refinement) | source.md:1; plan:30, plan:35; X-001/C-003 3/3 with R1-3's verifier. Refinement: align the plan:35 AC wording with the source. |
| INV-019 | sufficiency_challenge | The plan:52 regression list is sufficient. | UNADDRESSED | LOW | Add `tests/core/test_codegraph_guide.py`, `tests/cli/test_update_command.py` and `tests/core/test_how_we_work_routing_table.py`. |
| INV-020 | sufficiency_challenge | A forced safe install fixes a stale guide. | ADDRESSED | NONE | It does not, for an edited copy (`orca-discovery.md:21`); the intended outcome is a visible warning (source.md:1). plan:19 and plan:52 bound the claims. |
| INV-021 | state_variables | The Task 1 rule reaches the globally loaded file. | ADDRESSED | NONE (LOW refinement) | `../core-install-grounding.yaml`; `main.py:365` `install_core_files(force=True)`. plan:20 forbids a global install, so delivery is not verified at runtime. |
| INV-022 | guard_conditions | Selecting "meaningful" output cannot filter out skip lines. | ADDRESSED | NONE | plan:45 "without a new parser"; relay `result.stdout`/`result.stderr` as is. |

## Normal Installer Skip Debate (state/guard)

Situation: exit 0, all three files present, no `--force`, nothing overwritten. Runtime causation is not proven (plan:19).

- **Nonforce early return.** It survives, and an existing test pins it (INV-001).
- **Forced path against the trivial presence check.** Guarded for stdout skips (INV-003, INV-004). Not yet guarded for a stderr-only skip (INV-005) or for empty output (INV-006).
- **Safe skip reported as a refresh.** Forbidden by plan:24, plan:45 and plan:51. The remaining risk lies in the verifiers, not in the plan text.
- **No-`--force` guard.** Testable with the existing argv mock (INV-007). Orca's own non-overwrite stays documented, not observed (INV-008).
- **Sufficiency.** A forced safe install never refreshes an edited guide, and a visible warning is the intended outcome (INV-020). The new deadline spend is the one cost the review had not weighed (INV-009).

## Summary

- Total invariants probed: 22
- ADDRESSED: 13 (INV-001, 002, 003, 004, 007, 008, 012, 013, 016, 018, 020, 021, 022). Five of these carry a LOW wording refinement: 003, 007, 016, 018 and 021.
- UNADDRESSED: 9
  - HIGH: 0
  - MEDIUM: 3 (INV-005, INV-006, INV-009)
  - LOW: 6 (INV-010, INV-011, INV-014, INV-015, INV-017, INV-019)
- No HIGH item is UNADDRESSED, so the status is not BLOCKED_BY_INVARIANTS. Convergence status stays CONVERGED at 1.00.
- The MEDIUM items go into the merged verifier list as minor notes. They are not blocking findings.
