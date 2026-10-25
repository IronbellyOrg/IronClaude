<!-- Round 2.5 invariant probe, raw fault-finder output. Task worker: general-purpose, requested model opus; agentId a7bb1470be6ea683c. Persisted verbatim by the protocol driver. -->
Of 16 findings, 13 are UNADDRESSED and 3 are ADDRESSED. One is HIGH: the consensus remediation for the T-103 provenance gap cannot work as written, and a likely workaround would close the gap with made-up provenance. The consensus verdict (0/0/0/0 deviations, `partial`, `needs_human_decision`) holds. The remediation and some accounting details do not.

The key input is the provenance manifest, which none of the reviewers or advocates read. It says the repo has zero commits and every file is untracked. `--diff changes.patch` was supplied explicitly. `--scope src` was enumerated in full and contains only `src/greeting.py` (`provenance-manifest.json:8-9`, `:45-50`, `:117-122`).

`ADV` = `.../artifacts/adversarial/adversarial/`, snapshot = `reviewer-snapshot/root/`, taxonomy = `plugin/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`.

---

**ID: INV-001 | state_variables | ASSUMPTION:** `regression_present: false` is a settled value. | **STATUS: UNADDRESSED** | **SEVERITY: MEDIUM** | **EVIDENCE:**
- Verification never ran (`task-to-diff-map.md:31`, skip reason tool-unavailable). Taxonomy `:80` says unavailable verification "degrades to the task-log claim with a Grounding Gap entry", and no task log exists (`map:32-33`). So the value is "not observed", not "observed absent".
- V1:23 said exactly that ("cannot be asserted or excluded").
- R2-adv1:14 traded this for an unqualified `false` (preferring V2:72).
- The merged card should emit `false` together with `verification_skip_reason: tool-unavailable`, so a downstream consumer does not read it as an exclusion.

**ID: INV-002 | state_variables | ASSUMPTION:** Snapshot fidelity (A-006) can't be checked, so "Grounded" must be downgraded to "snapshot-grounded". | **STATUS: UNADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- The manifest has `"status": "verified"` (`provenance-manifest.json:2`). All 8 files have `sha256_before == sha256_copy == sha256_after` (`:56-58`, `:64-66`, `:72-74`, `:80-82`, `:88-90`, `:96-98`, `:104-106`, `:112-114`).
- A-006 can therefore be closed for audit time. R1-adv2:73 and R2-adv2:55 left it open without reading the file.
- Leftover risk: any future pytest run is against the live root. It binds to the audited bytes only if the hashes are re-checked at run time.

**ID: INV-003 | collection_boundaries | ASSUMPTION:** (X-002 consensus) The absence of `src/__init__.py` is only [INFERRED] for the live project. | **STATUS: UNADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- The manifest's `scoped_inventory_before/after` is built from `git ls-files --cached --others --exclude-standard` with `enumeration_complete: true`, and lists only `src/greeting.py` (`manifest:8-10`, `:45-50`, `:117-122`). The live absence is therefore grounded, unless a gitignored `__init__.py` exists.
- [INFERRED] remains correct for the root-level and `tests/` files (`tests/__init__.py`, `conftest.py`, `pytest.ini`, `pyproject.toml`). Those were never enumerated (`manifest:8`, scope `src` only).
- The consensus tag is too conservative for one file and correct for the rest.

**ID: INV-004 | collection_boundaries / sufficiency_challenge | ASSUMPTION:** The T-103 provenance gap and the A-001 scope gap close by widening `--scope` to `tests/` and re-auditing until a hunk maps T-103. | **STATUS: UNADDRESSED** | **SEVERITY: HIGH** | **EVIDENCE:**
- `manifest:8`: "repo has zero commits; all files untracked", and `--diff changes.patch` is explicit. `changes.patch:1-9` is a supplied file, not a git range.
- So widening scope cannot produce a T-103 hunk. The remediations as written assume it can: V1:64 ("re-run the audit with `tests/` in the diff scope and check for a `changes.patch` hunk"), `t1-card.md:68`, V2:89 (verifier "a hunk maps T-103"), R2-adv1:7, R2-adv2:53.
- **False-closure path:** with no commits, any regenerated patch (for example a `/dev/null` → file diff of the untracked `tests/test_greeting.py`) yields a hunk for any file that exists. It would "map" T-103 and could flip `partial` to complete with no real provenance.
- The provenance and A-001 rows must name the evidence that can actually close them: a user attestation or task log stating which files belong to the audited change. Diff tooling cannot.

