# Invariant Probe Results

<!-- Assembled by the neutral sc:debate-orchestrator from round-2-5/fault-finder-opus-raw.md (fault-finder, model slot opus, agentId a78bf335f88ed2257). The orchestrator did not add, drop, or re-grade any finding. Evidence cells are condensed from the raw output; the raw file remains authoritative. -->

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The runtime gap "needs no user decision" because the orchestrator can simply re-run | UNADDRESSED | MEDIUM | `invocations.yaml:3`: the orchestrator "did not substitute Bash for the sanctioned surface", so the skip was deliberate and closing it requires approval of an execution surface (a permission decision). A R2 (rebuttal:51-52) and B R2 (rebuttal:36) both call it "closable by a re-run" without noting that someone has to approve the surface. Bears on C-007 and X-002. |
| INV-002 | state_variables | Bare `status: done` and `[x]` imply acceptance although `verification_ran` is false | ADDRESSED | LOW | `completed.md:2,:8`; `invocations.yaml:2`. A R2:17-21 and B R2:10 both treat "what `done` means" as a user decision. The remaining dispute (X-001) is about wording, not the verdict. |
| INV-003 | state_variables | Snapshot files match the source fixture (A-007); the consensus rests this on a re-read of greeting.py only | ADDRESSED | LOW | `reviewer-snapshot/provenance-manifest.json:153-167` has matching before/copy/after sha256 for `src/greeting.py` and `tests/test_greeting.py`. This stronger evidence went unused. It extends A-007 to the tests file's content but proves nothing about authorship. |
| INV-004 | guard_conditions | The D-1 broadening is fully described as "None, 0, [], False" | UNADDRESSED | LOW | `src/greeting.py:2` `if not name` also rejects `0.0`, `{}`, `()`, `set()`, `b""` and any object whose `__bool__`/`__len__` is falsy. The closed list comes from `t1-card.md:20` and was never challenged. The class does not change; the merged rationale should say "non-str falsy values". Bears on A-002 and C-004. |
| INV-005 | guard_conditions | "Empty" in R-002 means only `""`, so `greet("   ")` returning a greeting is not a Regression | ADDRESSED | LOW | `spec.md:9` says "empty name"; `greeting.py:2,4` returns `"Hello,    !"`. Raised by B (`variant-2-original.md:24`, [INFERRED]) and `t1-card.md:38`. The literal reading supports "no Regression"; the merged verdict should state that it depends on that reading. |
| INV-006 | guard_conditions | The test guard and the proposed verifiers would detect a change in the guard | ADDRESSED | LOW | `tests/test_greeting.py:9-13` accepts any `ValueError` (B, `variant-2-original.md:26`). A's verifier (`variant-1-original.md:28`) cannot see the `None` change; B R2:28 says so. No test pins non-str falsy behaviour. |
| INV-007 | count_divergence | "25/30 points agreed" means the content behind them is settled | UNADDRESSED | MEDIUM | The count is correct: the five contested points are S-005, C-003, C-004, X-001 and A-005. Rows record which card is better, not whether a claim is true. C-008 is equal/equal (A R2:136, B R2:92) yet rests on "no `__init__`/conftest in the snapshot", which the snapshot cannot show (INV-009). Agreement on a row is not verification of its evidence. |
| INV-008 | count_divergence | The tasklist counts add up | ADDRESSED | LOW | `task-to-work-map.yaml:33` `1.0` ("3/3") includes T-103 with `in_supplied_diff: false`, `in_scope_flag: false` (`:30-31`). `S_scope: 1` (`:11`) vs `S_domains: 2` (`:13`) counts out-of-scope tests. Covered by X-001 and A-005. |
| INV-009 | collection_boundaries | "No conftest/pytest config in the snapshot" shows that no such config exists | UNADDRESSED | LOW | The snapshot covers only `["src","tests"]` (`provenance-manifest.json:13-16, 46-55`), so root-level config can never appear in it. Claimed at `variant-1-original.md:19`, B R2:61, A R2:104. A fault-finder glob of `fixtures/project/**` finds no `conftest.py`, `pyproject.toml`, `pytest.ini`, `setup.cfg`, `tox.ini` or `__init__.py`. The conclusion holds; the cited evidence does not support it. |
| INV-010 | collection_boundaries | The search for an approving artifact covered everything relevant | ADDRESSED | LOW | `fixtures/project/proposed.md` is outside the snapshot with no manifest hash; its line 7 does not authorize the broadening. A-006 is QUALIFY on both sides (A R2:114, B R2:70). |
| INV-011 | collection_boundaries | No other code changed, so "no Regression" is complete without a HEAD baseline | UNADDRESSED | LOW | The consensus cites nothing for this, but evidence supports it: `changes.patch:2-3` is a new file from `/dev/null` (no earlier behaviour); the fixture has only two `.py` files; the only call sites are `tests:5,:10` (`interaction-effects.yaml:9`); no HEAD (`task-to-work-map.yaml:36`). |
| INV-012 | interaction_effects | "Run pytest from the project root" is a self-contained check that gives one answer | UNADDRESSED | MEDIUM | The fixture has no ini file, so pytest walks upward to `ci-followup/pyproject.toml:107-116` (`[tool.pytest.ini_options]`, `addopts -v --strict-markers --tb=short`, no `pythonpath`), making `ci-followup/` the rootdir. Lines 75-76 register `pytest11` plugin `superclaude.pytest_plugin`, which loads if installed. The run is environment-dependent. No card or rebuttal mentions this. Bears on C-007 and C-013. |
| INV-013 | interaction_effects | T-101 and T-102 are coupled through the guard, and narrowing it has side effects | ADDRESSED | LOW | `interaction-effects.yaml:7,12` cover the coupling. `greet(None)` → `"Hello, None!"` is covered in B R1 concession 7, A R2:34 and B R2:26. A R2:103 notes that the ":12 both paths covered" note does not cover the D-1 delta. |
| INV-014 | sufficiency_challenge | The evidence is enough for "T-103 implemented" / "R-003 met". Falsifier: under the project's normal runner the tests cannot be collected, so they exercise nothing | UNADDRESSED | HIGH | Branch enumeration: `tests/test_greeting.py:1` is `from src.greeting import greet`; `fixtures/project` has no `src/__init__.py`, `tests/__init__.py`, conftest or ini (glob); ancestor `ci-followup/pyproject.toml:107-116` has no `pythonpath`. In the default prepend import mode, plain `pytest` puts `tests/` on `sys.path`, not the fixture root, so the predicted result is `ModuleNotFoundError: src` at collection. `python -m pytest` from `fixtures/project` adds CWD and would probably pass, which would mask the plain-pytest failure. The consensus labels this [INFERRED] and does not make the T-103/R-003 verdict depend on collection or name which run counts (A R2:22 and B R2:12 admit "exercise" depends on the import). `variant-1-original.md:19` asks for both runs; the merge should keep both and reach no verdict until both are in. Bears on C-003, X-001, A-005, C-008, C-010. |
| INV-015 | sufficiency_challenge | "T-103 implemented" means the executor wrote the tests. Falsifier: the test file existed before the executor's work | ADDRESSED | MEDIUM | The file is untracked and outside the diff (`task-to-work-map.yaml:30-31, 35-36`). The only authorship evidence is the executor's self-report (`execution.log:4`). This is handled as a user decision under A-005, but still contested (B R2:46 says "implemented" implies authorship). The merge should use B's authorship-neutral `static_cases_present_runtime_unproven`. |

