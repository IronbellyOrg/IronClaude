# R5 Research — Eval Path: Grader + UC-2 Cases + C-5 Materializer

**Status:** Complete
**Date:** 2026-06-22
**Researcher:** R5 (of 8)
**Topic:** Eval-harness wiring for FR-DRS Phase-3 items — grader assertion dispatch, C-6 target bucketing, 5 UC-2 cases, **C-5 materializer location**.
**Track goal:** Implement FR-DRS + eval path (Phase 3). Write accurate Phase-3 task items.

All file:line citations re-verified this turn. Tags: `[CODE-VERIFIED]` = read the exact line this turn; `[UNVERIFIED]` = could not confirm in tracked code.

---

## 0. TL;DR for the builder (Phase-3 items)

1. **The grader is `grader.py`** (`.dev/eval-workspaces/sc-reflect/grader.py`). It dispatches 19 assertion types (8 baseline + 11 extension) by `assertion["type"]` in `check_assertion` (`grader.py:318-434`). `[CODE-VERIFIED]`
2. **C-6 (load-bearing):** `grade_eval` buckets assertions into `with_skill`/`old_skill` configs **solely** by `assertion.get("target","").startswith("with_skill/" | "old_skill/")` (`grader.py:448-449`). Any new FR-DRS oracle assertion **MUST carry a `target` key prefixed `with_skill/`** or it falls into neither bucket and is **silently never graded**. `[CODE-VERIFIED]`
3. **5 cases (ids 37–41)** in `evals/evals.json` + `cases/uc2-*/`; every existing UC-2 assertion already carries a `target` → all safe today. `[CODE-VERIFIED]`
4. **C-5 MATERIALIZER: confirmed NOT LOCATED in tracked code.** No script in the repo flattens `evals.json` → per-eval `eval_metadata.json` or copies `cases/uc2-*/` into `iterations/iteration-N/eval-<name>/`. The grader and `aggregate_iteration.py` only **read** `eval_metadata.json`; `make reflect-eval` only runs the grader against an empty timestamp dir. The materialization was done **by the LLM eval harness (skill-creator manual/agent loop) during prior eval sessions**, not by a tracked materializer. See §4. `[CODE-VERIFIED — absence confirmed]`
5. **Eval-wire recommendation (TDD §11.2):** the grader (or a thin oracle step) invokes the **same** `runtime_surface.run_sweep()` module → writes the ledger + 6 scalars into `with_skill/outputs/` **upstream of grading**, so the existing `yaml_field`/`yaml_field_min`/`yaml_list_len_eq` assertions grade a deterministic artifact (no LLM variance). The ≥3-run determinism gate (AC-2) then re-runs and diffs.

---

## 1. Grader assertion-type dispatch + `check_yaml_list_len_eq` + contract.yaml read

### 1.1 Dispatch (`check_assertion`, `grader.py:318-434`) `[CODE-VERIFIED]`

`check_assertion(assertion, base_dir) -> (passed, evidence)` reads `a_type = assertion.get("type")` (`:320`) and `target = assertion.get("target","")` (`:321`), then `target_path = base_dir / target` (`:322`). It is a flat `if a_type == ...` ladder:

**8 baseline (inherited from sc-brainstorm), inline in `check_assertion`:**
- `file_exists` (`:324`), `frontmatter_field` (`:330`), `section_present` (`:342`), `section_enumerated` (`:350`), `yaml_field` (`:360`), `yaml_field_min` (`:372`), `yaml_substring` (`:387`), `dir_count` (`:400`).
- Baseline YAML types use the **flat** `parse_yaml_simple` parser (`:59-78`) — **no nesting**. (Relevant: `runtime_surface_unreached`, `runtime_surface_degraded` are flat top-level scalars in contract.yaml → graded fine by `yaml_field`/`yaml_field_min`.)

