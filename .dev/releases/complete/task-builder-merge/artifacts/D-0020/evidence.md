# D-0020 — Evidence (T02.05 Degradation Rule + Hidden-Input Guard)

**Status:** PASS
**Task:** T02.05 — Wire degradation rule + hidden-input guard
**Roadmap rows:** R-038 (Degradation rule), R-039 (Hidden-input guard)
**Implementation surfaces:**
- `src/superclaude/skills/task-builder/SKILL.md:942–973` — R-038 "Degradation rule" + R-039 "Header-wide hidden-input guard" paragraphs (replaces prior compact degradation note)
- `src/superclaude/agents/rf-qa.md:308` — TB-Add-7 extended with `tb-add-7-degraded-tolerated` verdict + consumer-side R-039 spot check
**Minimal-fixture artifact:** `artifacts/D-0020/sample-minimal-buildrequest.md` (block range = lines 41..47)
**Fully-populated regression artifact:** `artifacts/D-0017/sample-emitter-output.md` (block range = lines 39..47)
**Generated:** 2026-05-17

---

## 1. Sync Verification

```
$ make sync-dev
✅ Sync complete.
   Skills:   20 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    11 files

$ make verify-sync
✅ All components in sync.
```

Both `src/superclaude/{skills,agents,commands}` and `.claude/` mirrors are byte-identical after the T02.05 edits to `SKILL.md` and `rf-qa.md`.

## 2. Acceptance Criterion AC1 — Minimal fixture renders References-only; Source areas + Key constraints absent

**Block range:** lines 41..47 of `artifacts/D-0020/sample-minimal-buildrequest.md` (`^## Execution Context$` through the next `^---$`).

**Rendered block (verbatim from fixture):**

```markdown
## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-001: Wire the minimal-BUILD_REQUEST degradation sample so the References-only form is rendered with Source areas and Key constraints bullets absent (not blank).

---
```

**Absence assertions (R-038):**

```
$ sed -n '41,47p' artifacts/D-0020/sample-minimal-buildrequest.md | grep -c "Source areas:"
0
$ sed -n '41,47p' artifacts/D-0020/sample-minimal-buildrequest.md | grep -c "Key constraints:"
0
$ sed -n '41,47p' artifacts/D-0020/sample-minimal-buildrequest.md | grep -c "References:"
1
```

**Result:** **PASS** — Source areas and Key constraints bullets are physically absent (count = 0), not blank-but-present. References bullet is present (count = 1) with a `R-001:` ordinal derived from the GOAL field per the T02.02 emitter rule (`SKILL.md:898–907`). The `## Execution Context` heading and the `<!-- OPTIONAL header -->` reader-aid comment are retained per the R-038 "what stays" clause.

## 3. Acceptance Criterion AC2 — `grep -cE "src/|/.*:[0-9]+"` returns 0 on the minimal-fixture block range (R-039)

```
$ sed -n '41,47p' artifacts/D-0020/sample-minimal-buildrequest.md | grep -cE 'src/|/.*:[0-9]+'
0
```

**Result:** **PASS** — 0 hits. The R-039 header-wide hidden-input guard is satisfied on the degraded form.

**Regression coverage — fully-populated block (T02.02 fixture):**

```
$ sed -n '39,47p' artifacts/D-0017/sample-emitter-output.md | grep -cE 'src/|/.*:[0-9]+'
0
```

**Result:** **PASS** — 0 hits on the fully-populated form as well. R-039 is strictly additive: the post-assembly scan is uniform across both emission paths and does not regress any prior PASS.

## 4. Acceptance Criterion AC3 — TB-Add-7 tolerates the degraded form (D-0015 integration)

**Updated rule text** at `src/superclaude/agents/rf-qa.md:308`:

```
27. TB-Add-7: Execution Context source areas reappear in items (cross-validation
    for PR-01 header). If the task file contains an ## Execution Context block
    with a **Source areas:** line, every named source area MUST reappear in at
    least one item's Context field. ... Degraded-form tolerance (R-038, DM-001
    v1.0.0): if the block is present but the **Source areas:** line is absent
    (References-only degraded form on minimal BUILD_REQUEST), the
    cross-validation has no source-area set to check — this is the intended
    degradation, NOT a drift signal. Emit verdict tb-add-7-degraded-tolerated
    and do NOT FAIL. ... The header-wide hidden-input guard (R-039) is the
    producer-side enforcement; TB-Add-7 may additionally re-run
    grep -cE "src/|/.*:[0-9]+" against the block range as a consumer-side spot
    check, FAILing if count > 0.
```

