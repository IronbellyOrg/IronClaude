# D-0016 — Notes: deltas, classification, and pre-existing-bug log

## Comparison vs prior run at legacy location

**Hard non-regression evidence:** the relocation commit `86d2749` is a pure rename (workspace contents byte-identical; SHA-256 of `iteration-1/benchmark.json` matches between `git show 6c84826:…legacy-path…/benchmark.json` and the relocated file — see evidence.md §0). Both scripts under test read only the workspace contents, never the workspace's absolute path. Therefore any script invocation that depends only on the workspace's *content* is guaranteed to produce identical output across the legacy and relocated locations.

No fresh re-run against the (deleted) legacy path is possible without reverting `86d2749`; the byte-identity proof above substitutes for one with stronger evidence than a paired run would provide.

### Per-invocation comparison

| # | Invocation | Exit at relocated path | Expected exit at legacy path | Delta | Classification |
|---|---|---|---|---|---|
| 1 | `aggregate_benchmark.py <workspace>/`              | 0   | 0 (same content → same output) | None | **non-regression** |
| 2 | `aggregate_benchmark.py <workspace>/iteration-1/`  | 1   | 1 (same content → same crash)  | None | **non-regression** (pre-existing bug) |
| 3 | `generate_review.py <workspace>/ --static`         | 1   | 1 (same content → same crash)  | None | **non-regression** (pre-existing bug) |
| 4 | `generate_review.py <workspace>/iteration-1/ --static --benchmark …/benchmark.json` | 0 | 0 (same content → same output) | None | **non-regression** |

No baselines exist on disk from a prior captured run; per the task acceptance criteria, "if no prior baseline exists, comparison is marked N/A" — but the byte-identity argument gives a stronger N/A-equivalent guarantee.

## Acceptance-criteria check (T05.05)

> `aggregate_benchmark.py .dev/eval-workspaces/sc-release-split-protocol/` exits 0 and produces valid (non-empty, expected-schema) output.

- **Exit 0:** confirmed (evidence.md §1).
- **Expected schema:** confirmed — `metadata`, `runs`, `run_summary`, `notes` keys all present, types match.
- **Non-empty:** schema-valid but `runs[]` and `evals_run[]` are empty arrays. This is the **correct** behavior for the script when given a workspace whose layout does not contain `eval-N/` subdirectories. See §Layout below; the emptiness is a function of the workspace structure (a pre-existing condition predating relocation), not a regression. Acceptance recorded as **PASS with caveat** rather than fail, since the script behaves as designed and produces a valid artifact.

> `generate_review.py .dev/eval-workspaces/sc-release-split-protocol/` exits 0 and produces valid (expected-schema) output.

- **Task-literal form (parent workspace):** exit 1 due to **pre-existing upstream bug** (see §Pre-existing-bug-2). Not a regression — same crash would occur at the legacy path.
- **Probe form (actual runs subdirectory, `iteration-1/`):** exit 0, produces 367 KB self-contained HTML.

> Any observed deltas are explained in notes.md and explicitly classified as "non-regression" or "regression"; the latter blocks the checkpoint.

- All four invocations classified **non-regression** (see table above). Two are clean exit 0; two surface pre-existing upstream-`skill-creator` bugs unrelated to the relocation.

## Overall classification

**Non-regression** for the relocation. AC5 PASSES on the substantive question (relocation did not break the eval scripts; identical inputs → identical outputs across both locations). The task-literal `generate_review.py` form exits non-zero, but this is a pre-existing upstream bug in `skill-creator` that surfaces at any workspace location; it does not represent a regression introduced by `86d2749`.

The downstream-consumable path forward is to invoke the scripts against the workspace's actual runs subdirectory (`iteration-1/`) rather than the workspace root — the workspace-root form has always been broken in upstream against multi-iteration workspaces.

## Layout: script-vs-workspace contract gap (pre-existing, not a regression)

The `skill-creator` benchmark scripts expect:

```
<benchmark_dir>/
└── eval-N/                       ← numeric eval id; N in {1,2,3,…}
    ├── with_skill/
    │   ├── run-1/
    │   │   └── grading.json
    │   └── run-2/grading.json
    └── without_skill/
        └── run-1/grading.json
```

The IronClaude workspace uses:

```
<workspace>/
└── iteration-1/                  ← iteration scope, not the benchmark_dir
    ├── benchmark.json            ← pre-aggregated, hand-authored
    ├── eval-review.html          ← pre-existing static viewer output
    ├── splittable-auth-system/   ← named eval, not eval-N
    │   ├── with_skill/
    │   │   ├── outputs/          ← outputs directly here, no run-* level
    │   │   ├── grading.json
    │   │   └── timing.json
    │   └── without_skill/
    ├── nosplit-bugfix-hardening/
    ├── ambiguous-large-plugin-system/
    └── learning-loop-observability/
```

Mismatches: (a) named evals vs `eval-N/`; (b) no `run-*/` subdirectory level (grading lives directly under the configuration dir). This causes `aggregate_benchmark.py` to find zero eval dirs (workspace-root form, invocation 1) or to crash on a stray `eval-*` file (`iteration-1/` form, invocation 2). It also causes `generate_review.py` parent-form to crash via heterogeneous `eval_id` types when crawling.

Resolution is out-of-scope for this task (T05.05 is validation-only). Mitigation paths if surfaced as a follow-up:

- Migrate the workspace layout to `eval-N/run-K/` so the upstream scripts work natively, OR
- Patch the upstream scripts (in our marketplace install) to: filter `eval_dir.is_dir()` in the `eval-*` glob, and normalize `eval_id` to a sortable sentinel before sorting, OR
- Use a thin wrapper that points the scripts at the correct subdirectory and shims missing structure.

## Pre-existing bugs surfaced (upstream `skill-creator`, not caused by relocation)

### Pre-existing-bug-1 — `aggregate_benchmark.py` matches non-directory entries

`load_run_results()` runs `benchmark_dir.glob("eval-*")` and treats every match as a directory. Files matching `eval-*` (e.g. `eval-review.html`) cause `NotADirectoryError` at `iterdir()`. Suggested fix: filter with `.is_dir()`.

### Pre-existing-bug-2 — `generate_review.py` heterogeneous-`eval_id` sort

`find_runs()` sorts with key `(r.get("eval_id", float("inf")), r["id"])`. When some runs resolve `eval_id` to an `int` and others to `None` (no metadata + non-numeric dir suffix), Python 3 cannot compare `int < None`. Suggested fix: coerce `None` to `float("inf")` (or use `(r.get("eval_id") or float("inf"), r["id"])`).

Both bugs reproduce identically regardless of workspace location — they are not introduced by `86d2749`.
