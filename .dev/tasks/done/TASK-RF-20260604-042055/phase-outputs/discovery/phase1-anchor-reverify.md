# Phase 1 — Anchor Re-Verification (Drift Guard)

**Date:** 2026-06-04 (Step 1.4)
**Method:** `grep -nE` against the LIVE source files (the dedicated Grep tool was unavailable in this
harness; read-only Bash grep used as a tool-availability fallback, not a strategy pivot). Every anchor
checked against the actual file — none assumed from research.

**VERDICT: ALL load-bearing anchors CONFIRMED. ZERO structural drift vs research 01/02/03.**

---

## task-builder/SKILL.md (2190 lines — matches research 01)

| Anchor | Research line | Live grep | Status |
|---|---|---|---|
| `### A.10.5: Task File Qualitative Validation` | 1194 | 1194 | CONFIRMED |
| `### A.10.6: DM-005 Phase Contract …` | 1339 | 1339 | CONFIRMED |
| `### A.11: Present Results` | 1398 | 1398 | CONFIRMED |
| Critical Rule `16.` | 2030 | 2030 | CONFIRMED |
| Critical Rule `17.` | 2032 | 2032 | CONFIRMED |
| Critical Rule `18.` (HIGHEST — no 19 exists) | 2034 | 2034 | CONFIRMED |
| `**Precedence rule:**` (after rule 18) | 2036 | 2036 | CONFIRMED |
| `## Input` | 29 | 29 | CONFIRMED |
| `## Execution Overview` | 143 | 143 | CONFIRMED |
| `## Output Structure` | 1861 | 1861 | CONFIRMED |
| `## Task File Validation Checklist` | 1953 | 1953 | CONFIRMED |
| `## Critical Rules (Non-Negotiable)` | 1998 | 1998 | CONFIRMED |
| `## Research Quality Signals` | 2040 | 2040 | CONFIRMED |
| `### A.2: Parse & Triage` | 190 | 190 | CONFIRMED |
| `### A.9: Spawn Builder` | 781 | 781 | CONFIRMED |
| `EXECUTION_CONTEXT_REQUIREMENTS:` field | 827 | 827 | CONFIRMED |
| `DOCUMENTATION STALENESS WARNINGS:` (next field) | 849 | 849 | CONFIRMED |
| anti-orphaning checklist bullet | 1969 | 1969 | CONFIRMED |
| `TB-Add-8` (last TB-Add bullet) | 1979 | 1979 | CONFIRMED |
| `## Phase N: [Final Phase …]` | 1928 | 1928 | CONFIRMED |
| `**N.X — Update task status to Done**` | 1930 | 1930 | CONFIRMED |

**S4 trim grep confirmation (edit-site 11):** `blockedBy` = 0 hits; `depends_on` = 0 hits; `TCS`/`Tasklist
Complexity` = 0 hits; `after Phase` = 1 hit at **L1993** (the Content-Rules cell `| Phase dependencies |
Explicit ordering: "after Phase N completes" | …` — unrelated, must remain untouched). The new TCS section
is 100% NEW content; no existing TCS anchor to edit. S4 trim target `{after Phase \d+, depends_on:}` is safe.

---

## sc-tasklist-protocol/SKILL.md (1491 lines — matches research 02)

