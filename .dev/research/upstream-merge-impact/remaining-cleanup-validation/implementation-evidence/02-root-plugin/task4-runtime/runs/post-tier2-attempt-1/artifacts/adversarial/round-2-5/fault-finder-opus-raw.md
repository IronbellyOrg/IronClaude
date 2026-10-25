<!-- Round 2.5 invariant probe raw output. Independent fault-finder (not an advocate). Native Task worker (general-purpose), model slot: opus. agentId a78bf335f88ed2257. Persisted verbatim by the top-level pipeline driver. -->
The consensus survives on its main classifications: D-1 is Drift (LOW), and nothing is Authorized, Necessary or a Regression. It does not support "T-103 implemented" / "R-003 met" without a condition, and its claim that the runtime gap "needs no user decision" is shaky. I found one HIGH, four MEDIUM and ten LOW issues. I used only Read, Grep and Glob, wrote no files and ran no commands.

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: The runtime gap "needs no user decision" because the orchestrator can simply re-run.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `__run_evidence__/verify-logs/invocations.yaml:3` says the orchestrator "did not substitute Bash for the sanctioned surface". The skip was deliberate. Closing the gap means approving an execution surface the protocol did not sanction, which is a permission decision. A R2 (`advocate-A-sonnet-analyzer-rebuttal.md:51-52`) and B R2 (`advocate-B-haiku-qa-rebuttal.md:36`) both call it "closable by a re-run". Neither notes that someone has to approve the surface first.

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: The bare `status: done` and `[x]` imply acceptance even though `verification_ran` is false.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `completed.md:2` and `:8`; `invocations.yaml:2`. A R2 lines 17-21 and B R2 line 10 both treat "what `done` means" as a user decision. The remaining dispute (X-001) is about how to word it, not about the verdict.

ID: INV-003
CATEGORY: state_variables
ASSUMPTION: The snapshot files match the source fixture (A-007). The consensus rests this on a re-read of greeting.py only.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `reviewer-snapshot/provenance-manifest.json:153-167` has matching sha256 before/copy/after values for `src/greeting.py` and `tests/test_greeting.py`. That stronger evidence goes unused, and it extends A-007 to the tests file's content. It does not prove who wrote the file.

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: The D-1 broadening is fully described as "None, 0, [], False".
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `src/greeting.py:2` `if not name` also rejects `0.0`, `{}`, `()`, `set()`, `b""` and any object whose `__bool__`/`__len__` is falsy. The list comes from `t1-card.md:20` and was never challenged. The class does not change, but the merged rationale should say "non-str falsy values", not a closed list.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: "Empty" in R-002 means only `""`, so `greet("   ")` returning a greeting is not a Regression.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `spec.md:9` says "empty name". `greeting.py:2,4` returns `"Hello,    !"`. B raises it as a risk (`variant-2-original.md:24`, marked [INFERRED]); `t1-card.md:38` also has it. The literal reading supports "no Regression". The merged verdict should still state that it depends on that literal reading.

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: The test guard and the proposed verifiers would detect a change in the guard.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `tests/test_greeting.py:9-13` accepts any `ValueError` (B, `variant-2-original.md:26`). A's verifier (`variant-1-original.md:28`) cannot see the `None` change; B R2 line 28 points this out. No test pins non-str falsy behaviour.

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: "25/30 points agreed" means the content behind them is settled.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The count is correct; I checked both R2 tables row by row, and the five contested points are S-005, C-003, C-004, X-001 and A-005. But the rows record which card is better, not whether a claim is true. C-008 is "equal/equal" (A R2:136, B R2:92), yet both sides' evidence is "no `__init__`/conftest in the snapshot", and the snapshot cannot show that (INV-009). Agreement on a row is not verification of its evidence.

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: The tasklist counts add up.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `task-to-work-map.yaml:33` reports `1.0` ("3/3"), but that includes T-103 with `in_supplied_diff: false` and `in_scope_flag: false` (`:30-31`). Also `S_scope: 1` at `:11` versus `S_domains: 2` at `:13`, which counts tests even though they are out of scope. X-001 and A-005 cover this.