**ID: INV-005 | collection_boundaries | ASSUMPTION:** Every gap row, including the new A-001 scope row, can carry "a single range per `hunk_ref`". | **STATUS: UNADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- The schema requires `hunk_ref: <file:line-range>` (taxonomy `:141`), and the artifact is defined for "when a hunk cannot be classified" (`:134`).
- The scope gap has no file or line range. The T-103 provenance row is a no-hunk claim (`completed.md:8`), and the no-task-log row is a frontmatter claim (`completed.md:2`).
- R2-adv2:58 asks for one range per row without saying what to put in rows that have no hunk. `decision_needed_by_user` for the new scope row is also unspecified.

**ID: INV-006 | count_divergence | ASSUMPTION:** The "Unclassifiable: 1 (R-003 / T-103)" count (V2:71, adopted via C-005 in R2-adv1:47 and R2-adv2:48) stays valid in the merged card. | **STATUS: UNADDRESSED** | **SEVERITY: MEDIUM** | **EVIDENCE:**
- The consensus gap set is now 3-4 rows: provenance, execution, no-task-log (R2-adv2:17), and A-001 scope (R2-adv1:52).
- One unclassifiable item against 3-4 gap rows makes the return-contract counts disagree with each other. One unit has to be chosen (requirements or gap rows) and stated.

**ID: INV-007 | count_divergence | ASSUMPTION:** The execution row and the no-task-log row are independent decisions. | **STATUS: UNADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- V2:59 gives the no-task-log row `next_evidence_needed: Task log or the verification run above`. So one pytest run closes both, which matches `map:32-33` (the gap exists because verification was unavailable).
- The gap count overstates how many independent human decisions are needed.

**ID: INV-008 | guard_conditions | ASSUMPTION:** A future pytest exit 1 is automatically a Regression. | **STATUS: UNADDRESSED** | **SEVERITY: MEDIUM** | **EVIDENCE:**
- The Regression definition requires contradicting an acceptance criterion or "a previously-passing test" (taxonomy `:75`, `:80`). There is no baseline here: zero commits (`manifest:8`) and an untracked, never-run test file (`map:19`).
- The exit-1 row (`:107`) is table-conformant. But a failure caused by a defect in the test itself (`tests/test_greeting.py:8-13`), not a spec contradiction in `src/greeting.py:2-4`, would be minted as Regression.
- The consensus adds the `:112` retry rule (R2-adv1:27) but no failure-attribution step before minting.

**ID: INV-009 | sufficiency_challenge | ASSUMPTION:** Pytest exit 0 closes the R-003 execution gap. | **STATUS: UNADDRESSED** | **SEVERITY: MEDIUM** | **EVIDENCE:**
- R-003 requires that both cases are exercised (`spec.md:12`). Exit 0 still occurs when a test is skipped, deselected or xfailed, for example by a root `conftest.py` or `addopts`.
- The root and `tests/` configs were never enumerated (`manifest:8`, scope `src`).
- The verifiers check only the exit code: V1:65, V2:88, `t1-card.md:67`. Only the plain-pytest path checks "collects 2 tests" (V2:90).
- The closure condition should be: exit 0 AND 2 passed, 0 skipped/deselected/xfail, with `test_ordinary` and `test_empty` both reported.
- The provenance half of the claim, that running pytest alone closes R-003, is already ADDRESSED by the provenance/execution split (R2-adv2:17).

**ID: INV-010 | sufficiency_challenge | ASSUMPTION:** Adding `tests/__init__.py` alone makes collection succeed (consensus: T1 rec 3 is valid under prepend mode, [INFERRED]). | **STATUS: UNADDRESSED** | **SEVERITY: MEDIUM** | **EVIDENCE:** Three conditions falsify it:
- **(a) A project-root `__init__.py`.** Prepend-mode basedir would then climb above the project root, so the root is not put on `sys.path` and `from src.greeting import greet` (`tests/test_greeting.py:1`) fails. The root contents were never enumerated (`manifest:8`).
- **(b) A regular `src` package anywhere on `sys.path`.** Because `src/` has no `__init__.py` (`manifest:45-50`), local `src` is only a namespace portion. Python's path finder returns any regular package it finds before falling back to namespace portions, so a regular `src` in site-packages or an editable install shadows it even though the root is at `sys.path[0]`. The `pythonpath = .` alternative fails the same way.
- **(c) A root config with `--import-mode=importlib`** in `addopts`. R1-adv2:31 noted that the claim is false under importlib mode, but nobody checked for the config.
- Source enumeration: `src/greeting.py` is the only file in `src` (`manifest:47`), so a namespace package is the only resolution path.

