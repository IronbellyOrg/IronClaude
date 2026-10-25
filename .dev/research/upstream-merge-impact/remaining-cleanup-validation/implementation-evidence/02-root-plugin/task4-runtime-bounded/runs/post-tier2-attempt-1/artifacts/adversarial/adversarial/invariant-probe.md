# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Source: `round-2.5-fault-finder.md` (raw output, kept verbatim; single fault-finder Task worker, requested model opus, agentId a7bb1470be6ea683c). The orchestrator assembled this table following `invariant_probe_assembly` (SKILL.md, steps 1-7). Assumption and Evidence cells are condensed from the raw file. See the raw file for the full text.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `regression_present: false` is a settled value | UNADDRESSED | MEDIUM | Verification was not run (`task-to-diff-map.md:31`). Taxonomy `:80` says this degrades to a task-log claim, and no task log exists (`map:32-33`). So the value is "not observed", not "observed absent". V1:23 had this right, but R2-adv1:14 adopted an unqualified `false`. The fix is to emit it together with `verification_skip_reason: tool-unavailable`. |
| INV-002 | state_variables | A-006 snapshot fidelity can't be checked, so tags must be downgraded to "snapshot-grounded" | UNADDRESSED | LOW | `provenance-manifest.json:2` has `"status": "verified"`, and all 8 files have `sha256_before == sha256_copy == sha256_after`. That closes A-006 at audit time. R1-adv2:73 and R2-adv2:55 left it open without reading the manifest. |
| INV-003 | collection_boundaries | (X-002) Absence of `src/__init__.py` is only [INFERRED] for the live project | UNADDRESSED | LOW | The manifest's scoped inventory (`git ls-files --cached --others --exclude-standard`, `enumeration_complete: true`, `manifest:8-10, 45-50`) lists only `src/greeting.py`. So the absence is grounded for `src/`. It stays [INFERRED] for root-level and `tests/` files, which were never enumerated. |
| INV-004 | collection_boundaries / sufficiency_challenge (see V-1) | The T-103 provenance gap and the A-001 scope gap can be closed by widening `--scope` and re-auditing until a hunk maps T-103 | UNADDRESSED | HIGH | `manifest:8`: the repo has zero commits, all files are untracked, and `--diff changes.patch` was passed explicitly. Widening the scope cannot produce a real T-103 hunk. A regenerated `/dev/null`-to-file diff would "map" T-103 with fabricated provenance and could flip `partial` to complete. The remediations at V1:64, V2:89, `t1-card.md:68`, R2-adv1:7 and R2-adv2:53 all assume it can. Only a user attestation or task log can close these gaps. (The orchestrator re-read `manifest:8` and confirms the quoted text.) |
| INV-005 | collection_boundaries | Every gap row, including a new A-001 scope row, can carry a single `<file:line-range>` `hunk_ref` | UNADDRESSED | LOW | Taxonomy `:141` and `:134`. The scope gap has no file or range. The T-103 row is a no-hunk claim (`completed.md:8`), and the no-task-log row is a frontmatter claim (`completed.md:2`). R2-adv2:58 does not say what goes in those rows. `decision_needed_by_user` for the scope row is also unspecified. |
| INV-006 | count_divergence | "Unclassifiable: 1 (R-003 / T-103)" (V2:71, adopted via C-005) is still valid after the merge | UNADDRESSED | MEDIUM | The consensus now has 3-4 gap rows (provenance, execution, no-task-log, A-001 scope), but the unclassifiable count is 1. The return-contract counts would contradict each other unless one unit is chosen. |
| INV-007 | count_divergence | The execution row and the no-task-log row are independent decisions | UNADDRESSED | LOW | V2:59 gives `next_evidence_needed: Task log or the verification run above`, so one pytest run closes both rows (`map:32-33`). The gap count overstates how many independent human decisions are needed. |
| INV-008 | guard_conditions | A future pytest exit 1 is automatically a Regression | UNADDRESSED | MEDIUM | Regression needs either a contradicted acceptance criterion or a test that previously passed (taxonomy `:75`, `:80`). There is no baseline: zero commits, and the test was never run. The consensus adds the `:112` retry rule but no failure-attribution step, so a defect in the test file itself would be minted as Regression. |
| INV-009 | sufficiency_challenge | Pytest exit 0 closes the R-003 execution gap | UNADDRESSED | MEDIUM | `spec.md:12` requires both cases to be exercised. Exit 0 still occurs with skip, deselect or xfail, for example via an unenumerated root `conftest.py`/`addopts` (`manifest:8`). The verifiers check only the exit code (V1:65, V2:88, `t1-card.md:67`). The closure condition should be exit 0 AND 2 passed, 0 skipped. |
| INV-010 | sufficiency_challenge | Adding `tests/__init__.py` alone makes collection succeed (consensus on C-004) | UNADDRESSED | MEDIUM | Three conditions would falsify it: (a) a root `__init__.py`, (b) a regular `src` package on `sys.path` that shadows the local namespace portion (`src/` has no `__init__.py`, `manifest:45-50`), (c) `--import-mode=importlib` set in an unenumerated root config. |
| INV-011 | interaction_effects | Running both `python -m pytest` and plain `pytest` gives one usable R-003 outcome | UNADDRESSED | MEDIUM | Each invocation is classified separately and then joined by precedence (taxonomy `:103`). Plain pytest exiting 2 while `python -m pytest` exits 0 would keep a Grounding Gap open (`:108`). The consensus never says which invocation is authoritative. |
| INV-012 | interaction_effects | Applying rec 3 (`tests/__init__.py` or pytest config) does not affect the audit | UNADDRESSED | LOW | The new file is outside the 8 hashed files (`manifest:51-115`) and maps to no task (`completed.md:6-8`). Tests would then run on a tree that differs from the audited one, and a widened scope would show an unmapped change (taxonomy `:62`). |
| INV-013 | guard_conditions | The `if not name` falsy/whitespace behaviour is neither a deviation nor a correctness gap | ADDRESSED | LOW | `src/greeting.py:2` vs `spec.md:9`. The sibling rule (taxonomy `:161, :167, :175`) was conceded at R1-adv1:48 and R2-adv1:8, and the point was moved to Risks (V2:81) and a spec-amendment recommendation (V2:91). |
| INV-014 | guard_conditions | T-103 cannot become Drift except through exit 5 | ADDRESSED | LOW | Taxonomy `:62, :96, :109`. Conceded at R1-adv1:44-47 and R2-adv1:7. |
| INV-015 | state_variables | A-007 (Python 3.6+, pytest version) is harmless | ADDRESSED | LOW | A runtime older than 3.6 hits a SyntaxError at `src/greeting.py:4`, which surfaces as exit 2 and is a Grounding Gap (`:108`, R2-adv1:32). The pytest 7+ requirement for `pythonpath` is noted at R2-adv1:46. |
| INV-016 | interaction_effects (process) (see V-1) | The Tier-2 reviewers and advocates are heterogeneous and stayed in bounds | UNADDRESSED | LOW | All advocate workers requested opus (R1/R2 headers). The haiku reviewer slot resolved to grok (V2:1, :9; U-008). The V2 advocate made one in-scope shell read despite a brief that said no shell (R2-adv2:1, :60). |

