# Research 04 — Eval-Path Integration (Code Tracer)

**Task:** TASK-TDD-20260621-124414
**Topic:** How the sc-reflect eval harness grades the runtime-surface (FR-RSR) contract, and how it would invoke the deterministic reachability module so the eval becomes deterministic (testing-strategy §15 input).
**Investigation type:** Code Tracer.
**Component root:** `.dev/eval-workspaces/sc-reflect/`

All file paths are absolute under `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`.
Each claim is tagged `[CODE-VERIFIED]` (read from the live file this turn) or `[INFERRED]` (reasoned, not directly read).

Files read this turn:
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/grader.py` (518 lines)
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect/evals/evals.json` (1134 lines)
- the 5 `cases/uc2-*/expected.yaml` fixtures
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md`
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` (via grep) and `SKILL.md` §4b/§4b' (via grep)

---

## 1. The dispatcher mechanism

`check_assertion(assertion: dict, base_dir: Path) -> tuple[bool, str]` is the single dispatch point, at `grader.py:318`. [CODE-VERIFIED]

- It reads `a_type = assertion.get("type")` (`grader.py:320`) and runs a flat chain of `if a_type == "..."` branches. There is **no elif** — every branch returns inside the `if`, so the chain is effectively a switch. [CODE-VERIFIED]
- The **8 baseline (sc-brainstorm-inherited) types** are implemented inline inside `check_assertion` (`grader.py:324-408`): `file_exists`, `frontmatter_field`, `section_present`, `section_enumerated`, `yaml_field`, `yaml_field_min`, `yaml_substring`, `dir_count`. [CODE-VERIFIED]
- The **11 new types** are delegated to module-level `check_<name>` helper functions (`grader.py:410-432`): `citation_resolves`, `regex_present`, `regex_absent`, `yaml_list_contains`, `yaml_list_len_eq`, `matrix_covers_items`, `checkpoint_logged`, `deviation_class_matches`, `path_exists`, `path_does_not_exist`, `falsifier_skeleton_present`. [CODE-VERIFIED]
- Unknown type → `return False, f"Unknown assertion type: {a_type}"` (`grader.py:434`). A typo in `type` fails closed, not silently passes. [CODE-VERIFIED]

**How an assertion is routed to a configuration (with_skill vs old_skill).** Routing is by the `target` string prefix, NOT by an explicit config field. In `grade_eval` (`grader.py:437-484`):
- `with_skill_assertions = [a for a in assertions if a.get("target", "").startswith("with_skill/")]` (`grader.py:448`) [CODE-VERIFIED]
- `old_skill_assertions = [a for a in assertions if a.get("target", "").startswith("old_skill/")]` (`grader.py:449`) [CODE-VERIFIED]
- `build_grading` calls `check_assertion(a, eval_dir)` with `base_dir = eval_dir` (the `eval-<name>/` dir), writes `with_skill/grading.json` and `old_skill/grading.json`, and aggregates `{passed, failed, total, pass_rate}`. [CODE-VERIFIED]

**Consequence for the multi-target assertion types** (`citation_resolves`, `matrix_covers_items`, `deviation_class_matches`, `checkpoint_logged`, `path_exists`, `falsifier_skeleton_present`): these do **not** use a `target` key — they use `report`/`matrix`/`audit_log`/`case_yaml`/etc. So `assertion.get("target","").startswith("with_skill/")` is `False` for them, and they fall into **neither** config bucket and are never graded. The 5 UC-2 cases avoid this trap — every UC-2 assertion uses a `target` key (see §3) — and `yaml_list_len_eq` itself does carry `target` (it is the contract.yaml path). So routing is correct for the FR-RSR cases. [CODE-VERIFIED — the bucketing logic at grader.py:448-449 plus the per-case assertion shapes in §3.]

**Entry point.** `main()` (`grader.py:487`) takes one CLI arg, an `iterations/iteration-N/` dir, iterates its `eval-*/` subdirs, and calls `grade_eval` on each. It reads `eval_metadata.json` (per eval-dir) for the `assertions` list — NOT `evals.json` directly. So `evals.json` is the **registry/spec**; the executable per-iteration assertion list is `eval_metadata.json`, materialized from `evals.json` at run time. [CODE-VERIFIED for grader.py:440-446; INFERRED for the materialization step — no materializer was read this turn.]

---

## 2. `check_yaml_list_len_eq` — signature and logic (the FR-RSR count-invariant checker)

