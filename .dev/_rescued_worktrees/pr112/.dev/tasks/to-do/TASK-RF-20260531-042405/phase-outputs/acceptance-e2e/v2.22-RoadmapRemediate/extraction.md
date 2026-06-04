---
spec_source: spec-roadmap-remediate.compressed.md
generated: 2026-06-03T02:34:36Z
generator: requirements-extraction-specialist
functional_requirements: 33
nonfunctional_requirements: 7
total_requirements: 40
complexity_score: 0.7
complexity_class: HIGH
domains_detected: [backend, cli, quality, devops]
risks_identified: 5
dependencies_identified: 10
success_criteria_count: 8
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 211.0, started_at: "2026-06-03T02:34:33.956190+00:00", finished_at: "2026-06-03T02:38:04.980709+00:00"}
---

## Functional Requirements

The spec defines no native `FR-` identifiers for its new behavior (it only *references* inherited parent-pipeline IDs `FR-003`, `NFR-004`, `NFR-007`). Per the fallback rule, new functional requirements use `FR-NNN`. Inherited IDs are preserved verbatim and documented under Architectural Constraints. Artifact paths/step-IDs are recorded verbatim from §2–§3.

| ID | Requirement | Source | Exact paths / route patterns |
|---|---|---|---|
| FR-001 | Extend the existing `roadmap run` pipeline to a 12-step flow by adding Step 10 (remediate) and Step 11 (certify) after Step 9 (validate); no new CLI command — remediation is part of the default `roadmap run` workflow. | §2.1, §2 | `roadmap run`; steps: `extract`, `generate-A`, `generate-B`, `diff`, `debate`, `score`, `merge`, `test-strategy`, `spec-fidelity`, `validate`, `remediate`, `certify` |
| FR-002 | After validation completes, parse the merged validation report to extract finding counts by severity (BLOCKING / WARNING / INFO). | §2.2 | `validate/reflect-merged.md`, `validate/merged-validation-report.md` |
| FR-003 | Print a brief terminal summary box listing finding counts and per-severity finding IDs/descriptions. | §2.2 | (terminal output; box layout in §2.2) |
| FR-004 | Present an interactive tiered remediation prompt with options `[1] BLOCKING only`, `[2] BLOCKING + WARNING`, `[3] All (incl. INFO)`, `[n] Skip`. | §2.2, §2.8 OQ-001 | (terminal prompt) |
| FR-005 | On `n` (skip): pipeline ends, state saved as `validated-with-issues`, validation report remains on disk for manual review. | §2.2 | validation report file remains |
| FR-006 | On `1`/`2`/`3`: continue to Step 10 with the selected severity scope; findings outside the chosen scope are marked `SKIPPED` in the remediation tasklist. | §2.2 | `remediation-tasklist.md` |
| FR-007 | Auto-skip the prompt when 0 BLOCKING and 0 WARNING: if also 0 INFO → proceed directly to certify as a no-op; if INFO findings exist → skip remediation and proceed to certify. | §2.2 | — |
| FR-008 | Extract findings from the merged report into structured `Finding` objects carrying all 10 fields (id, severity, dimension, description, location, evidence, fix_guidance, files_affected, status, agreement_category). | §2.3.1 | `validate/reflect-merged.md` or `validate/merged-validation-report.md` |
| FR-009 | Filter findings by user-selected scope: Option 1 → only BLOCKING with fix guidance proceed (WARNING/INFO SKIPPED); Option 2 → BLOCKING+WARNING proceed (INFO SKIPPED); Option 3 → all severities with fix guidance proceed. | §2.3.2 | — |
| FR-010 | Always mark findings already tagged `NO_ACTION_REQUIRED` or `OUT_OF_SCOPE` as SKIPPED, regardless of the user's selection. | §2.3.2 | — |
| FR-011 | Zero-findings guard: if filtering yields 0 actionable findings, emit `remediation-tasklist.md` with `actionable: 0` and all entries SKIPPED; certify then produces `certification-report.md` with `findings_verified: 0`, `certified: true` (vacuously certified). | §2.3.2 | `remediation-tasklist.md`, `certification-report.md` |
| FR-012 | Group actionable findings by primary target file (batch-by-file); all findings for one file route to one agent; agents targeting different files run in parallel. | §2.3.3 | `roadmap.md`, `test-strategy.md`, `extraction.md` |
| FR-013 | Handle cross-file findings (e.g., F-05 spanning roadmap.md + test-strategy.md) by including the finding in both agents' prompts with a scoped "YOUR FILE" fix-guidance fragment and a note that the other side is handled by a separate agent. | §2.3.4 | `roadmap.md:§3.1`, `test-strategy.md:§2.1` |
| FR-014 | Build each remediation agent prompt with the constrained structure: edit ONLY the one target file, apply ONLY the listed fixes, preserve YAML frontmatter, preserve markdown heading hierarchy, and do not reorder sections unless fix guidance requires it. | §2.3.4, §2.3.5 | `{file_path}` |
| FR-015 | Apply agent execution parameters: 300-second timeout per agent, 1 retry on failure, model inherited from parent pipeline config. | §2.3.4 | — |
| FR-016 | Enforce the editable-files constraint: remediation agents may ONLY edit `roadmap.md`, `extraction.md`, `test-strategy.md`; phase tasklist files are not in scope (generated downstream). | §2.3.5, §5.2 | `roadmap.md`, `extraction.md`, `test-strategy.md` |
| FR-017 | Emit `remediation-tasklist.md` as a standalone file (not phase-tasklist format) with the specified frontmatter and BLOCKING/WARNING/SKIPPED sections. | §2.3.6 | `remediation-tasklist.md` |
| FR-018 | Present the remediate step as a single Step to `execute_pipeline()` while internally using `ClaudeProcess` directly (one process per file group, parallel via `threading`) — NOT `execute_pipeline()`, matching `validate_executor.py:validate_run_step()`. | §2.3.7, §2.5 | `remediate_executor.py`, `pipeline.process`, `validate_executor.py:validate_run_step()` |
| FR-019 | Define `REMEDIATE_GATE` (required frontmatter: type, source_report, source_report_hash, total_findings, actionable, skipped; min_lines 10; STRICT; semantic checks `frontmatter_values_non_empty`, `all_actionable_have_status`). | §2.3.7 | `remediation-tasklist.md` |
| FR-020 | Before spawning agents, snapshot all target files to `<file>.pre-remediate` for rollback. | §2.3.8 | `roadmap.md.pre-remediate`, `test-strategy.md.pre-remediate`, `extraction.md.pre-remediate` |
| FR-021 | On any agent non-zero exit or timeout: halt remaining agents, roll back all target files from snapshots, mark the failed agent's findings FAILED, mark all cross-file findings involving the failed file FAILED, set remediate step FAIL, and halt the pipeline. | §2.3.8 | `.pre-remediate` snapshots |
| FR-022 | On full success: delete `.pre-remediate` snapshots and set all agent-targeted findings to FIXED. | §2.3.8 | `.pre-remediate` snapshots |
| FR-023 | Step 11 (certify): perform lightweight re-validation scoped to the fixed findings via a single agent, single pass, checklist verification — without the full adversarial multi-agent debate. | §2.4.1, §2.4.2 | — |
| FR-024 | Provide the certify agent only the relevant sections surrounding each finding's location (not full file content) to minimize token cost while preserving verification accuracy. | §2.4.2, §2.8 OQ-002 | — |
| FR-025 | Emit `certification-report.md` with the specified frontmatter, a per-finding results table (Finding/Severity/Result/Justification), and a summary. | §2.4.3 | `certification-report.md` |
| FR-026 | Certification outcomes: all PASS → state `certified: true`, `tasklist_ready: true`, pipeline completes; any FAIL → state `certified-with-caveats`, report lists failures, pipeline completes (no loop), user may re-run `roadmap validate`. | §2.4.4 | `roadmap validate` |
| FR-027 | No automatic remediation loop: certification runs a single pass; if issues remain it reports and stops, leaving the user in control. | §2.4.4, §5.2 | — |
| FR-028 | Define `CERTIFY_GATE` (required frontmatter: findings_verified, findings_passed, findings_failed, certified; min_lines 15; STRICT; semantic checks `frontmatter_values_non_empty`, `per_finding_table_present`). | §2.4.5 | `certification-report.md` |
| FR-029 | Execute the extended pipeline as two phases with the interactive prompt handled in `execute_roadmap()` (not `execute_pipeline()`): Phase A = `execute_pipeline(steps 1-9)` + `_auto_invoke_validate()`; Phase B = `remediate_executor.execute()` (internal dispatch) then certify via `execute_pipeline([certify_step])`. | §2.5 | `execute_roadmap()`, `execute_pipeline()`, `_auto_invoke_validate()` |
| FR-030 | Extend `.roadmap-state.json` with additive step entries: enhanced `validate` (blocking_count, warning_count, info_count, report_file), `remediate` (scope, findings_total/actionable/fixed/failed/skipped, agents_spawned, tasklist_file), `certify` (findings_verified/passed/failed, certified, report_file). | §3.1 | `.roadmap-state.json` |
| FR-031 | Resume behavior: if `validate` output passes its gate → skip to remediate; if `remediate` output exists with all FIXED and `source_report_hash` matches the current report's SHA-256 → skip to certify, else re-run remediate from scratch; if `certify` passes its gate → pipeline complete. | §3.2 | `.roadmap-state.json`, `remediation-tasklist.md`, `--resume` |
| FR-032 | Maintain the validation status lifecycle: `validated-with-issues` → `remediated` → `certified`, with the alternate terminal state `certified-with-caveats`. | §3.3 | — |
| FR-033 | Fallback parser (OQ-003): when the merged report is missing/malformed, parse individual reflect reports; deduplicate by (a) location match — same file AND locations overlapping or within 5 lines — and (b) severity resolution — keep higher severity (BLOCKING>WARNING>INFO), merging fix guidance and preferring the more specific; non-matching findings included as-is; if no parseable reports exist, skip remediation with a warning. | §2.8 OQ-003, §4.4 Phase 1 | `reflect-opus-architect.md`, `reflect-haiku-analyzer.md`, `reflect-*.md` |

