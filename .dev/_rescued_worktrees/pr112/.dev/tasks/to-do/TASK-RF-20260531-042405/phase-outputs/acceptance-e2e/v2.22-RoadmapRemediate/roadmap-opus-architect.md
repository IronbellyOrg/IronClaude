---
spec_source: "spec-roadmap-remediate.compressed.md"
complexity_score: 0.7
complexity_class: HIGH
primary_persona: architect
adversarial: false
base_variant: "none"
variant_scores: "none"
convergence_score: none
---

# Roadmap Remediate & Certify Pipeline Extension — Project Roadmap

## Executive Summary

This roadmap delivers a two-step extension (Step 10 remediate, Step 11 certify) plus a Step-9 validation enhancement to the existing `roadmap run` pipeline, converting it from a 9-step generate/validate flow into a 12-step generate → validate → remediate → certify flow. Remediation is invoked as part of the default `roadmap run` workflow — no new CLI command is introduced. After validation, the pipeline parses the merged report, surfaces a tiered interactive remediation prompt, dispatches parallel batch-by-file remediation agents under all-or-nothing rollback semantics, then runs a single-pass lightweight certification to confirm fixes before handing the certified roadmap to the downstream `sc:tasklist` boundary.

**Business Impact:** Closes the quality loop inside a single `roadmap run`, so BLOCKING and WARNING findings are corrected and re-verified automatically instead of requiring a manual edit-and-revalidate cycle. This raises the proportion of roadmaps that reach `tasklist_ready` on the first pass, reduces operator round-trips, and preserves auditability through on-disk remediation and certification reports.

**Complexity:** HIGH (0.7) — driven by parallel multi-agent orchestration (`threading`, one `ClaudeProcess` per file group), all-or-nothing rollback with `.pre-remediate` snapshots, cross-file consistency handling, SHA-256 hash-gated resume across a four-state validation lifecycle, and a robust multi-format report parser with individual-report fallback and two-step dedup. Complexity is bounded below very-high by heavy reuse of existing pipeline primitives (`ClaudeProcess`, `execute_pipeline`, `GateCriteria`) and a strict single-pass model (no remediation loop).

**Critical path:** DM-001 `Finding` model + COMP-001 parser (M1) → COMP-003 remediate executor with snapshot/rollback + REMEDIATE_GATE (M2) → COMP-005 certify gate + certification report (M3) → COMP-006 executor wiring, state schema, and resume (M4) → success-criteria validation and performance budget (M5).

**Key architectural decisions:**

- Remediate runs via **internal dispatch** (`remediate_executor.execute()` driving `ClaudeProcess` directly through `threading`), presented as a single conceptual Step, mirroring `validate_executor.py:validate_run_step()`; certify runs as a **standard single Step** through `execute_pipeline()`. The interactive prompt lives in `execute_roadmap()` to preserve `execute_pipeline()`'s non-interactive contract.
- **Batch-by-file** conflict avoidance: all findings targeting one file route to one agent; agents for different files run in parallel — eliminating concurrent edits to the same file. Cross-file findings are split into scoped "YOUR FILE" fragments handed to both file agents.
- **All-or-nothing rollback**: every target file is snapshotted to `<file>.pre-remediate` before agents spawn; any non-zero exit/timeout halts remaining agents and restores all snapshots, with the pipeline halting.
- **Single-pass, no-loop** certification: lightweight checklist re-validation scoped to fixed findings via one agent; failures yield `certified-with-caveats` and stop, leaving the user in control.

**Open risks requiring resolution before M1:**

- OQ-R-006 — Confirm the on-disk artifact filename remediation agents target is `extraction.md` (scope lists) vs. the pipeline step ID `extract`; M1 parser and editable-files boundary both depend on this.

## Milestone Summary

|ID|Title|Type|Priority|Effort|Dependencies|Deliverables|Risk|
|----|-------|------|----------|--------|--------------|--------------|------|
|M1|Foundation — Finding Model & Report Parsing|Foundation|P0|L|v2.20-WorkflowEvolution|16|Medium|
|M2|Remediation Engine — Filter, Batch, Orchestrate, Rollback|Core|P0|XL|M1|27|High|
|M3|Certification — Lightweight Re-Validation|Core|P0|L|M1, M2|12|Medium|
|M4|Pipeline Integration, State & Resume|Integration|P0|L|M2, M3|12|Medium|
|M5|Validation, Performance & Hardening|Quality|P1|M|M1, M2, M3, M4|13|Low|

## Dependency Graph

```
v2.20-WorkflowEvolution
        │
        ▼
       M1 (Foundation: Finding model, parser, fallback+dedup)
        │
        ▼
       M2 (Remediation Engine: filter → batch → snapshot → spawn → rollback)
        │
        ├──────────────┐
        ▼              ▼
       M3 (Certify)   (M2 outputs feed M4 directly)
        │              │
        └──────┬───────┘
               ▼
              M4 (Pipeline Integration, State & Resume)
               │
               ▼
              M5 (Validation, Performance & Hardening)
```

- M1 → M2 → {M3, M4}; M3 → M4; M4 → M5
- M3 depends on M1 (`Finding` model) and M2 (FIXED findings + remediation report)
- M5 validates outputs of M1–M4 against SC-001…SC-008

## M1: Foundation — Finding Model & Report Parsing

