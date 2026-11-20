9e97e622ffb744b63e9e9ddb5cd5767036eefc07
Review one task for spec compliance.

Task brief: ## Task 2: Move the reflect contract checkers, scripts and tests to 1.9.0

Depends on: Task 1

Edit `src/superclaude/cli/reflect/panel_lint.py`: rename the field tuple `STABLE_FIELDS_1_8_0` to `STABLE_FIELDS_1_9_0` and add `finding_counts` to it, make the lint accept both recorded 1.8.0 contracts (where `finding_counts` is optional) and 1.9.0 contracts (where it is part of the field list) through a `CONTRACT_VERSIONS` tuple, and update the L1, L2, L3 and B-bump failure messages and the module docstring that name 1.8.0 (its users are `scripts/reflect_shadow_exit.py` and `tests/cli/reflect/test_panel_contract_lint.py`). Edit `scripts/reflect_shadow_exit.py` and `scripts/reflect_verdict_replay.py` (`VERSION = "1.8.0"`) so a recorded 1.8.0 or 1.9.0 contract is counted and no other version is. Edit `tests/cli/reflect/test_panel_contract_lint.py`, `tests/cli/reflect/test_shadow_skill_contract.py` (both pin the heading `### 9.1 Stable contract (contract_version: 1.8.0)`), `tests/cli/reflect/test_shadow_exit_script.py`, `tests/cli/reflect/test_verdict_replay_script.py`, `tests/review/test_reflect_consumer_inventory.py` and the fixtures `tests/cli/reflect/fixtures/panel_lint_legacy/return-contract.yaml`, `tests/cli/reflect/fixtures/autofixable_drift_both.yaml` and `tests/cli/reflect/fixtures/autofixable_drift_plan.yaml` wherever they pin the current version. `src/superclaude/cli/reflect/contract.py` (checks the major version only) and `src/superclaude/cli/reflect/models.py` need no change; `scripts/reflect_consumer_inventory.py` only reports and changes only if its test requires it. In `tests/cli/reflect/test_shadow_skill_contract.py` also rewrite two tests that compare the reflect SKILL.md with git HEAD: `test_stable_contract_block_and_version_are_byte_identical_to_head` (compare the section 9.1 block with a pinned copy of the 1.9.0 block stored under `tests/cli/reflect/fixtures/`) and `test_skill_changes_are_confined_to_the_allowed_sections` (add every section Task 1 edits to the allowed list: `### 4.3a `, `### 9.1 ` (it also holds the sentence "Contract version is v1.8.0"), `### 9.4 ` only if Task 1 edits it, and `## 17.6` (it holds the grader row); drop the assertion that 9.1 is untouched).

Acceptance criteria:
- Both a 1.8.0 contract without `finding_counts` and a 1.9.0 contract with it pass `lint_panel_contract` (checks L1, L2 and the B bump rule); a contract with an unknown top-level key or any other version still fails for the right reason (new cases in `tests/cli/reflect/test_panel_contract_lint.py`), and `scripts/reflect_shadow_exit.py` still passes on a recorded 1.8.0 shadow-run fixture.
- The two rewritten tests in `tests/cli/reflect/test_shadow_skill_contract.py` pass against the edited reflect SKILL.md.
- `uv run pytest tests/cli/reflect tests/review/test_reflect_consumer_inventory.py -q` passes.
- `src/superclaude/cli/reflect/contract.py` parses a fixture 1.9.0 contract that has `finding_counts` without error (one new assertion in an existing test under `tests/cli/reflect/`).
Global constraints: ## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of the edited files (including the new `refs/remediation.md` and `scripts/remediate.py` of the workflow skill, which the plugin mirror must carry (the `diff -rq` checks of Task 6 require it), and `plugins/superclaude/commands/workflow.md`), `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/` mirrors an edited file (the workflow and implement protocols and `commands/workflow.md`), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference); a new file in an already mirrored folder is mirrored too. `remediate.py` uses only the Python standard library (installed skill scripts run under `uv run --no-project`) and edits archived contracts by appending lines, never by loading and re-writing the YAML.
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag). On the panel path, `medium` counts findings-v2 severity MAJOR with `blocking` false and `note` counts severity MINOR.
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).
Start sha: 9e97e622ffb744b63e9e9ddb5cd5767036eefc07
Diff against the start snapshot: diff --git a/scripts/reflect_consumer_inventory.py b/scripts/reflect_consumer_inventory.py
index bf21d5bc6..ce57ec599 100644
--- a/scripts/reflect_consumer_inventory.py
+++ b/scripts/reflect_consumer_inventory.py
@@ -388,7 +388,7 @@ def render(root: Path, res: dict) -> str:
     out += _equality_line(res)
     out.append(
         "- The Task 15 lint (`src/superclaude/cli/reflect/panel_lint.py`) checks the version as "
-        '`version != CONTRACT_VERSION` with `CONTRACT_VERSION = "1.8.0"`, not as the literal equality this search '
+        '`version not in CONTRACT_VERSIONS` with `CONTRACT_VERSIONS = ("1.8.0", "1.9.0")`, not as the literal equality this search '
         "looks for, so a rerun does not list it here."
     )
     out.append(_grader_line(root, res))
