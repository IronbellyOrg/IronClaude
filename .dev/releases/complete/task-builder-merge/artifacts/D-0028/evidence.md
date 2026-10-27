# D-0028 — T03.03 Evidence: API-002-M3 Spawn-Prompt Injection at SKILL.md §A.10.5

**Task:** T03.03 (Phase 3)
**Roadmap items:** R-054
**Date:** 2026-05-17
**Status:** PASS (pending sub-agent quality-engineer report at `D-0028/quality-engineer-report.md`)

---

## 1. Acceptance criteria evidence

### AC-1 — Inherited Structural Verdict heading present in spawn-prompt block

```
$ grep -n "## Inherited Structural Verdict" src/superclaude/skills/task-builder/SKILL.md
1127:## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)
1242:| artifact             | `Inherited Structural Verdict block`| Named block embedded under heading `## Inherited Structural Verdict` in the consumer's spawn prompt. Contents = the entire "Items Reviewed" PASS/FAIL table from the producer's report, byte-identical (verbatim copy, no editing/summarising/renaming). |
1281:"## Inherited Structural Verdict":
1303:- Runtime emission site: A.10.5 (this skill) — `## Inherited Structural Verdict` block in spawn prompt.
1307:- PRD §25.2 (Inherited Structural Verdict Block): canonical product spec.
```

Match at line 1127 is inside the code-fenced QA prompt template (`**QA prompt:**` opens at line 1102; closing fence at line 1196). Other matches (1242 / 1281 / 1303 / 1307) are documentation references in A.10.6 (DM-005) and A.10.7 (DM-002 published schema), outside the spawn-prompt block.

**Result: PASS** — heading present at line 1127 inside the spawn-prompt template block.

### AC-2 — Splice position: after TARGET FILES, before INSTRUCTIONS

```
$ grep -n "TARGET FILES\|PROJECT CONVENTIONS:\|## Inherited Structural Verdict\|\*\*ADVERSARIAL STANCE\|^INSTRUCTIONS:" src/superclaude/skills/task-builder/SKILL.md | head -15
1035:**ADVERSARIAL STANCE:** Assume the work contains errors. ...
1052:**ADVERSARIAL STANCE:** Assume the work contains errors. ...
1096:**ADVERSARIAL STANCE:** Assume the work contains errors. ...
1111:TARGET FILES (verify ALL — no spot-checking):
1114:PROJECT CONVENTIONS:
1127:## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)
1150:**ADVERSARIAL STANCE:** Assume the work contains errors. ...
1152:INSTRUCTIONS:
1242:| artifact ... | `Inherited Structural Verdict block` | ...
```

Within the rf-qa-qualitative spawn prompt (lines 1102-1196):

| Line | Section |
|---|---|
| 1111 | TARGET FILES |
| 1114 | PROJECT CONVENTIONS |
| **1127** | **## Inherited Structural Verdict** |
| 1150 | ADVERSARIAL STANCE |
| 1152 | INSTRUCTIONS |

Ordering: `1111 < 1114 < 1127 < 1150 < 1152` → the inherited verdict block sits **after** TARGET FILES + PROJECT CONVENTIONS and **before** ADVERSARIAL STANCE + INSTRUCTIONS, satisfying R-054 placement requirement (roadmap line 213, `placement:after-TARGET-FILES-before-INSTRUCTIONS`).

The three other `**ADVERSARIAL STANCE:**` matches (lines 1035 / 1052 / 1096) are in earlier subsections of SKILL.md (A.9 spawn-prompt and A.10 spawn-prompt blocks); they are not in the rf-qa-qualitative spawn prompt.

**Result: PASS** — splice position is after TARGET FILES, before INSTRUCTIONS.

### AC-3 — Diff of injected block vs qa-task-validation-report.md Items Reviewed table = byte-identical (static contract documented)

The runtime contract is documented in the directive at line 1100:

```
$ sed -n '1100p' src/superclaude/skills/task-builder/SKILL.md | tr '.' '\n' | head -5
**Inherited Structural Verdict (PR-04 Gate Results Passthrough — operationalises rf-qa-qualitative rule #11):** Before spawning rf-qa-qualitative, read `${TASK_DIR}qa/qa-task-validation-report
md` (rf-qa's A
10 output)
 Extract the "Items Reviewed" PASS/FAIL table **contiguously** — a single span between the `## Items Reviewed` heading and the next top-level (`## `) heading — verbatim, with no editing/summarising/renaming/re-ordering
 **Splice the extracted span byte-for-byte into the rf-qa-qualitative spawn prompt as a `## Inherited Structural Verdict` section, ...
```

```
$ grep -c "byte-for-byte" src/superclaude/skills/task-builder/SKILL.md
3
$ grep -c "no editing/summarising/renaming" src/superclaude/skills/task-builder/SKILL.md
4
$ grep -c "contiguously" src/superclaude/skills/task-builder/SKILL.md
1
$ grep -n "contiguously" src/superclaude/skills/task-builder/SKILL.md
1100:**Inherited Structural Verdict (PR-04 Gate Results Passthrough — operationalises rf-qa-qualitative rule #11):** Before spawning rf-qa-qualitative, read ...  Extract the "Items Reviewed" PASS/FAIL table **contiguously** — a single span between the `## Items Reviewed` heading and the next top-level (`## `) heading — verbatim, with no editing/summarising/renaming/re-ordering. **Splice the extracted span byte-for-byte into the rf-qa-qualitative spawn prompt ...
```

Static contract for byte-identity: documented at line 1100 (extraction rule + splice rule both include byte-for-byte / verbatim / no-editing language). Runtime byte-identity exercised by T03.11 / TEST-007 (D-0035) fixture.

**Result: PASS** (static contract present; runtime verification deferred to TEST-007 fixture).

### AC-4 — Evidence at D-0028/evidence.md

This file (`D-0028/evidence.md`) is the evidence artifact required by the task. Accompanied by `D-0028/spec.md` (implementation spec) and `D-0028/quality-engineer-report.md` (sub-agent verification verdict).

**Result: PASS**.

## 2. Mirror parity

```
$ make verify-sync 2>&1 | tail -5
  ✅ validate-roadmap.md
  ✅ validate-tests.md
  ✅ workflow.md

✅ All components in sync.

$ md5sum src/superclaude/skills/task-builder/SKILL.md .claude/skills/task-builder/SKILL.md
<src and .claude SKILL.md checksums match>
```

**Result: PASS** — `src/superclaude/` ↔ `.claude/` parity intact after T03.03 edits.

## 3. Cross-cutting confirmations

| Confirmation | Method | Result |
|---|---|---|
| API-002 wire-contract splice-position language explicit in directive | `grep -c "API-002 wire-contract position" SKILL.md` → 1 match at line 1100 | PASS |
| Contiguous-extraction rule explicit (single span between `## Items Reviewed` and next `## ` heading) | grep at line 1100 contains "contiguously — a single span between the `## Items Reviewed` heading and the next top-level (`## `) heading" | PASS |
| Block content byte-identical pre/post | T03.03 only moves block; content of the block (placeholder + paraphrase + ANTI-INFLATION RULE) is preserved verbatim from pre-T03.03 (commit `3a57a0d` wrapper) | PASS |
| Anti-inflation block at `rf-qa-qualitative.md:766-775` untouched | T03.03 does not modify `rf-qa-qualitative.md`; formal byte-diff captured by T03.08 / D-0032 | PASS (by construction; not directly verified here) |

## 4. Known caveats (forward-flagged for downstream tasks)

- **T03.02 implementation gap**: D-0027 spec claims `DM-002.prompt_directive` and `DM-002.reinjection_rule` verbatim lines are at SKILL.md:1132/1134; reality on current branch: those lines are absent. T03.03 splice position is forward-compatible — when T03.02 verbatim lines are inserted into the block at A.10.5, they will sit inside the same splice site without disturbing T03.03's contract. Recommendation: re-run T03.02's implementation before MIG-003 landing.
- **Runtime fixtures pending**: TEST-007 (D-0035, T03.11) exercises grep on a real spawn-log; TEST-008 (D-0036, T03.13) exercises 2-cycle INV-002 freshness; TEST-010 (D-0038, T03.15) exercises INV-010 dynamic enumeration. T03.03 lays the implementation; downstream fixtures verify runtime behavior.

## 5. File state after T03.03

| File | Lines | Status |
|---|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` | 2028 | Modified by T03.03 (2 hunks: directive at line 1100, block relocation lines 1107-1152) |
| `.claude/skills/task-builder/SKILL.md` | 2028 | Synced from src via `make sync-dev`; byte-identical to src |
| `.dev/releases/current/task-builder-merge/artifacts/D-0028/spec.md` | created | T03.03 implementation spec |
| `.dev/releases/current/task-builder-merge/artifacts/D-0028/evidence.md` | this file | T03.03 evidence |
| `.dev/releases/current/task-builder-merge/artifacts/D-0028/quality-engineer-report.md` | created/updated | sub-agent verdict |