**Objective:** Establish the `Finding` data model, the validation-report parser with multi-format detection, the individual-report fallback with two-step dedup, and the foundational architectural constraints (atomic writes, pure prompts, unidirectional imports) before any orchestration is built. | **Duration:** Weeks 1–2 | **Entry:** v2.20-WorkflowEvolution pipeline infrastructure present; merged validation report format known | **Exit:** `Finding` objects parse from merged and individual reports; fallback+dedup verified; severity counts extracted; terminal summary box renders

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-007|Unidirectional import boundary|Establish import direction so `remediate_*`/`certify_*` modules import from `pipeline.models` and `roadmap.models` only, never the reverse|roadmap.models|-|`remediate_*`/`certify_*` → `pipeline.models`,`roadmap.models` only; reverse import absent; import-lint check passes|S|P0|
|2|NFR-002|Reuse subprocess abstraction|Mandate reuse of existing `ClaudeProcess` from `pipeline.process`; introduce no new subprocess abstraction|pipeline.process|-|no new subprocess class created; all agent spawns route through `ClaudeProcess`|S|P0|
|3|NFR-001|Atomic file writes|All file writes (tasklist, reports, snapshots) use tmp-file + `os.replace()` pattern|remediate_parser|-|every write goes tmp→`os.replace()`; no partial file observable on crash; verified by interrupted-write test|M|P0|
|4|NFR-004|Pure prompt builders|All prompt-builder functions are pure: no I/O, no subprocess calls, no side effects|remediate_prompts|-|prompt builders accept data, return str; zero I/O/subprocess in builder bodies; unit-test purity|S|P0|
|5|DM-001|`Finding` dataclass|Define `Finding` dataclass carrying all 10 fields for structured remediation|models.py|-|id:str("F-01"); severity:str(BLOCKING/WARNING/INFO); dimension:str; description:str; location:str("roadmap.md:§3.1"); evidence:str(expected-vs-found); fix_guidance:str; files_affected:list[str]; status:str(PENDING/FIXED/FAILED/SKIPPED); agreement_category:str(BOTH_AGREE/ONLY_A/ONLY_B/CONFLICT)|M|P0|
|6|COMP-007|`models.py` extension|Add `Finding` dataclass to `roadmap.models`; `RoadmapConfig` unchanged (no new fields)|models.py|DM-001|`Finding` importable from `roadmap.models`; `RoadmapConfig` signature unchanged; existing consumers unaffected|S|P0|
|7|COMP-001|`remediate_parser.py`|New ~120–150 LOC module: parse validation reports → `Finding` objects; carries fallback + dedup logic|remediate_parser|DM-001,COMP-007|merged report parses to `Finding[]`; all 10 fields populated; module ≤~150 LOC; imports `roadmap.models` only|L|P0|
|8|COMP-020|Report-format detection dispatch|Dispatch logic selecting parse path: merged report (`reflect-merged.md`/`merged-validation-report.md`) vs. individual reflect reports|remediate_parser|COMP-001|detects merged-present→merged path; merged-missing/malformed→fallback path; dispatch unit-tested for both branches|M|P0|
|9|FR-002|Parse severity counts|After validation, parse merged report to extract finding counts by severity (BLOCKING/WARNING/INFO)|remediate_parser|COMP-001|returns blocking_count,warning_count,info_count from `validate/reflect-merged.md` or `validate/merged-validation-report.md`; counts match report contents|M|P0|
|10|FR-008|Extract structured findings|Extract findings from merged report into `Finding` objects carrying all 10 fields|remediate_parser|DM-001,COMP-001|each report finding → one `Finding`; all 10 fields non-null where source provides; source = `reflect-merged.md` or `merged-validation-report.md`|M|P0|
|11|FR-033|Fallback parser + two-step dedup|When merged report missing/malformed, parse individual reflect reports and dedup by location-proximity then severity-resolution|remediate_parser|COMP-020,OQ-R-002|parses `reflect-*.md`; dedup-a: same file AND locations overlap/within 5 lines; dedup-b: keep higher severity (BLOCKING>WARNING>INFO), merge fix_guidance preferring specific; non-matching kept as-is; zero parseable→skip remediation with warning|L|P0|
|12|FR-003|Terminal summary box|Print a brief terminal summary box listing finding counts and per-severity finding IDs/descriptions|executor.py|FR-002|box lists BLOCKING/WARNING/INFO counts + each finding id/description; renders after validation parse; pure-format from parsed counts|S|P1|
|13|COMP-009|`ClaudeProcess` reuse verification|Confirm `ClaudeProcess` (`pipeline.process`) is the sole agent-spawn primitive consumed downstream|pipeline.process|NFR-002|`ClaudeProcess` importable and callable with prompt+`--file`; no wrapper added; context-isolation flags absent|S|P0|
|14|COMP-008|`validate_executor.py` count contract|Confirm `validate_executor.py` returns structured finding counts and serves as the direct-`ClaudeProcess` reference pattern (`validate_run_step()`)|validate_executor|-|`validate_run_step()` returns blocking/warning/info counts; pattern documented as remediate reference; file unchanged|S|P0|
|15|COMP-011|`_auto_invoke_validate()` reuse|Confirm existing post-step-9 validation invocation feeds counts into the remediation entry point|executor.py|COMP-008|`_auto_invoke_validate()` runs after step 9; its report path is consumed by parser; no behavior change to step 9|S|P0|
|16|COMP-010|`execute_pipeline()` contract baseline|Confirm `execute_pipeline()` remains the non-interactive runner for steps 1–9 (and later certify); document its interactive-free contract|executor.py|-|`execute_pipeline()` invoked for steps 1–9; no prompt logic inside it; contract recorded for M4 wiring|S|P0|

### Integration Points — M1

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Report-format detection dispatch (COMP-020)|Strategy/dispatch|M1|M1|COMP-001 parser, FR-033 fallback|
|`ClaudeProcess` (`pipeline.process`)|Subprocess primitive (reused)|Pre-existing (v2.20)|M1|COMP-003 (M2), certify agent (M3)|
|`_auto_invoke_validate()` → parser handoff|Callback wiring|M1|M1|FR-002/FR-008 parse entry|

### Milestone Dependencies — M1

- v2.20-WorkflowEvolution pipeline infrastructure (external; declared spec dependency)

### Open Questions — M1

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-R-002|`agreement_category` population when findings come from the individual-report fallback path (no two-generator merge) — what value is assigned?|Determines `Finding.agreement_category` semantics on fallback; affects DM-001 field validity and downstream filtering|Architect + spec owner|Before M1 exit|
|2|OQ-R-006|Confirm the on-disk artifact filename agents target is `extraction.md` vs. pipeline step ID `extract`|Parser location resolution + editable-files boundary (M2) both depend on exact filename|Architect|Before M1 exit|
|3|OQ-R-007|Confirm no external HTTP/route surface is expected — all "paths" are artifact files and pipeline step IDs|Bounds scope; confirms no API-layer deliverables required|Architect|Before M1 exit|

