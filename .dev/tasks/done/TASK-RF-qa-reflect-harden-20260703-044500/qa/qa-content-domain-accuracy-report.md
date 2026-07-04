# QA Report — Task Qualitative Review (domain-accuracy lens)

**Topic:** PR-209 hardening — FX3/FX5 regression backstops (contract_setup)
**Date:** 2026-07-03
**Phase:** task-qualitative
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Lens:** domain-accuracy — verify the test files' factual claims against the ACTUAL source in
`src/superclaude/pr_submit/contract_setup/`.

---

## Overall Verdict: PASS

Every domain claim asserted by the FX3 (`test_setup_questions_resolution.py`) and FX5
(`test_gate_helper_differentials.py` + `conftest.py`) backstops was independently verified
against the real source modules. The four numbered confirmation targets in the spawn brief
all hold true against the code. Both test files pass green (26/26), and the FX5 parametrized
coverage collector passes live (11/11). No CRITICAL, IMPORTANT, or MINOR domain-accuracy
defects found. The one nuance surfaced (a conftest explanatory-comment mechanism grouping)
was adjudicated non-defective — see Observations.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | FX3 F3 trap is real (SUBSET direction; `augment_app_slug` no false-positive; call-site `answer_key` reconstruction; buggy `_evidence_attr("pr_number")` would fail) | none | PASS | See Claim 1 |
| 2 | FX5 enforced registry == HELPER_TEST_MAP.keys(); hand-registers the 2 §5 differentials; both are dataclass-method / `_*_checks` and NOT auto-enumerable | none | PASS | See Claim 2 |
| 3 | Auto-enumeration non-goals + scope-boundary non-goals documented in conftest | none | PASS | See Claim 3 |
| 4 | GATE_HELPER_DEF_PATTERN matches EXACTLY the 9 module-level helpers (strict subset of the 11-registry); over-match tokens dropped/narrowed | none | PASS | See Claim 4 (empirical) |

<!-- task-qualitative Axis column: all rows PASS -> `none` sentinel (five-axis lens applied,
no axis-attributable finding fired). -->

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)
- Axis lens status: drift-axis-inactive (no BUILD_REQUEST.GOAL verbatim supplied in spawn brief;
  AX-1 Drift disabled for this review — the other four axes AX-2..AX-5 were applied normally)

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 4

---

## Claim-by-Claim Verification

### Claim 1 — FX3 F3 trap is real (PASS)

Verified against `src/superclaude/pr_submit/contract_setup/questions.py` and
`tests/pr_submit/test_setup_questions_resolution.py`.

- **SUBSET direction** — the three resolution tests assert `name in valid` /
  `answer_key in valid` / `attr in valid` (test lines 128, 162, 186): referenced ⊆ valid.
  This is the subset direction the docstring claims (test lines 19-21). VERIFIED.
- **`augment_app_slug` does not false-positive** — it IS a real `SetupAnswers` field
  (`questions.py:28`), added "part of the `detected_augment_identity` question" per the field
  comment (`questions.py:24-28`), but it is referenced by NO deriver-factory call in
  `SETUP_QUESTIONS` (`questions.py:129-216` — the `_answer_default(...)` / `_evidence_attr(...)`
  literals never name it). Under SUBSET direction an unreferenced-but-valid field is never
  required to be referenced, so it cannot false-positive. VERIFIED — matches test docstring.
- **`answer_key = answer_attr or attr` reconstructed from CALL-SITE literals** — the helper
  `_evidence_attr_pairs` (test lines 85-109) extracts `attr` = `call.args[0]` and `answer_attr`
  = the `answer_attr` keyword (else 2nd positional) from the `ast.Call` node, then
  `test_...answer_key...` reconstructs `answer_key = attr if answer_attr is None else answer_attr`
  (test lines 154-161). This mirrors the source indirection `answer_key = answer_attr or attr`
  (`questions.py:68`) reconstructed from the call site — it does NOT parse the parameterized
  `getattr(answers, answer_key, None)` in the helper body (`questions.py:71`). VERIFIED.
