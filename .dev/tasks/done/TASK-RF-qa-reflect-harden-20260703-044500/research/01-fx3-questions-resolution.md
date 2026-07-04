# Research: FX3 questions.py resolution

Status: Complete
Date: 2026-07-03
Researcher: R1 (task-builder Deep tier)
Topic: File Inventory + Data Flow Tracer for FX3 (AST field-resolution backstop)
Scope: `src/superclaude/pr_submit/contract_setup/questions.py` (+ `evidence.py`, `__init__.py` for target-name resolution)

All file:line citations are against the pr209-harden worktree at
`/config/workspace/IronClaude/.dev/worktrees/pr209-harden/`.

---

## 0. Headline finding (read this first)

The `questions.py` in this worktree is the **already-FIXED** version of F3.
Line 136 reads:

```python
_evidence_attr("pr_number", answer_attr="probe_pr"),
```

The `answer_attr="probe_pr"` argument is the fix. The **original F3 bug** was a
call of `_evidence_attr("pr_number")` with **no** `answer_attr`, so the deriver's
`answer_key` resolved to `"pr_number"` — a name that does **not** exist on
`SetupAnswers` — and `getattr(answers, "pr_number", None)` silently returned
`None`, discarding the operator's `probe_pr` answer and always falling through to
`evidence.pr_number`.

FX3 (`tests/pr_submit/test_setup_questions_resolution.py`) is the **regression
backstop** for that class of bug: an AST introspection test that asserts every
deriver's string-literal attribute reference resolves to a REAL, flow-through
`SetupAnswers` field (for the answer side) or a REAL `EvidenceBundle` attr (for
the evidence side). It would have failed on the original buggy line and will fail
on any future recurrence.

**Why the bug is silent (and why a test is the only backstop):** the two
`getattr` calls in `_evidence_attr` (L71, L74) both pass an explicit `None`
default, so a wrong attr name never raises — it just returns `None`. By contrast
`_answer_default` (L56) uses `getattr(answers, attr)` with **no** default, so a
wrong literal there raises `AttributeError` at first use (louder, but still worth
statically catching before runtime).

---

## 1. Full field inventory of `class SetupAnswers`

`@dataclass(frozen=True) class SetupAnswers` — defined `questions.py` L14-38.
**17 fields**, all with defaults:

| # | Field | Type | Line |
|---|-------|------|------|
| 1 | `repo` | `str \| None = None` | L18 |
| 2 | `probe_pr` | `int \| None = None` | L19 |
| 3 | `operation` | `str \| None = None` | L20 |
| 4 | `evidence_source` | `str \| None = None` | L21 |
| 5 | `surfaces_to_inspect` | `tuple[str, ...] = ()` | L22 |
| 6 | `detected_augment_identity` | `str \| None = None` | L23 |
| 7 | `augment_app_slug` | `str \| None = None` | L28 |
| 8 | `author_association_values` | `tuple[str, ...] = ()` | L29 |
| 9 | `emission_shape` | `str \| None = None` | L30 |
| 10 | `findings_locus` | `str \| None = None` | L31 |
| 11 | `severity_field_path` | `str \| None = None` | L32 |
| 12 | `review_completeness_signal` | `str \| None = None` | L33 |
| 13 | `decline_detection_fields` | `dict[str, Any] = field(default_factory=dict)` | L34 |
| 14 | `expected_classifier_result` | `str \| None = None` | L35 |
| 15 | `run_validation` | `bool \| None = None` | L36 |
| 16 | `write_local_locked_contract` | `bool \| None = None` | L37 |
| 17 | `next_step` | `bool \| None = None` | L38 |

Note: **`augment_app_slug` (L28)** is present but is NOT referenced by any
`SETUP_QUESTIONS` deriver (comment L24-28: it is set alongside the
`detected_augment_identity` question, not a standalone question). This matters for
FX3's assertion direction — see §4.

### EvidenceBundle attr inventory (`evidence.py` L18-37, needed for the evidence side)

