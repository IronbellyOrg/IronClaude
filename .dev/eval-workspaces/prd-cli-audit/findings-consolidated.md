# PRD CLI Audit — Stage 2 Consolidated Findings Index

**Date**: 2026-05-20
**Agents**: A (orchestration), B (gates), C (config), D (process), E (prompts), F (tests)
**Raw findings**: 76 across 6 agents
**Consolidated findings**: 39 (after deduplication)
**MEDIUM+ findings (Stage 3 candidates)**: 27

---

## Anchor Verification Block

| Anchor Bug | Description | Consolidated Finding | Status |
|---|---|---|---|
| **Bug 1** | `_STEP_ARTIFACT_FILES` missing `build-task-file` | **F-01** | Accounted |
| **Bug 2** | Artifact name `TASK-PRD-{slug}.md` — slug-templated; static dict cannot carry interpolation | **F-02** | Accounted |
| **Bug 3** | `_tier_min_lines` defined but zero consumers; heavyweight runs use 400 standard default | **F-03** | Accounted |

All three anchor bugs are accounted for. Stage 2 may proceed to Stage 3.

---

## Severity-Ranked Table

Sorted: CRITICAL → LOW; within tier, by pattern-tag count desc, then confidence desc.

| ID | Severity | Pattern tags | File:line | Identified by | One-line summary |
|---|---|---|---|---|---|
| F-01 | **CRITICAL** | P1, P3, P4, P6 | executor.py:246-269 | A-1, B-11, E-1, F-1, F-2, F-3, F-10 | `_STEP_ARTIFACT_FILES` missing `build-task-file` — proximate halt cause |
| F-02 | **CRITICAL** | P3, P5 | executor.py:246-293, prompts.py:381 | A-2, E-2, C-5, F-4 | Static dict cannot express slug-templated artifact names |
| F-03 | **CRITICAL** | P2, P7 | gates.py:281-292, executor.py:530 | B-1, C-1, F-5, F-12 | `_tier_min_lines` unwired — tier thresholds are dead code |
| F-04 | **CRITICAL** | P1, P3, P4, P5, P6 | executor.py:246-251, prompts.py (13 sites) | E-1, E-4, E-5, E-6, E-14, D-1, A-12 | Systemic inversion — all 13 Write-emitting steps missing from dispatch table |
| F-05 | **HIGH** | P1, P3 | executor.py:727-757, gates.py:407-432 | A-3, B-3 | Dynamic step IDs not matched by static GATE_CRITERIA keys |
| F-06 | **HIGH** | P2, P5, P7, P8 | executor.py (no refs), commands.py:135-191 | A-4, C-3 | Resume entirely broken — executor ignores config, CLI drops flags |
| F-07 | **HIGH** | P2 | commands.py:41-45, models.py:182 | C-2 | `--where` flag stored on config, never read by any consumer |
| F-08 | **HIGH** | P1, P2, P7 | executor.py:587-624, gates.py (17 entries) | B-2 | `required_frontmatter_fields` declared but never checked |
| F-09 | **HIGH** | P1, P8 | executor.py:957-970, models.py:220-235 | A-7 | `_handle_shutdown` accesses non-existent `step` attribute |
| F-10 | **HIGH** | P4, P8 | executor.py:99-130 | A-10, D-4 | NDJSON extraction silently swallows errors and falls back to raw |
| F-11 | **HIGH** | P2, P4, P8 | monitor.py:1-202, executor.py:334 | D-2 | `PrdMonitor` entirely dead code — `stall_timeout` unwired |
| F-12 | **HIGH** | P4, P8 | process.py:63-86, 208-219 | D-5 | Retry only fires on `OSError` — post-launch transients bypass |
| F-13 | **HIGH** | P7 | filtering.py:108-112 | E-8 | Double-braced regex in raw string never matches |
| F-14 | **HIGH** | P5, P7 | config.py:102-117, prompts.py:919,1093 | C-4 | `output_path` file-vs-directory pun |
| F-15 | **HIGH** | P5, P7 | config.py:120-125, prompts.py:381,384 | C-5 | Empty `product_slug` produces malformed paths and IDs |
| F-16 | **MEDIUM** | P3, P6 | executor.py:279-291 | A-11 | `_resolve_step_content` picks largest file without validation |
| F-17 | **MEDIUM** | P8 | executor.py:392-409, 692-705 | A-8 | STRICT failures in structural/qualitative-qa not propagated |
| F-18 | **MEDIUM** | P3, P4 | executor.py:577-583, gates.py:36-53 | A-9, B-8 | Verdict literal matching brittle in executor and gate layers |
| F-19 | **MEDIUM** | P6 | executor.py:518-532 | A-17 | Sentinel detection and gate evaluation read different sources |
| F-20 | **MEDIUM** | P4, P7, P8 | executor.py:499, models.py:190-191 | A-13, D-3 | Stall timeout semantic shift — 30× multiplier for wall-clock |
| F-21 | **MEDIUM** | P2, P7 | config.py:120-125, prompts.py:65-101 | C-6 | Dual slug sources (CLI vs LLM) with no reconciliation |
| F-22 | **MEDIUM** | P2, P7 | gates.py:300-504, executor.py:531-540 | B-4 | EXEMPT/LIGHT enforcement tiers not recognized |
| F-23 | **MEDIUM** | P7 | filtering.py:331-366 | E-7 | `_filter_research_for_sections` keyword heuristic drops files |
| F-24 | **MEDIUM** | P7 | inventory.py:55-59 | E-10 | `check_existing_work` returns `ALREADY_COMPLETE` for any `.md` |
| F-25 | **MEDIUM** | P4, P7, P8 | executor.py:562-585, pipeline/process.py:159-171 | D-6, D-7 | Subprocess lifecycle gaps — exit codes collapse, signals not relayed |
| F-26 | **MEDIUM** | P5, P7 | config.py:108-117 | C-9 | `output_path` default resolves at CWD without project-root check |
| F-27 | **MEDIUM** | P6, P9 | test_integration.py:197-223, test_e2e.py:224-253 | F-6, F-8, F-9 | Test surface gaps — gate barely exercised, mocks defeat real chain |
| F-28 | **LOW** | P4, P6 | prompts.py:148-260 | E-3 | Stdout-only steps risk disk-Write divergence |
| F-29 | **LOW** | P1, P2, P8 | executor.py:300-316, 366-367 | A-5, A-6 | Step metadata declared but not consumed |
| F-30 | **LOW** | P8 | executor.py:463-467, 792-802 | A-14 | Dual step_results list maintenance hazard |
| F-31 | **LOW** | P3, P7 | executor.py:1006-1019 | A-15 | `_estimate_turns` substring collision |
| F-32 | **LOW** | P1, P8 | executor.py:396-409 | A-16 | `present-complete` effectively cosmetic |
| F-33 | **LOW** | P1 | executor.py:99-130, monitor.py:69-98 | D-10 | Duplicated NDJSON parser |
| F-34 | **LOW** | P1, P3 | process.py:95-113, config.py:26-33 | D-11, C-10 | Static dispatch tables for step IDs |
| F-35 | **LOW** | P7 | commands.py:55, config.py:85 | C-8 | Tier default duplicated |
| F-36 | **LOW** | P2, P5, P7 | inventory.py:138-160, filtering.py:74,309 | E-9, E-11, E-12 | Inventory/filtering dead code |
| F-37 | **LOW** | P3 | prompts.py:1145, 1172-1173 | E-13 | `failure_area_slug` truncation collision |
| F-38 | **LOW** | P4 | logging_.py:166-174, pipeline/process.py:140-146 | D-8, D-9, D-12 | Process I/O robustness gaps |
| F-39 | **LOW** | P2, P3 | gates.py:83-212 | B-5, B-6, B-7, B-9, B-10 | Gate-check regexes overly permissive |

