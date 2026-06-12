# Grader DSL Extensions for sc-reflect

This reference specifies the assertion types `grader.py` must implement for sc-reflect eval cases, **beyond** the 8 syntactic types inherited from sc-brainstorm's `grader.py`. All 9 types documented here are **truly new** — none exist in the baseline grader (verified against `.dev/eval-workspaces/sc-brainstorm/grader.py`, 279 lines).

Implementation pattern follows the baseline's `check_assertion(assertion: dict, base_dir: Path) -> tuple[bool, str]` dispatcher. Each new type adds another `if a_type == "..."` branch returning `(passed: bool, evidence: str)`. Sketches below assume `import yaml` (PyYAML) is available; the baseline grader's hand-rolled `parse_yaml_simple` is insufficient for nested YAML used by §12.4 / §12.5 / §14.5.7 assertions.

## New assertion types overview

Baseline (sc-brainstorm, 8 syntactic): `file_exists`, `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, `dir_count`.

| # | Name | Purpose | Fixture input | Output | Complexity |
|---|------|---------|---------------|--------|------------|
| 1 | `citation_resolves` | Re-Read cited `file:line` and verify snippet match (±5 lines) | REPORT.md, optional `fixture_root` remap | `(passed, evidence)` with cited+actual snippet | Medium |
| 2 | `regex_present` | Pattern presence (seeded requirement mention) | Target file, `pattern` | `(passed, match_count)` | Low |
| 3 | `regex_absent` | Pattern absence (false clean-pass detection) | Target file, `pattern` | `(passed, first_match_or_clean)` | Low |
| 4 | `yaml_list_contains` | Nested YAML list-field membership | YAML file, `field_path`, `value` | `(passed, list_contents)` | Low |
| 5 | `matrix_covers_items` | Coverage matrix covers ≥ threshold of source items | matrix YAML, source-fixture path, threshold | `(passed, coverage_ratio)` | Medium |
| 6 | `checkpoint_logged` | `audit.log` has row for named checkpoint | audit.log JSONL, `checkpoint_name` | `(passed, matching_rows)` | Low |
| 7 | `deviation_class_matches` | Report register tags annotated diff with same class | report deviation register, annotated fixture | `(passed, expected_vs_actual)` | Medium |
| 8 | `path_exists` | Verify path exists post-promotion (§14.5.7) | Path string | `(passed, stat_info)` | Trivial |
| 9 | `path_does_not_exist` | Inverse: source removed after move (§14.5.7) | Path string | `(passed, absence_evidence)` | Trivial |
| 10 | `falsifier_skeleton_present` | `falsifier-suite/<case>.yaml` parses + meets skeleton-OR-active contract | Case YAML | `(passed, status_and_telemetry)` | Medium |

Count: **9 truly-new types** (rows 1–9 in the §12.4 / §14.5.7 specs plus #10 from §12.5). Including the falsifier assertion brings the new total to 10; the spec text in §12.4 enumerates 6 semantic types + §14.5.7 adds 2 path types + §12.5 adds 1 falsifier = **9 truly new** when `regex_present` and `regex_absent` are counted as one row (they are listed together in the §12.4 bullet). This document treats them as separate assertion types for implementation clarity.

## citation_resolves

```python
def citation_resolves(report_path: str, fixture_root: str = None) -> AssertionResult: ...
```

**Semantics.** Parse `REPORT.md` for citations of the shape `path/to/file.py:LINE` or `path/to/file.md:LINE`. For each citation, re-Read the referenced file and verify the surrounding ±5 lines contain the snippet quoted in the report. When `fixture_root` is provided, remap the citation's path so synthetic-eval diffs (which live under `fixtures/<case>/`) resolve to the in-fixture file rather than the absolute repo path.

```python
import re
from pathlib import Path

CITATION_RE = re.compile(r"`?([\w./\-]+\.(?:py|md|yaml|ts|js)):(\d+)`?")