## M2: Remediation Engine — Filter, Batch, Orchestrate, Rollback

**Objective:** Build the interactive tiered prompt, scope filtering, batch-by-file grouping, cross-file handling, the parallel `ClaudeProcess` dispatch pool, snapshot/rollback with all-or-nothing semantics, the `remediation-tasklist.md` emitter, and the `REMEDIATE_GATE`. This is the highest-risk milestone (concurrency + rollback). | **Duration:** Weeks 3–5 | **Entry:** M1 `Finding` objects + parser available; editable-files filename confirmed (OQ-R-006) | **Exit:** Parallel agents remediate batched files; failure rolls back all snapshots and halts; success sets findings FIXED; `remediation-tasklist.md` passes `REMEDIATE_GATE`

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-004|Interactive tiered remediation prompt|Present options `[1] BLOCKING only`, `[2] BLOCKING+WARNING`, `[3] All (incl INFO)`, `[n] Skip`|executor.py|FR-003|prompt shows 4 options; lives in `execute_roadmap()` not `execute_pipeline()`; reads single-keystroke choice|M|P0|
|2|FR-005|Skip-path termination|On `n`: pipeline ends, state saved `validated-with-issues`, validation report remains on disk for manual review|executor.py|FR-004|choice=n→state `validated-with-issues`; report file retained; no remediate/certify run|S|P0|
|3|FR-006|Scope continuation + SKIPPED tagging|On `1`/`2`/`3`: continue to Step 10 with selected scope; out-of-scope findings marked SKIPPED in tasklist|remediate_executor|FR-004|selected severity scope passed to filter; out-of-scope findings → SKIPPED rows in `remediation-tasklist.md`|M|P0|
|4|FR-007|Auto-skip prompt branch|When 0 BLOCKING and 0 WARNING: 0 INFO→proceed direct to certify (no-op); INFO present→skip remediation, proceed to certify|executor.py|FR-002,OQ-R-005|0B/0W/0I→certify no-op; 0B/0W/INFO>0→skip remediate→certify; prompt not shown in either branch|M|P0|
|5|FR-009|Scope filtering|Filter findings by selected scope: Opt1 BLOCKING-with-guidance only (W/I SKIPPED); Opt2 BLOCKING+WARNING (INFO SKIPPED); Opt3 all-with-guidance|remediate_executor|FR-006,FR-008|Opt1→only BLOCKING w/ fix_guidance proceed; Opt2→B+W proceed; Opt3→all severities w/ guidance proceed; others SKIPPED|M|P0|
|6|FR-010|Always-skip protected statuses|Mark findings tagged `NO_ACTION_REQUIRED` or `OUT_OF_SCOPE` as SKIPPED regardless of user selection|remediate_executor|FR-009|NO_ACTION_REQUIRED→SKIPPED; OUT_OF_SCOPE→SKIPPED; overrides any chosen scope|S|P0|
|7|FR-011|Zero-findings guard|If filtering yields 0 actionable findings, emit `remediation-tasklist.md` with `actionable:0` all-SKIPPED; certify produces `certified:true`, `findings_verified:0` (vacuous)|remediate_executor|FR-009|0 actionable→tasklist `actionable:0`+all SKIPPED; certify report `findings_verified:0`,`certified:true`|M|P0|
|8|FR-012|Batch-by-file grouping|Group actionable findings by primary target file; all findings for one file → one agent; different-file agents run in parallel|remediate_executor|FR-009|findings keyed by primary file; one agent per file group; distinct files dispatched concurrently|M|P0|
|9|FR-013|Cross-file finding split|Handle cross-file findings (e.g. F-05 spanning roadmap.md+test-strategy.md) by including in both agents' prompts with scoped "YOUR FILE" fragment + note other side handled separately|remediate_prompts|FR-012|cross-file finding appears in both file agents; each gets scoped fix fragment for its file only; note references separate agent|M|P0|
|10|FR-014|Constrained agent prompt structure|Build each agent prompt: edit ONLY the one target file, apply ONLY listed fixes, preserve YAML frontmatter, preserve heading hierarchy, no section reorder unless fix requires|remediate_prompts|FR-013,NFR-004|prompt names single `{file_path}`; lists only that file's fixes; constraints present verbatim; builder is pure|M|P0|
|11|FR-015|Agent execution parameters|Apply per-agent params: 300s timeout, 1 retry on failure, model inherited from parent pipeline config|remediate_executor|FR-014|timeout=300s; retries=1; model from parent config; params applied per `ClaudeProcess` spawn|S|P0|
|12|FR-016|Editable-files constraint enforcement|Enforce that agents may edit ONLY `roadmap.md`, `extraction.md`, `test-strategy.md`; phase tasklist files out of scope|remediate_executor|FR-014,OQ-R-006|edits restricted to the 3 allowed files; phase tasklists never targeted; violation→FAIL|M|P0|
|13|FR-017|`remediation-tasklist.md` emitter|Emit standalone (non-phase-tasklist) file with specified frontmatter and BLOCKING/WARNING/SKIPPED sections|remediate_executor|DM-002|file has DM-002 frontmatter; BLOCKING/WARNING/SKIPPED sections present; not phase-tasklist format; atomic write|M|P0|
|14|FR-018|Single-Step internal dispatch|Present remediate as one Step to `execute_pipeline()` while internally using `ClaudeProcess` directly (one process per file group, parallel via `threading`) — NOT `execute_pipeline()`, matching `validate_run_step()`|remediate_executor|COMP-008|remediate surfaces as single step; internal `threading`+`ClaudeProcess`; mirrors `validate_executor.py:validate_run_step()`|L|P0|
|15|FR-019|`REMEDIATE_GATE` definition|Define gate: required frontmatter type/source_report/source_report_hash/total_findings/actionable/skipped; min_lines 10; STRICT; semantic checks frontmatter_values_non_empty, all_actionable_have_status|certify_gates|DM-005|gate requires the 6 frontmatter fields; min_lines=10; tier=STRICT; both semantic checks bound|M|P0|
|16|FR-020|Pre-remediate snapshot|Before spawning agents, snapshot all target files to `<file>.pre-remediate` for rollback|remediate_executor|FR-012|`roadmap.md.pre-remediate`,`test-strategy.md.pre-remediate`,`extraction.md.pre-remediate` written atomically before any agent spawn|M|P0|
|17|FR-021|All-or-nothing rollback|On any non-zero exit/timeout: halt remaining agents, roll back all target files from snapshots, mark failed agent's findings FAILED, mark all cross-file findings involving failed file FAILED, set remediate FAIL, halt pipeline|remediate_executor|FR-020|failure→remaining agents halted; all files restored from `.pre-remediate`; failed+cross-file findings FAILED; remediate step FAIL; pipeline halts|L|P0|
|18|FR-022|Success cleanup|On full success: delete `.pre-remediate` snapshots and set all agent-targeted findings to FIXED|remediate_executor|FR-021|all agents exit 0→snapshots deleted; targeted findings→FIXED|S|P0|
|19|COMP-002|`remediate_prompts.py`|New ~80–100 LOC module: build scoped fix prompts per file-group (pure functions)|remediate_prompts|NFR-004|builds per-file-group prompt; pure (no I/O); imports `pipeline.models`,`roadmap.models`; ≤~100 LOC|M|P0|
|20|COMP-003|`remediate_executor.py`|New ~200–250 LOC orchestrator: extract→filter→batch→snapshot→spawn→collect→rollback|remediate_executor|COMP-001,COMP-002,COMP-009|orchestrates full sequence; parallel via `threading`; ≤~250 LOC; consumes parser+prompts+`ClaudeProcess`|XL|P0|
|21|COMP-016|Parallel agent dispatch pool|`threading`-based dispatch: one `ClaudeProcess` per file group, joined for collect; batch-by-file guarantees no same-file concurrency|remediate_executor|FR-012,FR-018|spawns N threads for N file groups; each owns one `ClaudeProcess`; results joined; no two agents touch same file|L|P0|
|22|COMP-012|`REMEDIATE_GATE` instance|Instantiate `GateCriteria` for `remediation-tasklist.md` per DM-005|certify_gates|FR-019,COMP-014|`REMEDIATE_GATE` is a `GateCriteria` instance binding DM-005 fields+checks; importable for gate evaluation|S|P0|
|23|COMP-014|Semantic-check functions|Implement `_frontmatter_values_non_empty`, `_all_actionable_have_status`, `_has_per_finding_table`|certify_gates|-|three functions return bool; `_frontmatter_values_non_empty` rejects empty values; `_all_actionable_have_status` requires every actionable row have status|M|P0|
|24|COMP-018|`REMEDIATE_GATE` registry binding|Bind `REMEDIATE_GATE` + its semantic checks into the `GateCriteria`/`SemanticCheck` framework so gate evaluation dispatches to the right checks|certify_gates|COMP-012,COMP-014|gate framework resolves `frontmatter_values_non_empty`→`_frontmatter_values_non_empty` and `all_actionable_have_status`→`_all_actionable_have_status`; evaluation invoked on tasklist|M|P0|
|25|COMP-019|Semantic-check registry wiring|Register the three semantic-check functions in the dispatch map keyed by their string names used in gate definitions|certify_gates|COMP-014|registry maps each check-name string→function; unknown name→error; used by COMP-018/COMP-021|S|P0|
|26|DM-002|`remediation-tasklist.md` frontmatter|Define frontmatter schema for the remediation tasklist|remediate_executor|-|type:str("remediation-tasklist"); source_report:str(path); source_report_hash:str(SHA-256); generated:str(ISO-8601); total_findings:int; actionable:int; skipped:int|S|P0|
|27|DM-005|`REMEDIATE_GATE` (`GateCriteria`)|Define gate-criteria values for the remediation tasklist|certify_gates|DM-002|required_frontmatter_fields:type,source_report,source_report_hash,total_findings,actionable,skipped; min_lines:10; enforcement_tier:STRICT; semantic_checks:frontmatter_values_non_empty,all_actionable_have_status|S|P0|