Defined at `grader.py:191`. [CODE-VERIFIED]

```python
def check_yaml_list_len_eq(assertion: dict, base_dir: Path) -> tuple[bool, str]:
    target = base_dir / assertion["target"]
    if not target.exists():
        return False, f"YAML file missing: {assertion['target']}"
    data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    list_field = assertion["list_field"]
    count_field = assertion["count_field"]
    items = data.get(list_field)
    if not isinstance(items, list):
        return False, f"{list_field!r} is not a list (got {type(items).__name__})"
    try:
        expected = int(data[count_field])
    except KeyError:
        return False, f"count field {count_field!r} missing"
    except (TypeError, ValueError):
        return False, f"count field {count_field!r} not an integer: {data.get(count_field)!r}"
    actual = len(items)
    if actual == expected:
        return True, f"len({list_field}) == {count_field} == {actual}"
    return False, f"len({list_field})={actual}, {count_field}={expected}"
```

**Assertion keys it consumes:** `target` (YAML file path, relative to `base_dir`), `list_field` (top-level list key), `count_field` (top-level scalar count key). [CODE-VERIFIED grader.py:192-197]

**Logic / semantics (all [CODE-VERIFIED]):**
1. Resolves `target` against `base_dir` (the eval-dir); missing file → fail with a specific message (`grader.py:192-194`).
2. Parses with **`yaml.safe_load`** — the proper nested parser, NOT the legacy hand-rolled `parse_yaml_simple`. This matters: `unreached_surfaces` is a list of dicts, which `parse_yaml_simple` cannot represent. (`grader.py:195`)
3. Reads `list_field` and requires it to be a `list`; a non-list (e.g. `None` when the key is absent) fails with `"'<field>' is not a list (got NoneType)"` (`grader.py:198-200`).
4. Reads `count_field`, coerces via `int(...)`; **missing key** → `KeyError` branch ("count field ... missing"); **non-int** → `(TypeError, ValueError)` branch ("not an integer") (`grader.py:201-206`).
5. Passes iff `len(items) == int(count_field)` (`grader.py:207-210`).

**What it enforces:** the FR-RSR count invariant `len(unreached_surfaces) == runtime_surface_unreached`, computed *from the two already-emitted contract fields*. Per `grader-extensions.md:141`, it **does not require or authorize a producer-emitted helper scalar** such as `unreached_surfaces_len`; it derives the length itself. [CODE-VERIFIED grader-extensions.md:135-166]

**Self-consistency-only caveat (load-bearing for §5).** This check is an *internal consistency* gate: it verifies the producer's own list length matches the producer's own scalar. Both operands come from the same LLM-emitted `contract.yaml`. If the producer emits `runtime_surface_unreached: 2` with a 2-element `unreached_surfaces`, the assertion PASSES even if the *correct* answer is 1 (i.e. the LLM hallucinated a coherent-but-wrong pair). The grader's docstring header explicitly notes the FR-RSR checker "currently grades LLM-emitted scalars" — it cannot, by construction, catch a self-consistent fabrication. This is the precise reason §5 / testing-strategy §15 wants the deterministic module wired in. [CODE-VERIFIED grader.py:191-210 + the task brief's framing; INFERRED that this is the §15 motivation.]

---

## 3. The `case_dir` registry structure in `evals.json` + the 5 UC-2 cases

**Registry shape.** `evals.json` is a top-level object `{skill_name, iteration, scope, notes, evals: [...], grading_criteria: [...]}`. The `grading_criteria` array (`evals.json:1112-1132`) enumerates all 19 supported assertion types (8 baseline + 11 new), matching the dispatcher. [CODE-VERIFIED]

**Per-eval entry shape.** Each element of `evals[]` carries `{id, name, mode, use_case, spec_ref, description, inputs, expected, assertions[]}` and EITHER a `case_dir` (directory-backed cases) OR a `case_file` (single-YAML promotion/falsifier cases). [CODE-VERIFIED — e.g. id 1 uses `case_dir`, id 4 uses `case_file`.]