`@dataclass(frozen=True) class EvidenceBundle` — 13 data attributes:

| Attr | Type | Line |
|------|------|------|
| `probe_dir` | `Path` | L22 |
| `repo` | `str \| None` | L23 |
| `pr_number` | `int \| None` | L24 |
| `captured_at` | `str \| None` | L25 |
| `surfaces` | `list[str]` | L26 |
| `omitted_surfaces` | `list[str]` | L28 |
| `reviews` | `list[dict[str, Any]]` | L29 |
| `comments` | `list[dict[str, Any]]` | L30 |
| `check_runs` | `list[dict[str, Any]]` | L31 |
| `combined_payload` | `dict[str, Any]` | L32 |
| `sha256` | `str` | L33 |
| `pagination_complete` | `bool \| None` | L34 |
| `cross_pr_shape_only` | `bool = False` | L36 |

Plus one method: `summary(self)` (L38). A `getattr(evidence, attr, None)` scan
should treat `summary` as a valid-but-non-data name (unlikely to be referenced;
none of the derivers reference it).

---

## 2. `_default_deriver` mechanics

There is no symbol literally named `_default_deriver`. The task brief's "L56 /
L64" pointers correspond to the two generic deriver **factories**:

### `_answer_default(attr)` — factory, def L52-61

```python
def _answer_default(attr: str) -> DefaultDeriver:
    def derive(_evidence, answers) -> object | None:
        value = getattr(answers, attr)          # L56 — NO default
        if value in ((), {}, None):
            return None
        return value
    return derive
```

- Reads **only** `answers` (the `_evidence` param is unused — underscore-prefixed).
- The attribute name is the **call-site string literal** `attr`, closed over.
- `getattr(answers, attr)` at **L56 has no default** → a bogus literal raises
  `AttributeError` the first time the deriver runs (loud failure).
- Empty sentinels `()`, `{}`, `None` are normalized to `None` (treated as
  "unanswered").

### `_evidence_attr(attr, answer_attr=None)` — factory, def L64-76 (F3 site)

```python
def _evidence_attr(attr, answer_attr=None) -> DefaultDeriver:
    answer_key = answer_attr or attr            # L68 — the indirection
    def derive(evidence, answers) -> object | None:
        answered = getattr(answers, answer_key, None)   # L71 — default None (SILENT)
        if answered not in ((), {}, None):
            return answered
        return getattr(evidence, attr, None) if evidence is not None else None  # L74 — default None (SILENT)
    return derive
```

**The `answer_attr`/`answer_key` indirection (the crux of F3):**

- `answer_key = answer_attr or attr` (L68). When `answer_attr` is omitted, the
  answer side and evidence side share the **same** name `attr`.
- `answered = getattr(answers, answer_key, None)` (L71) reads the **operator
  answer** under `answer_key`.
- Fallback `getattr(evidence, attr, None)` (L74) reads the **evidence field**
  under `attr`.
- The design intent (comment L65-67): the operator-answer field name and the
  evidence field name **differ** for probe_pr — answer field is `probe_pr`,
  evidence field is `pr_number`. So the call MUST pass `answer_attr="probe_pr"`
  to bridge them.
- **Failure mode:** if `answer_key` is not a real `SetupAnswers` field, L71's
  `None` default silently swallows the operator answer → the deriver always
  returns the evidence fallback. This is exactly F3. Because both getattrs carry
  `None` defaults, **no exception ever surfaces** — hence the need for FX3.

---

## 3. COMPLETE `SETUP_QUESTIONS` trace (L129-216)

16 questions. For each: deriver, string literal(s) referenced, and whether each
literal resolves to a real target.