## Non-Functional Requirements

The spec preserves inherited parent-pipeline IDs verbatim (`NFR-004`, `NFR-007`, and `FR-003` for context isolation). New non-functional requirements use the `NFR-NNN` fallback (IDs 004/007 reserved for inherited).

| ID | Category | Requirement | Source |
|---|---|---|---|
| NFR-001 | Maintainability / Data integrity | Atomic writes — all file writes use the tmp + `os.replace()` pattern. | §5.1 |
| NFR-002 | Maintainability / Architecture | No new subprocess abstractions — reuse existing `ClaudeProcess` from `pipeline.process`. | §5.1 |
| NFR-003 | Performance | Steps 10–11 (remediate + certify) add ≤30% wall-clock time relative to steps 1–9 of the same run (baseline = step 1 start → step 9 completion). | §7 SC-006 |
| NFR-004 (inherited) | Maintainability | Pure prompts — all prompt builders are pure functions with no I/O, subprocess calls, or side effects. | §5.1 |
| NFR-005 | Compatibility | `.roadmap-state.json` schema remains backward-compatible — new fields are additive; existing consumers unaffected. | §7 SC-008 |
| NFR-006 | Security / Isolation | Context isolation — each agent subprocess receives only its prompt and `--file` inputs; no `--continue`, `--session`, or `--resume` flags. (Spec labels this inherited `FR-003`.) | §5.1 |
| NFR-007 (inherited) | Architecture | Unidirectional imports — `remediate_*` and `certify_*` modules may import from `pipeline.models` and `roadmap.models`, but not vice versa. | §5.1 |