diff --git a/scripts/reflect_shadow_exit.py b/scripts/reflect_shadow_exit.py
index fa09f0559..bb88a761b 100644
--- a/scripts/reflect_shadow_exit.py
+++ b/scripts/reflect_shadow_exit.py
@@ -6,7 +6,7 @@ files only (no model, no process, no network) and writes only the optional ``--o
 
 Shadow runs: every ``<runs-root>/pre-*/panel/manifest.json`` whose ``t2_engine_effective`` is ``shadow``. A manifest in
 state ``published`` is counted; ``failed`` fails the exit; any other state is an incomplete run, listed and not
-counted. The legacy baseline is the recorded 1.8.0 pre runs without ``panel/manifest.json`` (the set of
+counted. The legacy baseline is the recorded 1.8.0 or 1.9.0 pre runs without ``panel/manifest.json`` (the set of
 ``scripts/reflect_verdict_replay.py``).
 
 Per counted run the script joins ``return-contract.yaml`` and ``adversarial/merged-verdict.yaml`` and checks:
diff --git a/scripts/reflect_verdict_replay.py b/scripts/reflect_verdict_replay.py
index 0ced29ba9..e2d762799 100644
--- a/scripts/reflect_verdict_replay.py
+++ b/scripts/reflect_verdict_replay.py
@@ -6,7 +6,7 @@ files only: no model, no process, no network, and it writes nothing.
 
 Legacy set: every ``<runs-root>/pre-*`` directory (default runs root: ``.dev/reflect`` under the repository that
 holds this script) that holds a ``return-contract.yaml`` which parses to a mapping with ``contract_version`` equal
-to the string ``"1.8.0"`` and has no ``panel/manifest.json``. Other contracts are counted and listed as skipped,
+to the string ``"1.8.0"`` or ``"1.9.0"`` and has no ``panel/manifest.json``. Other contracts are counted and listed as skipped,
 with the reason.
 
 Shadow set: the run directories given with ``--shadow`` (a shadow run is one with ``panel/manifest.json``; the
@@ -29,7 +29,7 @@ Differences: runs are paired by directory name. A paired run differs when its (v
 degraded reason is a shadow run whose verdict is ``degraded`` and that either (a) is paired with a legacy run whose
 (verdict, reason) is not the same, or (b) is unpaired and has a degraded reason that no legacy run has. The script
 prints both sets, for each ``allow_single_vendor`` value, and exits 1 when there is any new degraded reason, 0
-otherwise, 2 on a usage error. Limits: a shadow contract that is unusable or not 1.8.0 is skipped and listed, and a
+otherwise, 2 on a usage error. Limits: a shadow contract that is unusable or not 1.8.0 or 1.9.0 is skipped and listed, and a
 shadow verdict of ``blocked`` or ``halted`` is a difference when paired but not a new degraded reason; neither
 changes the exit code.
 
@@ -51,7 +51,7 @@ from superclaude.cli.reflect.contract import derive_verdict
 
 ROOT = Path(__file__).resolve().parents[1]
 CONTRACT = "return-contract.yaml"
-VERSION = "1.8.0"
+VERSIONS = ("1.8.0", "1.9.0")
 DERIVE_ARGS = {"expected_tier": 2, "child_rc": 0}
 SINGLE_VENDOR_MODES = (
     False,
@@ -70,7 +70,7 @@ def load(run: Path) -> tuple[dict | None, str | None]:
         return None, "unreadable or unparseable"
     if not isinstance(data, dict):
         return None, "not a mapping"
-    if data.get("contract_version") != VERSION:
+    if data.get("contract_version") not in VERSIONS:
         return None, f"contract_version {data.get('contract_version')!r}"
     return data, None
 
diff --git a/src/superclaude/cli/reflect/panel_lint.py b/src/superclaude/cli/reflect/panel_lint.py
index b235932d0..23d7ccbf5 100644
--- a/src/superclaude/cli/reflect/panel_lint.py
+++ b/src/superclaude/cli/reflect/panel_lint.py
@@ -1,7 +1,8 @@
 """Contract lint for panel-run reflect output directories (the reflect Tier 2 panel, Stages 0-2).
 
 lint_panel_contract(out_dir, legacy_contract) returns the failure lines of a panel run's return-contract.yaml
-against the frozen 1.8.0 contract; an empty list is a pass. It is a read-only checker: it reads
+against the frozen 1.9.0 contract (a recorded 1.8.0 contract, where finding_counts is optional, passes too); an empty
+list is a pass. It is a read-only checker: it reads
 out_dir/return-contract.yaml, out_dir/panel/manifest.json, out_dir/adversarial/merged-verdict.yaml,
 out_dir/reviewer-cards/ and out_dir/audit.log, and writes nothing. The assertion ids (L0 to L7, B) and their exact
 messages are those of the plan's lint design (artifacts/lint-test-design.md of the managed package).
@@ -11,7 +12,7 @@ shadow mode use. The --unattended layout (nested/adversarial-<n>/, SKILL.md sect
 run L6 reports `merged-verdict: absent`. The lint is meant for panel-run contracts and the matched legacy fixture,
 not as a retro-check of every recorded run.
 
-STABLE_FIELDS_1_8_0 and TELEMETRY_FIELDS are copies of the top-level keys of the YAML blocks of SKILL.md sections
+STABLE_FIELDS_1_9_0 and TELEMETRY_FIELDS are copies of the top-level keys of the YAML blocks of SKILL.md sections
 9.1 and 9.2. Those blocks do not parse as YAML (they hold `a | b` value forms), so the keys are taken line by line:
 every line of the block matching ^([a-z_0-9]+): (no indent). extract_field_list applies that rule, and a test fails
 when the constants and the SKILL.md sections differ.
@@ -30,7 +31,7 @@ import yaml
 
 from .contract import _LOAD_BEARING_BOOL_FIELDS
 
-STABLE_FIELDS_1_8_0 = (
+STABLE_FIELDS_1_9_0 = (
     "contract_version",
     "status",
     "mode",
@@ -114,6 +115,7 @@ STABLE_FIELDS_1_8_0 = (
     "remediation_task_path",
     "remediation_plan_path",
     "handoff_memory_key",
+    "finding_counts",
     "cannot_validate_without_user_input",
     "regression_present",
     "unauthorized_deviation_present",
@@ -182,7 +184,7 @@ PARITY_FIELDS = (
     "reviewer_cards",
 )
 LEGAL_MERGE_METHODS = ("adversarial", "single-reviewer-fallback")
-CONTRACT_VERSION = "1.8.0"
+CONTRACT_VERSIONS = ("1.8.0", "1.9.0")  # 1.8.0 is a recorded contract; finding_counts is optional there
 
 _KEY_LINE = re.compile(r"(?m)^([a-z_0-9]+):")
 _CARD_FILE = re.compile(r"^reviewer-(\d+)-card\.(?:yaml|yml|md)$")
@@ -300,7 +302,7 @@ def _ev1(out: Path, c: dict, *, use_manifest: bool = True) -> list[str]:
 
 
 def lint_panel_contract(out_dir: str | Path, legacy_contract: dict) -> list[str]:
-    """Failure lines of the panel run in out_dir against the 1.8.0 contract and the matched legacy contract."""
+    """Failure lines of the panel run in out_dir against the 1.9.0 contract and the matched legacy contract."""
     out = Path(out_dir)
     state, c = _read_yaml_mapping(out / "return-contract.yaml")
     if state != "ok":
@@ -309,13 +311,13 @@ def lint_panel_contract(out_dir: str | Path, legacy_contract: dict) -> list[str]
         ]
     lines: list[str] = []
     version = c.get("contract_version")
-    if version != CONTRACT_VERSION:
+    if version not in CONTRACT_VERSIONS:
         lines.append(
-            f"L1 contract_version: expected {CONTRACT_VERSION!r}, got {version!r}"
+            f"L1 contract_version: expected one of {', '.join(map(repr, CONTRACT_VERSIONS))}, got {version!r}"
         )
-    known = set(STABLE_FIELDS_1_8_0) | set(TELEMETRY_FIELDS) | {"telemetry"}
+    known = set(STABLE_FIELDS_1_9_0) | set(TELEMETRY_FIELDS) | {"telemetry"}
     key_lines = [
-        f"L2 stable keys: top-level key {k!r} is not in the 1.8.0 stable field list or the telemetry block"
+        f"L2 stable keys: top-level key {k!r} is not in the 1.9.0 stable field list or the telemetry block"
         for k in sorted((k for k in c if k not in known), key=str)
     ]
     lines += key_lines
@@ -330,7 +332,7 @@ def lint_panel_contract(out_dir: str | Path, legacy_contract: dict) -> list[str]
     l3_failed = not legal if wave4 else not (merge is None or legal)
     if l3_failed:
         lines.append(
-            f"L3 merge_method: {merge!r} is not a legal 1.8.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')"
+            f"L3 merge_method: {merge!r} is not a legal 1.9.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')"
         )
     score = c.get("adversarial_convergence_score")
     if score is not None and not (type(score) is float and math.isfinite(score)):
@@ -359,7 +361,7 @@ def lint_panel_contract(out_dir: str | Path, legacy_contract: dict) -> list[str]
             )
     if key_lines or l3_failed:
         lines.append(
-            f"B bump rule: the contract leaves 1.8.0 ({len(key_lines)} stable-key violation(s), "
+            f"B bump rule: the contract leaves 1.9.0 ({len(key_lines)} stable-key violation(s), "
             f"{1 if l3_failed else 0} EV-2 value violation(s)); a new stable key or merge_method value needs a "
             "contract version bump, which this plan does not make"
         )
diff --git a/tests/cli/reflect/fixtures/stable_contract_1_9_0_block.yaml.txt b/tests/cli/reflect/fixtures/stable_contract_1_9_0_block.yaml.txt
new file mode 100644
index 000000000..055c52824
--- /dev/null
+++ b/tests/cli/reflect/fixtures/stable_contract_1_9_0_block.yaml.txt
@@ -0,0 +1,168 @@
+```yaml
+contract_version: "1.9.0"   # #323: the change-summary corroboration field was removed (no consumer read it); the other fields keep their names. 1.9.0 ADDITIVE ONLY: +finding_counts ({blocking, label_high, medium, note}); 1.8.0 ADDITIVE ONLY: +remediation_plan_path (plan-route sibling of remediation_task_path); 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.7.x runtime/semantic hardening: EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate + EV-2 merge_method legal-values guard (no stable-field change); 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields); 1.7.0 (FR-RH1) ADDITIVE ONLY: +reachability_* fields
+status: success | partial | failed | dry-run
+mode: pre | post
+tier_reached: 1 | 2 | 3
+report_path: <abs path to REPORT.md>
+audit_log_path: <abs path>
+confidence_calibrated: <float 0.00-1.00>
+escalation_rule_matched: <int 1-8> | null
+onboarding_ran: false                 # constant false since #323: the one-shot onboarding bootstrap was removed; kept for contract stability
+
+# UC-1 specific
+coverage_pct: <float 0.0-1.0> | null            # PARSED-ONLY denominator; pre-D13 semantics UNCHANGED (consumer-safe per the 9.4 additive policy)
+coverage_pct_union: <float 0.0-1.0> | null      # NEW (1.5.0, D13): union denominator (parsed + inferred rows) per Step 1B.0; reflect-internal gates read this
+coverage_undefined: <bool>           # true when no parseable requirement IDs across BOTH extraction passes
+coverage_degraded: <string> | null   # NEW (1.5.0, D13): "parsed-sparse" when inferred_count > parsed_count (Step 1B.2b); table-wide T1-stop pre-filter
+unmapped_requirements: [<list>]                 # PARSED-ONLY; pre-D13 semantics unchanged
+unmapped_requirements_union: [<list>]           # NEW (1.5.0, D13): union set incl. unmatched INF-NNN rows
+best_practice_grade: <int 0-5> | null
+implementation_coverage_pct: <float 0.0-1.0> | null   # FR-1 (null when the kind-guard never fired — C5)
+missing_implementations:                              # FR-1
+  - abstract_name_path: <string>
+    expected_count: <int>
+    found_count: <int>
+hierarchy_slice_path: null                            # constant null since #323: the type-hierarchy step was removed; kept for contract stability
+hierarchy_coverage_pct: null                          # constant null since #323 (same reason)
+
+# UC-2 specific
+tasklist_completion_pct: <float 0.0-1.0> | null
+deviation_count_by_class:
+  authorized: <int>
+  necessary: <int>
+  drift: <int>
+  regression: <int>
+deviation_register_path: <abs path> | null
+grounding_gaps_path: <abs path> | null    # parallel artifact for evidence-insufficient findings
+hunk_to_declaration_map_path: <abs path>   # FR-2 (UC-2 only)
+third_party_api_grounding:                 # FR-4
+  - api_name: <string>
+    dep_version: <string>
+    resolution_path: <string>
+third_party_api_verified: <bool>           # FR-4 (always false while Step 7 `search_deps` is skipped)
+verification_ran: <bool>                   # FR-4 (UC-2 Bash verification run, §6.1 steps 5 and 5.5)
+verification_invocations: <int>            # FR-4 (count of verify-log invocation entries)
+verification_failures: <int>               # FR-4 (exit_code != 0 count)
+verification_regressions_detected: <int>   # FR-4 (taxonomy-classified Regression exits on a claimed-passing file)
+verification_skip_reason: tool-unavailable|read-only-project|--no-verify|null   # FR-4
+
+# Runtime-surface reachability (FR-RSR — UC-2)
+# MANDATORY EMISSION (FR-RSR.7): whenever runtime_surface_sweep_ran is true, ALL SIX fields
+# below MUST be emitted with these EXACT names on EVERY path — REACHED, DEGRADE, and UNREACHED
+# alike. Do NOT invent alternative field names (e.g. runtime_surface_reachable,
+# reachability_path, static_caller_absent_is_expected); those are NOT contract fields and a
+# consumer keyed on §9.3 will not see them. Record the per-symbol verdict ONLY through these
+# six fields:
+#   • REACHED  → runtime_surface_unreached: 0, runtime_surface_degraded: false, unreached_surfaces: []
+#   • DEGRADE  → runtime_surface_degraded: true (+ a §10.6 Grounding Gap row); the symbol is NOT in unreached_surfaces
+#   • UNREACHED→ runtime_surface_unreached: <count ≥ 1>, with one unreached_surfaces[] entry per UNREACHED symbol
+# The count invariant len(unreached_surfaces) == runtime_surface_unreached MUST hold every run.
+runtime_surface_requirements: [<list str>]          # FR-RSR.1 (surface requirement ids tagged from symbol kind/decorator; [] when none)
+runtime_surface_sweep_ran: <bool>                   # FR-RSR.2 (true only when ≥1 tagged surface triggered the sweep)
+runtime_surface_ledger_path: <abs path> | null      # FR-RSR.2 (<output>/artifacts/runtime-surface-ledger.yaml; null when sweep did not run)
+runtime_surface_unreached: <int>                    # FR-RSR.2/6 (count of SYMBOLS reduced to UNREACHED; 0 on a fully-REACHED run; drives §5.3 pre-filter)
+runtime_surface_degraded: <bool>                    # FR-RSR.3/8 (true when ≥1 symbol reduced to DEGRADE → §10.6 Grounding Gap; false on a fully-REACHED run)
+unreached_surfaces: [<list of UnreachedSurface>]    # FR-RSR.6 (one entry per UNREACHED symbol; [] on REACHED and on DEGRADE-only runs)
+
+# Contracted-sink reachability / oracle-admissibility (FR-RH1 — UC-2)
+reachability_gate_ran: <bool>
+reachability_ledger_path: <abs path> | null          # null when the gate did not run
+reachability_requirements_scanned: <int>             # side-effect-bearing requirements evaluated
+reachability_unreachable: <int>                      # verdict==unreachable rows (each → regression_present); set by EITHER Step 5.6 real-boot durable-sink absence OR Step 5.6a static behavioral-unreachability of a spec-declared REQUIRED capability (annotation-free, no real-boot)
+reachability_unproven: <int>                         # verdict==unproven rows (each → a grounding-gaps row)
+reachability_real_boot_ran: <bool>                   # best-effort step-5.5 boot fired at least once
+reachability_skip_reason: --no-reachability|no-side-effect-requirements|spec-and-tasklist-absent|null
+
+# Reuse-Miss neighbour sweep (FR-REUSE — §6.1 step 4a / §10.8; UC-2). NO deviation_count_by_class.reuse_miss key (§17.7).
+reuse_sweep_ran: <bool>
+reuse_audit_path: <abs path> | null          # reuse-auditor's reuse-audit.yaml
+reuse_miss_blocking: <int>                    # rung-L3 findings mapped to Drift/Regression (§10.8)
+reuse_miss_advisory: <int>                    # rung ≤ L2 (non-gating)
+reuse_verdict_count_by_type: { reuse_by_import: <int>, mirror_shape: <int>, extract_shared: <int>, distinct: <int> }
+reuse_grounding_gap_count: <int>              # maybe-related/insufficient routed to §10.6
+neighbour_search_sampled: <bool>              # candidates exceeded the ≤12 cap
+neighbour_search_degraded: <bool>             # auggie-unavailable fallback used (caps findings at advisory L2)
+max_overlap_score: <float 0.0-1.0> | null
+
+# Input integrity
+input_sha256:                         # legacy single-file hashes preserved for backward-compat
+  tasklist: <hex>
+  spec: <hex> | null
+input_tree_sha256: <hex>              # AUTHORITATIVE: tree-hash over every input file
+input_tree_file_count: <int>          # number of files in the tree-hash; 1 for spec-only UC-1
+input_tree_snapshot_path: <abs path>  # <output>/artifacts/input-snapshot.yaml
+input_drift_detected: <bool>          # true if input_tree_sha256 mismatch at Wave 5 OR Wave 7 step 7.2
+input_drift_diff: [<list of {path, old_sha, new_sha, change_kind: added|removed|modified}>] | null
+
+# Hallucination guard
+citations_total: <int>
+citations_revalidated: <int>          # M; size of the re-Read subset; equals citations_total in full_reread mode
+citations_dropped: <int>              # >0 forces status: partial; in sampled mode this is the SAMPLE COUNT (§11.5)
+citations_dropped_extrapolated: <int> # population projection in sampled mode; recording-only, does NOT gate promotion
+citations_inferred: <int>             # [INFERRED]-tagged; does not force partial
+citation_budget_policy: full_reread | sampled
+evidence_validator_ran: bool
+citation_revalidation_at_promotion: bool   # true when Wave 7 step 7.2 re-Read cited files (Wave 6 ran)
+
+# Tier 2 artifacts
+reviewer_cards: [<list of paths>] | []
+adversarial_artifacts_dir: <path> | null   # consumer-side remap from sc-adversarial's `artifacts_dir` field (see §8)
+adversarial_convergence_score: <float> | null
+adversarial_unavailable: <bool>      # F3 path
+merge_method: adversarial | single-reviewer-fallback   # F2 path. [EV-2] LEGAL VALUES ARE EXACTLY {adversarial, single-reviewer-fallback}: any other value (inline, convergence-inline, an in-context "convergence" of the cards) is MALFORMED -> reject. A non-adversarial merge is legal ONLY via the F2/F3 fallback (single-reviewer-fallback + adversarial_unavailable: true + audit.log). Reflect MUST NOT synthesize its own merge.
+t2_model_class_diversity: full | degraded
+t2_vendor_diversity: multi | single   # warn-only in v1.0
+t2_effective_diversity: full | model-only | vendor-only | none   # derived; combines both diversity axes
+calibrator_diversity: full | degraded
+
+# Tier 3
+remediation_offered: bool
+remediation_accepted: bool | null
+task_file_path: <path> | null
+remediation_task_path: null   # FR-8, retired in 6.1.0: the MDTM route is gone, so this is always null. Kept in the schema so older reports still load.
+remediation_plan_path: <abs path> | null   # 1.8.0: absolute path of the sc:workflow tasklist `.dev/tasks/to-do/<slug>/<slug>.md` built in Wave 6 (the only route); null when no plan was built. The wrapper auto-fix loop READS this to auto-run /sc:implement.
+handoff_memory_key: null   # FR-3, retired in 6.1.0: always null, no handoff file is written. Kept in the schema so older reports still load.
+finding_counts: {blocking: <int>, label_high: <int>, medium: <int>, note: <int>}   # 1.9.0: computed from the merged findings after the evidence validator, in both pre and post modes. label_high counts the Deviations-table label HIGH (legacy path) or findings-v2 severity CRITICAL (panel path); blocking, medium and note count the grades `Blocking (...)`, `Medium:` and `Note:` (panel: the `blocking` flag, severity MAJOR not blocking, severity MINOR; see refs/reviewer-spec.md).
+
+# Asymmetric-cost flags (downstream automation must respect these)
+cannot_validate_without_user_input: bool
+regression_present: bool                   # FR-4: now verified-sourced from the §6.1 step 5.5 exit-code taxonomy (was task-log self-report)
+unauthorized_deviation_present: bool
+blocked_by_low_confidence: bool            # every actionable rec gated to <0.70 by confidence-check
+spec_is_wrong: bool                        # UC-2 — code is correct, spec contradicts on-disk reality
+user_decision_required: bool               # convergence < threshold AND no auto-route applies
+needs_human_decision: bool                 # grounding-gaps.yaml non-empty
+
+# Per-task verdict array (P1 + P2) — populated when UC-2 input is a multi-task tasklist
+per_task_verdicts:                       # empty list for UC-1 or single-task UC-2
+  - task_id: <string>
+    status: success | partial | failed
+    deviation_class: authorized | necessary | drift | regression | none
+    citations_dropped: <int>
+    per_task_validation_strength: <float 0.00-1.00>   # P2: calibrated, post-evidence-validator
+    evidence_anchor: <abs path or task-log ref>
+
+# Cross-task interaction-effects (P3) — UC-2 tasklist-scope only
+interaction_effects_scanned: bool         # true when Wave 1B.3 ran; false when skipped
+interaction_effects_findings: <int>       # count of cross_task invariant probe entries (sum of HIGH+MEDIUM+LOW)
+
+# Budget pre-flight (P5)
+budget_forced_tier_downgrade: bool        # true when --budget-remaining triggered tier downgrade
+budget_forced_stop: bool                  # true when --budget-remaining < 5
+budget_check_skipped: bool                # true when --budget-remaining was not provided
+forced_tier: 1 | 2 | null                 # populated when budget_forced_tier_downgrade == true
+
+# Promotion (UC-2 only — §14.5)
+promotion_action: moved | skipped | rejected | failed | already-promoted | resumed | dry-run | not-applicable
+promotion_adapter: task | sprint-release | none | null
+promotion_source: <abs path> | null
+promotion_destination: <abs path> | null
+promotion_log_path: <abs path> | null      # always set when Wave 7 ran
+promotion_gate_passed: bool | null         # null when mode == pre or Wave 7 skipped pre-gate
+promotion_skip_reason: user-flag | gate-failed | adapter-unresolved | dry-run | null
+promotion_fail_reason: source_disappeared | destination_collision | mv_error | sha_mismatch | null
+promotion_override_used: --promote-anyway | --promote-resume | null
+promotion_rollback_command: <string> | null   # only set on promotion_action: moved or resumed
+promotion_checkpoint_path: <abs path> | null  # set when cross-fs move occurred; see §14.5.5
+promotion_cross_fs: bool                       # true when source and destination on different filesystems
+promotion_pending: bool                        # true between pre-write (7.3.6) and finalization (7.6); only true in a crashed-mid-run log entry
diff --git a/tests/cli/reflect/test_panel_contract_lint.py b/tests/cli/reflect/test_panel_contract_lint.py
index e3c7f5337..880e5d08e 100644
--- a/tests/cli/reflect/test_panel_contract_lint.py
+++ b/tests/cli/reflect/test_panel_contract_lint.py
@@ -66,7 +66,7 @@ def own(run):
 
 def bump(n, m):
     return (
-        f"B bump rule: the contract leaves 1.8.0 ({n} stable-key violation(s), {m} EV-2 value violation(s)); "
+        f"B bump rule: the contract leaves 1.9.0 ({n} stable-key violation(s), {m} EV-2 value violation(s)); "
         "a new stable key or merge_method value needs a contract version bump, which this plan does not make"
     )
 
@@ -90,7 +90,7 @@ ALL_MISSING = "adversarial_unavailable: true, merge_method: single-reviewer-fall
 @pytest.mark.parametrize(
     "heading, constant",
     [
-        ("### 9.1 Stable contract (contract_version: 1.8.0)", pl.STABLE_FIELDS_1_8_0),
+        ("### 9.1 Stable contract (contract_version: 1.9.0)", pl.STABLE_FIELDS_1_9_0),
         ("### 9.2 Telemetry (non-stable)", pl.TELEMETRY_FIELDS),
     ],
 )
@@ -106,10 +106,13 @@ def test_pinned_field_lists_match_skill_md(heading, constant):
 
 def test_constant_sizes_and_load_bearing_import():
     # 26 telemetry names of the original section 9.2 plus the `telemetry` block that Task 19 added to it
-    assert len(pl.STABLE_FIELDS_1_8_0) == 110 and len(pl.TELEMETRY_FIELDS) == 27
+    # 110 fields of 1.8.0 plus finding_counts (1.9.0)
+    assert len(pl.STABLE_FIELDS_1_9_0) == 111 and len(pl.TELEMETRY_FIELDS) == 27
+    assert "finding_counts" in pl.STABLE_FIELDS_1_9_0
+    assert pl.CONTRACT_VERSIONS == ("1.8.0", "1.9.0")
     assert pl.LOAD_BEARING_BOOLS is _LOAD_BEARING_BOOL_FIELDS
     assert (
-        "citations_dropped_extrapolated" in pl.STABLE_FIELDS_1_8_0
+        "citations_dropped_extrapolated" in pl.STABLE_FIELDS_1_9_0
         and "citations_dropped_extrapolated" in pl.TELEMETRY_FIELDS
     )
 
@@ -156,6 +159,36 @@ def test_other_pass_variants(tmp_path, mutate):
     assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []
 
 
+COUNTS = {"blocking": 0, "label_high": 1, "medium": 2, "note": 3}
+
+
+def test_a_1_9_0_contract_with_finding_counts_passes(tmp_path):
+    run = make(
+        tmp_path,
+        mutate=lambda c: c.update(contract_version="1.9.0", finding_counts=COUNTS),
+    )
+    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []
+
+
+def test_a_recorded_1_8_0_contract_passes_with_or_without_finding_counts(tmp_path):
+    assert "finding_counts" not in LEGACY_CONTRACT
+    assert LEGACY_CONTRACT["contract_version"] == "1.8.0"
+    assert pl.lint_panel_contract(LEGACY, LEGACY_CONTRACT) == []
+    run = make(tmp_path, mutate=lambda c: c.update(finding_counts=COUNTS))
+    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == []
+
+
+def test_a_1_9_0_contract_with_an_unknown_key_still_fails(tmp_path):
+    run = make(
+        tmp_path,
+        mutate=lambda c: c.update(contract_version="1.9.0", finding_count=COUNTS),
+    )
+    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
+        "L2 stable keys: top-level key 'finding_count' is not in the 1.9.0 stable field list or the telemetry block",
+        bump(1, 0),
+    ]
+
+
 def test_p8_loud_fallback_passes(tmp_path):
     run = make(tmp_path, mutate=no_fallback_set, no_adv=True, audit=FALLBACK_AUDIT)
     assert pl.lint_panel_contract(run, own(run)) == []
@@ -176,7 +209,7 @@ def test_p9_tier_one_passes(tmp_path):
 def test_f1_extra_stable_key_is_named(tmp_path):
     run = make(tmp_path, mutate=lambda c: c.update(cluster_agreement=1.0))
     assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
-        "L2 stable keys: top-level key 'cluster_agreement' is not in the 1.8.0 stable field list or the telemetry block",
+        "L2 stable keys: top-level key 'cluster_agreement' is not in the 1.9.0 stable field list or the telemetry block",
         bump(1, 0),
     ]
 
@@ -185,19 +218,23 @@ def test_f2_merge_method_panel_fails(tmp_path):
     # merge_method is not a parity field, so only L3 and B appear
     run = make(tmp_path, mutate=lambda c: c.update(merge_method="panel"))
     assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
-        "L3 merge_method: 'panel' is not a legal 1.8.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')",
+        "L3 merge_method: 'panel' is not a legal 1.9.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')",
         bump(0, 1),
     ]
 
 
 def test_f3_f4_contract_version(tmp_path):
-    run = make(tmp_path, mutate=lambda c: c.update(contract_version="1.9.0"))
+    run = make(tmp_path, mutate=lambda c: c.update(contract_version="1.10.0"))
     assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
-        "L1 contract_version: expected '1.8.0', got '1.9.0'"
+        "L1 contract_version: expected one of '1.8.0', '1.9.0', got '1.10.0'"
     ]
     run = make(tmp_path, mutate=lambda c: c.pop("contract_version"), name="run2")
     assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
-        "L1 contract_version: expected '1.8.0', got None"
+        "L1 contract_version: expected one of '1.8.0', '1.9.0', got None"
+    ]
+    run = make(tmp_path, mutate=lambda c: c.update(contract_version="1.7.0"), name="run3")
+    assert pl.lint_panel_contract(run, LEGACY_CONTRACT) == [
+        "L1 contract_version: expected one of '1.8.0', '1.9.0', got '1.7.0'"
     ]
 
 
diff --git a/tests/cli/reflect/test_shadow_skill_contract.py b/tests/cli/reflect/test_shadow_skill_contract.py
index 6a784db8c..bb66b0b93 100644
--- a/tests/cli/reflect/test_shadow_skill_contract.py
+++ b/tests/cli/reflect/test_shadow_skill_contract.py
@@ -18,6 +18,7 @@ SKILL_REL = "src/superclaude/skills/sc-reflect-protocol/SKILL.md"
 SKILL = ROOT / SKILL_REL
 SPEC = ROOT / "src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md"
 SKILL_DIR = ROOT / "src/superclaude/skills/sc-reflect-protocol"
+FIXTURES = Path(__file__).parent / "fixtures"
 
 
 def git(*args: str) -> str | None:
@@ -39,14 +40,14 @@ def block_after(text: str, heading: str) -> str:
 # ------------------------------------------------------------ where the skill may change (AC1)
 
 
-def test_stable_contract_block_and_version_are_byte_identical_to_head():
-    head = git("show", f"HEAD:{SKILL_REL}")
-    if head is None:
-        pytest.skip("no git history for the skill")
-    heading = "### 9.1 Stable contract (contract_version: 1.8.0)"
-    current = SKILL.read_text(encoding="utf-8")
-    assert block_after(current, heading) == block_after(head, heading)
-    assert 'contract_version: "1.8.0"' in block_after(current, heading)
+def test_stable_contract_block_and_version_match_the_pinned_1_9_0_block():
+    pinned = (FIXTURES / "stable_contract_1_9_0_block.yaml.txt").read_text(
+        encoding="utf-8"
+    )
+    heading = "### 9.1 Stable contract (contract_version: 1.9.0)"
+    block = block_after(SKILL.read_text(encoding="utf-8"), heading)
+    assert block == pinned.rstrip("\n")
+    assert 'contract_version: "1.9.0"' in block and "finding_counts:" in block
 
 
 def test_skill_changes_are_confined_to_the_allowed_sections():
@@ -62,7 +63,8 @@ def test_skill_changes_are_confined_to_the_allowed_sections():
         above = [h for i, h in headings if i <= lineno]
         return above[-1] if above else ""
 
-    allowed = ("### 3.1 ", "### 4.3a ", "### 5.4 ", "### 9.2 ")
+    # 9.1 holds the 1.9.0 heading, finding_counts and the version sentence; 17.6 holds the grader row
+    allowed = ("### 3.1 ", "### 4.3a ", "### 5.4 ", "### 9.1 ", "### 9.2 ", "## 17.6 ")
     seen = set()
     for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
         start, count = int(m.group(1)), int(m.group(2) or 1)
@@ -72,7 +74,6 @@ def test_skill_changes_are_confined_to_the_allowed_sections():
             assert sec.startswith(allowed), f"line {n} changed under {sec!r}"
             if sec.startswith("### 3.1 "):
                 assert "--t2-engine" in lines[n - 1]
-    assert not any(s.startswith("### 9.1 ") for s in seen)
 
 
 def test_no_new_src_superclaude_hit_in_the_skill_directory():
diff --git a/tests/cli/reflect/test_verdict_mapping.py b/tests/cli/reflect/test_verdict_mapping.py
index 0e595efc0..d353c4ee8 100644
--- a/tests/cli/reflect/test_verdict_mapping.py
+++ b/tests/cli/reflect/test_verdict_mapping.py
@@ -606,6 +606,28 @@ def test_fx7_vacuous_no_verify_stays_exempt_but_visible() -> None:
     assert result.verification_verified is False
 
 
+def test_1_9_0_contract_with_finding_counts_parses_and_passes(tmp_path) -> None:
+    """contract 1.9.0: ``finding_counts`` is an additive field; parse_contract and derive_verdict take it."""
+    from superclaude.cli.reflect.contract import parse_contract
+
+    contract = _load("pass.yaml")
+    contract["contract_version"] = "1.9.0"
+    contract["finding_counts"] = {
+        "blocking": 0,
+        "label_high": 1,
+        "medium": 2,
+        "note": 3,
+    }
+    path = tmp_path / "return-contract.yaml"
+    path.write_text(yaml.safe_dump(contract), encoding="utf-8")
+    parsed = parse_contract(path)
+    assert parsed is not None and parsed["finding_counts"]["note"] == 3
+    result = derive_verdict(
+        parsed, expected_tier=2, allow_single_vendor=False, child_rc=0
+    )
+    assert result.verdict is Verdict.PASS
+
+
 def test_graph_tokens_do_not_halt() -> None:
     """P3-D7 (issue #323): ``graph:*`` codegraph tokens are informational telemetry.
 


Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