## Assembly Validation

| Step | Check | Result |
|------|-------|--------|
| step_1 | Parse fault-finder output | 15 structured `ID/CATEGORY/ASSUMPTION/STATUS/SEVERITY/EVIDENCE` blocks parsed |
| step_2 | All 6 fields present per finding | PASS (15/15) |
| step_3 | Sequential IDs | PASS: INV-001..INV-015 are contiguous, no renumbering needed |
| step_4 | Status ∈ {ADDRESSED, UNADDRESSED} | PASS (15/15) |
| step_5 | Severity ∈ {HIGH, MEDIUM, LOW} | PASS (15/15) |
| — | Category values | 13/15 use the 5 categories listed in `invariant_probe_assembly.table_schema`. INV-014 and INV-015 use `sufficiency_challenge`, the 6th category added to `round_2_5_invariant_probe.five_category_checklist` on 2026-05-17. Accepted as valid. The assembly schema's category list predates that addition (schema-staleness note, not a finding defect). |
| — | sufficiency_challenge evidence rule | INV-014 includes an inline source-file branch enumeration (no branch-trace.md exists). INV-015 cites file:line evidence. PASS |
| — | Cross-check vs raw self-summary | The raw summary says "15 findings, 8 ADDRESSED and 7 UNADDRESSED; 1 HIGH, 4 MEDIUM, 10 LOW". The recount matches. |

## Summary

- **Total findings**: 15
- **ADDRESSED**: 8 (INV-002, INV-003, INV-005, INV-006, INV-008, INV-010, INV-013, INV-015)
- **UNADDRESSED**: 7
  - HIGH: 1 (INV-014)
  - MEDIUM: 3 (INV-001, INV-007, INV-012)
  - LOW: 3 (INV-004, INV-009, INV-011)
- **By severity (all statuses)**: HIGH 1, MEDIUM 4 (INV-001, INV-007, INV-012, INV-015), LOW 10
- **Invariant probe gate input**: count(HIGH ∧ UNADDRESSED) = 1 → gate BLOCKS (blocking item: INV-014). MEDIUM ∧ UNADDRESSED = 3 → warnings (INV-001, INV-007, INV-012).