## Complexity Assessment

**complexity_score: 0.7 — complexity_class: HIGH**

Scoring rationale:
- **Requirement volume (high):** 33 functional + 7 non-functional requirements across two new pipeline steps plus a Step-9 enhancement.
- **Concurrency (high):** Parallel multi-agent orchestration via `threading`, one `ClaudeProcess` per file group, with batch-by-file conflict avoidance.
- **Failure handling (high):** All-or-nothing rollback semantics with `.pre-remediate` snapshots, cross-file consistency dependencies, and pipeline halt-on-failure.
- **State & resume (medium-high):** Schema extensions, SHA-256 hash-gated resume, four-state validation lifecycle, backward-compatibility constraint.
- **Parsing robustness (medium-high):** Multi-format report parser with fallback to individual reflect reports and a two-step dedup (location proximity + severity resolution).
- **Mitigating factors (lowers from very-high):** Reuses existing pipeline primitives (`ClaudeProcess`, `execute_pipeline`, `GateCriteria`); single-pass (no loop); estimated 5 new files (~500–630 lines); 3–5 sprints; self-rated risk medium.

## Architectural Constraints

- **AC-1 / FR-003 (inherited):** Context isolation — agents receive only prompt + `--file`; no `--continue`/`--session`/`--resume`.
- **AC-2 / NFR-004 (inherited):** Pure prompt builders (no I/O, subprocess, or side effects).
- **AC-3 / NFR-007 (inherited):** Unidirectional imports — `remediate_*`/`certify_*` → `pipeline.models`, `roadmap.models` only.
- **AC-4:** Atomic writes (tmp + `os.replace()`).
- **AC-5:** No new subprocess abstractions — reuse `ClaudeProcess` from `pipeline.process` (per roadmap constraint).
- **AC-6:** Editable-files boundary — agents may edit only `roadmap.md`, `extraction.md`, `test-strategy.md`; phase tasklists are out of scope (downstream).
- **AC-7:** Pipeline contract — the user prompt lives in `execute_roadmap()`, preserving `execute_pipeline()`'s non-interactive contract; remediate uses internal dispatch, certify is a standard single-Step via `execute_pipeline()`.
- **AC-8:** Single-pass model — no automatic remediation/certification loop.
- **AC-9 (scope):** No full re-validation (adversarial multi-agent) after remediation; no tasklist-level remediation; no per-finding cherry-picking (severity-scope selection only).
- **AC-10:** Module placement — new code under `src/superclaude/cli/roadmap/`.
- **AC-11:** Dependency — requires v2.20-WorkflowEvolution pipeline infrastructure.

