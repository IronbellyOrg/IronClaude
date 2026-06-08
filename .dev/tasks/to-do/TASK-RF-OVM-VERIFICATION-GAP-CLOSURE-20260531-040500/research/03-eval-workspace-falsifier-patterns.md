# R3 Research — eval-workspace + falsifier YAML patterns

**Researcher:** R3 (Test & Verification + Template & Examples — eval-workspace concerns)
**Date:** 2026-05-31
**Topic:** sc-reflect eval-workspace existence, falsifier YAML shape, `grader.py` invocation semantics

---

## eval-workspace existence verdict (exists? structure?)

**MAJOR FINDING — wrong-repo blocker.** The sc-reflect eval-workspace does **NOT** exist anywhere under `/config/workspace/Coder/`. The full infrastructure (eval-workspaces, grader.py, falsifier-suite, evals.json, Makefile reflect-eval targets, and even `src/superclaude/`) lives under a sibling repo at `/config/workspace/IronClaude/` instead.

Evidence:

- `ls /config/workspace/IronClaude/.dev/eval-workspaces/` → "No such file or directory" (verified 2026-05-31).
- `find /config/workspace/Coder -type d -name "eval-workspaces"` → empty.
- `find /config/workspace/Coder -name "Makefile"` → empty (the Coder repo has no Makefile at all).
- `find /config/workspace/Coder -name "grader.py"` → empty.
- `ls /config/workspace/Coder/` top-level contains: `.agents/`, `_bmad/`, `_bmad-output/`, `catalogue/`, `.claude/`, `.dev/`, `docs/`, `.github/`, `openspec/`, `postmortem/`, `scripts/`, `templates/` — no Python project, no Makefile, no `src/superclaude/`. This is a documentation/configuration repo, not the SuperClaude framework repo.
- The merged proposal at `/config/workspace/IronClaude/.dev/brainstorm/reflect-verification-gap-20260531/MERGED-PROPOSAL.md:503` writes paths as `.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/...` (repo-root-relative). The proposal implicitly assumes the IronClaude layout but is staged from the Coder repo.

The full sc-reflect workspace **does exist** under `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/`. Verified via `ls` (2026-05-31, dir mtime 2026-05-27 19:24). Layout there:

```text
/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/
├── SPEC.md                      # 155,423 bytes
├── grader.py                    # 20,939 bytes — DSL extensions implemented
├── aggregate_iteration.py       # 6,798 bytes
├── evals/evals.json             # 20 evals: 3 pilot + 15 promotion + 2 falsifier
├── iterations/.gitkeep
├── skill-snapshot/reflect-v1.md # frozen baseline
└── cases/
    ├── pre-trivial-coverage-gap/{expected.yaml, input/{spec.md, tasklist.md}}
    ├── post-small-diff-clean/{expected.yaml, input/{diff.patch, tasklist.md}}
    ├── post-large-diff-mixed/{expected.yaml, input/{diff.patch, tasklist.md}}
    ├── promotion/ (15 promotion-*.yaml cases)
    └── falsifier-suite/
        ├── README.md
        ├── T2-converges-on-wrong.yaml              (SKELETON, status: skeleton-pending-iteration-3-fixture)
        ├── T2-judge-class-collision.yaml           (SKELETON)
        └── fixtures/spec-with-deliberate-misclassification.md  (placeholder)
```

