# R4 — Eval Workspace + Grader Inventory (FR-RSR.10)

Status: Complete
Date: 2026-06-20
Researcher: R4 of 5 (Test & Verification)
Scope: `.dev/eval-workspaces/sc-reflect/` — evals.json, MAIN case dirs, grader.py, skill-snapshot/, falsifier-suite/

Workspace root (absolute): `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/`

---

## 0. Workspace layout (top-level)

```
aggregate_iteration.py
cases/                  ← all case dirs live HERE (NOT under evals/)
evals/evals.json        ← the ONLY file in evals/; it is the registry
grader.py               ← 20,939 bytes; assertion checkers + dispatcher
iterations/             ← EMPTY (run-time output; eval_metadata.json generated here, not checked in)
skill-snapshot/reflect-v1.md   ← pre-change baseline (5,942 bytes / 111 lines)
SPEC.md                 ← 155 KB
```

GOTCHA for the builder: case directories live under `cases/`, NOT under `evals/`. A new UC-2 case must be created at `cases/<name>/` and REGISTERED by an entry in `evals/evals.json`. Entry `case_dir` values are repo-relative to the workspace root, e.g. `"cases/post-small-diff-clean/"`. There is NO `evals/uc2-*` directory convention — that phrasing in the task brief is incorrect; cases go in `cases/uc2-*`.

---

## 1. Registration schema — `evals/evals.json`

Top-level shape: `{ skill_name, iteration, scope, notes, evals: [ ... ] }`.

### Entry count / next ids
- Current entry count: **36** (`grep -c '"id":'` → 36; ids run 1..36 contiguously).
- New companions take ids **37, 38, 39, 40, 41** (5 new cases).

### Per-entry keys (observed across entries)
A `case_dir`-style entry (the kind UC-2 cases use) carries these keys:
- `id` (int)
- `name` (str; matches the case dir name)
- `case_dir` (str; `"cases/<name>/"` — trailing slash present in existing entries)
- `mode` (`"pre"` | `"post"`)  — UC-2 cases use `"post"`
- `use_case` (str; e.g. `"UC-2"`)
- `spec_ref` (str; e.g. `"§12.3 row 2 (line 977)"`)
- `description` (str)
- `inputs` (object; maps logical name → relative path under the case dir, e.g. `{ "diff": "input/diff.patch", "tasklist": "input/tasklist.md" }`)
- `expected` (str; `"expected.yaml"`)
- `assertions` (array of assertion objects)

NOTE: promotion/falsifier entries use `case_file` (a single YAML) + `status` instead of `case_dir`/`inputs`/`expected`. UC-2 MAIN cases follow the `case_dir` shape.

### TEMPLATE — full verbatim existing entry (id 2, the cleanest UC-2 MAIN analogue)
`evals/evals.json` lines 39–80:
```json
{
  "id": 2,
  "name": "post-small-diff-clean",
  "case_dir": "cases/post-small-diff-clean/",
  "mode": "post",
  "use_case": "UC-2",
  "spec_ref": "§12.3 row 2 (line 977)",
  "description": "3-file clean diff with no deviations → expected deviations=[], tier_reached=1, regression_recall=1.0.",
  "inputs": {
    "diff": "input/diff.patch",
    "tasklist": "input/tasklist.md"
  },
  "expected": "expected.yaml",
  "assertions": [
    {
      "type": "file_exists",
      "target": "with_skill/outputs/REPORT.md",
      "text": "REPORT.md is produced"
    },
    {
      "type": "yaml_field",
      "target": "with_skill/outputs/contract.yaml",
      "field": "tier_reached",
      "expected": "1",
      "text": "Tier 1 reached on a clean small diff"
    },
    {
      "type": "regex_absent",
      "target": "with_skill/outputs/REPORT.md",
      "pattern": "deviation_class:\\s*(drift|regression)",
      "text": "No drift/regression deviations falsely emitted on a clean diff"
    }
  ]
}
```