## Component Inventory

### Services / Modules / Classes (COMP)

| ID | Name / Path | Role | Dependencies | Source ref |
|---|---|---|---|---|
| COMP-001 | `remediate_parser.py` (new, ~120–150 LOC) | Parse validation reports → `Finding` objects; fallback + dedup logic | `roadmap.models` (Finding), report files | §4.1, §2.3.1 |
| COMP-002 | `remediate_prompts.py` (new, ~80–100 LOC) | Build scoped fix prompts per file-group (pure functions) | `pipeline.models`, `roadmap.models` | §4.1, §2.3.4 |
| COMP-003 | `remediate_executor.py` (new, ~200–250 LOC) | Orchestrate extract → filter → batch → snapshot → spawn → collect → rollback | COMP-001, COMP-002, `ClaudeProcess`, `threading` | §4.1, §2.3.7, §2.3.8 |
| COMP-004 | `certify_prompts.py` (new, ~60–80 LOC) | Build single-agent certification verification prompt (pure) | `pipeline.models`, `roadmap.models` | §4.1, §2.4.2 |
| COMP-005 | `certify_gates.py` (new, ~40–50 LOC) | Define `CERTIFY_GATE` gate criteria | `GateCriteria`, `SemanticCheck` | §4.1, §2.4.5 |
| COMP-006 | `executor.py` (modified) | `_build_steps()` wiring, post-validation user-prompt logic, `_get_all_step_ids()`, `_save_state()`, `execute_roadmap()`, `_apply_resume()` | COMP-003, COMP-005, `execute_pipeline` | §4.2, §2.5, §3.2 |
| COMP-007 | `models.py` (modified) | Add `Finding` dataclass; `RoadmapConfig` (no new fields) | — | §4.2, §2.3.1 |
| COMP-008 | `validate_executor.py` (referenced/unchanged) | Returns structured finding counts; pattern for direct `ClaudeProcess` use (`validate_run_step()`) | `ClaudeProcess` | §4.2, §2.3.7 |
| COMP-009 | `ClaudeProcess` (`pipeline.process`, reused) | Subprocess abstraction for spawning agents | — | §2.3.7, §5.1 |
| COMP-010 | `execute_pipeline()` (reused) | Outer non-interactive pipeline runner; runs certify as single Step | — | §2.5, §2.3.7 |
| COMP-011 | `_auto_invoke_validate()` (reused) | Existing post-step-9 validation invocation | — | §2.5 |
| COMP-012 | `REMEDIATE_GATE` (`GateCriteria` instance) | Gate for `remediation-tasklist.md` | `GateCriteria`, `SemanticCheck` | §2.3.7 |
| COMP-013 | `CERTIFY_GATE` (`GateCriteria` instance) | Gate for `certification-report.md` | `GateCriteria`, `SemanticCheck` | §2.4.5 |
| COMP-014 | Semantic-check functions | `_frontmatter_values_non_empty`, `_all_actionable_have_status`, `_has_per_finding_table` | — | §2.3.7, §2.4.5 |