**11 extension types (per `refs/grader-extensions.md`), delegated to helper fns (`:410-432`):**
- `citation_resolves`→`check_citation_resolves` (`:411`/`:121`); `regex_present`→`check_regex_present` (`:413`/`:153`); `regex_absent`→`check_regex_absent` (`:415`/`:163`); `yaml_list_contains` (`:417`/`:173`); `yaml_list_len_eq` (`:419`/`:191`); `matrix_covers_items` (`:421`/`:214`); `checkpoint_logged` (`:423`/`:236`); `deviation_class_matches` (`:425`/`:256`); `path_exists` (`:427`/`:275`); `path_does_not_exist` (`:429`/`:285`); `falsifier_skeleton_present` (`:431`/`:294`).
- Unknown type → `(False, "Unknown assertion type: …")` (`:434`).
- Extension YAML types use the **proper `yaml.safe_load`** parser (nested-capable).

### 1.2 `check_yaml_list_len_eq` (`grader.py:191-210`) `[CODE-VERIFIED]`

Signature: `check_yaml_list_len_eq(assertion: dict, base_dir: Path) -> tuple[bool, str]`. Behavior:
- `target = base_dir / assertion["target"]` (`:192`); missing file → `(False, "YAML file missing: …")` (`:193-194`).
- `data = yaml.safe_load(target.read_text(...)) or {}` (`:195`).
- Reads `list_field = assertion["list_field"]` (`:196`) and `count_field = assertion["count_field"]` (`:197`).
- `items = data.get(list_field)`; not-a-list → fail (`:198-200`).
- `expected = int(data[count_field])`; missing `count_field` → fail (`:202-204`); non-int → fail (`:205-206`).
- Pass iff `len(items) == expected` (`:207-210`).

This is the **count-invariant grader re-check** (TDD §15.4, AC-3). Case **41** uses it: `list_field: unreached_surfaces`, `count_field: runtime_surface_unreached`, both read from the **same** `with_skill/outputs/contract.yaml` (`evals.json:1107`). The invariant `len(unreached_surfaces) == runtime_surface_unreached` holds **by construction** in the module (both derived from the same ledger rows, TDD §8/§981) and the grader independently re-checks it (TDD §981, §15.4).

### 1.3 How the grader reads `contract.yaml`

There is **no dedicated `contract.yaml` reader** in the grader. The grader is **target-string-driven**: each assertion names its own file via `target` (e.g. `"with_skill/outputs/contract.yaml"`), and the relevant helper loads it (`yaml.safe_load` for extension types, `parse_yaml_simple` for baseline `yaml_field*`). `base_dir` is the per-eval dir (`iterations/.../eval-<name>/`), so `target` is resolved relative to it. `[CODE-VERIFIED]`

### 1.4 `grade_eval` flow (`grader.py:437-484`) `[CODE-VERIFIED]`

- `metadata_path = eval_dir / "eval_metadata.json"` (`:440`); **if missing → `print("SKIP…"); return {}`** (`:441-443`). ← the per-eval metadata file is mandatory; absent ⇒ the eval is silently skipped.
- `meta = json.loads(...)`; `assertions = meta.get("assertions", [])` (`:445-446`).
- **C-6 bucketing** (`:448-449`, see §2).
- `build_grading` (`:451-472`) loops assertions, calls `check_assertion(a, eval_dir)`, accumulates `passed/failed/total/pass_rate`.
- Writes `eval_dir/with_skill/grading.json` and `eval_dir/old_skill/grading.json` (`:477-478`).
- Entry point `main()` (`:487-514`) takes ONE arg = an `iterations/iteration-N/` dir, iterates `eval-*` subdirs, calls `grade_eval` on each.

---

## 2. C-6 target-prefix bucketing (HARD CONSTRAINT on FR-DRS oracle assertions)

`grade_eval`, **`grader.py:448-449`** `[CODE-VERIFIED]`:

```python
with_skill_assertions = [a for a in assertions if a.get("target", "").startswith("with_skill/")]
old_skill_assertions  = [a for a in assertions if a.get("target", "").startswith("old_skill/")]
```

**The constraint:** an assertion is graded **only** if its `target` starts with `with_skill/` or `old_skill/`. Assertion types that use **non-`target` keys** — `citation_resolves` (uses `report`/`fixture_root`), `checkpoint_logged` (uses `audit_log`), `matrix_covers_items` (`matrix`/`source`), `deviation_class_matches` (`annotated_fixture`/`report`) — fall into **neither bucket and are silently never graded**. (`path_exists`/`path_does_not_exist` DO use `target`, but may pass an absolute path that doesn't start with the prefix → same trap.)

**For FR-DRS:** the 5 current UC-2 cases are safe — **every** assertion in ids 37–41 carries a `target` prefixed `with_skill/` or `old_skill/` (verified §3). **But any NEW oracle assertion type FR-DRS adds (e.g. a deterministic-reachability check comparing the module's ground truth to the contract) MUST carry a `target` key prefixed `with_skill/`** (or the bucketing logic at `:448-449` must be extended). This is the load-bearing eval-wire constraint (TDD §15.4 C-6, §22.1 C-6). The simplest compliant design: have the oracle write into `with_skill/outputs/contract.yaml` and assert via existing `yaml_field`/`yaml_field_min`/`yaml_list_len_eq` (all `target`-keyed) — **no new assertion type needed**.

---

## 3. The 5 FR-RSR cases (ids 37–41): dir contents, expected.yaml, per-case verdict

**Common dir shape** (all 5, `[CODE-VERIFIED]`): `cases/<name>/input/diff.patch`, `cases/<name>/input/tasklist.md`, `cases/<name>/expected.yaml`. Each `evals.json` entry (`:1030-1110`): `mode: post`, `use_case: UC-2`, `spec_ref: FR-RSR.10 / TDD §15.2`, `inputs: {diff, tasklist}`, `expected: expected.yaml`, `assertions: [...]`.

**`diff.patch` shape** (verified on case 37): a **real unified git diff** adding a new `src/superclaude/cli/ai_*.py` surface handler + a `tests/cli/test_ai_*.py` that imports it directly — the handler is **not wired** into any production CLI/route/registry/`[project.scripts]`. The "unwired-ness" is encoded in the diff content (docstring states FR-S9-04 requires reachability; module adds handler but no entrypoint wiring). `[CODE-VERIFIED]`

| Id | Name | Key assertions (`evals.json`) | `expected.yaml` shape (case dir) | Per-case verdict |
|----|------|------------------------------|----------------------------------|------------------|
| **37** | `uc2-unwired-surface-passes` (`:1030-1044`) | `regex_present` on `old_skill/…REPORT.md` (clean-pass blind spot); `regex_absent` on `with_skill/…REPORT.md` (no clean-pass); **`yaml_field_min` `runtime_surface_unreached` ≥1** on `with_skill/…contract.yaml`; `regex_present` deviation_class regression | `runtime_surface_unreached: 1`, `runtime_surface_degraded: false`, `unreached_surfaces:[{requirement_id: FR-S9-04, symbol: …ai_spawn.handle_ai_spawn}]`, `deviation_counts.regression: 1`, `tier_reached: 2` | **UNREACHED ≥1, regression 1**; FAIL-pre/PASS-post; never clean-pass `[CODE-VERIFIED]` |
| **38** | `uc2-surface-positive-control` (`:1046-1060`) | `yaml_field runtime_surface_unreached==0`; `yaml_field runtime_surface_degraded==false`; `regex_absent` UNREACHED/STOP | `runtime_surface_unreached: 0`, `runtime_surface_degraded: false`, `unreached_surfaces: []`, all `deviation_counts: 0`, `tier_reached: 1` | **UNREACHED 0, degraded false**; no UNREACHED/STOP `[CODE-VERIFIED]` |
| **39** | `uc2-surface-dynamic-dispatch` (`:1062-1076`) | `yaml_field runtime_surface_degraded==true`; `yaml_field runtime_surface_unreached==0`; `regex_absent` Regression | `runtime_surface_degraded: true`, `runtime_surface_unreached: 0`, `grounding_gaps:[{source: runtime-surface, reason: registry-string-dispatch-undecidable, needs_human_decision: true}]`, `status: partial`, `deviation_counts.regression: 0` | **degraded true, regression 0** (`[project.scripts]` → DEGRADE, never UNREACHED) `[CODE-VERIFIED]` |
| **40** | `uc2-surface-degraded-backend` (`:1078-1093`) | `yaml_field runtime_surface_degraded==true`; `regex_present` Grounding Gap / `runtime-surface:backend_unavailable`; `regex_absent` STOP/HALT; `regex_absent` clean-pass | `runtime_surface_degraded: true`, `grounding_gaps:[{source: runtime-surface, reason: backend_unavailable, needs_human_decision: true}]`, `status: partial`, `deviation_counts.regression: 0` | **degraded true, status partial**; Grounding Gap, no hard-STOP, no clean-pass `[CODE-VERIFIED]` |
| **41** | `uc2-surface-test-only-ref` (`:1095-1109`) | `yaml_field_min runtime_surface_unreached ≥1`; **`yaml_list_len_eq` `unreached_surfaces`/`runtime_surface_unreached`** (count-invariant host); `regex_present` UNREACHED/Regression | `runtime_surface_unreached: 1`, `unreached_surfaces:[{requirement_id: FR-S9-07, symbol: …ai_export.handle_ai_export}]`, `deviation_counts.regression: 1`, `tier_reached: 2` | **UNREACHED ≥1 + count-invariant host** (test/comment-only referrers) `[CODE-VERIFIED]` |

**Maps exactly to the assignment's expected verdicts:** 37 unreached≥1/regression1; 38 unreached0/degraded false; 39 degraded true/regression0; 40 degraded true/status partial; 41 unreached≥1 + count-invariant host. ✅

**Builder note:** `expected.yaml` is the **human-readable ground-truth fixture** (mode/use_case/runtime_surface_* fields/unreached_surfaces/grounding_gaps/deviation_counts/per_task_verdicts). The **graded** file is `with_skill/outputs/contract.yaml` (named by each assertion's `target`). FR-DRS's eval-wire job is to make the deterministic module **produce that `contract.yaml`** so the grader's assertions match `expected.yaml` with zero LLM variance.

---

## 4. C-5 MATERIALIZER — LOCATION (top-priority deliverable)

### VERDICT: **CONFIRMED NOT LOCATED in tracked repo code.** `[CODE-VERIFIED — absence]`

The grader reads per-eval `eval_metadata.json` (`grader.py:440`), and `evals.json` is the **registry/spec** (`evals/evals.json`, top-level `skill_name`/`iteration`/`scope`/`notes`/`evals[]`/`grading_criteria`). The step that **flattens `evals.json` → per-eval `eval_metadata.json`** and **copies `cases/uc2-*/expected.yaml` + `input/` into `iterations/iteration-N/eval-<name>/`** does **not exist as a tracked script**. Evidence:

1. **Only two `.py` in the sc-reflect workspace touch `eval_metadata.json`, both READ-only:**
   - `grader.py:440` — `metadata_path = eval_dir / "eval_metadata.json"` (read). `[CODE-VERIFIED]`
   - `aggregate_iteration.py:49` — `meta = read_json(eval_dir / "eval_metadata.json")` (read). `[CODE-VERIFIED]`
   - `grep -rln 'eval_metadata.json").write_text'` across the sc-reflect workspace → **no hits** (the only `.write_text("eval_metadata…")` sites in the repo are a *different* skill: `.dev/research/.../cli-eval/grade_iter{1,2}.py`, the sc-troubleshoot/cli-eval harness, not sc-reflect). `[CODE-VERIFIED]`
2. **`make reflect-eval` does NOT materialize.** Makefile (`Makefile:505-512`): it `mkdir -p`s a **fresh empty timestamp dir** `iterations/<date>/` then runs `uv run python grader.py <that-empty-dir>`. With no `eval-*` subdirs and no `eval_metadata.json`, the grader's loop (`grader.py:498-504`) finds nothing / SKIPs. So the Makefile target is a **grader-only** entrypoint — it assumes the iteration dir was already populated by something else. `[CODE-VERIFIED]`
3. **`eval_metadata.json` files DO exist in `iterations/`** (e.g. `iterations/before-r1/eval-uc2-surface-positive-control/eval_metadata.json`), alongside `fixture/`, `with_skill/outputs/{contract.yaml,REPORT.md,…}`, `old_skill/grading.json`. Their shape is a **flattened single-eval projection** of the `evals.json` entry (`eval_id`, `eval_name`, `case_dir`, `mode`, `use_case`, `assertions[]`) — confirming a materialization step happened, but it was performed by the **LLM-driven skill-creator eval harness during a prior session**, not a checked-in materializer. `[CODE-VERIFIED]`
4. **skill-creator `run_loop.py` is NOT the materializer.** Located at `/config/.claude/plugins/.../skill-creator/skills/skill-creator/scripts/run_loop.py`, but it is a **description-trigger optimization loop** (`should_trigger`, train/test split, `improve_description`, `generate_html`) — it has **no** `eval_metadata.json`/`with_skill`/`cases`/`copytree` logic. It does not flatten `evals.json` for the assertion-grader path. `[CODE-VERIFIED]`
5. **SPEC.md confirms the harness is the (external) skill-creator plugin + local grader.py**, not a tracked materializer: §1084 "hybrid — skill-creator plugin for the draft/iterate loop, then local `grader.py` for deterministic assertions"; §1099-1100 maps the iteration harness to `skill-creator run_loop.py` and the assertion gate to the local `grader.py`; `evals.json:notes` states pilot/promotion/uc2 fixtures were authored as STUBS across prior `TASK-RF-…` tasklists (manual authoring, not a generator). `[CODE-VERIFIED]`

### Where the eval-path hook then lands (FR-DRS Phase 3)

Because no tracked materializer exists, the FR-DRS eval-path hook **cannot live "in the materializer."** Two viable landing sites:

- **Option B (RECOMMENDED — TDD §11.2 secondary flow): an oracle step in/around `grader.py`.** Add a thin pre-grade hook (a function in `grader.py`, or a sibling `materialize_runtime_surface.py` invoked before `grade_eval`) that, for each `eval-uc2-*` dir, calls `runtime_surface.run_sweep()` on the case's `input/diff.patch` + scope and **writes `with_skill/outputs/contract.yaml` (6 scalars) + `with_skill/outputs/artifacts/runtime-surface-ledger.yaml`** before the existing assertions run. The assertions (all `target`-keyed → C-6 safe) then grade a deterministic artifact. This is the cleanest place since the grader is the only tracked, runnable eval entrypoint.
  - Concretely: this oracle would also be the **de-facto materializer** for the FR-RSR slice — it must additionally write `eval_metadata.json` (flattened from `evals.json` ids 37–41) + copy `cases/uc2-*/{expected.yaml,input/}` into the iteration dir, OR the task must add a small `materialize.py` that does the generic flatten+copy and is invoked by `make reflect-eval` BEFORE the grader.
- **Option A (grader-as-oracle inline):** register a new assertion type (e.g. `runtime_surface_oracle`) in `check_assertion` that runs the sweep and compares to the contract. **C-6 caveat:** this new type MUST carry a `target` prefixed `with_skill/` or it is never bucketed (`:448-449`). More invasive than Option B; not recommended.

**Phase-3 task item implication:** the builder must include a **"locate-or-build the materializer" item** (TDD front-loads this to Phase 1 / I5, §23.2). Since R5 confirms it is NOT located, the task should treat it as **build a small materializer** (flatten `evals.json` ids 37–41 → `eval_metadata.json`; copy `cases/uc2-*/{expected.yaml,input/}` → `iterations/<iter>/eval-<name>/`) **plus** the `run_sweep` oracle that writes `contract.yaml`/ledger upstream of grading, wired into `make reflect-eval`. Until that lands, AC-2's "deterministic via grader" claim is **conditional** (TDD §23.2 Phase-1 exit, §22.1 C-5).

---

## 5. Eval-wire options + the ≥3-run determinism gate

### 5.1 The two wire options (TDD §11.2, FR-008 `tdd.md:289`)

> FR-008: "The eval harness/grader MUST invoke the same deterministic module so the FR-RSR eval (ids 37–41) is free of LLM variance — **either as a grader oracle assertion or by materializing the contract's six fields upstream of grading.**"

- **(i) Grader invokes `run_sweep` as oracle** — assertion-time, the grader runs the module and asserts module-truth vs contract. (C-6 risk: new assertion type needs `target`.)
- **(ii) Runner/materializer materializes the 6 fields upstream of grading** (RECOMMENDED) — the module writes `contract.yaml`'s `runtime_surface_*` scalars + `unreached_surfaces[]` + ledger into `with_skill/outputs/` BEFORE the grader runs; the existing `yaml_field`/`yaml_field_min`/`yaml_list_len_eq` assertions (all `target`-keyed) grade it. This is the §11.2 sequence diagram flow (`tdd.md:780-795`): Harness → Grader → Sweep → FS (ledger+scalars) → Assert.

Both share the **same `runtime_surface.run_sweep()` module as the product path** (TDD §11.2 "Why two flows share one module" `tdd.md:816`) — that shared module IS the determinism guarantee; the eval can no longer pass on LLM-emitted scalars (true falsifier for AC-1/AC-3).

### 5.2 The ≥3-run determinism gate (AC-2)

- **AC-2** (`tdd.md` §24.1): "The 5 FR-RSR eval cases (ids 37–41) pass **deterministically across ≥3 repeated runs (no variance)**." Phase-3 exit criterion (§23.2): "**AC-2 green with no variance across ≥3 runs.**"
- Mechanism: run the grader (with the oracle/materializer wired) **≥3 times** on the 5 cases and assert **byte-identical** `runtime_surface_*` fields + `grading.json` across runs. Because the sweep is pure-Python, no-network (NFR-003), no-LLM, the output is reproducible. The R3 ripgrep floor uses `--sort path` (TDD §23.2 Phase-1) precisely to keep referrer ordering deterministic across runs.
- The §15.4 grader re-check (`check_yaml_list_len_eq`, case 41) is the **count-invariant** half of the determinism story (AC-3); the ≥3-run repeat is the **variance** half (AC-2).
- **AC-5 safety-regression gate** (separate, §24.2): `tests/cli/reflect/test_runtime_surface_safety_regression.py` runs cases 37/39/40/41 through the **verdict layer** and FAILS the release if any clean-passes its surface. (R7 owns the pytest file; this is the eval-path's safety twin.)

---

## 6. Verdict→exit-code (context, FR-DRS does NOT change it)

The reflect `Verdict.exit_code` mapping (`pass=0/halted=10/degraded=11/blocked=2`) is owned by `models.py` (TDD §11.2 cross-ref `tdd.md:818`: def `models.py:39`, value dict `:44-49`, enum `:33-36`). FR-DRS does not alter it. Relevant only so the builder does not add a new exit code for `runtime_surface_degraded` — DEGRADE reuses `degraded` (11) via the existing `degraded-components` slug (TDD §23.2 Phase-2: append `"runtime-surface:backend_unavailable"` to `degraded_components`, add token to `_DEGRADED_COMPONENTS_HALT_SET`).

---

## 7. Citation ledger (re-verified this turn)

| Claim | File:line | Tag |
|-------|-----------|-----|
| `check_yaml_list_len_eq` signature/body | `grader.py:191-210` | CODE-VERIFIED |
| dispatch ladder | `grader.py:318-434` | CODE-VERIFIED |
| `grade_eval` + metadata read + SKIP | `grader.py:437-443` | CODE-VERIFIED |
| C-6 bucketing | `grader.py:448-449` | CODE-VERIFIED |
| `build_grading`/writes grading.json | `grader.py:451-478` | CODE-VERIFIED |
| ids 37–41 entries | `evals/evals.json:1030-1110` | CODE-VERIFIED |
| `evals.json` registry header/notes | `evals/evals.json:1-5`, `:1112-1132` | CODE-VERIFIED |
| 5 expected.yaml shapes | `cases/uc2-*/expected.yaml` | CODE-VERIFIED |
| diff.patch shape | `cases/uc2-unwired-surface-passes/input/diff.patch` | CODE-VERIFIED |
| `aggregate_iteration.py` reads metadata | `aggregate_iteration.py:49` | CODE-VERIFIED |
| `make reflect-eval` = grader-only on empty dir | `Makefile:505-516` | CODE-VERIFIED |
| skill-creator run_loop.py is trigger-loop, not materializer | `/config/.claude/plugins/.../skill-creator/scripts/run_loop.py:1-55` | CODE-VERIFIED |
| materializer absence (no write_text in workspace) | grep `.dev/eval-workspaces/sc-reflect/*.py` | CODE-VERIFIED |
| §11.2 eval flow + shared module | `tdd.md:778-818` | CODE-VERIFIED |
| §15.3 5 cases + commands | `tdd.md:1031-1055` | CODE-VERIFIED |
| §15.4 count-invariant re-check + C-6 | `tdd.md:1057-1068` | CODE-VERIFIED |
| §22.1 C-5/C-6 carry-forwards | `tdd.md:1326-1330` | CODE-VERIFIED |
| §23.2 Phase 3 (+ Phase-1 front-load of C-5 locate) | `tdd.md` §23.2 block | CODE-VERIFIED |
| FR-008 / AC-2 / AC-5 release criteria | `tdd.md:289`, §24.1/§24.2 | CODE-VERIFIED |

---

## Summary

The eval path is fully mapped. **Grader** (`grader.py`) is a target-string-driven, 19-type assertion dispatcher; `check_yaml_list_len_eq` (`:191`) is the AC-3 count-invariant re-check that case 41 hosts. **C-6** (`:448-449`) is the load-bearing constraint: every FR-DRS oracle assertion must carry a `target` prefixed `with_skill/` (cleanly satisfied by reusing existing `yaml_field*`/`yaml_list_len_eq` against a deterministically-written `contract.yaml` — no new assertion type needed). **All 5 cases (37–41)** are present with `input/{diff.patch,tasklist.md}` + `expected.yaml`, verdicts matching the assignment exactly. **C-5 materializer: CONFIRMED NOT LOCATED** — no tracked script flattens `evals.json`→`eval_metadata.json` or copies `cases/uc2-*/` into `iterations/`; `make reflect-eval` is grader-only on an empty dir; the prior materialization was LLM-harness-driven. **Therefore the Phase-3 eval hook lands as Option B**: a thin oracle/materializer (recommended sibling `materialize.py` + `run_sweep` call) that writes `contract.yaml`+ledger into `with_skill/outputs/` **upstream of grading** and is wired into `make reflect-eval`, validated by the **≥3-run determinism gate (AC-2)**. Until built, AC-2's grader-determinism is conditional (TDD §23.2 Phase-1 exit / §22.1 C-5).