---

## Deduplication Rules Applied

1. **Same file:line + same pattern tag + compatible severity** → MERGE. Example: A-1 (executor.py:246, CRITICAL) + B-11 (executor.py:246-251, HIGH) → F-01 (CRITICAL, most severe rating preserved).
2. **Same root cause from different angles** → MERGE with per-contributor cross-ref. Example: A-1 + B-11 + E-1 + F-1/2/3 → F-01.
3. **Same file, different lines, different defect** → KEEP SEPARATE. F-01 (executor.py:246, dispatch dict) and F-05 (executor.py:727, dynamic IDs) are different defects.
4. **One agent's "considered and rejected" vs another's promotion** → KEEP the promotion.
5. **Test-gap findings** merged into the defect they fail to catch when same defect from test angle (F-F-1/2/3 → F-01). Structural test-surface gaps (F-F-6/8/9) stay in F-27.
6. **Different regex defects in same file with same root cause and severity tier** → MERGE (F-39).

---

## Cross-Cutting Observations

### 1. Static dispatch vs dynamic reality (Agents A, B, D, E independently)
Contributing: F-01, F-02, F-04, F-05, F-34. Four agents independently identified the same shape: multiple static dispatch tables (`_STEP_ARTIFACT_FILES`, `GATE_CRITERIA`, `_PHASE_ALLOWED_REFS`, `_STEP_ID_PATTERN`) must be maintained in sync with dynamic step generators. Adding a step requires editing 4+ tables independently. **Remediation hint**: a canonical step registry as single source of truth, or pattern-based lookup.