| # | Question `id` | Line | Deriver call | Answer-side literal → resolves? | Evidence-side literal → resolves? |
|---|---------------|------|--------------|--------------------------------|-----------------------------------|
| 1 | `repo` | L130-132 | `_evidence_attr("repo")` | `answers.repo` ✓ (L18) | `evidence.repo` ✓ (L23) |
| 2 | `probe_pr` | L133-139 | `_evidence_attr("pr_number", answer_attr="probe_pr")` | `answers.probe_pr` ✓ (L19) | `evidence.pr_number` ✓ (L24) |
| 3 | `operation` | L140-144 | `_operation_default` | `answers.operation` ✓ (L20) [hardcoded L92] | — |
| 4 | `evidence_source` | L145-149 | `_evidence_source_default` | `answers.evidence_source` ✓ (L21) [L98] | — |
| 5 | `surfaces_to_inspect` | L150-154 | `_surfaces_default` | `answers.surfaces_to_inspect` ✓ (L22) [L82] | `evidence.surfaces` ✓ (L26) [L84-85] |
| 6 | `detected_augment_identity` | L155-161 | `_answer_default("detected_augment_identity")` | `answers.detected_augment_identity` ✓ (L23) | — |
| 7 | `author_association_values` | L162-166 | `_answer_default("author_association_values")` | `answers.author_association_values` ✓ (L29) | — |
| 8 | `emission_shape` | L167-173 | `_answer_default("emission_shape")` | `answers.emission_shape` ✓ (L30) | — |
| 9 | `findings_locus` | L174-180 | `_answer_default("findings_locus")` | `answers.findings_locus` ✓ (L31) | — |
| 10 | `severity_field_path` | L181-185 | `_answer_default("severity_field_path")` | `answers.severity_field_path` ✓ (L32) | — |
| 11 | `review_completeness_signal` | L186-192 | `_answer_default("review_completeness_signal")` | `answers.review_completeness_signal` ✓ (L33) | — |
| 12 | `decline_detection_fields` | L193-197 | `_answer_default("decline_detection_fields")` | `answers.decline_detection_fields` ✓ (L34) | — |
| 13 | `expected_classifier_result` | L198-203 | `_answer_default("expected_classifier_result")` | `answers.expected_classifier_result` ✓ (L35) | — |
| 14 | `run_validation` | L204-209 | `_run_validation_default` | `answers.run_validation` ✓ (L36) [L104] | — |
| 15 | `write_local_locked_contract` | L210-214 | `_write_lock_default` | `answers.write_local_locked_contract` ✓ (L37) [L110-114] | — |
| 16 | `next_step` | L215 | `_next_step_default` | `answers.next_step` ✓ (L38) [L120] | — |

**In this FIXED worktree, all 16 resolve correctly.** The F3 case (row 2) is
green *because* of `answer_attr="probe_pr"`.

### The F3 case in detail (row 2, L133-139)

- `_evidence_attr("pr_number", answer_attr="probe_pr")` → `answer_key = "probe_pr"`.
- `getattr(answers, "probe_pr", None)` → **`answers.probe_pr` EXISTS** (L19). ✓
- `getattr(evidence, "pr_number", None)` → **`evidence.pr_number` EXISTS** (L24). ✓
- **Buggy original** (`_evidence_attr("pr_number")`, no `answer_attr`):
  `answer_key = "pr_number"`; `getattr(answers, "pr_number", None)` →
  `SetupAnswers` has **no `pr_number` field** → always `None` → the operator's
  chosen PR was silently dropped and the deriver always used `evidence.pr_number`.
  No crash, no warning. That is the exact bug FX3 must trap.

### Named single-purpose derivers (hardcoded attribute access, not string literals)

These do NOT go through `_answer_default`/`_evidence_attr`; they reference fields
via `ast.Attribute` nodes (e.g. `answers.operation`), not string args:

- `_surfaces_default` L79-86 → `answers.surfaces_to_inspect` (L82), `evidence.surfaces` (L84)
- `_operation_default` L89-92 → `answers.operation` (L92)
- `_evidence_source_default` L95-98 → `answers.evidence_source` (L98)
- `_run_validation_default` L101-104 → `answers.run_validation` (L104)
- `_write_lock_default` L107-114 → `answers.write_local_locked_contract` (L110-113)
- `_next_step_default` L117-120 → `answers.next_step` (L120)
- `_none_default` L123-126 → references nothing; **UNUSED** in SETUP_QUESTIONS (dead helper)