### Integration Points — M2

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Parallel agent dispatch pool (COMP-016)|Threading dispatch table (file-group → `ClaudeProcess`)|M2|M2|FR-018 remediate step, FR-021 rollback|
|Interactive tiered prompt (FR-004)|Callback in `execute_roadmap()`|M2|M2|FR-005/FR-006/FR-007 branches|
|`REMEDIATE_GATE` registry binding (COMP-018)|Gate registry / strategy|M2|M2|gate evaluation on `remediation-tasklist.md`|
|Semantic-check registry (COMP-019)|Dispatch map (name → fn)|M2|M2|COMP-018, COMP-021 (M3)|
|Cross-file finding split (FR-013)|Fan-out wiring (finding → 2 agent prompts)|M2|M2|FR-012 batched agents|

### Milestone Dependencies — M2

- M1 (`Finding` model DM-001, parser COMP-001, severity counts FR-002)
- OQ-R-006 resolution (editable-files filename) before FR-016 lands

### Open Questions — M2

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-R-001|Retry semantics on partial cross-file success — does the single retry (FR-015) occur before the global halt/rollback (FR-021), or does halt preempt retry?|Determines FR-015↔FR-021 order of operations; affects rollback correctness and agent re-spawn logic|Architect|Before M2 exit|
|2|OQ-R-005|INFO-only auto-path: is `remediation-tasklist.md` still emitted when 0 BLOCKING/0 WARNING but INFO exist, and with what `actionable` value relative to the zero-findings guard?|Determines FR-007↔FR-011 artifact contract on the INFO-only branch|Architect|Before M2 exit|

## M3: Certification — Lightweight Re-Validation