- **Buggy `_evidence_attr("pr_number")` (answer_key="pr_number") would fail assertion (2)** —
  `"pr_number"` is NOT a `SetupAnswers` field (the dataclass fields are `repo, probe_pr,
  operation, ...` — `questions.py:18-38`; no `pr_number`), so `assert answer_key in valid`
  (test line 162) would fail. The CURRENT (fixed) source passes
  `_evidence_attr("pr_number", answer_attr="probe_pr")` (`questions.py:136`) → `answer_key =
  "probe_pr"`, which IS a field → passes. The evidence-side `attr="pr_number"` is a real
  `EvidenceBundle` field (assertion 3, test lines 170-190), so the fixed call is valid on both
  sides. VERIFIED.
- Line-number citations in the test docstring (`questions.py:68,71` for the getattr indirection;
  `questions.py:136` for the fix) match the current source exactly. VERIFIED.

### Claim 2 — FX5 enforced registry & the two hand-registered §5 differentials (PASS)

Verified against `conftest.py`, `test_gate_helper_differentials.py`, `candidate.py`,
`validation.py`.

- **Registry ≡ HELPER_TEST_MAP.keys(), no exemption hatch** — `conftest.py:200-204` asserts
  `set(GATE_LOAD_BEARING_HELPERS) == set(helper_map)`. Both contain 11 entries
  (9 drift-alarm-matched module-level helpers + 2 hand-registered). The parametrized collector
  requires BOTH a `negative` AND a `differential` per helper (`conftest.py:215-223`) with no
  per-helper skip. The 11/11 live run confirms equality holds. VERIFIED.
- **Hand-registers `candidate.CandidateContract.required_unobserved` (§5.3, dataclass method)** —
  registered in the "Hand-registered (2)" block (`conftest.py:128-130`) and in HELPER_TEST_MAP
  (`test_...:81-84`). It is a method on the `@dataclass(frozen=True) CandidateContract`
  (`candidate.py:39-60`, `def required_unobserved` at `candidate.py:47`) — NOT a module-level
  def. The drift alarm's AST walk iterates `tree.body` only (module-level FunctionDef;
  `conftest.py:184-190`), so it never descends into the class body → not auto-enumerable →
  correctly requires hand-registration. VERIFIED.
- **Hand-registers `validation._negative_control_checks` (§5.5, `_*_checks` builder)** —
  registered (`conftest.py:130`, HELPER_TEST_MAP `test_...:90-93`). It is a module-level function
  returning `list[CheckResult]` (`validation.py:228-246`). Empirically it IS module-level yet
  does NOT match `GATE_HELPER_DEF_PATTERN` (Bash run below), so the drift alarm's matched set
  excludes it → not auto-enumerable → correctly requires hand-registration. VERIFIED.
- Both are, as claimed, dataclass-method / `_*_checks`-builder respectively, and both escape the
  naive module-level pattern scan a drift-alarm would otherwise rely on. VERIFIED.

### Claim 3 — Documented non-goals (PASS)

Verified against `conftest.py:104-114` and `validation.py`.

- **Auto-enumeration non-goals** — `conftest.py:104-111` documents that the drift alarm walks
  module-level defs only and names `validation.ValidationReport.passed` and
  `candidate.CandidateContract.required_unobserved` (dataclass methods) plus the
  `validation._*_checks builder family` as NOT auto-enumerable. `ValidationReport.passed` is a
  real `@property` on the `ValidationReport` dataclass (`validation.py:62-65`). The residual
  `_structure_checks / _evidence_checks / _surface_checks / _freshness_checks / _identity_checks`
  family all exist as real module-level defs (`validation.py:133, 163, 197, 249, 186`
  respectively) and — per the empirical Bash run — none match the pattern. The conftest documents
  them collectively as "the validation._*_checks builder family", a valid collective reference.
  VERIFIED.