---

## 4. Exact FX3 AST contract (what to extract, what to validate against)

### 4a. String literals FX3's AST scan must EXTRACT (from `SETUP_QUESTIONS`/factory call sites)

Scan `questions.py` for `ast.Call` nodes whose `func` is `_answer_default` or
`_evidence_attr`, and pull their string-literal args:

**`_answer_default(<lit>)` — the `<lit>` is an answer-side field name:**
```
"detected_augment_identity", "author_association_values", "emission_shape",
"findings_locus", "severity_field_path", "review_completeness_signal",
"decline_detection_fields", "expected_classifier_result"
```
(8 literals — rows 6-13.)

**`_evidence_attr(attr, answer_attr=<opt>)` — split into two target spaces:**
```
call 1: attr="repo",       answer_attr=absent  → answer_key="repo",      evidence_attr="repo"
call 2: attr="pr_number",  answer_attr="probe_pr" → answer_key="probe_pr", evidence_attr="pr_number"
```
- `answer_key` (= `answer_attr` if present else `attr`): {`"repo"`, `"probe_pr"`}
  → must validate against **SetupAnswers fields**.
- `evidence_attr` (= positional `attr`): {`"repo"`, `"pr_number"`}
  → must validate against **EvidenceBundle attrs**.

### 4b. Valid target-name sets FX3 validates against

**SetupAnswers fields (17)** — assemble dynamically, e.g.
`{f.name for f in dataclasses.fields(SetupAnswers)}`:
```
repo, probe_pr, operation, evidence_source, surfaces_to_inspect,
detected_augment_identity, augment_app_slug, author_association_values,
emission_shape, findings_locus, severity_field_path,
review_completeness_signal, decline_detection_fields,
expected_classifier_result, run_validation, write_local_locked_contract,
next_step
```

**EvidenceBundle attrs (13 data fields)** — via
`{f.name for f in dataclasses.fields(EvidenceBundle)}`:
```
probe_dir, repo, pr_number, captured_at, surfaces, omitted_surfaces,
reviews, comments, check_runs, combined_payload, sha256,
pagination_complete, cross_pr_shape_only
```

### 4c. Concrete assertions FX3 must make

1. **Every** `_answer_default(<lit>)` literal ∈ SetupAnswers fields.
   (Would trap `_answer_default("pr_number")`, `_answer_default("typo")`.)
2. **Every** `_evidence_attr` `answer_key` (answer_attr or attr) ∈ SetupAnswers
   fields. **← This is the direct F3 trap.** With the buggy original,
   `answer_key="pr_number"` ∉ SetupAnswers → assertion fails.
3. **Every** `_evidence_attr` positional `attr` (evidence side) ∈ EvidenceBundle
   attrs. (Would trap a mistyped evidence field.)
4. (Recommended) Every `SETUP_QUESTIONS` entry's `id` equals the SetupAnswers
   field it drives, so the question table and the answer schema stay 1:1 (all 16
   ids currently match a field; `augment_app_slug` has no question, which is
   expected).

**Assertion DIRECTION matters — subset, not onto.** Validate
`referenced_literals ⊆ valid_fields`, NOT `valid_fields ⊆ referenced_literals`.
`augment_app_slug` (L28) is a real field that is intentionally NOT referenced by
any deriver (set via the `detected_augment_identity` question flow). An "every
field must be referenced" check would false-positive on it. FX3 must assert only
that each *used* literal is *valid*.

### 4d. Extending the scan to the named derivers (stronger FX3)

To also cover the 6 named single-purpose derivers (§3), FX3 can add a second AST
pass over `questions.py` collecting `ast.Attribute` nodes whose `.value` is a
`Name` in {`answers`, `evidence`} (note some derivers name the param `_answers` /
`_evidence` when unused — include those too), and assert each `.attr` is a valid
SetupAnswers / EvidenceBundle name respectively. Without this pass, a typo like
`answers.operatoin` in `_operation_default` would escape FX3 (though it would
`AttributeError` at runtime). Recommended but secondary — the primary F3 class is
fully covered by 4c items 1-3.