**Objective:** Build the single-agent, single-pass certification that re-validates fixed findings against a checklist (no adversarial multi-agent debate), scoped to relevant sections only, emitting `certification-report.md` under `CERTIFY_GATE`, with no automatic remediation loop. | **Duration:** Weeks 5–6 | **Entry:** M2 produces FIXED findings + `remediation-tasklist.md`; `Finding` model available | **Exit:** Certify agent verifies each fixed finding; `certification-report.md` passes `CERTIFY_GATE`; all-PASS→`certified:true`, any-FAIL→`certified-with-caveats`; pipeline completes without looping

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-023|Lightweight scoped re-validation|Step 11 performs re-validation scoped to fixed findings via a single agent, single pass, checklist verification — without full adversarial multi-agent debate|certify_prompts|FR-022|one agent, one pass; checklist per fixed finding; no multi-generator debate invoked|M|P0|
|2|FR-024|Relevant-sections-only context|Provide certify agent only the sections surrounding each finding's location (not full file content) to minimize token cost while preserving accuracy|certify_prompts|FR-023,OQ-R-002|prompt includes only location-adjacent sections per finding; full files not embedded; verification still resolves PASS/FAIL|M|P0|
|3|FR-025|`certification-report.md` emitter|Emit report with specified frontmatter, per-finding results table (Finding/Severity/Result/Justification), and summary|certify_prompts|DM-003|frontmatter per DM-003; per-finding table with 4 columns; summary present; atomic write|M|P0|
|4|FR-026|Certification outcomes|all PASS→`certified:true`,`tasklist_ready:true`,pipeline completes; any FAIL→`certified-with-caveats`,report lists failures,pipeline completes (no loop), user may re-run `roadmap validate`|executor.py|FR-025|all-PASS→`certified:true`+`tasklist_ready:true`; any-FAIL→`certified-with-caveats`+failure list; pipeline completes either way|M|P0|
|5|FR-027|No automatic loop|Certification runs a single pass; if issues remain it reports and stops, leaving the user in control|certify_prompts|FR-026|exactly one certify pass; residual issues→report+stop; no auto re-remediate|S|P0|
|6|FR-028|`CERTIFY_GATE` definition|Define gate: required frontmatter findings_verified/findings_passed/findings_failed/certified; min_lines 15; STRICT; semantic checks frontmatter_values_non_empty, per_finding_table_present|certify_gates|DM-006|gate requires the 4 frontmatter fields; min_lines=15; tier=STRICT; both semantic checks bound|M|P0|
|7|COMP-004|`certify_prompts.py`|New ~60–80 LOC module: build single-agent certification verification prompt (pure)|certify_prompts|NFR-004,FR-024|builds one certify prompt from findings+sections; pure; imports `pipeline.models`,`roadmap.models`; ≤~80 LOC|M|P0|
|8|COMP-005|`certify_gates.py`|New ~40–50 LOC module: define `CERTIFY_GATE` gate criteria|certify_gates|DM-006|defines `CERTIFY_GATE`; ≤~50 LOC; consumes `GateCriteria`,`SemanticCheck`|S|P0|
|9|COMP-013|`CERTIFY_GATE` instance|Instantiate `GateCriteria` for `certification-report.md` per DM-006|certify_gates|FR-028,COMP-014|`CERTIFY_GATE` is a `GateCriteria` instance binding DM-006 fields+checks; importable for gate evaluation|S|P0|
|10|COMP-021|`CERTIFY_GATE` registry binding|Bind `CERTIFY_GATE` + `per_finding_table_present` into the gate framework so certification evaluation dispatches to `_has_per_finding_table`|certify_gates|COMP-013,COMP-019|gate framework resolves `per_finding_table_present`→`_has_per_finding_table` and `frontmatter_values_non_empty`→`_frontmatter_values_non_empty`; evaluation invoked on certification report|M|P0|
|11|DM-003|`certification-report.md` frontmatter|Define frontmatter schema for the certification report|certify_prompts|-|findings_verified:int; findings_passed:int; findings_failed:int; certified:bool; certification_date:str(ISO-8601)|S|P0|
|12|DM-006|`CERTIFY_GATE` (`GateCriteria`)|Define gate-criteria values for the certification report|certify_gates|DM-003|required_frontmatter_fields:findings_verified,findings_passed,findings_failed,certified; min_lines:15; enforcement_tier:STRICT; semantic_checks:frontmatter_values_non_empty,per_finding_table_present|S|P0|

### Integration Points — M3

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|`CERTIFY_GATE` registry binding (COMP-021)|Gate registry / strategy|M3|M3|gate evaluation on `certification-report.md`|
|Certify step (FR-023)|Single Step via `execute_pipeline()`|M3|M4|`execute_roadmap()` Phase B|
|`_has_per_finding_table` (from COMP-014)|Semantic-check fn (reused)|M2|M3|COMP-021 binding|

### Milestone Dependencies — M3

- M1 (`Finding` model DM-001)
- M2 (FIXED findings FR-022, semantic-check functions COMP-014, semantic-check registry COMP-019)

### Open Questions — M3

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-R-003|Does `certified-with-caveats` count as pipeline success (SC-001) for a run with <10% BLOCKING certification failures (SC-002 tolerance)?|Determines whether SC-001 12/12-complete is satisfied under the SC-002 tolerance band; affects FR-026 terminal-state classification|Architect + spec owner|Before M3 exit|

## M4: Pipeline Integration, State & Resume