**Builder implication.** The task-builder MUST either (a) target the IronClaude repo (preferred — that's where the SuperClaude framework actually lives), or (b) include an explicit `mkdir -p .dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` step PLUS bootstrap items for `grader.py`, `evals/evals.json`, `Makefile`, `SPEC.md`, `aggregate_iteration.py` if the work is genuinely scoped to Coder. Option (a) is correct — verify with the PM before tasklist materialization.

---

## existing falsifier YAML shape (verbatim from IronClaude)

The existing two skeleton YAMLs at `IronClaude/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/` use a tighter shape than the §7.1/§7.2 prose-style merged-proposal blocks. Both are SKELETONS — they ship a minimal contract the grader can verify structurally, with a `TODO_ITERATION_3` block describing how to promote to active.

### T2-converges-on-wrong.yaml (skeleton, verbatim)

```yaml
# SKELETON — iteration-3 follow-up authors full fixture and flips status to active.
# Spec §12.5 lines 1018-1059 (canonical falsifier case shape) + W-A8 spec-panel fix.
id: T2-converges-on-wrong
status: skeleton-pending-iteration-3-fixture
description: "T2 reviewer ensemble converges on the WRONG answer when given a fixture with deliberate misclassification, exercising the heterogeneous-reviewer-ensemble guarantee."
expected_grader_emission:
  skeleton_present: true
iteration_3_fixture_path: cases/falsifier-suite/fixtures/spec-with-deliberate-misclassification.md
canonical_assertion_for_iteration_3: "convergence_score < 0.75 OR verdict == regression_present"
related_spec_references:
  - "§11.4 heterogeneous reviewer ensemble (anti-representational-bias rationale)"
  - "§7.1 reviewer composition rules"
  - "§11.3 blind calibration disjoint-set"

# When iteration-3 promotes to active, populate the following block and remove this placeholder.
TODO_ITERATION_3:
  - "Promote status field to `active` (byte-exact replacement)."
  - "Add canonical fields: `type`, `fixture`, `expected`, `assertion` per §12.5."
  - "Author the fixture content at `fixtures/spec-with-deliberate-misclassification.md` (currently a placeholder)."
  - "Run `make reflect-eval` against this case and confirm the canonical assertion `convergence_score < 0.75 OR verdict == regression_present` actually triggers."
  - "If the assertion fails to trigger, escalate per the falsifier-suite README: the sufficiency claim is empirically wrong."
```

(Source: `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-converges-on-wrong.yaml:1-22`.)

### T2-judge-class-collision.yaml (skeleton, verbatim)

Same shape, different ID/description and references. Source: `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/T2-judge-class-collision.yaml:1-23`.

### Required-field contract for skeleton state

The grader (see next section) only requires the YAML to parse and the `status` field to equal `skeleton-pending-iteration-3-fixture`. Everything else (`id`, `description`, `expected_grader_emission`, `iteration_3_fixture_path`, `canonical_assertion_for_iteration_3`, `related_spec_references`, `TODO_ITERATION_3`) is by **convention**, not enforced by the grader. The README at `IronClaude/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/README.md:23` documents the contract.

### Required-field contract for active state

When `status: active`, the grader requires `{id, type, fixture, expected, assertion}` (this set is named `CANONICAL_FALSIFIER_FIELDS` at `grader.py:117`). Missing any one → FAIL.

---

## grader.py assertions relevant to OVM cases

The grader at `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/grader.py` (20,939 bytes, 8 baseline + 10 new types per `refs/grader-extensions.md`) implements:

| Assertion type | Suitable for OVM YAML? | Notes |
|----------------|------------------------|-------|
| `falsifier_skeleton_present` | YES — primary | Defined at `grader.py:270-286`. Verifies case YAML exists, parses, `status` is `skeleton-pending-iteration-3-fixture` (PASS) or `active` with canonical fields (PASS). Anything else FAIL. |
| `yaml_field` (baseline) | YES — pin scalar fields | Verify `outcome_claims_total: >= 1` style scalar minima are NOT possible with this — `yaml_field` does exact-equal. Use `yaml_field_min` for `>=`. |
| `yaml_field_min` (baseline) | YES — numeric minima | For `outcome_claims_total: >= 1`, `outcome_claims_failed: >= 1`, `deviation_count_by_class.regression: >= 1`. |
| `yaml_list_contains` (new) | YES | For `outcome_claims_by_seat.external_spec`, `verification_seat: external-spec`, list membership in `deferred_runbook` fields. Doc: `refs/grader-extensions.md:104-132`. |
| `regex_present` (new) | MAYBE | For `claim_id matches "docker.io_provides_docker_cli"` style fuzzy pattern matches. Doc: `refs/grader-extensions.md:62-81`. |
| `path_exists` / `path_does_not_exist` (new) | YES | For `evidence_ref: matches "<output>/external-spec-cache/apt-cache-show-docker.io.*"`. Doc: `refs/grader-extensions.md:216-256`. |
| `citation_resolves` (new) | NO — OVM not citation-heavy | Mostly for REPORT.md grounding checks. |
| `matrix_covers_items` (new) | NO | Coverage-matrix-specific. |
| `checkpoint_logged` (new) | MAYBE | If OVM emits `audit.log` rows for `outcome_verification_complete` checkpoint, this would gate. |
| `deviation_class_matches` (new) | YES | For asserting `deviation_count_by_class.regression: >= 1` mapping in deviation-ledger.yaml. |

### `falsifier_skeleton_present` implementation (verbatim)

```python
CANONICAL_FALSIFIER_FIELDS = {"id", "type", "fixture", "expected", "assertion"}

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

Source: `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/grader.py:270-286`. Dispatcher wiring at `grader.py:405-406`.

**Key insight for OVM builder:** the v1 ship target should be SKELETONS (status `skeleton-pending-iteration-3-fixture`). The grader will accept them as PASS via `falsifier_skeleton_present`. The full assertion-level YAML (per merged proposal §7) is iteration-3 work. This matches the W-A8 spec-panel pattern already in use for the two T2 cases.

---

## merged-proposal § 7 falsifier specs → grader-YAML mapping

The merged-proposal §7 falsifier blocks use prose-style `expected:` / `assertion:` fields. These are NOT grader-evaluable as-written. Two paths:

**Path A (recommended for v1 ship): SKELETON shape.** Mirror the existing T2 cases — ship YAML with `status: skeleton-pending-iteration-3-fixture` + descriptive metadata. The grader's `falsifier_skeleton_present` returns PASS structurally. Promotion to `active` is iteration-3 follow-up.

**Path B (full iteration-3 fixture authoring):** Translate each prose `expected:` / `assertion:` block into grader-assertion entries in `evals/evals.json`. The case YAML still ships, but it gets paired with a full assertion array in `evals.json`.

### Mapping table — `outcome-verification-docker-cli-miss` → grader assertions (Path A: skeleton)

| Merged-proposal field (§7.1 lines 506-557) | Grader treatment (skeleton mode) |
|---|---|
| `id: outcome-verification-docker-cli-miss` | YAML field, structural only — not enforced |
| `type: held-out adversarial` | YAML field, structural only — not enforced |
| `status: active` (proposal) → CHANGE to `status: skeleton-pending-iteration-3-fixture` for v1 ship | Required for `falsifier_skeleton_present` PASS |
| `fixture:`, `setup:`, `pre_seeding_mechanism:`, `expected:`, `assertion:`, `severity:` | Documented in YAML but unverified by grader in skeleton mode; promoted to grader-evaluated fields in iteration-3 |
| `expected.outcome_claims_total: >= 1` | Iteration-3: `yaml_field_min` against `with_skill/outputs/outcome-claims.yaml`, field `outcome_claims_total`, min `1` |
| `expected.outcome_claims_failed: >= 1` | Iteration-3: `yaml_field_min` (same shape) |
| `expected.outcome_verification_complete: false` | Iteration-3: `yaml_field` against same file, field `outcome_verification_complete`, expected `false` |
| `expected.promotion_action: skipped` | Iteration-3: `yaml_field` against `promotion-log.yaml`, field `promotion_action`, expected `skipped` |
| `assertion: outcome_claims_failed >= 1 AND status == partial AND promotion_action == skipped` | Iteration-3: compound — split into 3 grader assertions of types `yaml_field_min` + `yaml_field` + `yaml_field` |
| `severity: AUTO-FAIL if ...` | Iteration-3: encoded as separate `regex_absent` or inverse assertions; severity itself is reporting metadata |

### Mapping table — `outcome-verification-deferred-runtime-config` → grader assertions (Path A: skeleton)

Same skeleton-mode treatment. Notable additional structure in §7.2:

| Field (§7.2 lines 573-619) | Grader treatment |
|---|---|
| `expected.deferred_outcomes_runbook_present: true` | Iteration-3: `yaml_field` |
| `expected.promotion_deferred_runbook_paths: not empty` | Iteration-3: `yaml_list_contains` (needs nonempty check helper) OR `yaml_field_min` on `len(...)` if grader supports |
| `assertion_pass:` / `assertion_fail_runbook_empty:` (dual block) | Iteration-3: two paired eval entries in `evals.json` — one fixture variant for "runbook complete" pass, one for "runbook empty" fail |

---

## invocation: how grader runs (Makefile target, env vars, exit codes)

From `/config/workspace/IronClaude/Makefile:493-505`:

```makefile
reflect-eval:
	@mkdir -p .dev/eval-workspaces/sc-reflect/iterations/$(shell date +%Y%m%d-%H%M%S)
	@uv run python .dev/eval-workspaces/sc-reflect/grader.py \
		.dev/eval-workspaces/sc-reflect/iterations/$(shell date +%Y%m%d-%H%M%S)

reflect-eval-quick:
	@mkdir -p .dev/eval-workspaces/sc-reflect/iterations/$(shell date +%Y%m%d-%H%M%S)-quick
	@uv run python .dev/eval-workspaces/sc-reflect/grader.py \
		.dev/eval-workspaces/sc-reflect/iterations/$(shell date +%Y%m%d-%H%M%S)-quick
	@echo "Note: pilot-subset filtering is iteration-2 follow-up; this target currently runs the full eval set in a -quick-suffixed iteration dir."
```

Key facts:
- Invocation: `uv run python <grader-path> <iteration-output-dir>` (CWD = repo root).
- Iteration dir naming: `iterations/<YYYYMMDD-HHMMSS>[-quick]/`.
- No env vars are documented as required. PyYAML must be available in the UV env (`yaml.safe_load` is used by every new assertion type — `refs/grader-extensions.md:5`).
- `reflect-eval-quick` and `reflect-eval` currently run the same eval set; the "-quick" pilot-subset filtering is iteration-2 follow-up per the Makefile comment.
- Per-PR CI cadence: every PR touching reflect skill/command (Makefile comments lines 491, 500).
- Per `grader.py:22-23` docstring: `python grader.py <iterations/iteration-N-dir>` — single positional argument.

The grader reads `eval_metadata.json` from each `eval-<name>/` subdirectory inside the iteration dir, evaluates assertions, writes `grading.json` to `eval-<name>/with_skill/grading.json` and `eval-<name>/old_skill/grading.json`. Output schema documented at `grader.py:11-12`: `{expectations: [{text, passed, evidence}], summary: {passed, failed, total, pass_rate}}`.

Exit codes are not explicitly documented in the snippet read; the grader likely uses `sys.exit(0)` / `sys.exit(1)` based on whether all assertions passed. CI gating logic lives in the Makefile target shell wrapping.

---

## sibling eval-workspace pattern

The canonical sibling is **`sc-brainstorm/`** at `/config/workspace/IronClaude/.dev/eval-workspaces/sc-brainstorm/`. Key differences vs sc-reflect:

- `sc-brainstorm/` has NO `cases/` directory — it uses `live-runs/` instead (per-eval subdirs like `eval-code-feature-flag-task/`, `eval-code-migrate-pytest-vitest/`).
- `sc-brainstorm/grader.py` ships the **8 baseline assertion types** that sc-reflect inherits and extends.
- `sc-brainstorm/` does NOT have a falsifier-suite — sc-reflect is the first workspace to ship one.

Other siblings:
- `sc-troubleshoot/`, `sc-auggie-review/`, `sc-release-split-protocol/` — all under `IronClaude/.dev/eval-workspaces/`.
- `prd-bug-test/`, `prd-cli-audit/`, `prd-test-product/`, `prd-dry-run-test/`, `__ac1_probe__/` — auxiliary fixtures.

**Pattern conclusion:** The `cases/falsifier-suite/` directory shape is unique to `sc-reflect/`. The merged-proposal §7 OVM additions land in the same directory, alongside `T2-converges-on-wrong.yaml` and `T2-judge-class-collision.yaml`. The skeleton shape (current T2 YAMLs) is the canonical template the builder should copy from for the new OVM cases.

**Skeleton template the builder should clone (8 fields):**

```yaml
# SKELETON — iteration-N follow-up authors full fixture and flips status to active.
# Spec <REF> + <provenance note>.
id: <case-id-slug>
status: skeleton-pending-iteration-3-fixture
description: "<one-line description>"
expected_grader_emission:
  skeleton_present: true
iteration_3_fixture_path: cases/falsifier-suite/fixtures/<fixture-file>
canonical_assertion_for_iteration_3: "<full assertion in plain English>"
related_spec_references:
  - "<§X.Y rationale>"
TODO_ITERATION_3:
  - "<step 1>"
  - "<step 2>"
```

The corresponding `evals.json` entry pattern (mirror IronClaude lines 465-495):

```json
{
  "id": <N>,
  "name": "<case-id-slug>",
  "case_file": "cases/falsifier-suite/<case-id-slug>.yaml",
  "use_case": "<short description>",
  "spec_ref": "<§ref>",
  "status": "skeleton-pending-iteration-3-fixture",
  "description": "<longer description>",
  "assertions": [
    {
      "type": "falsifier_skeleton_present",
      "case_yaml": "cases/falsifier-suite/<case-id-slug>.yaml",
      "text": "Falsifier skeleton <case-id-slug> is present and well-formed"
    }
  ]
}
```

---

## Summary

1. **The sc-reflect eval-workspace does NOT exist in `/config/workspace/Coder/`.** It exists at `/config/workspace/IronClaude/.dev/eval-workspaces/sc-reflect/`. The Coder repo has no `Makefile`, no `src/superclaude/`, no `grader.py`. **This is a wrong-repo / cross-repo blocker the builder MUST resolve with the PM before generating task items.** Likely correct target repo: IronClaude.

2. **`grader.py` and the `falsifier_skeleton_present` assertion are fully implemented** at `IronClaude/.dev/eval-workspaces/sc-reflect/grader.py:270-286` and dispatched at `grader.py:405-406`. The 10 new + 8 baseline assertion types are all available. No `grader.py` work is needed.

3. **Existing falsifier YAML shape ships as SKELETONS.** Both `T2-converges-on-wrong.yaml` and `T2-judge-class-collision.yaml` use a tight 8-field skeleton template with `status: skeleton-pending-iteration-3-fixture` + `TODO_ITERATION_3:` block. The merged-proposal §7 prose `expected:` / `assertion:` blocks are NOT grader-evaluable as-written; the v1-ship target should be skeleton YAMLs that the grader accepts via `falsifier_skeleton_present`, with full assertion authoring deferred to iteration-3 (matching W-A8 spec-panel precedent).

4. **Builder action items (assuming IronClaude target):**
   - Write 2 new skeleton YAMLs at `IronClaude/.dev/eval-workspaces/sc-reflect/cases/falsifier-suite/`:
     - `outcome-verification-docker-cli-miss.yaml`
     - `outcome-verification-deferred-runtime-config.yaml`
   - Both use the 8-field skeleton template above.
   - Append 2 entries to `IronClaude/.dev/eval-workspaces/sc-reflect/evals/evals.json` (ids 21, 22) mirroring entries 19-20 (lines 465-495).
   - No grader.py changes required — `falsifier_skeleton_present` already exists.
   - No Makefile changes required — `reflect-eval` already runs every case in `evals.json`.

5. **Blockers / open questions:**
   - **Cross-repo confusion**: Coder repo vs IronClaude repo — PM must clarify. The merged proposal was authored in Coder but references infrastructure that only exists in IronClaude.
   - The §7.1 merged-proposal block marks `status: active` rather than skeleton — this contradicts the established W-A8 skeleton-first pattern. Confirm with PM whether iteration-3 fixture content is also in-scope (Path B), or whether v1-ship is skeleton-only (Path A, recommended).

---

**File:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-OVM-VERIFICATION-GAP-CLOSURE-20260531-040500/research/03-eval-workspace-falsifier-patterns.md`