**The 5 FR-RSR UC-2 cases are ids 37-41**, all `case_dir`-backed under `cases/uc2-*/`, all `mode: post`, `use_case: UC-2`, `spec_ref: "FR-RSR.10 / TDD §15.2"`, each with `inputs: {diff: input/diff.patch, tasklist: input/tasklist.md}` and `expected: expected.yaml`. [CODE-VERIFIED evals.json:1030-1110]. On disk each `cases/uc2-*/` holds `expected.yaml` + `input/{diff.patch, tasklist.md}` (no `with_skill/` outputs yet — these are scaffolds whose assertions target a *future* run's `with_skill/outputs/`). [CODE-VERIFIED via `ls`]

The `notes` field (`evals.json:5`) explicitly records: *"FR-RSR UC-2 reachability cases live under cases/uc2-*/ (case_dir entries), not evals/uc2-*/; evals/ contains only this registry."* [CODE-VERIFIED]

### Case 37 — `uc2-unwired-surface-passes` (ACTIVE HEADLINE)
An added `/ai Spawn` handler referenced only from tests/comments, not wired to any production entrypoint. Pre-change snapshot clean-passes (the blind spot); post-change must emit `runtime_surface_unreached >= 1` and suppress clean PASS. **Assertion focus = the headline FAIL-pre / PASS-post regression-detection contract.** Assertions (evals.json:1039-1044): [CODE-VERIFIED]
1. `regex_present` on **`old_skill/outputs/REPORT.md`** pattern `clean[_ -]?pass|status:\s*success|no deviations` — baseline EXHIBITS the clean-pass blind spot (this is the only UC-2 assertion targeting `old_skill/`).
2. `regex_absent` on `with_skill/outputs/REPORT.md`, same pattern — post-change must NOT clean-pass.
3. `yaml_field_min` on `with_skill/outputs/contract.yaml` `runtime_surface_unreached >= 1`.
4. `regex_present` on `with_skill/outputs/REPORT.md` `deviation_class:\s*regression|Regression` — surfaced as Regression.
expected.yaml: `runtime_surface_unreached: 1`, `unreached_surfaces:[FR-S9-04 → superclaude.cli.ai_spawn.handle_ai_spawn]`, `deviation_counts.regression: 1`, `tier_reached: 2`. [CODE-VERIFIED]

### Case 38 — `uc2-surface-positive-control` (REACHABLE NEGATIVE/NO-FIRE CONTROL)
An `/ai status` handler wired through the production CLI, plus a pure-internal helper showing non-surface no-sweep behavior. **Assertion focus = the reachable surface must emit ZERO unreached and must NOT escalate or STOP (false-positive guard).** Assertions (evals.json:1056-1060): [CODE-VERIFIED]
1. `yaml_field` `runtime_surface_unreached == "0"`.
2. `yaml_field` `runtime_surface_degraded == "false"`.
3. `regex_absent` on REPORT.md `surface_unreached|UNREACHED|stop_reason`.
expected.yaml: all-zero deviation counts, `tier_reached: 1`, `unreached_surfaces: []`. [CODE-VERIFIED]

### Case 39 — `uc2-surface-dynamic-dispatch` (DEGRADE, NOT REGRESSION)
An `/ai Spawn` entrypoint wired via `[project.scripts]` (registry-string dispatch). Static reachability is undecidable, so it must **DEGRADE loudly and never increment Regression.** **Assertion focus = dynamic wiring → degrade, never false-UNREACHED, never false-Regression.** Assertions (evals.json:1072-1075): [CODE-VERIFIED]
1. `yaml_field` `runtime_surface_degraded == "true"`.
2. `yaml_field` `runtime_surface_unreached == "0"`.
3. `regex_absent` on REPORT.md `deviation_class:\s*regression|Regression`.
expected.yaml: `runtime_surface_degraded: true`, `grounding_gaps:[runtime-surface / registry-string-dispatch-undecidable / needs_human_decision: true]`, `status: partial`, `tier_reached: 1`, zero deviations. [CODE-VERIFIED]

### Case 40 — `uc2-surface-degraded-backend` (BACKEND-LOSS GROUNDING GAP)
`backend:none` prevents static reachability evaluation, so the skill must file a Grounding Gap, continue, and suppress clean PASS without STOPing. **Assertion focus = backend unavailability → degraded + Grounding Gap + no-STOP + no-clean-PASS.** Assertions (evals.json:1088-1092): [CODE-VERIFIED]
1. `yaml_field` `runtime_surface_degraded == "true"`.
2. `regex_present` on REPORT.md `Grounding Gap|grounding[_ -]?gap|runtime-surface:backend_unavailable`.
3. `regex_absent` on REPORT.md `STOP|HALT|stop_reason` — does NOT hard-STOP.
4. `regex_absent` on REPORT.md `clean[_ -]?pass|status:\s*success|no deviations`.
expected.yaml: `runtime_surface_degraded: true`, `grounding_gaps:[runtime-surface / backend_unavailable / needs_human_decision: true]`, `status: partial`, `tier_reached: 1`, zero deviations. [CODE-VERIFIED]

### Case 41 — `uc2-surface-test-only-ref` (COUNT-INVARIANT CASE — the `yaml_list_len_eq` host)
An `/ai export` handler referenced only from tests/comments → UNREACHED, and **asserts the count invariant via `yaml_list_len_eq`.** **Assertion focus = UNREACHED classification AND the `len(unreached_surfaces) == runtime_surface_unreached` invariant (the §2 checker's only live use in the FR-RSR suite).** Assertions (evals.json:1105-1108): [CODE-VERIFIED]
1. `yaml_field_min` `runtime_surface_unreached >= 1`.
2. `yaml_list_len_eq` `target: with_skill/outputs/contract.yaml, list_field: unreached_surfaces, count_field: runtime_surface_unreached`.
3. `regex_present` on REPORT.md `UNREACHED|runtime_surface_unreached|deviation_class:\s*regression|Regression`.
expected.yaml: `runtime_surface_unreached: 1`, `unreached_surfaces:[FR-S9-07 → superclaude.cli.ai_export.handle_ai_export]`, `deviation_counts.regression: 1`, `tier_reached: 2`. [CODE-VERIFIED]

**Cross-case requirement-id map** (from the expected.yaml files): 37→FR-S9-04, 38→FR-S9-05, 39→FR-S9-04, 40→FR-S9-06, 41→FR-S9-07. [CODE-VERIFIED]

---

## 4. Current grading model vs. the deterministic-module target (testing-strategy §15 input)

### 4.1 What grades the runtime-surface contract today
Today the grader is a pure **artifact reader**: every UC-2 assertion above (`yaml_field`, `yaml_field_min`, `yaml_list_len_eq`, `regex_present`, `regex_absent`) reads files the *skill run* already produced (`with_skill/outputs/contract.yaml`, `.../REPORT.md`). The grader never computes reachability; it only checks that the LLM-emitted contract is *internally* shaped right. [CODE-VERIFIED grader.py:191-210, 360-398, 153-170 + the 5 cases in §3.]

The producer of those fields is the skill's **Wave-1 step 4b'/4b** sweep, described in `SKILL.md:487-491` as "the **deterministic, LLM-free runtime-surface tagger**" + a "read-only production-caller sweep." It emits the six `runtime_surface_*` contract fields (SKILL.md:731-735) and `<output>/artifacts/runtime-surface-ledger.yaml` (one row per evaluated edge; schema in `refs/runtime-surface.md:61-98`). The invariant `len(unreached_surfaces) == runtime_surface_unreached` is asserted by the skill itself (SKILL.md:730, runtime-surface.md:96). [CODE-VERIFIED via grep this turn.]

**The gap.** Although the *spec* calls the tagger "deterministic, LLM-free," in the eval harness the tagger's output is produced by an LLM run of the skill (Wave 1 is executed by the model, consulting Serena `find_referencing_symbols`). So `contract.yaml.runtime_surface_unreached` is, at grading time, an **LLM-emitted scalar** (grader.py module docstring + §2 caveat). The eval is therefore non-deterministic: re-running the skill can produce a different (but self-consistent) contract, and `check_yaml_list_len_eq` would still pass it. [CODE-VERIFIED grader.py:191-210; INFERRED for the LLM-run characterization, grounded in SKILL.md Wave-1 description.]

### 4.2 How the grader would invoke the deterministic module to become deterministic
This is the §15 design input. The deterministic reachability module would be a standalone, importable Python function (no LLM, identical input → identical output — the property `refs/runtime-surface.md` and `SKILL.md:487` already claim for the tagger) that, given the case's `input/diff.patch` + `input/tasklist.md` (+ a static caller index / `[project.scripts]` table / backend-availability flag), returns the canonical `{runtime_surface_unreached, runtime_surface_degraded, unreached_surfaces[], grounding_gaps[]}` tuple. The grader would gain a **new assertion type** that calls it and compares to either `expected.yaml` or the producer's `contract.yaml`. Two viable wirings (both consistent with the existing dispatcher pattern at grader.py:410-432):

**Option A — oracle assertion type (recommended; matches the dispatcher convention).** Add `check_runtime_surface_reachable(assertion, base_dir)` registered with `if a_type == "runtime_surface_reachable": return check_runtime_surface_reachable(...)` after grader.py:432. It would:
1. Import the deterministic module (e.g. `from reachability import compute_surface`), call it on `base_dir / assertion["diff"]` + `assertion["tasklist"]` (+ optional `backend`/`scripts` keys), yielding the **ground-truth** tuple.
2. Compare ground-truth against the producer's `with_skill/outputs/contract.yaml` (or against `expected.yaml` for fixture self-checks): assert `runtime_surface_unreached`, `runtime_surface_degraded`, and the *member set* of `unreached_surfaces` (by `symbol`) all match. This upgrades the check from "self-consistent" to "correct," because one operand is now grader-computed, not skill-emitted. [INFERRED — design proposal; the dispatcher/return-shape it must conform to is CODE-VERIFIED at grader.py:318-434.]

**Option B — externalize the producer.** Have the eval runner call the deterministic module to MATERIALIZE `with_skill/outputs/contract.yaml`'s six fields (and the ledger) directly, then keep the existing `yaml_field` / `yaml_list_len_eq` / `regex_*` assertions exactly as written in §3. No new assertion type; the determinism comes from replacing the LLM-emitted scalars with module-emitted ones upstream of grading. The current `check_yaml_list_len_eq` then becomes a meaningful correctness gate (both operands are module-derived). [INFERRED — design proposal.]

**Why `yaml_list_len_eq` stays either way.** Under either option the count-invariant checker remains the *shape* gate (list length == scalar). Option A adds a *value* gate on top; Option B makes both of `yaml_list_len_eq`'s operands trustworthy. Neither requires changing `check_yaml_list_len_eq`'s signature — it already reads two named fields from one YAML file (grader.py:192-210), so it is agnostic to whether those fields were written by the LLM or the deterministic module. [CODE-VERIFIED grader.py:192-210.]

**Determinism boundary already drawn in the spec.** `SKILL.md:487` ("deterministic, LLM-free runtime-surface tagger") + `refs/runtime-surface.md:9,38` ("Deterministic tagger signal," "Deterministic match predicate") + `coverage-mapping.md:109` ("Pure string arithmetic; deterministic for identical inputs; no LLM") show the project already specifies a deterministic algorithm for this surface. The §15 work is to LIFT that algorithm out of the skill prose into an importable module the grader (Option A) or runner (Option B) can call, closing the "grades LLM-emitted scalars" gap noted in the grader docstring. [CODE-VERIFIED via grep this turn.]

---

## Gaps and Questions

1. **No deterministic module exists yet on disk.** Grep over `src/superclaude/skills/sc-reflect-protocol/` found the reachability *algorithm described in prose* (SKILL.md §4b/§4b', refs/runtime-surface.md) but no importable `.py` reachability module. The grader has no import target today. Q: where will the module live — a new file in `.dev/eval-workspaces/sc-reflect/` next to `grader.py`, or under `src/superclaude/`? (Not determinable from the files read.)
2. **`eval_metadata.json` materializer not located.** The grader reads `eval_metadata.json` (grader.py:445), but `evals.json` is the registry. The step that flattens `evals.json` → per-eval `eval_metadata.json` (and copies `cases/uc2-*/expected.yaml` + `input/` into `iterations/iteration-N/eval-<name>/`) was not found this turn. Whether Option B's "runner materializes contract.yaml" hook would live there is unverified.
3. **`target`-prefix routing fragility.** `grade_eval` buckets assertions ONLY by `target.startswith("with_skill/" | "old_skill/")` (grader.py:448-449). A future FR-RSR assertion using a non-`target` key (like `citation_resolves`/`checkpoint_logged` do) would be silently dropped from BOTH buckets. The 5 current UC-2 cases are safe (all use `target`), but a new oracle assertion type (§4.2 Option A) MUST use a `target` key or extend the bucketing logic, else it never runs.
4. **`unreached_surfaces` membership is unchecked today.** `yaml_list_len_eq` checks only the *count*, not WHICH symbols. Case 41's expected `superclaude.cli.ai_export.handle_ai_export` member is asserted only loosely via `regex_present` on REPORT.md (id 41 assertion 3). A deterministic module (Option A) should assert the member *set*, not just the length.
5. **old_skill baseline outputs.** Only case 37 references `old_skill/outputs/REPORT.md` (the FAIL-pre baseline). The other 4 cases have zero `old_skill/` assertions, so their `old_skill` grading.json will be `0/0` (pass_rate 0.0 by the `total > 0` guard at grader.py:470). This is expected for PASS-post-only cases but worth noting for any "all configs must have assertions" sanity gate.

## Stale Documentation Found

1. **`grader-extensions.md:25` undercount vs. dispatcher.** The doc header says "10 truly-new semantic groups" / "11 dispatcher branches beyond the 8 syntactic baseline types," then enumerates 11 rows (1-11) in the table at lines 13-23. The dispatcher (grader.py:411-432) registers **11** new `if` branches and `evals.json:1112-1132` `grading_criteria` lists **19 total** (8 + 11). The "10 ... groups" phrasing is an internal accounting note (it folds `regex_present`+`regex_absent` into one group) and is potentially confusing but not wrong; the authoritative count is 11 new branches / 19 total — consistent between grader.py and evals.json. [CODE-VERIFIED]
2. **`grader-extensions.md:43` sketch diverges from shipped code (benign).** The doc's `check_citation_resolves` sketch uses `Path(assertion.get("fixture_root", base_dir))` directly; the shipped grader.py:126-129 adds an `is_absolute()` remap (`fixture_root = base_dir / fixture_root` when relative). The shipped version is more correct; the doc sketch is illustrative ("Sketches below assume...", line 5). Not a contract drift, but the doc sketch would mis-resolve a relative `fixture_root`. [CODE-VERIFIED grader.py:126-129 vs grader-extensions.md:42-47]
3. **No staleness found in the FR-RSR path itself.** `check_yaml_list_len_eq` in grader.py:191-210 is byte-for-byte consistent with the spec sketch at grader-extensions.md:146-165, and the canonical usage at grader-extensions.md:143 matches case 41's assertion exactly (`list_field: unreached_surfaces, count_field: runtime_surface_unreached`). [CODE-VERIFIED]

## Summary

The sc-reflect eval harness grades the FR-RSR runtime-surface contract **purely by reading skill-produced artifacts** — there is no reachability computation in the grader. `check_assertion` (grader.py:318) dispatches via a flat `if a_type == ...` switch; the 8 baseline types run inline, the 11 new types delegate to `check_<name>` helpers, and assertions are routed to the `with_skill`/`old_skill` config buckets solely by their `target` string prefix (grader.py:448-449). The FR-RSR count-invariant checker `check_yaml_list_len_eq` (grader.py:191-210) parses `contract.yaml` with `yaml.safe_load`, reads `list_field` (`unreached_surfaces`) and `count_field` (`runtime_surface_unreached`), and passes iff their length/value match — a **self-consistency** gate over two LLM-emitted scalars, which by construction cannot catch a coherent fabrication. The 5 UC-2 cases (ids 37-41, `case_dir: cases/uc2-*/`) exercise the four reachability verdicts plus the count invariant. To make the eval deterministic (§15), the project's already-specified "deterministic, LLM-free tagger" (SKILL.md:487) must be lifted into an importable module that the grader calls as a new oracle assertion type (Option A) or that the runner uses to materialize the contract's six fields upstream of grading (Option B); `yaml_list_len_eq`'s signature needs no change under either path.

### The 5 cases and their assertion focus
- **uc2-unwired-surface-passes** (id 37): headline FAIL-pre/PASS-post — old snapshot clean-passes the unwired `/ai Spawn` surface; new run must emit `runtime_surface_unreached>=1` + Regression and suppress clean PASS.
- **uc2-surface-positive-control** (id 38): reachable no-fire control — wired `/ai status` surface must emit `runtime_surface_unreached==0`, `degraded==false`, no UNREACHED/STOP escalation.
- **uc2-surface-dynamic-dispatch** (id 39): `[project.scripts]` dynamic wiring must DEGRADE (`degraded==true`), never UNREACHED (`==0`), never false-Regression.
- **uc2-surface-degraded-backend** (id 40): `backend:none` → degraded + Grounding Gap, no hard-STOP, no clean-PASS.
- **uc2-surface-test-only-ref** (id 41): test/comment-only `/ai export` → UNREACHED, and the host of the `yaml_list_len_eq` count-invariant assertion `len(unreached_surfaces)==runtime_surface_unreached`.