- **Scope-boundary non-goal** — `conftest.py:112-114` documents that gate-load-bearing helpers
  OUTSIDE the 4 modules (`classify`, `DetectionContract.from_yaml`, `load_evidence`) are handed
  to their own suites and FX5 does not cover them. These three are genuinely external to the 4
  covered modules: `classify` from `superclaude.pr_submit.classifier`,
  `DetectionContract.from_yaml` from `pr_submit.detection`, `load_evidence` from
  `contract_setup.evidence` (the 5th module, used by diagnosis). VERIFIED.

### Claim 4 — Drift-alarm pattern matches EXACTLY the 9 module-level helpers (PASS, empirical)

Verified by re-running the exact `GATE_HELPER_DEF_PATTERN` from `conftest.py:148-151` against
the AST-parsed module-level defs of all 4 modules:

```
MATCHED (9): candidate._findings_locus, candidate._path_resolves,
  candidate._review_completeness_signal, candidate._selected_app_slug,
  candidate._selected_identity, diagnosis._resolve_optional_path,
  diagnosis._stale_blockers, lockgate._emission_shape_observed, lockgate._paths_resolve
REGISTERED == MATCHED: True   (matched-only: [], registered-only: [])
```

- The matched set equals exactly the 9 drift-alarm-registered module-level helpers, and is a
  strict subset of the 11-entry registry (constructively catches an unregistered gate-shaped
  module-level def while never over-matching). VERIFIED.
- **Bare `_observed_` token dropped** — `candidate._observed_logins`, `_observed_app_slugs`,
  `_observed_associations`, `_observed_severity_path` all exist as module-level defs and none
  match the pattern. VERIFIED.
- **`_shape_observed` narrowed to `_emission_shape_observed`** — `candidate._shape_observed`
  (`candidate.py:352`) exists and does NOT match; only `lockgate._emission_shape_observed`
  matches. `candidate._emission_shape` (the sibling) also does not match. VERIFIED — the
  narrowing avoids over-matching the candidate resolution primitives exactly as claimed.

## Cross-file simulation (task-qualitative items 4, 6, 10, 14)

- **Item 14 (existence claims grep-verified)** — every "field/function exists / does not exist"
  claim in both test files was verified against source: `SetupAnswers` / `EvidenceBundle` fields
  (dynamic via `dataclasses.fields`), the 11 registered helpers all resolve on their live modules
  (the collector's existence check + the 11/11 run prove it), and the naive-mutant differentials
  reference only real symbols (`FieldProvenance`, `PROVENANCE_OBSERVED`, `derive_candidate`,
  `lockgate_mod._check`, `validation_mod.classify`, `CheckResult`, `STATE_POLLING`,
  `MUST_OBSERVE_FIELDS`, `diagnosis_mod._first_str`) — all confirmed present. VERIFIED.
- **Item 6 (downstream consumer / differential wiring)** — each differential monkeypatches the
  real module global and asserts a downstream observation flips (e.g. `_path_resolves` →
  `_findings_locus().observed`; `_findings_locus` → `derive_candidate(ev).required_unobserved()`;
  `classify` → `_negative_control_checks`). The wiring matches the real call graph
  (`candidate.py:259/268` reads `_path_resolves`; `validation.py:229/234` reads `classify`).
  VERIFIED.
- **Item 4/10 (mutant fidelity)** — `_naive_path_resolves` (test) is a faithful pre-F4 version of
  the real `_path_resolves` MINUS the all-None-collapse guard (`candidate.py:360-381` keeps only
  present values; the mutant keeps None). `_naive_resolve_optional_path` drops the `if not value`
  guard present at `diagnosis.py:286-287`. `_naive_stale_blockers` drops the hash comparison
  present at `diagnosis.py:357-360`. All mutants correctly re-introduce the exact bug the guard
  prevents. VERIFIED.

## Test execution evidence

- `pytest test_setup_questions_resolution.py test_gate_helper_differentials.py` → **26 passed**.
- `pytest -k gate_helper_has_negative_and_differential` → **11 passed** (registry-equivalence,
  per-helper existence + coverage, and drift-alarm all green live).

## Issues Found

None. No CRITICAL, IMPORTANT, or MINOR domain-accuracy defect. Every factual claim in the
FX3/FX5 backstops matches the actual source.

## Observations (non-defective, recorded for transparency)

- **Conftest comment mechanism grouping (`conftest.py:104-111`)** — the comment states "the drift
  alarm walks MODULE-LEVEL defs ONLY, so [dataclass methods] ... and the `validation._*_checks`
  builder family are NOT auto-enumerable." For the dataclass methods the causal reason (not
  module-level) is exact. For the `_*_checks` family the reason is subtly different: they ARE
  module-level, and they escape enumeration because `GATE_HELPER_DEF_PATTERN` does not include a
  `_checks` token (empirically confirmed). Read as a *list* of shapes-that-escape (rather than a
  strict single-cause claim), the comment is accurate, and its actionable conclusion — "a future
  gate helper of those shapes must be hand-registered" — is correct. The precise pattern behavior
  is fully documented 30 lines below (`conftest.py:140-151`). Adjudicated NON-DEFECTIVE: no
  functional impact, the registry-equivalence assertion enforces correctness regardless, and the
  claim the spawn brief asked me to confirm ("NOT auto-enumerable by the drift-alarm") is true in
  outcome for both. Flagged only so a future editor may optionally sharpen the wording.