### Data Models / DTOs (DM)

**DM-001 — `Finding` dataclass** (`models.py`; §2.3.1)
| Field | Type | Notes |
|---|---|---|
| id | str | "F-01", "F-02", … |
| severity | str | BLOCKING / WARNING / INFO |
| dimension | str | Schema / Structure / Traceability / etc. |
| description | str | one-line summary |
| location | str | "roadmap.md:§3.1" or "test-strategy.md:1-4" |
| evidence | str | expected vs found |
| fix_guidance | str | concrete resolution steps |
| files_affected | list[str] | e.g. ["roadmap.md", "test-strategy.md"] |
| status | str | PENDING / FIXED / FAILED / SKIPPED |
| agreement_category | str | BOTH_AGREE / ONLY_A / ONLY_B / CONFLICT |

**DM-002 — `remediation-tasklist.md` frontmatter** (§2.3.6)
| Field | Type |
|---|---|
| type | str ("remediation-tasklist") |
| source_report | str (path) |
| source_report_hash | str (SHA-256) |
| generated | str (ISO-8601) |
| total_findings | int |
| actionable | int |
| skipped | int |

**DM-003 — `certification-report.md` frontmatter** (§2.4.3)
| Field | Type |
|---|---|
| findings_verified | int |
| findings_passed | int |
| findings_failed | int |
| certified | bool |
| certification_date | str (ISO-8601) |

**DM-004 — `.roadmap-state.json` schema** (§3.1)
| Field | Type | Notes |
|---|---|---|
| schema_version | int | =2 |
| steps | object | per-step status maps |
| steps.validate | object | status, blocking_count, warning_count, info_count, report_file |
| steps.remediate | object | status, scope, findings_total, findings_actionable, findings_fixed, findings_failed, findings_skipped, agents_spawned, tasklist_file |
| steps.certify | object | status, findings_verified, findings_passed, findings_failed, certified, report_file |
| validation | object | status (lifecycle value) |
| fidelity_status | str | e.g. "pass" |

**DM-005 — `REMEDIATE_GATE` (`GateCriteria`)** (§2.3.7)
| Field | Value |
|---|---|
| required_frontmatter_fields | type, source_report, source_report_hash, total_findings, actionable, skipped |
| min_lines | 10 |
| enforcement_tier | STRICT |
| semantic_checks | frontmatter_values_non_empty, all_actionable_have_status |

**DM-006 — `CERTIFY_GATE` (`GateCriteria`)** (§2.4.5)
| Field | Value |
|---|---|
| required_frontmatter_fields | findings_verified, findings_passed, findings_failed, certified |
| min_lines | 15 |
| enforcement_tier | STRICT |
| semantic_checks | frontmatter_values_non_empty, per_finding_table_present |

## Risk Inventory

1. **Remediation agent introduces new issues** — severity: medium (prob. Medium / impact Medium). Mitigation: certification step catches regressions; user can re-run validate. (§6)
2. **Report format changes break parser** — severity: high (prob. Low / impact High). Mitigation: parser tested against multiple known formats; graceful degradation + individual-report fallback. (§6, §2.8 OQ-003)
3. **Cross-file findings cause conflicting edits** — severity: medium (prob. Low / impact Medium). Mitigation: batch-by-file strategy eliminates concurrent edits to the same file. (§6, §2.3.3)
4. **User interrupts during remediation** — severity: low (prob. Low / impact Low). Mitigation: resume support picks up from last completed step. (§6, §3.2)
5. **Certification agent is too lenient (false passes)** — severity: low (prob. Medium / impact Low). Mitigation: gate criteria enforce structured output; user can re-run full validate. (§6, SC-003)

## Dependency Inventory

