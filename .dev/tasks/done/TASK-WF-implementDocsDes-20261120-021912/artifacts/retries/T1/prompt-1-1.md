80dde4a56e9986cf923834ee4d1f0bf3c7be0530
Review one task for spec compliance.

Task brief: ## Task 1: Add `finding_counts` and bump the reflect contract text to 1.9.0

Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md`: the section 9.1 heading (`### 9.1 Stable contract (contract_version: 1.8.0)`) and its field list gain `finding_counts: {blocking, label_high, medium, note}` (computed from the merged findings after the evidence validator, in both pre and post modes); the sentence `Contract version is v1.8.0` (it sits in section 9.1), the grader row `return-contract.yaml contract_version == "1.8.0"` and the three sentences that say the contract stays 1.8.0 (the section 4.3a sentence "contract 1.8.0 is unchanged", the panel publish step and the three-engine-keys sentence) move to 1.9.0. Keep the historical "1.8.0" remark on `remediation_plan_path` (the field was added in 1.8.0). Edit `src/superclaude/skills/sc-reflect-protocol/refs/report-template.md` (`contract_version: 1.8.0` in the example) and `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md` (the `contract_version == "1.8.0"` row) to 1.9.0. Edit `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` to state how a panel reviewer's findings map to `label_high` (severity CRITICAL), `blocking` (the `blocking` flag), `medium` (severity MAJOR, not blocking) and `note` (severity MINOR); keep the edit outside the region that `test_the_brief_template_has_exactly_three_sections` slices. Edit `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` only for the 1.8.0 pin on `remediation_plan_path` if it names the current version rather than the introducing version (Task 10 owns its other changes).