## Validation (assembly steps 2-5)

| Check | Result |
|-------|--------|
| Step 2: all 6 fields present (ID, Category, Assumption, Status, Severity, Evidence) | PASS, 16/16 findings |
| Step 3: sequential IDs | PASS, INV-001..INV-016 contiguous. No renumbering was needed. |
| Step 4: Status ∈ {ADDRESSED, UNADDRESSED} | PASS, 16/16 (3 ADDRESSED, 13 UNADDRESSED) |
| Step 5: Severity ∈ {HIGH, MEDIUM, LOW} | PASS, 16/16 (1 HIGH, 6 MEDIUM, 9 LOW) |
| V-1: Category conformance (advisory; not a numbered assembly step) | 14/16 use exactly one category name. **INV-004** has a compound category (`collection_boundaries / sufficiency_challenge`). **INV-016** has a qualifier (`interaction_effects (process)`). Both values are kept as emitted and not rewritten. Spec inconsistency: `invariant_probe_assembly.table_schema` lists 5 categories and omits `sufficiency_challenge`, while the Round 2.5 `output_format` and checklist list 6. INV-009 and INV-010 are valid under the 6-category definition. None of this affects any gate, because the gates read only Status and Severity. |
| Fault-finder summary table vs this table | Matches: ADDRESSED 0/0/3, UNADDRESSED 1/6/6, total 16 |

## Summary

- **Total findings**: 16
- **ADDRESSED**: 3 (INV-013, INV-014, INV-015; all LOW)
- **UNADDRESSED**: 13
  - HIGH: 1 (INV-004)
  - MEDIUM: 6 (INV-001, INV-006, INV-008, INV-009, INV-010, INV-011)
  - LOW: 6 (INV-002, INV-003, INV-005, INV-007, INV-012, INV-016)
- Counts by severity, all statuses: HIGH 1, MEDIUM 6, LOW 9

### Gate output (consumed by debate-transcript.md)

```
CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-004
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```
WARNING: 6 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-006, INV-008, INV-009, INV-010, INV-011
These items do not block convergence but should be reviewed.
```

LOW items (INV-002, INV-003, INV-005, INV-007, INV-012, INV-016): no action.