### 2. Knob wired to config but never consumed (Agents B, C, D)
Contributing: F-03, F-07, F-11, F-20, F-22, F-35. Multiple config knobs reach `PrdConfig` correctly but have zero downstream consumers. **Remediation hint**: audit all `PrdConfig` fields for consumer count; remove dead fields or wire them.

### 3. NDJSON stream treated as authoritative content (Agents A, D, F)
Contributing: F-01, F-04, F-10, F-19. Subprocess produces two channels (NDJSON stream + disk artifacts via Write). Gate evaluation conflates them. **Remediation hint**: gate evaluation must always prefer disk artifacts for steps that instruct Write; `_resolve_step_content` needs a two-phase strategy.

### 4. Test surface structurally cannot catch dispatch regressions (Agent F + cross-refs)
Contributing: F-27 plus test-gap components of F-01–F-04. The mock harness writes gate-passing content into the NDJSON stream file, making it impossible for any test to distinguish "gate read the disk artifact" from "gate read the stream." This is the structural reason Bug 1 shipped. **Remediation hint**: two-actor mock pattern; structural tests asserting dispatch table completeness.

---

## Stage 3 Invocation Plan

**Per the user's verified invocation pattern (no extra flags):**

```
/sc:adversarial \
  --source .dev/eval-workspaces/prd-cli-audit/findings/F-<NN>-<slug>.md \
  --generate bug-report-adjudication \
  --agents opus:analyzer,opus:refactorer,sonnet:architect \
  --depth standard \
  --focus reproducibility,blast-radius,severity-calibration \
  --output .dev/eval-workspaces/prd-cli-audit/adjudications/F-<NN>/
```

Run in parallel across findings; cap parallelism at 4.

### MEDIUM+ findings to adjudicate (27 total)

CRITICAL (4): F-01, F-02, F-03, F-04
HIGH (11): F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15
MEDIUM (12): F-16, F-17, F-18, F-19, F-20, F-21, F-22, F-23, F-24, F-25, F-26, F-27

### LOW findings (12): Stage 1 only — not adjudicated
F-28, F-29, F-30, F-31, F-32, F-33, F-34, F-35, F-36, F-37, F-38, F-39

---

## Summary

- **Total consolidated findings**: 39 (from 76 raw)
- **Anchor bug mapping**: Bug 1 → F-01, Bug 2 → F-02, Bug 3 → F-03 (all 3 accounted)
- **MEDIUM+ findings (Stage 3 invocation count)**: 27
- **CRITICAL**: 4 | **HIGH**: 11 | **MEDIUM**: 12 | **LOW**: 12
- **Cross-cutting patterns**: 4 systemic themes identified across 3+ agents each
- **Standalone files**: 39 (F-01 … F-39) under `.dev/eval-workspaces/prd-cli-audit/findings/`