Acceptance criteria:
- `finding_counts` appears once in the section 9.1 field list with the four keys, and `grep -n '1\.8\.0' src/superclaude/skills/sc-reflect-protocol/SKILL.md` leaves only lines that say a field was introduced in 1.8.0.
- `report-template.md` and `grader-extensions.md` say 1.9.0 and contain no current-version 1.8.0 pin.
- `reviewer-spec.md` states the CRITICAL-to-`label_high` mapping and the panel `blocking` flag mapping in plain words.
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
Start sha: 80dde4a56e9986cf923834ee4d1f0bf3c7be0530
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-reflect-protocol/SKILL.md b/src/superclaude/skills/sc-reflect-protocol/SKILL.md
index e08ee5485..8f5f513e7 100644
--- a/src/superclaude/skills/sc-reflect-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-reflect-protocol/SKILL.md
@@ -308,7 +308,7 @@ Emit `interaction_effects_scanned: true` in the contract when this step runs; `i
 
 ### 4.3a T2 engine selection (`--t2-engine`)
 
-With the default `--t2-engine legacy` the panel code is never called, the Wave 3 reviewer rotation of §7.1 runs exactly as before, and contract 1.8.0 is unchanged (no stable field, `merge_method` value or contract version changes). `--t2-engine shadow` additionally runs the panel offline for measurement, UC-1 only (Stage 2); the legacy rotation and the Wave 4 debate stay authoritative, and everything the panel writes goes under `<output>/panel/` and into telemetry. In UC-2 (post-execution) runs the flag is accepted and ignored until Stage 5.
+With the default `--t2-engine legacy` the panel code is never called, the Wave 3 reviewer rotation of §7.1 runs exactly as before, and contract 1.9.0 is unchanged (no stable field, `merge_method` value or contract version changes). `--t2-engine shadow` additionally runs the panel offline for measurement, UC-1 only (Stage 2); the legacy rotation and the Wave 4 debate stay authoritative, and everything the panel writes goes under `<output>/panel/` and into telemetry. In UC-2 (post-execution) runs the flag is accepted and ignored until Stage 5.
 
 The panel is a Tier 2 mechanism and is called only after the **final** tier is 2. Order of decisions: (1) Wave 0 alias routing (§4 Wave 0 step 0.5) and executor class (§7.1); (2) budget pre-flight (§4.0 step 0.9); (3) Waves 1-2: the T1 card, coverage map, blind calibration of the T1 card, rubric; (4) only now `--t2-engine` is read, at the start of Wave 3. Both the requested and the effective engine are written to `tier_decision.yaml` (§5.4) and, when the panel runs, to its manifest.
 
@@ -346,7 +346,7 @@ The panel is a Tier 2 mechanism and is called only after the **final** tier is 2
 7. **Debate (legacy, unchanged).** After it, write `<output>/adversarial/merged-verdict.yaml` from the debate's merged output and return contract (`merge_method`, `verdict`, `convergence_score`, `base_variant`, `source_cards` and the merged findings; copy, never invent a value) and confirm it with Glob or Bash: the EV-1 rule of Wave 4 reads exactly that path, and a copy under `adversarial/adversarial/` or a `merged-verdict.md` alone does not satisfy it. Then advance `debated`, record `debate_skipped_similar` (true when the child's log says the variants were substantially identical; the real null score stays null). Read the installed `sc-adversarial-protocol` return contract: when it names a judge record it as `judge_identity`; when it does not, record `judge_identity: unknown` and `judge_class_collision: unknown`, never `false`. When a judge id is known, assert it is not a Fable model and not a Tier 0 alias, and note a class collision with a reviewer or the executor in `<output>/panel/notes.md`.
 8. **After the evidence validator.** Write the finding ids it kept to `<output>/panel/kept-ids.txt`, one `reviewer-<N>:<finding id>` per line (each reviewer numbers its own findings, so a bare id would keep that id in every card) and run `superclaude review cluster <output>/panel/cards --snapshot <output>/artifacts/input-snapshot.yaml --out <output> --kept <output>/panel/kept-ids.txt` (the `clusters_kept` pass; `clusters.json` is not touched). Advance `validated`.
 9. **Identity.** Record `identity_source` from the S-ID spike: `observed` when the adapter read the reviewer's resolved model id from its transcript, `requested-pinned` (an unverified assumption) when it only knows the model it asked for. Compare each card's `reviewer_model_self_report` with the pin; a mismatch sets `identity_mismatch_suspected: true` in telemetry and in `<output>/panel/notes.md`. While the identity is `requested-pinned` or the executor class is unknown, the panel notes make no claim of verified independence.
-10. **Publish.** Before it, confirm that the contract records `reviewer_personas` and `reviewer_models` (the legacy rotation as it ran, as in §9.1) and no top-level key outside the stable list; every shadow field goes under `telemetry:`. After the legacy writers have written `REPORT.md`, `return-contract.yaml` and `audit.log`, run `superclaude review manifest advance --out <output> --stage published`: it records their hashes and rewrites nothing. The panel telemetry fields are listed in §9.2 under `telemetry:`; the three stable-contract files stay as the legacy writers produce them, with `contract_version` 1.8.0.
+10. **Publish.** Before it, confirm that the contract records `reviewer_personas` and `reviewer_models` (the legacy rotation as it ran, as in §9.1) and no top-level key outside the stable list; every shadow field goes under `telemetry:`. After the legacy writers have written `REPORT.md`, `return-contract.yaml` and `audit.log`, run `superclaude review manifest advance --out <output> --stage published`: it records their hashes and rewrites nothing. The panel telemetry fields are listed in §9.2 under `telemetry:`; the three stable-contract files stay as the legacy writers produce them, with `contract_version` 1.9.0.
 
 ### 4.5 Wave 5 — Detailed step addition
 
@@ -455,7 +455,7 @@ t2_engine_effective: legacy | shadow | null  # §4.3a: the engine that ran; null
 panel_fallback_reason: <string> | null  # §4.3a rule D4: why a requested non-legacy engine ran the legacy rotation; null otherwise
 ```
 
-The three engine keys are additive audit keys of this artifact, not contract fields; `contract_version` stays 1.8.0.
+The three engine keys are additive audit keys of this artifact, not contract fields; `contract_version` stays 1.9.0.
 
 Grader `yaml_field` asserts both `fired_rule_number` and `composite_score` are present. The composite is *recording*, not deciding.
 