**Objective:** Wire the 12-step flow end-to-end via the two-phase `execute_roadmap()` (Phase A = steps 1–9 + validate; Phase B = remediate internal dispatch then certify single Step), extend `.roadmap-state.json` additively, implement SHA-256 hash-gated resume across the four-state validation lifecycle, and preserve backward compatibility and context isolation. | **Duration:** Weeks 6–7 | **Entry:** M2 remediate engine + M3 certify step complete | **Exit:** `roadmap run` executes all 12 steps; state persists additively; `--resume` skips completed remediate/certify correctly; lifecycle transitions verified

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|FR-001|12-step pipeline flow|Extend `roadmap run` to 12 steps by adding Step 10 (remediate) + Step 11 (certify) after Step 9 (validate); no new CLI command|executor.py|COMP-003,COMP-005|step order: extract,generate-A,generate-B,diff,debate,score,merge,test-strategy,spec-fidelity,validate,remediate,certify; single `roadmap run` invocation|M|P0|
|2|FR-029|Two-phase execution|Phase A=`execute_pipeline(steps 1-9)`+`_auto_invoke_validate()`; Phase B=`remediate_executor.execute()` (internal dispatch) then certify via `execute_pipeline([certify_step])`; interactive prompt in `execute_roadmap()`|executor.py|FR-001,FR-018,FR-023|Phase A non-interactive; prompt between phases in `execute_roadmap()`; Phase B runs remediate-internal then certify-Step; `execute_pipeline()` stays non-interactive|L|P0|
|3|COMP-006|`executor.py` modification|Modify `_build_steps()` wiring, post-validation prompt logic, `_get_all_step_ids()`, `_save_state()`, `execute_roadmap()`, `_apply_resume()`|executor.py|FR-029|all six surfaces updated; remediate+certify in `_build_steps()`/`_get_all_step_ids()`; state saved per step; resume applied|L|P0|
|4|COMP-015|Step registration wiring|Register remediate + certify steps in `_build_steps()` and `_get_all_step_ids()` so the pipeline enumerates and dispatches all 12 steps|executor.py|COMP-006|`_build_steps()` yields 12 steps incl. remediate(internal)+certify(Step); `_get_all_step_ids()` returns 12 IDs in order|M|P0|
|5|COMP-022|Resume dispatch handler|`_apply_resume()` logic mapping per-step gate/hash state to skip-or-rerun decisions|executor.py|FR-031|`_apply_resume()` dispatches: validate-pass→skip-to-remediate; remediate-FIXED+hash-match→skip-to-certify; else rerun; certify-pass→complete|M|P0|
|6|FR-030|State schema extension|Extend `.roadmap-state.json` additively: enhanced `validate`(blocking/warning/info_count,report_file), `remediate`(scope,findings totals,agents_spawned,tasklist_file), `certify`(findings_verified/passed/failed,certified,report_file)|models.py|DM-004|validate/remediate/certify step entries written with all listed fields; additive only; existing fields untouched|M|P0|
|7|FR-031|Hash-gated resume|Resume: validate-pass→skip to remediate; remediate exists all-FIXED + `source_report_hash`==current report SHA-256→skip to certify, else re-run remediate from scratch; certify-pass→complete|executor.py|COMP-022,FR-030|hash match+all-FIXED→skip remediate; hash differs→full re-run; validate/certify gate-pass→skip respective step|L|P0|
|8|FR-032|Validation status lifecycle|Maintain lifecycle `validated-with-issues`→`remediated`→`certified`, with alternate terminal `certified-with-caveats`|models.py|FR-030|state transitions follow the 4-state lifecycle; `certified-with-caveats` reachable from certify FAIL; no invalid transitions|S|P0|
|9|DM-004|`.roadmap-state.json` schema|Define extended state schema (schema_version=2)|models.py|-|schema_version:int(=2); steps:object; steps.validate:{status,blocking_count,warning_count,info_count,report_file}; steps.remediate:{status,scope,findings_total,findings_actionable,findings_fixed,findings_failed,findings_skipped,agents_spawned,tasklist_file}; steps.certify:{status,findings_verified,findings_passed,findings_failed,certified,report_file}; validation:{status}; fidelity_status:str|M|P0|
|10|MIG-001|State schema v1→v2 compatibility|Ensure schema_version bump to 2 is additive: v1 states load without error; missing new fields default; existing consumers unaffected|models.py|DM-004,NFR-005|v1 `.roadmap-state.json` loads under v2 reader; absent new fields→defaults; no consumer breakage; round-trip preserves unknown fields|M|P0|
|11|NFR-005|Backward-compatible schema|`.roadmap-state.json` schema remains backward-compatible — new fields additive; existing consumers unaffected|models.py|DM-004|no field renamed/removed; new fields additive; pre-existing consumers read state unchanged|S|P0|
|12|NFR-006|Context isolation enforcement|Each agent subprocess receives only its prompt and `--file` inputs; no `--continue`, `--session`, or `--resume` flags (inherited FR-003)|remediate_executor|FR-018,COMP-009|every spawned agent gets prompt+`--file` only; `--continue`/`--session`/`--resume` never passed; verified across remediate+certify spawns|S|P0|

### Integration Points — M4

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Step registration (COMP-015)|Step registry / dispatch (`_build_steps`)|M4|M4|`execute_pipeline()` dispatch loop|
|Two-phase orchestration (FR-029)|Phase dispatch in `execute_roadmap()`|M4|M4|remediate internal + certify Step|
|Resume dispatch handler (COMP-022)|Strategy dispatch (state→skip/rerun)|M4|M4|`--resume` flow|
|`.roadmap-state.json` writer (`_save_state`)|State serialization|M4|M4|resume, downstream consumers|

### Milestone Dependencies — M4

- M2 (remediate engine COMP-003, REMEDIATE_GATE)
- M3 (certify step FR-023, CERTIFY_GATE)

### Open Questions — M4

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-R-004|Resume behavior when the tasklist has some FAILED entries but the `source_report_hash` matches — re-run remediate or report-and-stop?|§3.2 covers all-FIXED+match and hash-differs but not partial-FAILED+match; affects FR-031 resume correctness|Architect|Before M4 exit|

## M5: Validation, Performance & Hardening

**Objective:** Validate the integrated pipeline against all eight success criteria, enforce the ≤30% wall-clock performance budget for steps 10–11, add performance instrumentation, and document the new steps. Closes out residual ambiguity OQ-R-003 against SC-001/SC-002. | **Duration:** Weeks 7–8 | **Entry:** M4 12-step pipeline integrated and resumable | **Exit:** SC-001…SC-008 pass; (t10+t11)/(t1→t9)≤0.30 measured; docs updated; no edits outside the allowed file set in any test run