def check_citation_resolves(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    report = (base_dir / assertion["report"]).read_text(encoding="utf-8")
    fixture_root = Path(assertion.get("fixture_root", base_dir))
    resolved, failed = 0, []
    for m in CITATION_RE.finditer(report):
        rel_path, line_no = m.group(1), int(m.group(2))
        target = (fixture_root / rel_path) if not Path(rel_path).is_absolute() else Path(rel_path)
        if not target.exists():
            failed.append(f"{rel_path}:{line_no} (file missing)")
            continue
        lines = target.read_text(encoding="utf-8").splitlines()
        window = "\n".join(lines[max(0, line_no - 6):line_no + 5])
        # Optional snippet check: assertion may carry expected substring
        snippet = assertion.get("expected_snippets", {}).get(f"{rel_path}:{line_no}")
        if snippet and snippet not in window:
            failed.append(f"{rel_path}:{line_no} (snippet not in ±5 window)")
        else:
            resolved += 1
    total = resolved + len(failed)
    return (len(failed) == 0, f"{resolved}/{total} citations resolved; failures={failed}")
```

## regex_present

```python
def regex_present(target: str, pattern: str) -> AssertionResult: ...
```

**Semantics.** Open the target file relative to `base_dir`, search for `pattern` (Python regex, MULTILINE | DOTALL by default). Pass when ≥1 match. Used to verify seeded requirements ("the report mentions REQ-AUTH-42") survived the reviewer pass.

```python
import re

def check_regex_present(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
    matches = pattern.findall(text)
    if matches:
        return True, f"Pattern {assertion['pattern']!r} found {len(matches)} match(es) in {assertion['target']}"
    return False, f"Pattern {assertion['pattern']!r} NOT found in {assertion['target']}"
```

## regex_absent

```python
def regex_absent(target: str, pattern: str) -> AssertionResult: ...
```

**Semantics.** Inverse of `regex_present`. Used for false-clean-pass detection: e.g., assert that a regression-laden report does NOT contain the phrase `verdict: clean_pass`.

```python
import re

def check_regex_absent(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    text = target.read_text(encoding="utf-8") if target.exists() else ""
    pattern = re.compile(assertion["pattern"], re.MULTILINE | re.DOTALL)
    m = pattern.search(text)
    if m is None:
        return True, f"Pattern {assertion['pattern']!r} correctly absent from {assertion['target']}"
    return False, f"Pattern {assertion['pattern']!r} unexpectedly present at offset {m.start()}: {m.group(0)[:80]!r}"
```

## yaml_list_contains

```python
def yaml_list_contains(target: str, field_path: str, value: str) -> AssertionResult: ...
```

**Semantics.** Load the YAML file, traverse nested `field_path` (dotted, e.g., `deviations.0.deviation_class`), confirm the resolved node is a list and contains `value`. Canonical example: `deviation-ledger.yaml` field `deviations[*].deviation_class` contains `regression`.

```python
import yaml
from functools import reduce

def check_yaml_list_contains(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    if not target.exists():
        return False, f"YAML file missing: {assertion['target']}"
    data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    keys = assertion["field_path"].split(".")
    try:
        node = reduce(lambda d, k: d[int(k)] if k.isdigit() else d[k], keys, data)
    except (KeyError, IndexError, TypeError) as e:
        return False, f"field_path {assertion['field_path']!r} unresolvable: {e}"
    if not isinstance(node, list):
        return False, f"field_path {assertion['field_path']!r} is not a list (got {type(node).__name__})"
    expected = assertion["value"]
    if expected in node:
        return True, f"List at {assertion['field_path']} contains {expected!r}; members={node}"
    return False, f"List at {assertion['field_path']} missing {expected!r}; members={node}"
```

## matrix_covers_items

```python
def matrix_covers_items(matrix: str, source: str, threshold: float) -> AssertionResult: ...
```

**Semantics.** Load coverage matrix YAML (a list of `{item_id, status}` rows) and the source fixture (which enumerates the requirements/items to be covered). Compute `coverage = len({row.item_id : status != "uncovered"}) / len(source_items)`. Pass when `coverage >= threshold`.

```python
import yaml

def check_matrix_covers_items(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    matrix_path = base_dir / assertion["matrix"]
    source_path = base_dir / assertion["source"]
    threshold = float(assertion.get("threshold", 0.8))
    matrix = yaml.safe_load(matrix_path.read_text(encoding="utf-8")) or []
    source = yaml.safe_load(source_path.read_text(encoding="utf-8")) or {}
    source_items = {item["id"] for item in source.get("items", [])}
    covered = {row["item_id"] for row in matrix if row.get("status") and row["status"] != "uncovered"}
    if not source_items:
        return False, "Source fixture has no items to cover"
    ratio = len(covered & source_items) / len(source_items)
    if ratio >= threshold:
        return True, f"Coverage {ratio:.2%} >= {threshold:.2%} ({len(covered & source_items)}/{len(source_items)} items)"
    return False, f"Coverage {ratio:.2%} < {threshold:.2%}; missing={sorted(source_items - covered)}"
```

## checkpoint_logged

```python
def checkpoint_logged(audit_log: str, checkpoint_name: str) -> AssertionResult: ...
```

**Semantics.** Read `audit.log` as JSONL (one event per line, schema `{ts, step, checkpoint, ...}`). Pass when ≥1 row has `checkpoint == checkpoint_name`. Confirms scripted Serena think-checkpoints and audit-emit-per-step actually fired.

```python
import json

def check_checkpoint_logged(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    audit = base_dir / assertion["audit_log"]
    if not audit.exists():
        return False, f"audit.log missing: {assertion['audit_log']}"
    name = assertion["checkpoint_name"]
    matches = []
    for i, raw in enumerate(audit.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if row.get("checkpoint") == name:
            matches.append((i, row.get("step"), row.get("ts")))
    if matches:
        return True, f"checkpoint {name!r} logged {len(matches)}x; first={matches[0]}"
    return False, f"checkpoint {name!r} not found in {assertion['audit_log']}"
```

## deviation_class_matches

```python
def deviation_class_matches(report: str, annotated_fixture: str, diff_hunk_id: str) -> AssertionResult: ...
```

**Semantics.** Load the annotated eval fixture (which tags each diff hunk with its true deviation class per §10) and the report's deviation register. For the given `diff_hunk_id`, confirm the report tags the same hunk with the same class (`authorized` / `necessary` / `drift` / `regression` — the canonical 4-category set per spec §10.1-§10.4).

```python
import yaml

def check_deviation_class_matches(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    fixture = yaml.safe_load((base_dir / assertion["annotated_fixture"]).read_text(encoding="utf-8")) or {}
    report = yaml.safe_load((base_dir / assertion["report"]).read_text(encoding="utf-8")) or {}
    hunk_id = assertion["diff_hunk_id"]
    expected = next((h["deviation_class"] for h in fixture.get("hunks", []) if h["id"] == hunk_id), None)
    actual = next((e["deviation_class"] for e in report.get("deviation_register", []) if e.get("hunk_id") == hunk_id), None)
    if expected is None:
        return False, f"hunk {hunk_id!r} not present in annotated fixture"
    if expected == actual:
        return True, f"hunk {hunk_id} class matches: {expected}"
    return False, f"hunk {hunk_id} expected {expected!r}, report has {actual!r}"
```

## path_exists

```python
def path_exists(target: str) -> AssertionResult: ...
```

**Semantics.** After a promotion mutation (§14.5.7 step 7.4), confirm the destination path exists (either file or directory). Pass when `Path(target).exists()`. Used by `promotion-task-strict-pass`, `promotion-sprint-release-pass`, and `promotion-cross-fs-crash-recovery`.

```python
from pathlib import Path

def check_path_exists(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = Path(assertion["target"])
    target = target if target.is_absolute() else (base_dir / target)
    if target.exists():
        stat = target.stat()
        kind = "dir" if target.is_dir() else "file"
        return True, f"path exists ({kind}, {stat.st_size} bytes): {target}"
    return False, f"path does not exist: {target}"
```

## path_does_not_exist

```python
def path_does_not_exist(target: str) -> AssertionResult: ...
```

**Semantics.** Inverse of `path_exists`. After a successful move, confirm the source path was removed. Used by `promotion-task-strict-pass` (source `.dev/tasks/to-do/TASK-EVAL-001/` removed) and `promotion-collision-identical` (idempotent re-run).

```python
from pathlib import Path

def check_path_does_not_exist(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = Path(assertion["target"])
    target = target if target.is_absolute() else (base_dir / target)
    if not target.exists():
        return True, f"path correctly absent: {target}"
    kind = "dir" if target.is_dir() else "file"
    return False, f"path unexpectedly present ({kind}): {target}"
```

## falsifier_skeleton_present

```python
def falsifier_skeleton_present(case_yaml: str) -> AssertionResult: ...
```

**Semantics.** Verify `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/<case>.yaml` exists and parses, then enforce the §12.5 two-state contract:

1. `status: skeleton-pending-iteration-3-fixture` AND grader emits `skeleton_present: true` telemetry row → pass (acceptable in iteration-1 and iteration-2).
2. `status: active` AND meets the canonical assertion `convergence_score < 0.75 OR verdict == regression_present` against the iteration-3 fixture run → pass.

Any other `status` value fails. Missing canonical fields (`id`, `type`, `fixture`, `expected`, `assertion`) when `status: active` fails.

```python
import yaml
from pathlib import Path

CANONICAL_FIELDS = {"id", "type", "fixture", "expected", "assertion"}

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
        missing = CANONICAL_FIELDS - set(data.keys())
        if missing:
            return False, f"active falsifier missing required fields: {sorted(missing)}"
        # Iteration-3 grading: caller must additionally evaluate the runtime
        # `convergence_score < 0.75 OR verdict == regression_present` assertion
        # against the case's executed run results. This function confirms only
        # the structural contract; the runtime check is layered by the eval runner.
        return True, f"active falsifier with canonical fields; id={data.get('id')!r}"
    return False, f"unexpected status {status!r}; expected 'skeleton-pending-iteration-3-fixture' or 'active'"
```

## Wiring into `check_assertion`

Each new type is registered in the dispatcher by appending an `elif a_type == "<name>": return check_<name>(assertion, base_dir)` branch after the 8 baseline branches. The dispatcher signature is unchanged from sc-brainstorm's `grader.py`. The `import yaml` (PyYAML) requirement is added to the grader's module header — the baseline's hand-rolled `parse_yaml_simple` is retained for backward compatibility with the 8 inherited types but is NOT used by the new types defined here.

## D13 coverage-hardening fixtures (Step 1B.0 / 1B.2b)

Three eval fixtures pin the D13 two-pass extraction + parse-density guard (upstream change-spec: rf-harness D13; see the PR that introduced this section). They belong in `.dev/eval-workspaces/sc-reflect/cases/` alongside the existing case set; this section is the authoritative contract for authoring them:

1. **`sparse-labeled-spec`**: a spec fixture with 3 labeled requirements (`REQ-1..3`) and 8+ unlabeled requirement-bearing statements (MUST/SHALL imperatives, acceptance bullets). Assertions: `yaml_field` on return-contract.yaml proves `coverage_degraded: parsed-sparse`, `tier_reached: 2` (even at `--depth standard`), `coverage_pct_union` non-null, and `unmapped_requirements_union` present; `matrix_covers_items` over the union source fixture at threshold 0.85+; `section_present` on REPORT.md for `## Inferred requirements (Pass 2)`; every INF row passes `citation_resolves` against REPORT.md (the verbatim quote matches its cited spec lines); `regex_present` on the qa reviewer brief file (reviewer-briefs/reviewer-N.md for the qa persona) proving the spec-body grounding hunk header is present.
2. **`fabricated-inference`**: a doctored run whose matrix contains one INF row citing lines that do NOT contain its quote. Assertions (per-file targets named because regex assertions are file-scoped): `citation_resolves` against the doctored matrix YAML FAILS on the doctored row; `regex_absent` for the doctored INF id targeting the FINAL coverage-matrix artifact (post-validator); `regex_present` for the same id targeting REPORT.md (the drop postscript inside the Inferred-requirements section); `yaml_field` on return-contract.yaml proves `coverage_pct_union` reflects the post-drop recompute and `status: partial` per the dropped-citation rule.
3. **`range-notation`**: a spec fixture containing the single token `SPEC-001..021` plus a tasklist matching 18 of the 21. Assertions: the eval runner loads the matrix YAML and asserts `len(rows) == 21` with every row `source: parsed` (a direct length check; `matrix_covers_items` alone proves coverage ratio, not row count); `yaml_field` on return-contract.yaml proves `coverage_pct` = 0.8571 (18/21, 4 decimals; parsed semantics per contract 1.5.0); `regex_absent` for any literal `SPEC-001..021` row id targeting the matrix YAML (the range token itself never becomes a row).

Backward-compatibility invariant (scoped): pre-existing fixtures keep passing unchanged because `coverage_pct` and `unmapped_requirements` retain parsed-only semantics at contract 1.5.0, and per-row `source: parsed` filters give legacy matrix assertions their pre-D13 view. EXCEPTION, stated honestly: any legacy fixture whose spec is zero-LABEL but prose-RICH previously hit the coverage_undefined route and now exercises Pass 2 instead (INF rows + the parse-density guard); such fixtures migrate to the sparse-labeled pattern above. Fixtures with truly empty/ID-free AND requirement-free specs still hit coverage_undefined unchanged.
