# Research: FX5 gate helpers

Status: Complete
Date: 2026-07-03

Summary: Enumerated all helpers across the 4 contract_setup modules (lockgate 14, candidate 18, diagnosis 14, validation 11). Identified the F4 anchor chain `_path_resolves` (candidate.py:360) → `_findings_locus` (253)/`_review_completeness_signal` (290) → `_paths_resolve` (lockgate.py:119) + `required_unobserved` (candidate.py:47), gated by `MUST_OBSERVE_FIELDS` (candidate.py:18). The current worktree ALREADY carries the F4 fix (all-None list collapses to `[]` → unresolved); FX5 is a REGRESSION LOCK, not a first-fix. Defined a registry-anchored collector (≥21 gate helpers) with existence + negative-test + differential-test gates, and cataloged residual risks a naive name-pattern misses: dataclass methods, the `*_checks` builder family, keyword-less primitives, and cross-module load-bearing helpers (`classify`, `from_yaml`, `load_evidence`) outside the 4-file scan window. Provided 5 concrete differential (mutation) examples.

Topic: File Inventory + Patterns for FX5 (negative/differential test mandate for gate helpers).
Scope: lockgate.py, candidate.py, diagnosis.py, validation.py (pr_submit/contract_setup).

All 4 files read fully in worktree `/config/workspace/IronClaude/.dev/worktrees/pr209-harden`. Line numbers below are verified against the read snapshot (2026-07-03). Absolute module paths:

- `src/superclaude/pr_submit/contract_setup/lockgate.py` (198L)
- `src/superclaude/pr_submit/contract_setup/candidate.py` (396L)
- `src/superclaude/pr_submit/contract_setup/diagnosis.py` (394L)
- `src/superclaude/pr_submit/contract_setup/validation.py` (279L)

---

## 1. Complete helper inventory (name · signature · file:line · purpose)

### 1.1 lockgate.py — the safe-lock gate (12 ordered predicates)

| Helper | Signature | Line | Purpose | Load-bearing? |
|---|---|---|---|---|
| `LockGate.evaluate` | `(candidate, evidence, report, *, confirmed, dest, validation_report_path=None) -> GateResult` | 42 | Runs all 12 predicates; `GateResult(passed=not failures, failures=[...])` | GATE ROOT |
| `_check` | `(name, passed, detail) -> CheckResult` | 71 | CheckResult constructor sugar | infra |
| `_evidence_readable` | `(evidence) -> CheckResult` | 75 | `bool(evidence.combined_payload)` | gate #1 |
| `_evidence_repo_bound` | `(candidate, evidence) -> CheckResult` | 81 | candidate `provenance["repo"].value == evidence.repo` | gate #2 |
| `_pr_identity_recorded` | `(evidence) -> CheckResult` | 92 | `pr_number is not None and not cross_pr_shape_only` | gate #3 |
| `_identity_observed` | `(candidate) -> CheckResult` | 100 | `(bot.observed) or (app.observed)` from provenance | gate #4 |
| `_emission_shape_observed` | `(candidate) -> CheckResult` | 110 | `provenance["emission_shape"].observed` | gate #5 |
| **`_paths_resolve`** | `(candidate) -> CheckResult` | **119** | **`findings.observed and signal.observed`** — reads `findings_locus` + `review_completeness_signal` provenance `.observed` flags | **gate #6 — F4 SINK** |
| `_expected_not_polling` | `(candidate) -> CheckResult` | 129 | `expected_classifier_result in {clean,findings,declined}` | gate #7 |
| `_classifier_matches` | `(report) -> CheckResult` | 137 | `report.classifier_result == expected and != POLLING` | gate #8 |
| `_negative_controls_pass` | `(report) -> CheckResult` | 146 | both `empty_negative_control` and `non_augment_negative_control` True | gate #9 |
| `_report_written` | `(report, validation_report_path) -> CheckResult` | 160 | report file exists + contains `evidence_sha256` + `result=="passed"` | gate #10 |
| `_user_confirmed` | `(confirmed) -> CheckResult` | 182 | `confirmed is True` | gate #11 |
| `_dest_under_pr_monitor` | `(dest) -> CheckResult` | 188 | resolved dest `==` `.dev/pr-monitor/...` and not under `.claude`/`src` | gate #12 |

### 1.2 candidate.py — provenance derivation + path resolution