|#|ID|Title|Description|Comp|Deps|AC|Eff|Pri|
|---|---|---|---|---|---|---|---|---|
|1|NFR-003|Performance budget ≤30%|Steps 10–11 (remediate+certify) add ≤30% wall-clock relative to steps 1–9 (baseline = step 1 start → step 9 completion)|remediate_executor|FR-029|measured `(t10+t11)/(t1→t9) ≤ 0.30` on representative run; regression check in CI|M|P1|
|2|OPS-001|Performance instrumentation|Add per-phase timing capture (t1→t9, t10, t11) and emit to state/logs for the NFR-003 budget check|executor.py|FR-030|timing recorded for steps 1–9, remediate, certify; values surfaced for SC-006 computation; no measurable overhead|S|P1|
|3|OPS-002|Documentation update|Document the remediate + certify steps, the tiered prompt, resume semantics, and the four-state lifecycle in user/developer docs|executor.py|FR-001|docs describe 12-step flow, prompt options, lifecycle states, resume rules; examples included|S|P2|
|4|TEST-001|E2E 12-step completion test (SC-001)|Verify `roadmap run` completes all 12 steps without manual intervention when user approves remediation|executor.py|FR-001,FR-029|12/12 steps complete on approve path; asserts terminal `certified`/`tasklist_ready`|M|P1|
|5|TEST-002|BLOCKING PASS-rate test (SC-002)|Verify ≥90% of BLOCKING findings receive PASS in certification|certify_prompts|FR-025|`findings_passed/findings_verified` (BLOCKING) ≥ 0.90 on fixture run|M|P1|
|6|TEST-003|Unfixed-finding detection test (SC-003)|Verify certification correctly identifies unfixed findings (no false passes)|certify_prompts|FR-025|injected unfixed finding→FAIL in report; 0 false passes|M|P1|
|7|TEST-004|Resume skip test (SC-004)|Verify `--resume` correctly skips completed remediation/certification steps per §3.2|executor.py|FR-031|resume skips passing gates; hash-match→skip; hash-differ→rerun asserted|M|P1|
|8|TEST-005|Editable-files boundary test (SC-005)|Verify no edits to files outside `roadmap.md`,`extraction.md`,`test-strategy.md`|remediate_executor|FR-016|0 violations across remediation runs; phase tasklists untouched|M|P1|
|9|TEST-006|Performance budget test (SC-006)|Verify steps 10–11 add ≤30% wall-clock relative to steps 1–9|remediate_executor|NFR-003,OPS-001|`(t10+t11)/(t1→t9) ≤ 0.30` asserted from instrumentation|S|P1|
|10|TEST-007|Tasklist accuracy test (SC-007)|Verify `remediation-tasklist.md` reflects all findings with correct final status|remediate_executor|FR-017|100% findings represented; status matches FIXED/FAILED/SKIPPED outcome|M|P1|
|11|TEST-008|State back-compat test (SC-008)|Verify `.roadmap-state.json` schema remains backward-compatible (new fields additive)|models.py|MIG-001,NFR-005|v1 state loads under v2; existing consumers unaffected; additive-only diff|S|P1|
|12|TEST-009|Rollback integrity test|Verify any agent non-zero exit/timeout halts remaining agents and restores all files from `.pre-remediate`|remediate_executor|FR-021|injected agent failure→all files byte-identical to pre-remediate snapshot; findings FAILED; pipeline halts|M|P1|
|13|TEST-010|Cross-file consistency test|Verify cross-file findings are split into both agents with scoped fragments and resolve consistently|remediate_prompts|FR-013|cross-file finding edits both files coherently; failure of one marks both involved findings FAILED|M|P1|

### Integration Points — M5

|Artifact|Type|Wired|Milestone|Consumed By|
|---|---|---|---|---|
|Performance instrumentation (OPS-001)|Timing hooks → state/logs|M5|M5|TEST-006 / NFR-003 budget check|

### Milestone Dependencies — M5

- M1, M2, M3, M4 (validates integrated outputs against SC-001…SC-008)

### Open Questions — M5

|#|ID|Question|Impact|Resolution Owner|Target|
|---|---|---|---|---|---|
|1|OQ-R-003|Confirm SC-001 success classification for `certified-with-caveats` runs within the SC-002 10% BLOCKING-failure tolerance (cross-referenced from M3)|Determines pass/fail verdict of TEST-001 vs TEST-002 interaction|Architect + spec owner|Before M5 exit|

## Resource Requirements and Dependencies

### External Dependencies

|Dependency|Required By Milestone|Status|Fallback|
|---|---|---|---|
|v2.20-WorkflowEvolution pipeline infrastructure|M1|Required (declared spec dependency)|None — hard prerequisite; M1 blocked until present|
|`ClaudeProcess` (`pipeline.process`)|M1, M2, M3|Available (reused)|None — mandated; no new abstraction permitted (NFR-002)|
|`execute_pipeline()` outer runner|M1, M4|Available (reused)|None — required for steps 1–9 + certify Step|
|`validate_executor.py` (counts + direct-process pattern)|M1, M2|Available (reference)|None — supplies severity counts and `validate_run_step()` pattern|
|`GateCriteria` / `SemanticCheck` framework|M2, M3|Available (reused)|None — gate definitions depend on it|
|`pipeline.models`|M1–M4|Available|None — import source per NFR-007|
|`roadmap.models` (+ new `Finding`)|M1–M5|Extended in M1|None — `Finding` added here|
|`threading` (stdlib)|M2|Available|Sequential fallback degrades NFR-003 budget; not preferred|
|`os.replace` / filesystem (stdlib)|M1, M2|Available|None — atomic writes + snapshot/rollback depend on it|
|`sc:tasklist` (downstream boundary)|Post-M4|External consumer|N/A — runs after certification; not blocking|

### Infrastructure Requirements

- Filesystem supporting atomic `os.replace()` rename semantics on the artifact directory (same volume for tmp + target) — required by NFR-001 and `.pre-remediate` snapshot/rollback.
- Sufficient concurrent process capacity to run one `ClaudeProcess` per target file group (up to 3 parallel agents: roadmap.md / extraction.md / test-strategy.md) within the 300s per-agent timeout.
- Parent-pipeline model configuration accessible to remediate agents (model inherited, FR-015); no separate model credentials introduced.
- CI capacity to run the E2E 12-step test (TEST-001) and performance-budget check (TEST-006) with timing instrumentation.

## Risk Register