ID: INV-009
CATEGORY: collection_boundaries
ASSUMPTION: "No conftest/pytest config in the snapshot" shows that no such config exists.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The snapshot only covers `["src","tests"]` (`provenance-manifest.json:13-16, 46-55`), so root-level config files can never appear in it. The claim is made at `variant-1-original.md:19`, B R2:61 and A R2:104. I globbed `fixtures/project/**` myself: there is no `conftest.py`, `pyproject.toml`, `pytest.ini`, `setup.cfg`, `tox.ini` or any `__init__.py`. The conclusion holds; the cited evidence does not support it. `t1-card.md:40` did check, but cites no line.

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: The search for an approving artifact covered everything relevant.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `fixtures/project/proposed.md` is outside the snapshot and has no hash in the manifest. Its line 7 does not authorize the broadening. A-006 is QUALIFY on both sides (A R2:114, B R2:70).

ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: No other code changed, so "no Regression" is complete even without a HEAD baseline.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The consensus never cites anything for this, but the evidence supports it. `changes.patch:2-3` shows a new file from `/dev/null`, so `greet` had no earlier behaviour. My Glob of `fixtures/project` finds only two `.py` files. The only call sites are `tests:5` and `:10` (`interaction-effects.yaml:9`). The fixture has no HEAD (`task-to-work-map.yaml:36`).

ID: INV-012
CATEGORY: interaction_effects
ASSUMPTION: "Run pytest from the project root" is a self-contained check that gives one answer.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The fixture has no ini file, so pytest looks upward for one. The nearest is `/config/workspace/IronClaude/.dev/worktrees/ci-followup/pyproject.toml:107-116`, which has `[tool.pytest.ini_options]` with `addopts -v --strict-markers --tb=short` and no `pythonpath`. That makes `ci-followup/` the rootdir. Lines 75-76 of the same file register a `pytest11` plugin, `superclaude.pytest_plugin`, which loads automatically if the package is installed in the venv. The `.pytest_cache` would land at that rootdir. The run is therefore environment-dependent. Neither card nor any rebuttal mentions it.

ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: T-101 and T-102 are coupled through the guard, and narrowing it has side effects.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `interaction-effects.yaml:7,12` cover the coupling. The `greet(None)` → `"Hello, None!"` effect is covered in B R1 concession 7, A R2:34 and B R2:26. The note at `:12`, "both paths covered", does not cover the D-1 delta, as A R2:103 points out.

ID: INV-014
CATEGORY: sufficiency_challenge
ASSUMPTION: The evidence is enough for "T-103 implemented" and "R-003 met". The thing that would falsify it: under the project's normal runner the tests cannot be collected, so they exercise nothing.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Files I enumerated:
- `tests/test_greeting.py:1` is `from src.greeting import greet`.
- `fixtures/project` has no `src/__init__.py`, `tests/__init__.py`, conftest or ini file (my Glob).
- The ancestor inifile `ci-followup/pyproject.toml:107-116` has no `pythonpath`.

In pytest's default prepend import mode, plain `pytest` puts `tests/` on `sys.path`, not the fixture root. The predicted result is a `ModuleNotFoundError: src` collection error. `python -m pytest` from `fixtures/project` adds the current directory and would probably pass, which would hide the plain-pytest failure.

The consensus labels this [INFERRED] and "closable by a pytest run". It does not make the T-103/R-003 verdict depend on tests being collected, and it does not name which run counts. A R2:22 and B R2:12 admit that "exercise" depends on the import, but consensus item 3 still says "statically implemented". `variant-1-original.md:19` asks for both a plain `pytest` and a `python -m pytest` run; the merge should keep both and reach no verdict until both are in.

ID: INV-015
CATEGORY: sufficiency_challenge
ASSUMPTION: "T-103 implemented" means the executor wrote the tests. The thing that would falsify it: the test file existed before the executor's work.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The file is untracked and outside the diff (`task-to-work-map.yaml:30-31, 35-36`). The only authorship evidence is the executor's own claim (`execution.log:4`). It is a user decision under A-005, but still contested: B R2:46 says "implemented" implies authorship. The merge should use B's authorship-neutral wording, `static_cases_present_runtime_unproven`.

Summary: 15 findings, 8 ADDRESSED and 7 UNADDRESSED. Severity: 1 HIGH (INV-014), 4 MEDIUM (INV-001, INV-007, INV-012, INV-015), 10 LOW.
The verdict that is not yet supported is "T-103 implemented / R-003 met": it needs to say it depends on the tests being collected, and to name which pytest invocations, in which environment, count.
