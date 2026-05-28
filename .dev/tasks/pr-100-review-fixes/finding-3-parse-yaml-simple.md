# Finding 3 — `parse_yaml_simple` drops nested values (r3312667807)

## Reviewer claim

> `parse_yaml_simple()` ignores any indented lines, so any top-level YAML key whose value is a nested mapping/list (e.g., `enrichment_used`, `token_usage`) is parsed as an empty string and its nested content becomes uncheckable. This can lead to false negatives (or silently skipped validation) if assertions ever need to inspect nested return-contract fields.

## Validation result

**CONFIRMED** (latent — no current false negatives, but the hazard is real).

Evidence from `origin/chore/brainstorm-live-evals`:

- `.dev/eval-workspaces/sc-brainstorm/grader.py:45-57` — `parse_yaml_simple` explicitly does `if not line or line.startswith("#") or line.startswith(" "): continue`, silently skipping every indented line. A top-level key like `enrichment_used:` (no inline value) then hits the `if ":" in line` branch, splits as `("enrichment_used", "", "")`, and gets stored as `result["enrichment_used"] = ""`. Same fate for `token_usage:`, `wave_durations_ms:`, `enrichment_artifact_sizes:` in real contract files (see `.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-code-add-rate-limiting/with_skill/outputs/return-contract.yaml:9-37`).
- `grader.py:135-167` — `check_assertion` consumes the parsed dict only via `y.get(field, "")`, `float(y.get(field, "0"))`, and substring scans over the string. With nested keys flattened to `""`, every `yaml_field` / `yaml_field_min` / `yaml_substring` assertion targeting a nested key would pass-or-fail purely on the empty-string comparison — `yaml_field` with `expected=""` would falsely PASS; `yaml_field_min` would fail with a non-numeric error; `yaml_substring` would always fail. None of these surface a meaningful diagnostic about the nesting.
- Audit of every `"field":` in `iterations/**/eval_metadata.json` (iteration-1 + iteration-2) shows current targets are all top-level scalars: `contract_version`, `status`, `convergence_score`, `domain`, `strategy`, `handoff_action`, `handoff_output_path`, `proposal_count`, `agent_spec`, `adversarial_status`, `depth`, `blind_mode`, `blind_labels`, `interactive_mode`, `spec_type`, `handoff_target`. No assertion currently dotted-references nested keys (`enrichment_used.source`, `token_usage.wave_3`, etc.) — so the parser is producing correct results today, but any future assertion of nested return-contract content (which the contract schema explicitly defines as nested) would silently misbehave.

## Root cause

A line-oriented parser written under the simplifying assumption that "the contract is flat top-level scalars" — implemented by treating any leading-whitespace line as a comment/skip. The docstring even advertises this: `"Parse a simple flat YAML file (no nesting)."` (`grader.py:46`). The risk is the parser shares its name with general YAML and is now applied to a contract that *is* nested (`return-contract.yaml` has four nested blocks).

## Proposed fix

**Chosen option:** **A — replace with `yaml.safe_load`.** `pyyaml>=6.0` is already a top-level project dependency (`pyproject.toml` — `dependencies = [ ... "pyyaml>=6.0", ... ]`), so no new dep is needed. Option B (indent-aware hand parser) is strictly worse: more code, more bugs, no upside given pyyaml is already present.

**Files to change:**

- `.dev/eval-workspaces/sc-brainstorm/grader.py` lines `45-57`: replace `parse_yaml_simple` body with `yaml.safe_load(text) or {}`; add `import yaml` at the top alongside existing imports (line 21-24). Keep the function name and signature so callers (`grader.py:151, 162, 176`) need no edits.
- `.dev/eval-workspaces/sc-brainstorm/grader.py` lines `135-167` (`check_assertion`, the three `yaml_*` branches): **optional, recommended** — extend `field` resolution to support dotted paths (e.g., `enrichment_used.0.source`, `token_usage.wave_3`) via a small `_get_dotted(d, path)` helper so future assertions can reach nested values. Without this, the fix unblocks `yaml.safe_load` returning nested dicts/lists, but `y.get("enrichment_used", "")` would now return a list instead of `""` and downstream `.lower()` / `float(...)` calls would raise — so either (a) coerce non-scalars to `repr()` for the substring branch and skip them for the numeric branch with a clear evidence message, or (b) add dotted-path resolution. (b) is the cleaner option and matches what the reviewer is gesturing toward.
- `pyproject.toml` — no change required; `pyyaml>=6.0` is already declared.

**Exact diff sketch:**

```diff
 import json
 import re
 import sys
 from pathlib import Path
+import yaml

@@
-def parse_yaml_simple(text: str) -> dict:
-    """Parse a simple flat YAML file (no nesting). Returns dict of string values."""
-    if not text:
-        return {}
-    result = {}
-    for line in text.split("\n"):
-        line = line.rstrip()
-        if not line or line.startswith("#") or line.startswith(" "):
-            continue
-        if ":" in line:
-            k, _, v = line.partition(":")
-            v = v.strip().strip("'\"")
-            result[k.strip()] = v
-    return result
+def parse_yaml_simple(text: str) -> dict:
+    """Parse YAML. Returns dict (possibly nested). Empty/invalid input → {}."""
+    if not text:
+        return {}
+    try:
+        loaded = yaml.safe_load(text)
+    except yaml.YAMLError:
+        return {}
+    return loaded if isinstance(loaded, dict) else {}
+
+
+def _resolve_field(d: dict, path: str):
+    """Resolve dotted path 'a.b.0.c' through nested dicts/lists. Returns '' if missing."""
+    cur = d
+    for part in path.split("."):
+        if isinstance(cur, list):
+            try:
+                cur = cur[int(part)]
+            except (ValueError, IndexError):
+                return ""
+        elif isinstance(cur, dict):
+            cur = cur.get(part, "")
+        else:
+            return ""
+    return cur
```

Then in the three `yaml_*` branches of `check_assertion`, replace `y.get(field, "")` with `_resolve_field(y, field)` and coerce the result to `str(...)` before `.lower()` / substring checks (and reject non-numeric values cleanly in `yaml_field_min`).

## Risk / blast radius

Two callers index the returned dict with `.get(str)` and currently assume the value is a string: `actual.lower() == expected.lower()` (`grader.py:153`) and `s.lower() in actual.lower()` (`grader.py:174`). With `yaml.safe_load`, top-level scalars like `contract_version: "1.0"`, `status: success`, `domain: code` still come back as strings, so existing iteration-1/iteration-2 assertions remain correct (verified — every current `"field"` value is a top-level scalar). The risk is if a future assertion targets a top-level *block* key (e.g., `field: enrichment_used` with no dotted path), where `_resolve_field` would now return a list and `.lower()` would raise — guard with `str(actual)` coercion or `isinstance` checks in the three `yaml_*` branches when wiring `_resolve_field`. Numeric-typed scalars (`convergence_score: 0.78`) become `float` instead of `str`, but the only consumer is `yaml_field_min` which already does `float(y.get(...))` — `float(0.78)` works the same as `float("0.78")`, so no regression.

## Confidence

**95%** — Bug confirmed by reading the parser body and tracing both real contract YAML and every current assertion target. Fix path is unambiguous given pyyaml is already a declared dependency; only judgment call is whether to ship the optional dotted-path resolver in the same change (recommended — it's what the reviewer's "uncheckable" framing is pointing at, and skipping it leaves a sharp edge where a future assertion could throw `AttributeError` on `.lower()`).
