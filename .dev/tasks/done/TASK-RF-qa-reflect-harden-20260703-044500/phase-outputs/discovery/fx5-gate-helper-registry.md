# FX5 Gate-Helper Enforced Registry Inventory (Step 2.4)

Source (current tree, HEAD 46a787da), all under `src/superclaude/pr_submit/contract_setup/`:
`lockgate.py` (198L), `candidate.py` (396L), `diagnosis.py` (394L), `validation.py` (279L).
Def names + line numbers verified via direct enumeration of the current source (not fabricated).

---

## 1. THE ENFORCED REGISTRY (`GATE_LOAD_BEARING_HELPERS` == `HELPER_TEST_MAP.keys()`)

The enforced registry is the cleanly-enumerable gate-load-bearing helper set: the module-level
`def` resolution / lockability / provenance helpers matched by the single documented gate-shaped
pattern (§3), PLUS two explicitly hand-registered helpers the drift-alarm structurally cannot
auto-enumerate. **11 helpers total**, each of which MUST carry an authored negative + differential
test pair (Steps 2.5/2.6). There is NO per-helper exemption.

### 1a. Drift-alarm-matched module-level `def` helpers (9)

| # | Dotted name | file:line | Purpose |
|---|-------------|-----------|---------|
| 1 | `candidate._path_resolves` | candidate.py:360 | JSON-path existence test w/ all-None-list collapse — **F4 ROOT PRIMITIVE** |
| 2 | `candidate._findings_locus` | candidate.py:253 | picks findings locus; `observed = _path_resolves(...)` — **F4 CALLER** |
| 3 | `candidate._review_completeness_signal` | candidate.py:290 | picks completeness signal; `observed = _path_resolves(...)` — F4-shaped |
| 4 | `candidate._selected_identity` | candidate.py:134 | choose bot login; sets `observed = selected in observed_logins` |
| 5 | `candidate._selected_app_slug` | candidate.py:161 | choose app slug; `observed = answer in observed_slugs` |
| 6 | `lockgate._paths_resolve` | lockgate.py:119 | gate #6: `findings.observed and signal.observed` — **F4 SINK** |
| 7 | `lockgate._emission_shape_observed` | lockgate.py:110 | gate #5: `provenance["emission_shape"].observed` |
| 8 | `diagnosis._resolve_optional_path` | diagnosis.py:285 | None/empty→None; abs→as-is; rel→base/path (degenerate-input helper) |
| 9 | `diagnosis._stale_blockers` | diagnosis.py:334 | repo/PR/hash mismatch blockers — **STALE-state freshness gate** |

### 1b. Hand-registered helpers (2) — carried WITH pairs, OUTSIDE the auto-enumerated drift-alarm set by design

| # | Dotted name | file:line | Why hand-registered |
|---|-------------|-----------|---------------------|
| 10 | `candidate.CandidateContract.required_unobserved` | candidate.py:47 | dataclass METHOD (not a module-level `def`) → drift-alarm's module-level scan cannot enumerate it. Load-bearing F4 bridge (research §5.3). |
| 11 | `validation._negative_control_checks` | validation.py:228 | `_*_checks` builder family — its name contains no gate-shaped token, so the pattern cannot match it (research §5.5). Feeds lockgate #9. |

---

## 2. THE CONSISTENCY INVARIANT (stated explicitly)

> **enforced registry == `HELPER_TEST_MAP.keys()` == `GATE_LOAD_BEARING_HELPERS` == a SUPERSET of the drift-alarm's matched module-level defs.**

- Every registered helper (all 11) carries an authored negative + differential pair → Step 2.8 per-helper
  coverage is REACHABLE and green.
- The drift-alarm's matched set (the 9 in §1a) is a STRICT SUBSET of the registry (the 11) — the alarm can
  never match a helper the registry omits.
- NO registered helper may skip its pair; there is NO per-helper exemption mechanism.
- The Step 2.7a collector asserts `set(GATE_LOAD_BEARING_HELPERS) == set(HELPER_TEST_MAP)` so registry and
  authored-pair set can never silently diverge.

---

## 3. THE SINGLE DOCUMENTED GATE-SHAPED PATTERN (drift alarm) — RECONCILED per resolution (ii)

**The literal candidate pattern from the task brief OVER-MATCHES the current tree.** Applying the brief's
literal pattern
`r"_(path|paths)_resolv|_resolve_|_findings_|_observed_|_selected_|_stale_|_shape_observed|_review_completeness"`
to the enumerated module-level defs matches **14** defs — the 9 intended PLUS 5 that are NOT gate-load-bearing:

- `candidate._observed_logins` (192), `candidate._observed_app_slugs` (203),
  `candidate._observed_associations` (214), `candidate._observed_severity_path` (279) — matched by the
  bare `_observed_` token. Research §1.2/§2.3: these are **resolution primitives** (identity/severity
  observation), NOT directly gate-load-bearing; `_observed_severity_path` is explicitly "severity is
  nullable, not gated".
- `candidate._shape_observed` (352) — matched by the `_shape_observed` token. Research §1.2: a
  **resolution primitive** ("does the given shape exist in payload"). The GATE helper is
  `lockgate._emission_shape_observed`, NOT this bare primitive.

Because these 5 are genuinely not gate-load-bearing (research §2.3 gate set excludes them), the task's
**resolution (ii)** applies: tighten the SINGLE documented gate-shaped pattern so its matched set EQUALS the
registry's 9 module-level defs (never a superset). Two minimal tightenings, each governing registry + alarm
+ authored pairs together (MEDIUM-2 documented reconciliation):

1. Drop the bare `_observed_` token (no intended helper needs it — `_emission_shape_observed` is caught by
   the shape token; `lockgate._identity_observed` has no trailing `_` and was never matched).
2. Narrow `_shape_observed` → `_emission_shape_observed` so only the emission-shape GATE helper matches, not
   the bare `candidate._shape_observed` primitive.

**Reconciled pattern (authored EXACTLY in Step 2.7a):**

```python
GATE_HELPER_DEF_PATTERN = re.compile(
    r"_(path|paths)_resolv|_resolve_|_findings_|_selected_|_stale_"
    r"|_emission_shape_observed|_review_completeness"
)
```

Verified matched set over ALL module-level defs in the 4 files = EXACTLY the 9 in §1a (2 in lockgate,
5 in candidate, 2 in diagnosis, 0 in validation) — a strict subset of the 11-helper registry. This
reconciliation is a single reviewed definition, not a per-helper carve-out.

---

## 4. THE F4 ANCHOR CHAIN (recorded)

```
candidate._path_resolves (360)                     [F4 ROOT PRIMITIVE]
   └─▶ candidate._findings_locus (253).observed     [F4 CALLER]
   └─▶ candidate._review_completeness_signal (290).observed
          └─▶ lockgate._paths_resolve (119)          [F4 SINK — gate #6: findings.observed and signal.observed]
          └─▶ candidate.CandidateContract.required_unobserved (47)  [gate bridge → validation _identity_checks]
Gated by MUST_OBSERVE_FIELDS (candidate.py:18): {augment_identity, emission_shape, findings_locus,
   review_completeness_signal, probe_evidence, repo}.
```

The current worktree ALREADY carries the F4 fix (`_path_resolves` collapses an all-None list to `[]` →
returns `False`). FX5 is a REGRESSION LOCK: a differential test guarantees that reverting the list-comp to
the naive `[item.get(part) for item in current]` (which keeps `[None, None]` truthy) flips a test red.

---

## 5. DOCUMENTED RESIDUAL-RISK NON-GOALS (explicitly OUT of the enforced registry)

### 5a. Auto-enumeration residual-risk non-goals (structurally not drift-alarm-enumerable; research §4.3, MEDIUM-2)
- `validation.ValidationReport.passed` (validation.py:62-65 — `@property` L62, `def passed` L63) — a
  dataclass **method** (not a module-level `def`) and its name contains no gate-shaped token. A future gate
  helper of this shape will NOT auto-trip the drift-alarm and must be hand-registered.
- The residual `validation._*_checks` builder family — `_structure_checks` (133), `_evidence_checks` (163),
  `_surface_checks` (197), `_freshness_checks` (249), `_identity_checks` (186) — none contains a matched
  token; same residual risk. (`_negative_control_checks` IS carried in the registry with its §5.5 pair;
  `_identity_checks` is the bridge that consumes `required_unobserved`, which is registered.)

### 5b. Scope-boundary non-goals (load-bearing but OUTSIDE the 4-file scan window; research §4.3)
- `classify` (pr_submit/classifier.py), `DetectionContract.from_yaml` (pr_submit/detection.py),
  `load_evidence` (contract_setup/evidence.py) — handed to their own test suites; FX5 does not cover them.

Every dotted name and line number above is extracted from the current source; each residual-risk non-goal
is listed EXPLICITLY (never silently in-or-out of the enforced set).