| Anchor | Research line | Live grep | Status |
|---|---|---|---|
| `### Stage 7: Roadmap Validation (2N Parallel Agents)` | 1174 | 1174 | CONFIRMED |
| `### Stage 9: Patch Execution …` | 1339 | 1339 | CONFIRMED |
| `### Stage 10: Spot-Check Verification` | 1359 | 1359 | CONFIRMED |
| "executes in 10 stages" lead sentence | 1392 | 1392 | CONFIRMED |
| Stage table row `| 9 | Patch Execution` | 1404 | 1404 | CONFIRMED |
| Stage table row `| 10 | Spot-Check Verification` | 1405 | 1405 | CONFIRMED |
| Self-Check `6.` (per checks 18-20) | 1073 | 1073 | CONFIRMED |
| structural check `| 18 |` | 1113 | 1113 | CONFIRMED |
| structural gate `| 19 |` (no regular task following) | 1114 | 1114 | CONFIRMED |
| structural gate `| 20 |` (Checkpoint Report Path) | 1115 | 1115 | CONFIRMED |
| gate close-line "If any check 1-20 fails" | 1117 | 1117 | CONFIRMED |
| `### 4.8 Checkpoints (Exact Cadence)` | 343 | 343 | CONFIRMED |
| cadence rule "No regular task may appear after…" | 359 | 359 | CONFIRMED |
| `#### End-of-Phase Checkpoint (Mandatory, Last Task)` | 1011 | 1011 | CONFIRMED |
| template "No task may appear below it." | 1021 | 1021 | CONFIRMED |
| `### File Emission Rules (Deterministic)` | 91 | 91 | CONFIRMED |
| phase-file content contract ("inline checkpoints, end-of-phase checkpoint") | 96 | 96 | CONFIRMED |
| `#### Target Directory Layout` | ~106-123 | 106 | CONFIRMED |
| intended-locations "Validation reports: TASKLIST_ROOT/validation/" | 87 | 87 | CONFIRMED |
| index "Artifact Paths" Validation Reports row | 700 | 700 | CONFIRMED |
| `**Dependency chain** (Stages 7-10):` PROSE block | 1415 | 1415 | CONFIRMED |
| "- Stage 10 is blocked by Stage 9" (prose) | 1420 | 1420 | CONFIRMED |
| "create 10 tasks via TaskCreate" | 1424 | 1424 | CONFIRMED |
| "Stage 10: blockedBy Stage 9" (TaskCreate Deps) | 1449 | 1449 | CONFIRMED |
| completion line "Stage 10: \"Spot-Check…\"" | 1462 | 1462 | CONFIRMED |
| Tool Usage `| `Task` (Agent) |` row | 1479 | 1479 | CONFIRMED |
| `argument-hint:` frontmatter | 9 | 9 | CONFIRMED |
| `#### Phase Files Table` (index inline §6A) | 703 | 703 | CONFIRMED |
| `| Total Tasks |` (index metadata) | 682 | 682 | CONFIRMED |

---

## commands/tasklist.md (118 lines — matches research 03)

| Anchor | Research line | Live grep | Status |
|---|---|---|---|
| `## Usage` | 20 | 20 | CONFIRMED |
| Usage line `/sc:tasklist <roadmap-path> [--spec …] [--output …]` | 23 | 23 | CONFIRMED |
| `## Arguments` | 32 | 32 | CONFIRMED |
| `--spec <spec-path>` row (ALREADY EXISTS — do NOT re-add) | 37 | 37 | CONFIRMED |
| `--output <output-dir>` row (insert --no-reflect after) | 38 | 38 | CONFIRMED |
| `argument-hint:` key | ABSENT | 0 hits | CONFIRMED ABSENT |

---

## templates/phase-template.md (125 lines — research said 126; off-by-1, negligible)

| Anchor | Research line | Live grep | Status |
|---|---|---|---|
| read-only-mirror notice | 3-4 | 3 | CONFIRMED |
| `## End-of-Phase Checkpoint (Mandatory)` | 117 | 117 | CONFIRMED |
| "Every phase file MUST end with:" | 119 | 119 | CONFIRMED |
| `### Checkpoint: End of Phase <N>` | 122 | 122 | CONFIRMED |

## templates/index-template.md (140 lines — research said 141; off-by-1, negligible)

| Anchor | Research line | Live grep | Status |
|---|---|---|---|
| read-only-mirror notice | 3-4 | 3 | CONFIRMED |
| `| Total Deliverables |` | 29 | 29 | CONFIRMED |
| `| Complexity Class |` | 30 | 30 | CONFIRMED |
| `| Validation Reports |` (artifact paths) | 46 | 46 | CONFIRMED |
| Phase Files table header (5 cols) | 53 | 53 | CONFIRMED |

---

## Consequence for Phase 2/3

No anchor adjustments required — all research-01/02/03 line numbers and content anchors hold against the
live tree. The Phase 2/3 edit items may proceed using the research anchors verbatim. The only deviations
worth noting are the two template files being 1 line shorter than research recorded (immaterial — those
edits target file-tail content located by heading, not by absolute line number).
