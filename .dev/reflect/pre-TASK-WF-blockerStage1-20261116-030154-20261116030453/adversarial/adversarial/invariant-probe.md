# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent agent (opus class), read-only, run after Round 2. It traced the plan, the spec and the repository itself and listed its negative checks (counts, registry, packaging, scans) as traced-with-no-finding.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Task 11's tests can pass when Task 11 runs, before Tasks 12 and 13 exist (the code that gates M, C and E on supplied inputs, and the safety route, is built later) | UNADDRESSED | MEDIUM | PLAN:157 "Depends on: Task 9, Task 10"; PLAN:165 "A test asserts that a finding without a supplied required-item list never gets an M answer"; PLAN:171 puts "asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied" in Task 12; PLAN:159 test T12 names "the safety route", Task 13 (PLAN:181) |
| INV-002 | collection_boundaries | Every scale-map row has at least one native label for T4 to check | UNADDRESSED | MEDIUM | SPEC:748 "not mapped" for the code-assigned family; PLAN:59 "each native label, the shared outcome per label"; PLAN:209 "a label present in it" |
| INV-003 | interaction_effects | Scale-map rows can name their defining files without breaking the rule for installed primitives, and T4 knows the root it resolves paths against | UNADDRESSED (C-005 covered layout only) | MEDIUM | PLAN:25 forbids `src/superclaude/` paths in installed primitives; rows for `card_convert.py`, `findings_v2.py`, `validate_prompts.py`, `severity_router.py` and `remediate_parser.py` name package code; PLAN:209 "names an existing file"; no task fixes the root |
| INV-004 | guard_conditions | Task 2's grep acceptance line can be run as written | UNADDRESSED | LOW | PLAN:53 `grep -n "src/superclaude" refs/rule.md` names a path that does not exist from the repository root, so grep exits 2 and prints nothing; PLAN:39 and PLAN:66 use the full path |
| INV-005 | guard_conditions | The `lint` and `estimate` review subcommands exist | UNADDRESSED | LOW | PLAN:171 lists them as "existing"; `src/superclaude/cli/review/__init__.py:24-25` lists `lint_cmd` and `estimate_cmd` as optional modules and no such files exist, so `review --help` shows 7 subcommands, not 9; PLAN:174 "still lists every earlier subcommand" still holds |

Traced with no finding (fault-finder report): registry counts 11/1/2/5 = 19; 12 families; 14 worked cases; 6,400 = 4^4 x 5^2 (SPEC:551); 16 Items columns (SPEC:352-367); the 7 tasklist lines; the merge-rule grep of 13 lines in 10 files; all 11 digest source files exist and none contains `src/superclaude`; T2 passes at stage 1; `pragmatic.md:227`; PyYAML is a runtime dependency (`pyproject.toml:38`); the doctor skills check; the install inventory test is a subset check; Makefile check 2 covers only `sc-*-protocol`; `origin_repo.py`; the Task 14 test name; existing phrase scans over the spec text Tasks 2 to 5 copy: zero hits; Task 1's gate halts as designed at HEAD (no stage 0 summary, README:18 has no go for stage 1).

## Summary

- **Total findings**: 5
- **ADDRESSED**: 0
- **UNADDRESSED**: 5
  - HIGH: 0
  - MEDIUM: 3
  - LOW: 2

Gate result: no HIGH-severity UNADDRESSED invariant, so convergence is not blocked. The 3 MEDIUM items are warnings (INV-001, INV-002, INV-003); the 2 LOW items need no action beyond the merged card's minor list.