|ID|Risk|Affected Milestones|Probability|Impact|Mitigation|Owner|
|----|------|---------------------|-------------|--------|------------|-------|
|R-01|Remediation agent introduces new issues while fixing findings|M2|Medium|Medium|Certification step (M3) catches regressions; user can re-run `roadmap validate`; per-agent constrained prompt (FR-014)|Architect|
|R-02|Report format changes break the parser|M1|Low|High|Parser tested against multiple known formats (COMP-020); graceful degradation + individual-report fallback (FR-033); zero-parseable→skip with warning|Backend lead|
|R-03|Cross-file findings cause conflicting edits|M2|Low|Medium|Batch-by-file strategy (FR-012) eliminates concurrent same-file edits; cross-file split into scoped fragments (FR-013)|Architect|
|R-04|User interrupts during remediation|M2, M4|Low|Low|Hash-gated resume (FR-031) picks up from last completed step; `.pre-remediate` snapshots bound partial state|Backend lead|
|R-05|Certification agent too lenient (false passes)|M3|Medium|Low|`CERTIFY_GATE` enforces structured output (FR-028); user may re-run full validate; TEST-003 asserts unfixed-detection|QA lead|
|R-06|Parallel `threading` orchestration races / partial collect on failure|M2|Medium|High|All-or-nothing rollback (FR-021); batch-by-file isolation; TEST-009 rollback-integrity test; halt-remaining-on-failure|Architect|
|R-07|Resume hash/status edge cases (partial-FAILED + hash-match) under-specified|M4|Medium|Medium|Resolve OQ-R-004 before M4 exit; conservative default = re-run remediate from scratch on any non-all-FIXED state|Architect|
|R-08|Steps 10–11 exceed 30% wall-clock budget|M5|Low|Medium|Parallel agents (FR-012); relevant-sections-only certify context (FR-024); OPS-001 instrumentation + TEST-006 gate|Performance eng|

## Success Criteria and Validation Approach

|Criterion|Metric|Target|Validation Method|Milestone|
|---|---|---|---|---|
|SC-001|Steps completed without manual intervention on approve path|12/12 steps|TEST-001 E2E run of `roadmap run`|M5|
|SC-002|BLOCKING certification PASS rate|`findings_passed/findings_verified` (BLOCKING) ≥ 0.90|TEST-002 fixture certification run|M5|
|SC-003|Unfixed-finding detection|0 false passes|TEST-003 injected-unfixed-finding test|M5|
|SC-004|`--resume` skips completed remediate/certify|Skips passing gates per §3.2|TEST-004 resume test (hash match/differ)|M5|
|SC-005|No edits outside allowed file set|0 violations (only roadmap.md/extraction.md/test-strategy.md)|TEST-005 editable-files boundary test|M5|
|SC-006|Steps 10–11 wall-clock overhead|`(t10+t11)/(t1→t9) ≤ 0.30`|TEST-006 from OPS-001 instrumentation|M5|
|SC-007|Tasklist reflects all findings + status|100% findings, correct status|TEST-007 tasklist accuracy test|M5|
|SC-008|State schema backward-compatible|New fields additive; consumers unaffected|TEST-008 v1→v2 load + round-trip test|M5|

## Decision Summary

|Decision|Chosen|Alternatives Considered|Rationale|
|----------|--------|------------------------|----------|
|Remediate dispatch mechanism|Internal `threading`+`ClaudeProcess` dispatch presented as a single Step|(a) full `execute_pipeline()` per agent; (b) sequential single-agent loop|Mirrors proven `validate_executor.py:validate_run_step()`; preserves `execute_pipeline()` non-interactive contract; enables parallel batch-by-file without new abstraction (NFR-002)|
|Concurrency conflict avoidance|Batch-by-file (one agent per target file)|(a) per-finding agents; (b) global lock with serial edits|Eliminates concurrent same-file edits entirely (R-03); maximizes parallelism across distinct files; simplifies rollback granularity|
|Failure recovery model|All-or-nothing rollback via `.pre-remediate` snapshots|(a) per-file partial commit; (b) best-effort continue|Guarantees consistent on-disk state after failure; avoids half-remediated artifacts; cross-file findings stay coherent|
|Certification depth|Single-agent, single-pass, relevant-sections-only checklist|(a) full adversarial multi-agent re-validation; (b) full-file context|Bounds NFR-003 ≤30% budget; preserves verification accuracy at lower token cost (FR-024); single-pass avoids loop (AC-8)|
|Loop policy|Single-pass, no automatic remediation loop|(a) iterate until certified; (b) capped N-retry loop|Keeps user in control; bounds runtime; failures reported as `certified-with-caveats` for manual re-run (FR-027)|
|Interactive prompt placement|In `execute_roadmap()` (not `execute_pipeline()`)|(a) prompt inside `execute_pipeline()`; (b) CLI flag only|Preserves `execute_pipeline()` non-interactive contract (AC-7); keeps interactivity at the orchestration boundary|
|Resume gating|SHA-256 `source_report_hash` match + all-FIXED check|(a) timestamp-based; (b) always re-run remediate|Detects report drift deterministically; safe skip only when inputs unchanged and complete (FR-031)|
|State schema evolution|Additive fields, `schema_version=2`|(a) breaking re-design; (b) parallel sidecar file|Maintains backward compatibility (NFR-005); existing consumers unaffected; single source of truth|

## Timeline Estimates

|Milestone|Duration|Start|End|Key Milestones|
|---|---|---|---|---|
|M1|2 weeks|Week 1|Week 2|`Finding` model + parser + fallback/dedup; severity counts; OQ-R-006 confirmed|
|M2|3 weeks|Week 3|Week 5|Tiered prompt; batch-by-file; parallel dispatch; snapshot/rollback; REMEDIATE_GATE|
|M3|1.5 weeks|Week 5|Week 6|Certify agent + report; CERTIFY_GATE; outcome states|
|M4|1.5 weeks|Week 6|Week 7|12-step wiring; two-phase exec; state schema v2; hash-gated resume|
|M5|1.5 weeks|Week 7|Week 8|SC-001…SC-008 validation; ≤30% perf budget; docs|

**Total estimated duration:** ~8 weeks (3–5 sprints), consistent with the spec's self-rated 3–5 sprint, ~5-new-file (~500–630 LOC) estimate. M2 and M3 overlap at Week 5; M3 and M4 overlap at Week 6 (certify completion feeds integration wiring).