## Actions Taken

None (fix_authorization: false — report-only).

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn brief; standalone behavior
  applied (no structural PASS items relied upon). All verification was independent.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Re-ran `GATE_HELPER_DEF_PATTERN` from `conftest.py:148-151` against AST-parsed module-level defs
  of all 4 modules via Bash → proved the matched set equals exactly the 9 registered helpers and
  the `_observed_*` / `_shape_observed` / `_*_checks` families are excluded (a semantic
  subset-property proof, not a name/citation match).
- Read `questions.py:64-76` + `:129-216` and traced `answer_key = answer_attr or attr` against the
  test's call-site reconstruction to confirm the buggy `_evidence_attr("pr_number")` would fail
  assertion (2) — a semantic derivation.
- Executed both test files + the parametrized coverage collector (26 + 11 green) to confirm the
  claims hold against the live tree, not merely by reading.

### Self-Audit answers (mandatory)
1. **Factual claims independently verified against source:** All of them — every FX3 assertion
   (4 tests) traced to `questions.py` / `evidence.py`; every FX5 registry entry (11) traced to its
   live helper in `candidate.py` / `lockgate.py` / `diagnosis.py` / `validation.py`; the pattern
   re-run empirically; non-goals cross-checked against real symbols.
2. **Files read to verify:** `conftest.py`, `test_setup_questions_resolution.py`,
   `test_gate_helper_differentials.py`, `questions.py`, `candidate.py`, `lockgate.py`,
   `validation.py`, `diagnosis.py` (+ `evidence.py` field set read indirectly via the test builder
   and the dynamic `dataclasses.fields` resolution).
3. **Why trust the 0-defect verdict:** it is backed by (a) an empirical pattern re-run that
   reproduced the exact 9-helper matched set with zero drift, (b) a live 26+11 green test run, and
   (c) a claim-by-claim source trace with line citations — not by assertion. The adversarial
   assumption (≥5 contradictions) was tested and falsified with evidence; the one nuance found was
   examined and adjudicated non-defective rather than ignored.
4. **Web research:** none performed (all verification was local-file/source-bound); Tavily-first
   precedence not triggered.

## Recommendations

- Proceed. The FX3/FX5 backstops are domain-accurate against the current `contract_setup/` source.
- (Optional, cosmetic) Consider sharpening `conftest.py:104-111` so the `_*_checks` family's
  escape reason reads as "excluded by GATE_HELPER_DEF_PATTERN scope" rather than being grouped
  under the module-level-only rationale. Non-blocking.

## QA Complete