### Assertion object shapes (by `type`) — exact keys each reads
Different assertion types read DIFFERENT keys (the brief's "type, target/matrix/source, pattern, threshold, text" is a union; each type reads only its own subset). Authoritative source = `grader.py` (see §3). Keys observed across evals.json entries 1–3:
- `file_exists`:        `{ type, target, text }`
- `yaml_field`:         `{ type, target, field, expected, text }`  (expected is compared as a STRING)
- `yaml_field_min`:     `{ type, target, field, min_value, text }`  (numeric ≥)
- `regex_present`:      `{ type, target, pattern, text }`
- `regex_absent`:       `{ type, target, pattern, text }`
- `yaml_list_contains`: `{ type, target, field_path, value, text }`
- `matrix_covers_items`:`{ type, matrix, source, threshold, text }`
- `citation_resolves`:  `{ type, report, fixture_root, text }`
- `falsifier_skeleton_present`: `{ type, case_yaml, text }`  (skeleton entries) — also accepts `target` form for NFR-3 runner-gated skeleton (line 994).

CRITICAL run-time partition (grader.py §grade_eval, lines 422–423): assertions are split by the `target` PREFIX. Assertions whose `target` starts with `with_skill/` are graded against the POST-CHANGE skill outputs; `old_skill/` against the snapshot outputs. The dual-snapshot (FAIL-pre / PASS-post) headline behavior is realized by giving the headline eval assertions on BOTH prefixes (or by the runner running the same case twice). Existing UC-2 entries (1–3) only declare `with_skill/...` targets; `old_skill/...` is used once at line 994.

---

## 2. MAIN case directory — structural template

Both `cases/post-small-diff-clean/` and `cases/post-large-diff-mixed/` have the IDENTICAL 3-file layout. A new `cases/uc2-*/` MAIN case must mirror this exactly:

```
cases/<name>/
├── input/
│   ├── diff.patch        ← the change under audit (unified git diff)
│   └── tasklist.md       ← the tasklist the diff is graded against
└── expected.yaml         ← expected outcomes (the oracle; UC-2 shape below)
```

Conventions:
- `input/*` paths are exactly what the entry's `inputs` object points at (`"diff": "input/diff.patch"`, `"tasklist": "input/tasklist.md"`).
- `expected.yaml` is the value of the entry's `expected` key (`"expected.yaml"`).
- Assertions reference `with_skill/outputs/<file>` — these are RUN-TIME outputs produced when the runner executes the skill against the fixture (REPORT.md, contract.yaml, deviation-ledger.yaml, coverage-matrix.yaml, etc.). They do NOT exist in the checked-in case dir; the case dir only ships `input/` + `expected.yaml`.

### `expected.yaml` UC-2 shape (verbatim from post-small-diff-clean — flat top-level keys + nested blocks)
```yaml
mode: post
use_case: UC-2
deviations: []
deviation_counts:
  authorized: 0
  necessary: 0
  drift: 0
  regression: 0
tier_reached: 1
regression_recall: 1.0
calibrated_confidence_min: 0.85
per_task_verdicts:
  - task_id: 1
    verdict: clean_pass
  - task_id: 2
    verdict: clean_pass
  - task_id: 3
    verdict: clean_pass
```
Existing fixtures are marked `# STUB` at the top of each file. The diff.patch is a real unified git diff (docstring-only changes, each hunk mapped 1:1 to a tasklist item); tasklist.md is a `- Task N: ...` bullet list.

GOTCHA — `expected.yaml` is the oracle, NOT a grader target. The checked-in grader assertions read `with_skill/outputs/contract.yaml` etc., not `expected.yaml`. For UC-2 runtime-surface, the NEW runtime fields (`runtime_surface_unreached`, `runtime_surface_degraded`) must be asserted against whatever YAML the post-change skill EMITS at run time (likely `with_skill/outputs/contract.yaml`) — confirm the emitted-field location with R1/R2 (SKILL.md). `expected.yaml` documents the intended oracle values but is not itself graded by the existing assertion types.

---

## 3. `grader.py` — exact checker signatures / assertion-dict keys

Dispatcher at `check_assertion(assertion, base_dir)` (line 294). `base_dir` is the `eval-<name>/` run dir. All checkers return `(bool, str_evidence)`.

### 3a. `regex_absent` (def line 162; dispatch line 391–392)
```python
def check_regex_absent(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
    m = pattern.search(text)
    if m is None:
        return True, f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}"
    return False, f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}"
```
Keys: **`target`** (file, relative to base_dir), **`pattern`** (regex, compiled MULTILINE|DOTALL). PASS when pattern is NOT found. Missing target file ⇒ empty text ⇒ pattern absent ⇒ PASS (note this vacuous-pass on a missing file).

### 3b. `yaml_field` (dispatch line 336–346 — inline in `check_assertion`, NOT a separate function)
```python
if a_type == "yaml_field":
    content = read_text(target_path)
    if not content:
        return False, f"File not readable: {target}"
    y = parse_yaml_simple(content)
    field = assertion["field"]
    expected = str(assertion["expected"])
    actual = y.get(field, "")
    if actual == expected:
        return True, f"YAML field {field}={actual} matches expected {expected}"
    return False, f"YAML field {field}={actual!r}, expected {expected!r}"
```
Keys: **`target`**, **`field`**, **`expected`**. STRING comparison (`expected` coerced via `str()`; actual from parser is a string). Missing/empty file ⇒ FAIL.

### 3c. `yaml_field_min` (dispatch line 348–361 — inline)
```python
if a_type == "yaml_field_min":
    content = read_text(target_path)
    if not content:
        return False, f"File not readable: {target}"
    y = parse_yaml_simple(content)
    field = assertion["field"]
    try:
        actual = float(y.get(field, "0"))
    except (TypeError, ValueError):
        return False, f"YAML field {field} not numeric: {y.get(field)!r}"
    min_val = float(assertion["min_value"])
    if actual >= min_val:
        return True, f"YAML field {field}={actual} >= {min_val}"
    return False, f"YAML field {field}={actual} < {min_val}"
```
Keys: **`target`**, **`field`**, **`min_value`**. Numeric ≥ comparison (both float-coerced). Use this for `runtime_surface_unreached >= 1`. NOTE the key is `min_value` (NOT `value`/`threshold`).

### 3d. CRITICAL parser constraint for yaml_field / yaml_field_min / yaml_substring
These three use `parse_yaml_simple` (def line 58), NOT `yaml.safe_load`:
```python
for line in text.split("\n"):
    line = line.rstrip()
    if not line or line.startswith("#") or line.startswith(" "):
        continue   # ← any indented line is SKIPPED
    if ":" in line:
        k, _, v = line.partition(":")
        v = v.strip().strip("'\"")
        result[k.strip()] = v
```
⇒ It only sees **flat, top-level, non-indented `key: value` pairs**. A `runtime_surface_unreached:` field asserted by `yaml_field`/`yaml_field_min` MUST be a top-level key in the emitted YAML (e.g. `contract.yaml`), NOT nested under a parent. Comment lines (`#`) and indented lines are invisible to it. (The richer checkers — `yaml_list_contains`, `citation_resolves`, `matrix_covers_items`, `deviation_class_matches`, `falsifier_skeleton_present` — use full `yaml.safe_load` and DO handle nesting.)

### 3e. `falsifier_skeleton_present` (def line 270; dispatch line 405–406)
```python
def check_falsifier_skeleton_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    case = base_dir / assertion["case_yaml"]
    if not case.exists():
        return False, f"falsifier case YAML missing: {assertion['case_yaml']}"
    try:
        data = yaml.safe_load(case.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return False, f"falsifier case YAML unparsable: {e}"
    status = data.get("status")
    if status == "skeleton-pending-iteration-3-fixture":
        return True, f"skeleton present (pending iteration-3 fixture); id={data.get('id')!r}"
    if status == "active":
        missing = CANONICAL_FALSIFIER_FIELDS - set(data.keys())
        if missing:
            return False, f"active falsifier missing required fields: {sorted(missing)}"
        return True, f"active falsifier with canonical fields; id={data.get('id')!r}"
    return False, f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'"
```
Keys: **`case_yaml`** (path to the falsifier case YAML). PASS branch 1: `status == "skeleton-pending-iteration-3-fixture"` (vacuous skeleton pass). PASS branch 2: `status == "active"` AND all `CANONICAL_FALSIFIER_FIELDS` present. Any other status ⇒ FAIL. (`CANONICAL_FALSIFIER_FIELDS` per README = `id, type, fixture, expected, assertion`.)

### Other relevant checkers (keys, for completeness)
- `file_exists` (line 300): `{ target }` — PASS if file exists.
- `regex_present` (def 152): `{ target, pattern }` — PASS if pattern FOUND.
- `yaml_list_contains` (def 172): `{ target, field_path (dotted, supports int indices), value }` — full yaml.safe_load; PASS if `value in list_at(field_path)`.
- `citation_resolves` (def ~110): `{ report, fixture_root }` — checks every `file:line` in the report resolves (±5 line window) under fixture_root.

### grade_eval partition (lines 411–460)
Reads `eval_metadata.json` (in the run dir, generated by runner — NOT checked in). Splits `meta["assertions"]` into `with_skill_assertions` (target prefix `with_skill/`) and `old_skill_assertions` (prefix `old_skill/`); grades each, writes `with_skill/grading.json` + `old_skill/grading.json`. This is the mechanism that lets ONE eval entry express both the FAIL-pre (old_skill) and PASS-post (with_skill) sides of the headline.

---

## 4. `skill-snapshot/reflect-v1.md` — pre-change baseline (CONFIRMED)

- Path: `skill-snapshot/reflect-v1.md`. Size: **5,942 bytes / 111 lines**.
- First lines (frontmatter): `name: reflect`, `description: "Task reflection and validation using Serena MCP analysis capabilities"`, `category: special`, `complexity: standard`, `mcp-servers: [serena, context7]`. Body starts `# /sc:reflect - Task Reflection and Validation`.
- CONFIRMED pre-change: `grep -c 'runtime_surface\|reachability\|UC-2'` ⇒ **0 matches**. The snapshot has NO UC-2 / runtime-surface concepts whatsoever — it is the original v1 single-agent skill.
- PURPOSE: it is the **fail-before baseline**. The active headline eval (`uc2-unwired-surface-passes`) runs the skill against BOTH this snapshot (graded via `old_skill/` target prefix → EXPECT FAIL: the v1 skill cannot detect an unwired runtime surface, so the clean-pass marker is absent / the runtime_surface field is missing) AND the post-change `SKILL.md` (graded via `with_skill/` → EXPECT PASS). The builder must know this file EXISTS and is the regression anchor; it does NOT need editing.

---

## 5. `cases/falsifier-suite/` — dual-state lifecycle

Dir contents: `README.md` (5,438 bytes), `T2-converges-on-wrong.yaml`, `T2-judge-class-collision.yaml`, `fixtures/`.

### Dual-state lifecycle (README "Dual-state lifecycle" section)
| State | `status` value | Grader behavior |
|-------|----------------|-----------------|
| Skeleton | `skeleton-pending-iteration-3-fixture` | `falsifier_skeleton_present` returns PASS **vacuously** — only verifies file exists, parses, and has the byte-exact skeleton status string. No runtime assertion. |
| Active | `active` | PASS requires ALL canonical fields (`id, type, fixture, expected, assertion`) present AND (per README §"Active") the runtime canonical assertion `convergence_score < 0.75 OR verdict == regression_present` evaluated by the eval runner. |

"Promote to active with real fixtures" (README "Iteration-3 promotion checklist") requires: (1) replace status string with `active` byte-exact, (2) add canonical fields `type, fixture, expected, assertion`, (3) author the fixture content (e.g. `fixtures/spec-with-deliberate-misclassification.md`), (4) run `make reflect-eval` to confirm the canonical assertion actually TRIGGERS on the broken input, (5) if it does NOT trigger → falsifier succeeded → file incident, DO NOT widen the assertion to force a pass.

### MUST-REMAIN-GREEN + UNMODIFIED
- `cases/falsifier-suite/T2-converges-on-wrong.yaml` — id `T2-converges-on-wrong`, `status: skeleton-pending-iteration-3-fixture`. Registered as evals.json id 19 (line 466) with a single `falsifier_skeleton_present` assertion (`case_yaml: cases/falsifier-suite/T2-converges-on-wrong.yaml`).
- `cases/falsifier-suite/T2-judge-class-collision.yaml` — `status: skeleton-pending-iteration-3-fixture`. Registered as evals.json id 20 (line 482).
- The FR-RSR.10 work MUST NOT modify these two files or their registrations; they stay GREEN by virtue of the vacuous skeleton pass. The 5 new UC-2 cases are MAIN `case_dir` cases, NOT falsifier-suite cases — do not co-locate them under `cases/falsifier-suite/`.

---

## 6. The 5 new eval cases (ids 37–41) — fixtures + assertions per case

All are MAIN `case_dir` UC-2 (`mode: post`) cases at `cases/uc2-*/` with `input/diff.patch` + `input/tasklist.md` + `expected.yaml`, mirroring §2. Assertion keys per §3. The runtime YAML target for new fields is presumed `with_skill/outputs/contract.yaml` (flat top-level keys — see §3d constraint); R1/R2 must confirm the exact emitted filename + that fields are top-level.

### id 37 — `uc2-unwired-surface-passes` (ACTIVE HEADLINE; FAIL-pre / PASS-post)
- Fixtures: a diff that ADDS/EXPOSES a runtime surface (e.g. a CLI subcommand / API route / public entrypoint) that is NOT wired into any caller — i.e. unreachable from any runtime dispatch — plus a tasklist that claims the surface is delivered.
- Assertions (post side, `with_skill/`):
  - `regex_absent` on `with_skill/outputs/REPORT.md` for a false clean-pass marker — i.e. PASS means the clean-pass/"no issues" marker is ABSENT (the skill must NOT emit a clean pass; pattern = the clean-pass string).
  - `yaml_field_min` on `with_skill/outputs/contract.yaml` → `field: runtime_surface_unreached`, `min_value: 1` (≥1 unreached surface detected).
- Assertions (pre side, `old_skill/`): mirror the above with `old_skill/...` targets to assert the v1 snapshot FAILS (e.g. `regex_present` of the clean-pass marker, or `runtime_surface_unreached` field missing ⇒ yaml_field FAIL). This realizes the FAIL-pre / PASS-post headline via the §3e grade_eval prefix partition.

### id 38 — `uc2-surface-positive-control` (REACHED → no false sweep)
- Fixtures: a diff exposing a runtime surface that IS wired (reachable from a runtime entrypoint), + matching tasklist. Plus a non-surface (pure-internal) change as the negative control for "no sweep on non-surface".
- Assertions: `yaml_field` on `contract.yaml` `runtime_surface_unreached` `expected: "0"` (nothing unreached); `regex_absent` for any escalation/STOP marker (the reachable surface must not trigger the unreached escalation). Confirms the sweep does NOT fire on a reachable surface and does NOT run on non-surface diffs.

### id 39 — `uc2-surface-dynamic-dispatch` (degraded, not unreached)
- Fixtures: a diff where the surface is reached only via DYNAMIC dispatch — e.g. `[project.scripts]` entrypoint in pyproject, a decorator-registered handler, or a registry/plugin lookup — so static reachability can't confirm it.
- Assertions: `yaml_field` on `contract.yaml` `field: runtime_surface_degraded` `expected: "true"` (degraded-grounding, dynamic dispatch can't be statically traced); plus an assertion that `regression` count / verdict is UNCHANGED (e.g. `yaml_field` on the regression count = its baseline, or `regex_absent` of a regression class). I.e. degraded ⇒ telemetry flag, NOT a regression.

### id 40 — `uc2-surface-degraded-backend` (backend:none → Grounding Gap, no STOP)
- Fixtures: a diff exposing a surface but with the reachability backend unavailable (`backend: none` — no static-analysis tool present), so the skill must record a Grounding Gap rather than hard-STOP.
- Assertions: `regex_present`/`yaml_substring` for a "Grounding Gap" marker; `regex_absent` on `with_skill/outputs/REPORT.md` for a STOP/halt marker (backend:none must NOT STOP); `regex_absent` of a false clean-pass marker (clean-pass must not be emitted when grounding is degraded). I.e. degraded backend ⇒ Grounding Gap + clean-pass suppressed, no STOP.

### id 41 — `uc2-surface-test-only-ref` (UNREACHED + count invariant)
- Fixtures: a diff exposing a surface that is referenced ONLY from tests (no production/runtime caller) ⇒ classified UNREACHED.
- Assertions: `yaml_field_min` on `contract.yaml` `runtime_surface_unreached` `min_value: 1`; PLUS a COUNT-INVARIANT assertion `len(unreached_surfaces) == runtime_surface_unreached`. The invariant arithmetic cannot be expressed by `parse_yaml_simple` (it can't read a list length, §3d). Options for the builder: (a) emit a precomputed scalar field the skill writes (e.g. `unreached_surfaces_len`) and assert `yaml_field` equality against `runtime_surface_unreached`; OR (b) if `unreached_surfaces` is a top-level YAML list, use the full-yaml checker family — but no existing checker computes `len(list) == scalar`. FLAG TO BUILDER: this invariant likely needs the skill to emit BOTH the list and the matching scalar so two `yaml_field`/`yaml_list_contains` assertions can cross-check, OR a new grader assertion type (coordinate with R3 grader-extensions.md). Document the chosen mechanism explicitly.

### Registration note
Each of the 5 gets a new object appended to the `evals` array in `evals/evals.json` with the next id (37–41), `case_dir: "cases/uc2-<name>/"`, `mode: "post"`, `use_case: "UC-2"`, a `spec_ref` to TDD §15.2 / FR-RSR.10, `inputs: { diff: "input/diff.patch", tasklist: "input/tasklist.md" }`, `expected: "expected.yaml"`, and the assertions above. Update the top-level `scope`/`notes` strings if the builder wants to record the +5 UC-2 reachability cases (optional; existing notes already enumerate prior batches).

---

## 7. Summary for the builder (key load-bearing facts)

1. **Registry**: `evals/evals.json`, 36 entries today → new ids **37–41**. Template entry = id 2 verbatim (§1). MAIN cases use the `case_dir` shape (NOT `case_file`).
2. **Case layout**: `cases/<name>/{input/diff.patch, input/tasklist.md, expected.yaml}` — copy from `cases/post-small-diff-clean/`. Cases go in `cases/`, NOT `evals/`. Runtime outputs (`with_skill/outputs/*`) are produced by the runner, not checked in.
3. **Grader key contracts**: `regex_absent` reads `{target, pattern}` (PASS=absent); `yaml_field` reads `{target, field, expected}` (string ==); `yaml_field_min` reads `{target, field, min_value}` (numeric ≥, key is `min_value` not `value`); `falsifier_skeleton_present` reads `{case_yaml}`.
4. **HARD CONSTRAINT**: `yaml_field`/`yaml_field_min` use `parse_yaml_simple` → only flat, top-level, non-indented `key: value` lines. `runtime_surface_unreached`/`runtime_surface_degraded` MUST be emitted as top-level scalars in the asserted YAML (likely `contract.yaml`). The `len(unreached)==count` invariant (id 41) CANNOT be done by existing checkers — needs a precomputed scalar pair or a new grader type (coordinate R3).
5. **Dual-snapshot headline**: grade_eval partitions assertions by `target` prefix `with_skill/` (post → PASS) vs `old_skill/` (pre snapshot → FAIL). `skill-snapshot/reflect-v1.md` (111 lines, 0 runtime_surface refs) is the confirmed fail-before baseline.
6. **Do NOT touch**: `cases/falsifier-suite/T2-converges-on-wrong.yaml` + `T2-judge-class-collision.yaml` (ids 19/20) — stay GREEN via vacuous skeleton pass; new cases are MAIN cases, not falsifier cases.

---