| Helper | Signature | Line | Purpose | Load-bearing? |
|---|---|---|---|---|
| `CandidateContract.required_unobserved` | `(self) -> list[str]` | 47 | must-never-guess fields lacking `.observed` provenance; also `augment_identity` + `expected_classifier_result` | GATE (feeds validation `_identity_checks`) |
| `derive_candidate` | `(evidence, *, answers=None) -> CandidateContract` | 63 | top-level assembler: builds every FieldProvenance | orchestrator |
| `_selected_identity` | `(evidence, answers, provenance) -> str \| None` | 134 | choose bot login; sets `observed = selected in observed_logins` | provenance builder |
| `_selected_app_slug` | `(evidence, answers, provenance) -> str \| None` | 161 | choose app slug; `observed = answer in observed_slugs` | provenance builder |
| `_observed_logins` | `(evidence) -> set[str]` | 192 | augment-looking logins across reviews+comments | resolution primitive |
| `_observed_app_slugs` | `(evidence) -> set[str]` | 203 | augment-looking app slugs across reviews+comments+check_runs | resolution primitive |
| `_observed_associations` | `(evidence) -> tuple[str,...]` | 214 | distinct `author_association` values | resolution primitive |
| `_emission_shape` | `(evidence, answers, provenance) -> str \| None` | 223 | pick review/issue_comment/check_run by presence; sets observed | provenance builder |
| **`_findings_locus`** | `(evidence, answers, provenance) -> str \| None` | **253** | picks a locus path; `observed = _path_resolves(payload, path)` | **provenance builder — F4 CALLER** |
| `_observed_severity_path` | `(evidence) -> str \| None` | 279 | first severity-ish path that `_path_resolves` | resolution (severity is nullable, not gated) |
| `_review_completeness_signal` | `(evidence, answers, provenance) -> str \| None` | 290 | picks completeness signal; `observed = _path_resolves(...)` | provenance builder — F4-shaped |
| `_expected_result` | `(evidence) -> str` | 322 | derive clean/findings/declined/polling from body scan | classifier-shape derivation |
| `_evidence_path` | `(evidence) -> Path` | 334 | combined-payload.json file or probe_dir | path resolution |
| `_has_augmented_body` | `(evidence, needle) -> bool` | 339 | any augment body contains needle | resolution primitive |
| `_shape_observed` | `(evidence, shape) -> bool` | 352 | does the given shape exist in payload | resolution primitive |
| **`_path_resolves`** | `(payload: dict, path: str \| None) -> bool` | **360** | **JSON-path existence test with all-None-list collapse** | **F4 ROOT PRIMITIVE** |
| `_nested_str` | `(data, *keys) -> str \| None` | 384 | nested dict string lookup | resolution primitive |
| `_looks_like_augment` | `(value) -> bool` | 393 | substring `augment`/`auggie` | resolution primitive |

Module constants: `MUST_OBSERVE_FIELDS` (18), `LOCKABLE_RESULTS` (26), provenance source strings (14-16).

### 1.3 diagnosis.py — readiness diagnosis + resolution/freshness

| Helper | Signature | Line | Purpose | Load-bearing? |
|---|---|---|---|---|
| `Diagnosis.summary` | `(self) -> str` | 42 | safe render of state/paths/hashes/blockers | presentation |
| `diagnose` | `(*, repo=None, pr_number=None, cwd=None) -> Diagnosis` | 63 | read-only readiness probe; walks MISSING→...→READY | orchestrator |
| `declined_by_user` | `(*, repo, pr_number, cwd) -> Diagnosis` | 210 | cancellation state, no file touch | state builder |
| `render_pr_submit_missing_contract_halt` | `(diagnosis) -> str` | 236 | fail-closed halt text | presentation |
| `_override_path_for` | `(base, *, cwd_provided) -> Path` | 261 | resolve override path | path resolution |
| `_read_contract` | `(path) -> tuple[DetectionContract\|None, str\|None]` | 267 | parse contract YAML; returns (contract, error) | resolution |
| **`_resolve_optional_path`** | `(value: str\|None, base: Path) -> Path \| None` | **285** | **None/empty → None; abs → as-is; rel → base/path** | **resolution — degenerate-input helper** |
| `_evidence_sha256` | `(path) -> str` | 294 | canonical payload hash; `""` for unhashable dir | resolution (empty hash = unresolved) |
| `_sha256_file` | `(path) -> str` | 305 | raw byte hash of a file | resolution primitive |
| `_read_yaml_file` | `(path) -> dict` | 313 | safe YAML load → `{}` on any error | resolution primitive |
| `_validation_result` | `(data: dict) -> str \| None` | 321 | normalize result/status/verdict → passed/failed/... | provenance normalizer |
| **`_stale_blockers`** | `(data, repo, pr_number, evidence_sha256) -> list[str]` | **334** | **repo/PR/hash mismatch blockers (freshness gate)** | **GATE — STALE state driver** |
| `_first_str` | `(data, *keys) -> str \| None` | 364 | first non-empty string among keys | resolution primitive |
| `_next_command` | `(state, repo, pr_number) -> str` | 372 | next safe command per state | presentation |