@@ -703,10 +703,10 @@ Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) the worker f
 
 Two-block contract: stable + telemetry. Written to `<output>/return-contract.yaml` AND returned inline. (See `refs/report-template.md` for the human-facing REPORT.md skeleton that renders these fields.)
 
-### 9.1 Stable contract (contract_version: 1.8.0)
+### 9.1 Stable contract (contract_version: 1.9.0)
 
 ```yaml
-contract_version: "1.8.0"   # #323: the change-summary corroboration field was removed (no consumer read it); the other fields keep their names. 1.8.0 ADDITIVE ONLY: +remediation_plan_path (plan-route sibling of remediation_task_path); 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.7.x runtime/semantic hardening: EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate + EV-2 merge_method legal-values guard (no stable-field change); 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields); 1.7.0 (FR-RH1) ADDITIVE ONLY: +reachability_* fields
+contract_version: "1.9.0"   # #323: the change-summary corroboration field was removed (no consumer read it); the other fields keep their names. 1.9.0 ADDITIVE ONLY: +finding_counts ({blocking, label_high, medium, note}); 1.8.0 ADDITIVE ONLY: +remediation_plan_path (plan-route sibling of remediation_task_path); 1.4.0 added remediation_task_path (FR-8); 1.5.0 (D13) ADDITIVE ONLY: +coverage_pct_union, +coverage_degraded, +unmapped_requirements_union; coverage_pct and unmapped_requirements keep parsed-only semantics; 1.7.x runtime/semantic hardening: EV-1 Wave-4 ORCHESTRATOR-VERIFIES-ON-DISK merge gate + EV-2 merge_method legal-values guard (no stable-field change); 1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields); 1.7.0 (FR-RH1) ADDITIVE ONLY: +reachability_* fields
 status: success | partial | failed | dry-run
 mode: pre | post
 tier_reached: 1 | 2 | 3
@@ -829,6 +829,7 @@ task_file_path: <path> | null
 remediation_task_path: null   # FR-8, retired in 6.1.0: the MDTM route is gone, so this is always null. Kept in the schema so older reports still load.
 remediation_plan_path: <abs path> | null   # 1.8.0: absolute path of the sc:workflow tasklist `.dev/tasks/to-do/<slug>/<slug>.md` built in Wave 6 (the only route); null when no plan was built. The wrapper auto-fix loop READS this to auto-run /sc:implement.
 handoff_memory_key: null   # FR-3, retired in 6.1.0: always null, no handoff file is written. Kept in the schema so older reports still load.
+finding_counts: {blocking: <int>, label_high: <int>, medium: <int>, note: <int>}   # 1.9.0: computed from the merged findings after the evidence validator, in both pre and post modes. label_high counts the Deviations-table label HIGH (legacy path) or findings-v2 severity CRITICAL (panel path); blocking, medium and note count the grades `Blocking (...)`, `Medium:` and `Note:` (panel: the `blocking` flag, severity MAJOR not blocking, severity MINOR; see refs/reviewer-spec.md).
 
 # Asymmetric-cost flags (downstream automation must respect these)
 cannot_validate_without_user_input: bool
@@ -874,7 +875,7 @@ promotion_cross_fs: bool                       # true when source and destinatio
 promotion_pending: bool                        # true between pre-write (7.3.6) and finalization (7.6); only true in a crashed-mid-run log entry
 ```
 
-Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.8.0`.
+Each flag has a one-line semantics description in `refs/report-template.md`. Contract version is `v1.9.0`.
 
 **Reachability field-presence & consistency (FR-RH1, R7).** The `reachability_*` block is **mandatory for every UC-2 return contract at `contract_version: "1.7.0"`** and optional/absent for UC-1. Invariants:
 
@@ -1915,7 +1916,7 @@ Every load-bearing protocol decision maps to at least one deterministic or quali
 | §11.3 calibrator disjoint-set | `yaml_field` | `reflection-card.yaml calibrator_model_class NOT IN reviewer_model_classes` |
 | §11.5 citation-budget policy | `yaml_field` | `return-contract.yaml citation_budget_policy ∈ {full_reread, sampled}` |
 | §12.5 falsifier T2-convergence-wrong-answer | `yaml_field` + composite | `return-contract.yaml regression_present AND convergence_score < 0.75` |
-| §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.8.0"` |
+| §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.9.0"` |
 | §6.1 step 5.6 reachability R7 field presence (UC-2) | `yaml_field` | `return-contract.yaml reachability_gate_ran AND reachability_skip_reason` |
 | §6.1 step 5.6 unreachable → real-boot-proven Regression | `yaml_field` | `return-contract.yaml reachability_unreachable > 0 ⟹ reachability_real_boot_ran == true AND regression_present == true` |
 | §6.1 step 5.6 unproven → Grounding Gap (annotated sink) | `file_exists` + `yaml_field` | `grounding-gaps.yaml row AND return-contract.yaml reachability_unproven > 0 AND needs_human_decision == true` |
diff --git a/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md b/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
index 90876e72f..3783f1bda 100644
--- a/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
+++ b/src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md
@@ -177,7 +177,7 @@ The §6.1 step-5.6 contracted-sink reachability gate (contract `1.7.0`, UC-2) in
 | `--no-reachability` telemetry-only | `yaml_field` + `regex_absent` | `reachability_skip_reason == "--no-reachability"`, `reachability_gate_ran == false`; `regex_absent` on any reachability Grounding-Gap row |
 | `spec-and-tasklist-absent` telemetry-only | `yaml_field` | `reachability_skip_reason == "spec-and-tasklist-absent"`, `reachability_gate_ran == false`, `status != partial` |
 | Semantic-fallback advisory non-gating | `regex_absent` | no `reachability_unproven` increment / Grounding-Gap row from semantic-only classification lacking `durable_sink:` / `@sink` |
-| `contract_version == "1.8.0"` | `yaml_field` | additive bump check |
+| `contract_version == "1.9.0"` | `yaml_field` | additive bump check |
 
 A producer-level eval fixture (R6) drives Step 5.6 from real inputs; only if such an implemented fixture demonstrably needs a semantic check beyond `yaml_field` / `regex_present` / `regex_absent` / `yaml_list_contains` should a new assertion type be proposed — v1 invents none.
 
diff --git a/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md b/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md
index 8328ecb9d..19d14a066 100644
--- a/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md
+++ b/src/superclaude/skills/sc-reflect-protocol/refs/report-template.md
@@ -11,7 +11,7 @@ Wave 5 MUST NOT introduce findings that were not already classified upstream. Un
 The header block is the first content in the emitted artifact. It is rendered as a fenced YAML block so downstream parsers (budget ledgers, CI) can lift fields without Markdown parsing.
 
 ```yaml
-contract_version: 1.8.0
+contract_version: 1.9.0
 status: success | partial | needs_human_decision
 mode: pre | post
 tier_reached: 1 | 2
diff --git a/src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md b/src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
index 70bf760d4..25ba0bb20 100644
--- a/src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
+++ b/src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
@@ -77,6 +77,10 @@ Example shape:
 
 When Step 3B.0 completes, the contract emits `reviewer_briefs_materialized: <N>` (count of brief files written). Reviewer spawning Wave 3A reads each brief from disk; no in-memory state is shared between reviewers.
 
+### Finding counts (contract 1.9.0)
+
+The contract field `finding_counts: {blocking, label_high, medium, note}` is computed from the merged findings after the evidence validator. A shadow-panel reviewer's findings-v2 lines map as follows: severity CRITICAL counts as `label_high` (the panel has no HIGH label); a finding whose `blocking` flag is true counts as `blocking`; severity MAJOR with `blocking` false counts as `medium`; severity MINOR counts as `note`. On the legacy path the counts come from the Deviations-table grades instead: the label HIGH is `label_high`, and `Blocking (...)`, `Medium:` and `Note:` are `blocking`, `medium` and `note`.
+
 ---
 
 ## Composition


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