---

## 5. Dynamic / computed access a static AST scan would MISS (residual risk)

1. **`decline_detection_fields` dict keys** (L34, `dict[str, Any]`). The
   `augment_app_slug` comment (L24-28) notes the slug is deliberately NOT
   tunnelled through this bucket, but any code that DOES read/write
   `decline_detection_fields["some_key"]` uses runtime string keys AST cannot
   validate against a schema. Out of scope for `questions.py` (no dict-subscript
   here) but flag it as a known blind spot for downstream consumers.

2. **The `getattr` inside the factories is parameterized** (`getattr(answers, attr)`
   L56; `getattr(answers, answer_key, None)` L71; `getattr(evidence, attr, None)`
   L74). The *literal* lives at the CALL SITE, not at the getattr. FX3 must
   resolve call-site args (the closed-over `attr`/`answer_attr`), NOT the getattr
   in the helper body — scanning only getattr nodes would see variable names and
   learn nothing.

3. **`augment_app_slug` (L28)** — real field, zero deriver references. It is
   populated somewhere outside this file (the `detected_augment_identity`
   question flow, per the comment). A scan of `questions.py` alone cannot confirm
   it is ever set correctly; that write path lives in another module (lockgate /
   diagnosis / CLI — R2/R3 territory). Residual: FX3 verifies field EXISTENCE and
   correct REFERENCE, not correct POPULATION.

4. **`_none_default` (L123-126)** is defined but unused in `SETUP_QUESTIONS`.
   Dead code; harmless, but an AST "every helper is used" check would flag it.
   FX3 should not treat unused helpers as failures.

5. **Non-literal deriver args** — if a future edit passes a *variable* to
   `_answer_default(some_var)` instead of a literal, the AST scan cannot resolve
   `some_var` statically and would have to skip it (or fail-loud on non-`Constant`
   args). Recommend FX3 assert every `_answer_default`/`_evidence_attr` arg node
   is an `ast.Constant` str, so a future dynamic arg can't silently bypass the
   check.

6. **Facade re-export indirection** (`__init__.py` L52-55, 89-97): `SetupAnswers`,
   `SetupQuestion`, `SETUP_QUESTIONS` are lazily resolved via `__getattr__`. FX3
   should import directly from `...contract_setup.questions` (not the facade) to
   AST-parse the source file and to get the concrete `SETUP_QUESTIONS` list and
   dataclasses without triggering unrelated lazy imports. Both paths yield the
   same objects, but parsing the source file requires the module's `__file__`.

---

## 6. Summary for the task author

- **F3 root**: `_evidence_attr` reads the operator answer under
  `answer_key = answer_attr or attr` with a **silent** `getattr(..., None)`
  default (L68, L71). If `answer_key` isn't a real `SetupAnswers` field the
  answer is dropped with no error. The buggy original passed `"pr_number"` (not a
  field); the fix (L136) passes `answer_attr="probe_pr"`.
- **FX3 must**: AST-scan `questions.py`, extract every `_answer_default`
  literal + every `_evidence_attr` `(answer_key, evidence_attr)` pair, and assert
  answer-side names ∈ `dataclasses.fields(SetupAnswers)` and evidence-side names ∈
  `dataclasses.fields(EvidenceBundle)`. Use **subset** direction (allow unused
  fields like `augment_app_slug`). Optionally extend to named-deriver
  `ast.Attribute` access and to a `Constant`-arg guard.
- **Valid sets** are 17 SetupAnswers fields (§4b) and 13 EvidenceBundle attrs
  (§4b), best built at runtime from the dataclasses so the test stays in sync.
- **Blind spots**: dict-key access (`decline_detection_fields`), cross-module
  population (`augment_app_slug`), and non-literal deriver args — none blocking
  the core F3 trap, but worth the `Constant`-arg guard.

Status: Complete