### 1.4 validation.py — classifier-backed check builders (provenance/observation builders)

| Helper | Signature | Line | Purpose | Load-bearing? |
|---|---|---|---|---|
| `ValidationReport.summary` | `(self) -> str` | 40 | safe counts render | presentation |
| `ValidationReport.passed` | `(self) -> bool` (property) | 62 | `result == "passed"` | derived gate flag |
| `validate_candidate` | `(candidate, evidence, *, expected_result) -> ValidationReport` | 68 | assemble all checks + negative controls; `result` = passed/failed | GATE ROOT |
| `_decline_validation` | `(expected, classifier_result) -> str` | 125 | passed/failed/not_exercised for declined path | check builder |
| `_structure_checks` | `(candidate) -> list[CheckResult]` | 133 | required-field-populated checks + `candidate_loads` | observation builder |
| `_evidence_checks` | `(evidence) -> list[CheckResult]` | 163 | payload/hash/repo/pr/surfaces/pagination present | observation builder |
| `_identity_checks` | `(candidate) -> list[CheckResult]` | 186 | wraps `required_unobserved()` into `required_observed_provenance` | GATE bridge to candidate |
| `_surface_checks` | `(candidate, evidence) -> list[CheckResult]` | 197 | shape present + findings_locus/completion recorded (~L211) | observation builder |
| `_negative_control_checks` | `(candidate) -> list[CheckResult]` | 228 | empty + non-augment payloads must stay POLLING | anti-gaming controls (feeds lockgate #9) |
| `_freshness_checks` | `(candidate, evidence) -> list[CheckResult]` | 249 | repo_match + hash present + cross_pr_shape_only blocks | freshness gate |
| `_contract_to_yaml_dict` | `(contract) -> dict` | 267 | serialize for from_yaml round-trip (~L273) | serialization |

Module constant: `DECLINE_VALIDATION_VALUES` (14).

---

## 2. Behavior on degenerate input — which silently mis-resolve?

### 2.1 `_path_resolves` (candidate.py:360) — the F4 primitive, NOW FIXED IN THIS WORKTREE

The current worktree code (lines 360-381) already carries the F4 fix. The list branch (369-376) filters to elements where the key is **present and non-None**:

```python
current = [
    value
    for item in current
    if isinstance(item, dict) and (value := item.get(part)) is not None
]
...
if current in (None, []):
    return False
```

Degenerate inputs and results (verified against current code):
- `path=None` or `""` → `False` (line 361-362). Correct.
- all-None list e.g. `{"reviews":[{"body":None},{"body":None}]}`, path `"reviews[].body"` → list-comp yields `[]` → `if current in (None,[])` → `False`. **This is the fix.** The F4 bug was the pre-fix version treating this as resolved (a truthy `[None, None]`) → falsely `observed`.
- empty list `{"reviews":[]}` → `reviews` resolves to `[]`, then `if current in (None,[])` → `False`. Correct.
- missing key `{}`, path `"reviews[].body"` → `.get("reviews")` = None → `False`. Correct.
- non-dict/non-list mid-walk (e.g. a string where a dict expected) → `else: return False` (377-378). Correct.

**FX5's job is REGRESSION LOCK, not first-fix.** The differential test must guarantee that if someone reverts lines 369-376 to a naive `[item.get(part) for item in current]` (which keeps `[None, None]` truthy), a test flips red. Without a mutation/differential test, a "negative test exists" that only checks `path=None → False` would still pass against the buggy all-None variant — the exact anti-gaming hole FX5 closes.

### 2.2 Other silent-mis-resolve candidates

- `_findings_locus` (253) / `_review_completeness_signal` (290) / `_observed_severity_path` (279): all derive `observed` solely from `_path_resolves`. A regression in the primitive silently propagates to `.observed` here. These are the F4 *callers*; a differential test on the primitive protects all three.
- `_evidence_sha256` (294): returns `""` for a directory that `load_evidence` cannot hash. `_stale_blockers` line 357 (`if report_hash and report_hash != evidence_sha256`) with a present report_hash and empty `evidence_sha256` yields `"x" != ""` → adds a stale blocker (fails closed — safe). If both empty, no blocker. Edge worth a negative test.
- `_stale_blockers` (334): each comparison is guarded by truthiness of BOTH sides (`if repo and report_repo`, `if pr is not None and report_pr is not None`, `if report_hash`). A report **missing** repo/pr/hash produces **zero** blockers → READY reachable on an under-specified report. Silent-pass surface: absence treated as "no mismatch". Load-bearing (drives `ContractState.STALE`) → FX5 should mandate negative (`data={}` → `[]`) AND differential (drop a guard → a mismatch test must break).
- `_resolve_optional_path` (285): `None`/`""` → `None` (safe). No mis-resolve.
- `_read_yaml_file` (313) / `_first_str` (364) / `_validation_result` (321): degrade to `{}`/`None` on bad input. Safe; `_validation_result` returns the raw normalized string for unrecognized verdicts (330), and `diagnose` (186) treats `!= "passed"` as VALIDATION_FAILED (safe).

### 2.3 Gate-load-bearing set (feeds lockgate / MUST_OBSERVE_FIELDS)

Directly load-bearing on the lock decision:
- `_path_resolves` → `_findings_locus`/`_review_completeness_signal`.observed → `_paths_resolve` (lockgate #6) AND `required_unobserved` → `_identity_checks`.
- `_selected_identity`/`_selected_app_slug`.observed → `_identity_observed` (lockgate #4) + `augment_identity` in `required_unobserved`.
- `_emission_shape`.observed → `_emission_shape_observed` (lockgate #5).
- `_negative_control_checks` (validation) → `_negative_controls_pass` (lockgate #9).
- `_stale_blockers` → `ContractState.STALE` in `diagnose`.
- `required_unobserved` → `_identity_checks` → validation `result`.

---

## 3. `MUST_OBSERVE_FIELDS` and the exact F4 failure path

### 3.1 `MUST_OBSERVE_FIELDS` (candidate.py:18-25)

```python
MUST_OBSERVE_FIELDS = {
    "augment_identity",
    "emission_shape",
    "findings_locus",
    "review_completeness_signal",
    "probe_evidence",
    "repo",
}
```

These are the fields that must NOT be guessed — each requires `.observed == True` provenance before the contract may lock. `findings_locus ∈ MUST_OBSERVE_FIELDS` is what makes the F4 bug a **lock-integrity** bug rather than a cosmetic one.

### 3.2 The exact F4 failure path (pre-fix, the bug FX5 must lock against recurrence)

1. Evidence payload has a `reviews[]` list where every element's `body` is `None` (or the key is absent) — e.g. reviews present but bodies never populated.
2. `_findings_locus` (candidate.py:253) has no user answer, so it loops `("reviews[].body", "comments[].body", "check_runs[].output")` and calls `_path_resolves(evidence.combined_payload, "reviews[].body")` (line 268).
3. **Pre-fix bug:** `_path_resolves`'s list branch built `[item.get("body") for item in reviews]` = `[None, None]`, a **truthy** non-empty list, so the `if current in (None, [])` guard did NOT fire → returned `True`.
4. `_findings_locus` therefore sets `provenance["findings_locus"] = FieldProvenance("reviews[].body", PROVENANCE_OBSERVED, True, "reviews[].body")` — **`observed=True` for a path that resolves to no actual data**.
5. `CandidateContract.required_unobserved` (candidate.py:47) iterates `MUST_OBSERVE_FIELDS`, sees `findings_locus.observed == True`, and does NOT add it to `missing`. Gate #4 in validation (`_identity_checks` → `required_observed_provenance`) passes.
6. `LockGate._paths_resolve` (lockgate.py:119) reads `findings.observed` (True) `and signal.observed` → predicate #6 **passes**.
7. Net effect: the contract locks with `findings_locus="reviews[].body"` **falsely marked observed** → downstream `classify()` looks for findings in a body path that is always empty → Augment findings are silently never located ("paths falsely observed").

### 3.3 The post-fix invariant FX5 asserts

The all-None list must collapse to `[]` → `_path_resolves` returns `False` → `findings_locus.observed=False` → `required_unobserved` returns `["findings_locus", ...]` → validation `required_observed_provenance` fails → lockgate #6 fails → **the contract cannot lock**. FX5 guarantees a *differential* test exists so this chain stays wired; a mere "negative test present" checkmark is insufficient.

---

## 4. The FX5 collector: precise "helper set" rule

### 4.1 Recommended collector design (registry-anchored, pattern-assisted)

A pure name-pattern scan is fragile (see §4.3). The robust FX5 `tests/pr_submit/conftest.py` collector should be **registry-anchored**:

1. **Explicit registry** — a hand-maintained `GATE_LOAD_BEARING_HELPERS` set of dotted names, minimum:
   - `candidate._path_resolves`, `candidate._findings_locus`, `candidate._review_completeness_signal`, `candidate._observed_severity_path`, `candidate._selected_identity`, `candidate._selected_app_slug`, `candidate._emission_shape`, `candidate.CandidateContract.required_unobserved`
   - `lockgate._paths_resolve`, `lockgate._identity_observed`, `lockgate._emission_shape_observed`, `lockgate._negative_controls_pass`
   - `diagnosis._resolve_optional_path`, `diagnosis._stale_blockers`, `diagnosis._evidence_sha256`, `diagnosis._validation_result`
   - `validation._negative_control_checks`, `validation._structure_checks`, `validation._surface_checks`, `validation._freshness_checks`, `validation._identity_checks`
2. **Existence check** — for each registered dotted name, `getattr`/`inspect` the live module; FAIL (RF Phase-4) if a registered helper no longer exists (catches silent renames that would orphan its tests).
3. **Coverage check** — for each registered helper, require the test suite to contain (a) a **negative-input test** (a test that calls the helper with all-None / empty / missing-key / None input and asserts the "not resolved / blocker / missing" outcome) AND (b) a **differential test** (see §5). Enumerate tests by AST-scanning the test module for a naming/marker convention, e.g. `@pytest.mark.gate_helper("candidate._path_resolves")` with `kind="negative"` / `kind="differential"` params, so the collector can prove BOTH kinds exist per registered helper.
4. **Drift alarm (pattern-assisted)** — additionally AST-walk the 4 modules for module-level `def`s (and the two dataclass methods) whose name matches `re.compile(r'_(path|paths)_resolv|_resolve_|_findings_|_observed_|_selected_|_stale_|_shape_observed|_review_completeness')`. If a match is NOT in the registry, FAIL with "new gate-shaped helper not registered for FX5 coverage" — this forces a human to either register+cover it or explicitly exempt it.

### 4.2 Concrete "module-level def" rule a collector can implement

```python
import ast, inspect
MODULES = ["lockgate", "candidate", "diagnosis", "validation"]  # under contract_setup
# module-level defs:
tree = ast.parse(inspect.getsource(mod))
defs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
# plus dataclass methods that gate:
methods = ["CandidateContract.required_unobserved", "ValidationReport.passed"]
```

### 4.3 Residual risk — what a NAIVE name-pattern MISSES (§3.3 blind spots)

A collector that only greps for `resolve`/`observed` in `def` names would MISS these load-bearing helpers:

- **Dataclass methods** — `CandidateContract.required_unobserved` (candidate.py:47) and `ValidationReport.passed` (validation.py:62) are NOT module-level `def`s; an `ast.body`-only scan skips them entirely. `required_unobserved` is the single most F4-relevant gate bridge.
- **The `*_checks` builder family** — `_structure_checks`, `_evidence_checks`, `_surface_checks`, `_freshness_checks`, `_negative_control_checks`, `_identity_checks` (validation.py) build the CheckResults that become the ValidationReport → lockgate. Their names contain neither `resolve` nor `observed`, so a pattern scan drops them despite being gate-load-bearing.
- **Resolution primitives without keyword names** — `_nested_str`, `_looks_like_augment`, `_has_augmented_body` (candidate.py) feed `_observed_logins`/`_observed_app_slugs`; a bug here silently corrupts identity observation but the names don't match.
- **`_stale_blockers` / `_resolve_optional_path`** — `_stale_blockers` matches only if the pattern includes `_stale_`; a generic `resolve|observed` pattern misses it though it drives `ContractState.STALE`.
- **Cross-module load-bearing helpers OUTSIDE the 4 scanned files** — `classify()` (pr_submit/classifier.py), `DetectionContract.from_yaml` (pr_submit/detection.py), and `load_evidence`/`EvidenceBundle.sha256` (contract_setup/evidence.py — R5 territory) all feed the same lock decision but live outside FX5's 4-module scan window. FX5's scope boundary is itself a residual risk: a regression in `classify` would not be caught by an FX5 collector scoped to these 4 files. This should be documented as an explicit FX5 non-goal / hand-off to the classifier's own test suite.

---

## 5. Differential check — concrete "mutate the output must fail a test" examples

The anti-gaming rule: it is not enough that a negative test EXISTS; **mutating the helper's return must make at least one test fail**. For each representative helper, describe the mutation and the test that must break.

### 5.1 `_path_resolves` (candidate.py:360) — the F4 anchor

- **Negative test:** `_path_resolves({"reviews":[{"body":None},{"body":None}]}, "reviews[].body") is False` AND `_path_resolves({}, "reviews[].body") is False` AND `_path_resolves(payload, None) is False`.
- **Differential:** the mutation to guard against is reverting the list-comp (lines 372-376) to the naive `current = [item.get(part) for item in current if isinstance(item, dict)]`. Under that mutation, the all-None input yields `[None, None]` (truthy) → returns `True`. The negative test above flips red. Additionally, an *integration-level* differential asserts that with the mutation, `_findings_locus(all_none_evidence, SetupAnswers(), {})` sets `provenance["findings_locus"].observed == False` — the mutation breaks it. Wiring both the unit and the propagation test proves the fix is load-bearing, not incidental.

### 5.2 `LockGate._paths_resolve` (lockgate.py:119) — gate #6

- **Negative test:** build a `CandidateContract` whose `provenance["findings_locus"]` has `observed=False` (or is absent) → `_paths_resolve(candidate).passed is False`.
- **Differential:** mutate the predicate from `bool(findings and findings.observed and signal and signal.observed)` to `bool(findings and signal)` (drop the `.observed` checks — the classic "presence ≠ observation" regression). The negative test flips red because a present-but-unobserved locus now passes. This directly guards the F4 sink.

### 5.3 `CandidateContract.required_unobserved` (candidate.py:47)

- **Negative test:** provenance with `findings_locus.observed=False` → `"findings_locus" in required_unobserved()`.
- **Differential:** mutate the loop to skip `findings_locus` (e.g. `MUST_OBSERVE_FIELDS - {"findings_locus"}`) → the assertion `"findings_locus" in missing` breaks. Proves every `MUST_OBSERVE_FIELDS` member is actually enforced, not just iterated.

### 5.4 `_stale_blockers` (diagnosis.py:334) — freshness gate

- **Negative test:** `_stale_blockers({}, None, None, "") == []` (empty report, no context → no false stale) AND `_stale_blockers({"evidence_sha256":"aaa"}, None, None, "bbb")` returns a non-empty list (hash mismatch → stale).
- **Differential:** mutate line 357 to drop the hash comparison (`return blockers` before the hash check) → the mismatch test loses its blocker and flips red. Guards the freshness/staleness detection that gates `ContractState.STALE`.

### 5.5 `_negative_control_checks` (validation.py:228) — anti-gaming controls

- **Negative test:** for a well-formed contract, both controls pass (`empty => POLLING`, `non_augment => POLLING`); for a contract that would classify an empty payload as non-polling, `empty_negative_control.passed is False`.
- **Differential:** mutate `empty == STATE_POLLING` to a constant `True` → a contract that mis-classifies the empty control still reports pass; a test asserting the control catches a permissive contract flips red. This protects lockgate #9 (`_negative_controls_pass`).

---

## 6. Summary of FX5 requirements derived from this inventory

1. FX5's collector must enumerate a **registry** of ≥21 gate-load-bearing helpers across the 4 modules (§4.1), not rely on a name pattern alone.
2. Each registered helper needs BOTH a **negative-input test** and a **differential (mutation) test**; the collector FAILs RF Phase-4 if either is absent (§4.1 step 3).
3. The registry MUST include the two **dataclass methods** (`required_unobserved`, `ValidationReport.passed`) and the **`*_checks` builder family** that a naive scan misses (§4.3).
4. The **F4 anchor** (`_path_resolves` → `_findings_locus`/`_review_completeness_signal` → `_paths_resolve`/`required_unobserved`) must carry the differential in §5.1-5.3, wiring both unit and propagation levels.
5. Document the **scope-boundary residual risk**: `classify`, `DetectionContract.from_yaml`, and `load_evidence` are load-bearing but OUTSIDE the 4 files — an explicit FX5 non-goal handed to their own suites (§4.3).