**ID: INV-011 | interaction_effects | ASSUMPTION:** Running both `python -m pytest` and plain `pytest` (V1:65, V2:88, consensus) gives one usable R-003 outcome. | **STATUS: UNADDRESSED** | **SEVERITY: MEDIUM** | **EVIDENCE:**
- The taxonomy classifies each invocation separately and joins them by precedence (`:103`).
- Plain `pytest` returning exit 2 (V2 Risk 2, V2:80) while `python -m pytest` returns 0 would keep a Grounding Gap open (`:108`), so `partial` persists even though the tests passed.
- The consensus never says which invocation is authoritative for R-003 "exercise", or whether a plain-pytest exit 2 is a test-harness gap separate from R-003.

**ID: INV-012 | interaction_effects | ASSUMPTION:** Applying rec 3 (`tests/__init__.py` or pytest config) doesn't affect the audit. | **STATUS: UNADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- The new file sits outside the 8 hashed files (`manifest:51-115`) and maps to no task (`completed.md:6-8`).
- If tests are run after adding it, they run against a tree that differs from the audited one.
- If scope is later widened, the file is an unmapped change, i.e. a Drift signal (taxonomy `:62`). It needs a task or authorization entry.

**ID: INV-013 | guard_conditions | ASSUMPTION:** The `if not name` falsy/whitespace behaviour is not a deviation or a correctness gap. | **STATUS: ADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- `src/greeting.py:2` against `spec.md:9`.
- The sibling rule (taxonomy `:161`, `:167`, `:175`) is conceded at R1-adv1:48 and R2-adv1:8. The point moves to Risks (V2:81) and a spec-amendment recommendation (V2:91).

**ID: INV-014 | guard_conditions | ASSUMPTION:** T-103 cannot become Drift except through exit 5. | **STATUS: ADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- Taxonomy `:62`, `:96`, `:109`, conceded at R1-adv1:44-47 and R2-adv1:7.
- INV-004 is a separate issue: the scope gap's remediation, not this boundary.

**ID: INV-015 | state_variables | ASSUMPTION:** A-007 (Python 3.6+, pytest version) is harmless. | **STATUS: ADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- A runtime older than 3.6 hits a SyntaxError at `src/greeting.py:4`, which surfaces as exit 2 and is a Grounding Gap (`:108`), per R2-adv1:32.
- The `pythonpath` option's pytest 7+ requirement is noted at R2-adv1:46.

**ID: INV-016 | interaction_effects (process) | ASSUMPTION:** The Tier-2 reviewers and advocates are heterogeneous and stayed in bounds. | **STATUS: UNADDRESSED** | **SEVERITY: LOW** | **EVIDENCE:**
- Both advocates requested opus (R1-adv1:1, R1-adv2:1, R2-adv1:1, R2-adv2:1). The haiku reviewer slot resolved to grok (V2:1, V2:9; U-008).
- The V2 advocate made a shell read in breach of its brief (R2-adv2:1, :60).
- This does not affect the verdict, but the merged report should disclose both.

---

**Summary**

| | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|
| ADDRESSED | 0 | 0 | 3 (INV-013/014/015) | 3 |
| UNADDRESSED | 1 (INV-004) | 6 (INV-001/006/008/009/010/011) | 6 (INV-002/003/005/007/012/016) | 13 |
| **Total** | 1 | 6 | 9 | 16 |

What this means for the verdict:
- **Status holds.** 0/0/0/0 deviations, R-001 and R-002 statically adherent, `partial`, and `needs_human_decision: true` are all sound, and nothing found here forces a Regression or Drift.
- **INV-004 must be fixed before the merged card ships.** The provenance and scope gaps can only be closed by a user attestation or task log, never by a regenerated diff, which would close them with false provenance.
- **No single action is sufficient.** Neither a pytest run (INV-009, INV-011) nor `tests/__init__.py` (INV-010) is enough on its own, and the merged card should state the stricter closure conditions.
- **A-006 can be closed now** from the manifest (INV-002), and the X-002 tag should be split per file (INV-003).

I wrote no files and used only Read and Glob within the allowed paths.