**Verdict simulation against the minimal fixture:**

| Input to TB-Add-7 | Detection | Verdict |
|---|---|---|
| `## Execution Context` heading present | YES (block exists; check is ACTIVE per the "heading absent" inactive clause) | check runs |
| `**Source areas:**` line present | NO (R-038 degraded form — bullet absent) | enter degraded-form branch |
| Cross-validation set (source areas to check against items) | empty | nothing to cross-validate |
| Producer-side R-039 grep | 0 hits | consumer-side spot check optional; also 0 |
| **Final verdict** | — | **`tb-add-7-degraded-tolerated`** (NOT FAIL) |

**Result:** **PASS** — the updated TB-Add-7 paragraph names the `tb-add-7-degraded-tolerated` verdict explicitly and forbids FAIL on the References-only form. The deliverable "TB-Add-7 (M1) cross-validator integration verified" (phase-2-tasklist.md L232) is met.

## 5. Implementation Verification — R-038 + R-039 paragraphs present in SKILL.md

```
$ grep -n "Degradation rule (R-038\|Header-wide hidden-input guard (R-039" \
    src/superclaude/skills/task-builder/SKILL.md
942:    Degradation rule (R-038 — minimal BUILD_REQUEST → References-only):
956:    Header-wide hidden-input guard (R-039 — NFR-CONV.3 enforcement at the
```

Both named rules are present in the spawn-prompt body adjacent to the per-emitter rules from T02.02 (`SKILL.md:898–932`).

## 6. Implementation Verification — TB-Add-7 degraded-form tolerance present in rf-qa.md

```
$ grep -n "tb-add-7-degraded-tolerated\|Degraded-form tolerance (R-038" \
    src/superclaude/agents/rf-qa.md
308:27. **TB-Add-7: Execution Context source areas reappear in items
    (cross-validation for PR-01 header).** ... **Degraded-form tolerance
    (R-038, DM-001 v1.0.0):** ... Emit verdict `tb-add-7-degraded-tolerated`
    and do NOT FAIL. ...
```

The verdict identifier and the R-038 cross-reference are both present in the TB-Add-7 paragraph.

## 7. Acceptance Summary

| AC | Criterion | Status | Reference |
|---|---|---|---|
| AC1 | Minimal fixture renders References-only; Source areas + Key constraints absent (not blank) | **PASS** | § 2 |
| AC2 | `grep -cE "src/|/.*:[0-9]+" <header-range>` returns 0 on minimal fixture | **PASS** | § 3 |
| AC3 | TB-Add-7 cross-validator tolerates the degraded form (no FAIL) | **PASS** | § 4 |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0020/evidence.md` | **PASS** | this file |

**Overall: PASS** — all four T02.05 acceptance criteria met. Dependencies for T02.06 (mid-phase checkpoint) are now satisfied: T02.01..T02.05 all PASS with evidence artifacts at D-0016..D-0020.

## 8. Notes

- **Strict-additivity of R-039 verified.** The header-wide grep returns 0 on both the minimal (lines 41..47 of `sample-minimal-buildrequest.md`) and fully-populated (lines 39..47 of `sample-emitter-output.md`) fixtures. R-039 does not regress any prior PASS — it is a boundary check that strengthens NFR-CONV.3 enforcement without altering the emission rules from T02.02.
- **One-rewrite-cycle policy + `header-leak-suppressed` annotation.** The R-039 paragraph specifies that on a grep hit, the builder rewrites the offending bullet, re-assembles, and re-scans once. If the second scan still hits, the entire block is omitted and a `header-leak-suppressed` annotation is added to the builder's return value. This bounds the rewrite cost (no infinite loop) and surfaces the failure mode to the orchestrator without crashing the build.
- **TB-Add-7 consumer-side spot check is optional, not required.** The R-039 grep is producer-side primary enforcement. The TB-Add-7 paragraph notes the consumer-side re-run as a defense-in-depth option ("may additionally re-run"). This pattern matches the M1 producer/consumer split where rf-qa is the cross-validator, not the primary author.
- **Per-item Context preservation (CASE-D PR-01) unchanged.** The R-038 / R-039 changes apply ONLY to the `## Execution Context` block range. Per-item `**Context**:` fields retain `file:line` citations and remain enforced by TB-Add-8. The scope-confinement rule at `SKILL.md:934–940` is unchanged.
- **DM-001 wire ABI v1.0.0 unchanged.** R-038 / R-039 are derivation rules over the same DM-001 fields frozen at T01.13 (D-0011 § 1). No schema field is added, removed, or renamed.