1. **v2.20-WorkflowEvolution** — pipeline infrastructure (declared spec dependency). (frontmatter, §1)
2. **`ClaudeProcess`** (`pipeline.process`) — agent subprocess abstraction (must reuse). (§2.3.7, §5.1)
3. **`execute_pipeline()`** — outer pipeline runner (steps 1–9 and certify step). (§2.5)
4. **`validate_executor.py`** — supplies structured finding counts; reference pattern for direct process use. (§2.3.7, §4.2)
5. **`GateCriteria` / `SemanticCheck`** — gate framework for REMEDIATE_GATE / CERTIFY_GATE. (§2.3.7, §2.4.5)
6. **`pipeline.models`** — import source for shared models. (§5.1)
7. **`roadmap.models`** — import source incl. new `Finding` dataclass. (§5.1, §4.2)
8. **`threading` (stdlib)** — parallel agent execution. (§2.3.7)
9. **`os.replace` / filesystem (stdlib)** — atomic writes + `.pre-remediate` snapshot/rollback. (§5.1, §2.3.8)
10. **`sc:tasklist` (downstream integration boundary)** — consumes certified roadmap; runs after certification, generating phase tasklists. (§2.3.5, §2.4.4)

## Success Criteria

| ID | Criterion | Measurable threshold |
|---|---|---|
| SC-001 | `roadmap run` completes all 12 steps without manual intervention when user approves remediation | 12/12 steps complete |
| SC-002 | ≥90% of BLOCKING findings receive PASS in the certification report | `findings_passed / findings_verified` (BLOCKING severity) ≥ 0.90 |
| SC-003 | Certification correctly identifies unfixed findings | 0 false passes |
| SC-004 | `--resume` correctly skips completed remediation/certification steps | resume skips passing gates per §3.2 |
| SC-005 | No edits to files outside the allowed set | edits limited to `roadmap.md`, `extraction.md`, `test-strategy.md` (0 violations) |
| SC-006 | Steps 10–11 add ≤30% wall-clock relative to steps 1–9 | `(t10+t11) / (t1→t9) ≤ 0.30` |
| SC-007 | `remediation-tasklist.md` accurately reflects all findings and final status | 100% findings represented with correct status |
| SC-008 | `.roadmap-state.json` schema remains backward-compatible | new fields additive; existing consumers unaffected |

## Open Questions

OQ-001, OQ-002, OQ-003 are already RESOLVED in the spec (§8) — tiered scope prompt, relevant-sections-only certification, and missing/malformed-report fallback with dedup, respectively. Residual ambiguities requiring stakeholder clarification:

1. **Retry semantics on partial cross-file success** — spec states "1 retry on failure" (§2.3.4) but also "halt remaining agents on any failure" (§2.3.8). Order of operations is undefined: does the single retry occur *before* the global halt/rollback, or does halt preempt retry? Needs clarification.
2. **`agreement_category` population from non-merged sources** — the field is BOTH_AGREE/ONLY_A/ONLY_B/CONFLICT, which presupposes a two-generator merged report. Its value when findings come from the individual-report fallback path (OQ-003) is unspecified.
3. **SC-002 vs. pipeline success** — SC-002 allows up to 10% of BLOCKING findings to FAIL certification, yet any FAIL drives `certified-with-caveats`. Whether `certified-with-caveats` counts as pipeline success (SC-001) for a run with <10% BLOCKING failures is ambiguous.
4. **Resume hash mismatch on a partially-FIXED tasklist** — §3.2 covers "all FIXED + hash matches" and "hash differs"; behavior when the tasklist has some FAILED entries but the hash matches (re-run vs. report) is not explicitly stated.
5. **INFO-only auto-path output artifacts** — when 0 BLOCKING/0 WARNING but INFO exist, the pipeline "skips remediation and proceeds to certify" (§2.2); whether a `remediation-tasklist.md` is still emitted (and with what `actionable` value) for this branch is not fully specified relative to the zero-findings guard (§2.3.2).
6. **`extraction.md` vs. `extraction` filename** — the spec uses `extraction.md` in scope lists (§2.3.5) but the pipeline step is `extract`; confirm the on-disk artifact filename the remediation agents target.
7. **No HTTP/route surface** — this is a CLI/pipeline spec; no URL endpoints exist. All "paths" recorded above are artifact files and pipeline step IDs. Confirm no external API surface is expected.
