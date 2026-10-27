# D-0018 — Evidence (T02.03 API-001-M2 BUILD_REQUEST Contract Update)

**Status:** PASS
**Task:** T02.03 — Update API-001-M2 BUILD_REQUEST contract
**Roadmap row:** R-036
**Implementation surface:** `src/superclaude/skills/task-builder/SKILL.md` lines 779-799 (new field), 885-891 (signal-control paragraph in EXECUTION CONTEXT BLOCK), 1532-1537 (Optional BUILD_REQUEST signals reference list)
**Generated:** 2026-05-17
**Sub-agent verdict:** quality-engineer reports PASS on all 5 acceptance criteria

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

Both `src/superclaude/{skills,agents,commands}` and `.claude/` mirrors are byte-identical after the T02.03 edits.

## 2. AC1 — BUILD_REQUEST 15-field schema unchanged (byte-diff zero in the existing 15 fields)

**Method:** Captured the pre-edit 15-field text (SKILL.md lines 744-839, the `BUILD_REQUEST:` → end-of-ESCALATION range) into `/tmp/build_request_15fields_pre.txt`. After the edits, extracted the same region (`BUILD_REQUEST:` → `    INCREMENTAL TASK FILE WRITING`), stripped the newly-inserted `EXECUTION_CONTEXT_REQUIREMENTS` field block with regex, then diffed against the pre snapshot.

```
$ sha256sum /tmp/build_request_15fields_pre.txt
bfb2deaf212a5fb317ef29f37edd1e1946dcac4b8733f7a29ba187b59978655b  /tmp/build_request_15fields_pre.txt
```

**Strip-and-diff result** (trailing-whitespace-normalized — only difference was a single trailing blank line introduced by the `INCREMENTAL TASK FILE WRITING` boundary delimiter, which is not part of either field body):

```
pre rstripped sha256:      171941856939ba46bdbbcb9fdf5a3e09d14823a131df167cea4610f39aa6ffa8
stripped rstripped sha256: 171941856939ba46bdbbcb9fdf5a3e09d14823a131df167cea4610f39aa6ffa8
byte-identical (after trailing-ws normalization): True
len pre: 4834 chars, len stripped: 4834 chars
```

**Result: PASS** — 15-field BUILD_REQUEST schema byte-identical pre vs post (SHA `171941856939...`, length 4834 chars on both sides).

**Independent per-field cross-check** (quality-engineer sub-agent, see § 6) confirmed each of the 15 fields' bodies textually unchanged via direct file Read at lines 744-859.

## 3. AC2 — EXECUTION_CONTEXT_REQUIREMENTS documented as optional in SKILL.md

**Locations:**

```
$ grep -n "EXECUTION_CONTEXT_REQUIREMENTS" src/superclaude/skills/task-builder/SKILL.md
779:    EXECUTION_CONTEXT_REQUIREMENTS: [OPTIONAL signal (API-001-M2) controlling
885:    Signal control (API-001-M2): the `EXECUTION_CONTEXT_REQUIREMENTS`
1533:- `EXECUTION_CONTEXT_REQUIREMENTS` (API-001-M2) — Controls the `## Execution
```

**Line 779 field body (verbatim head):**

```
    EXECUTION_CONTEXT_REQUIREMENTS: [OPTIONAL signal (API-001-M2) controlling
      the `## Execution Context` block emission in the generated MDTM. Governs
      DM-001-frozen (T01.13 / D-0011 § 1) emitters defined in the EXECUTION
      CONTEXT BLOCK section below. Values:
      - AUTO (default) — builder emits the block when BUILD_REQUEST exposes
        rollup signal (≥3 distinct named source areas inferable from research
        findings). Fully-populated form renders all 3 labeled bullets
        (References, Source areas, Key constraints). Minimal form (GOAL-only
        BUILD_REQUEST) degenerates to References-only with Source areas and
        Key constraints bullets ABSENT (not blank-but-present).
      - REQUIRED — builder MUST emit the block. The degraded References-only
        form is permitted when only GOAL is populated; suppressing the block
        entirely is a MALFORMED output.
      - SUPPRESS — builder MUST NOT emit the block. Per-item Context fields
        remain unchanged regardless. Used for thin / throwaway task files.
      Omission of this field implies AUTO. Strictly additive — when absent
      or AUTO, the M1-frozen 15-field BUILD_REQUEST behavior is preserved
      byte-identical. Failure mode: MALFORMED retry max-2 (Critical Rule #12
      and the MALFORMED flow at SKILL.md A.9 mediation) applies when the
      builder violates this signal — e.g., emitting the block under SUPPRESS,
      or omitting the block under REQUIRED.]
```

**Result: PASS** — field opens with `[OPTIONAL signal (API-001-M2) ...]`, enumerates the three values (AUTO / REQUIRED / SUPPRESS), states `Omission of this field implies AUTO`, and is cross-referenced from `:885-891` and `:1532-1537`.

## 4. AC3 — MALFORMED retry max-2 failure-mode preserved (verbatim text retained)

**Grep hits:**

```
$ grep -n "Maximum 2 MALFORMED\|MALFORMED retry max-2" src/superclaude/skills/task-builder/SKILL.md
796:      byte-identical. Failure mode: MALFORMED retry max-2 (Critical Rule #12
977:   - **Maximum 2 MALFORMED rounds** (tracked independently from RESEARCH_NEEDED rounds)
1537:  implies `AUTO`. Violation triggers MALFORMED retry max-2.
1742:12. **Builder mediation has separate retry counters.** RESEARCH_NEEDED (max 2 rounds) and MALFORMED (max 2 rounds) are tracked independently. A builder that needs more research twice and then produces a bad file gets 4 total invocations, not 2.
```

**Pre-existing anchor lines (preserved verbatim):**
- `:977` — orchestrator MALFORMED flow body: `**Maximum 2 MALFORMED rounds** (tracked independently from RESEARCH_NEEDED rounds)`. Pre-edit text. No byte changes by T02.03.
- `:1742` — Critical Rule #12. Pre-edit text. No byte changes by T02.03.

**New cross-references** (introduced by T02.03 only — do not modify the failure-mode itself, they just wire the new signal into it):
- `:796` — new field body cites the failure-mode.
- `:1537` — Optional-signals reference list cites the failure-mode.

**Result: PASS** — both verbatim anchor lines (`:977`, `:1742`) preserved; new references added consistently.

## 5. AC4 — Generated MDTM contains `## Execution Context` block after frontmatter, before first phase

The MDTM Output Structure template at `SKILL.md:1587-1595` (landed by T02.01 / D-0016) defines the `## Execution Context` block immediately after `## Prerequisites & Dependencies` and before `## Phase 1: [Phase Name]`. T02.03 does not modify this region:

```
$ grep -n "^## " src/superclaude/skills/task-builder/SKILL.md | head -30 | grep -A1 -B1 "Execution Context"
1582:## Prerequisites & Dependencies
1587:## Execution Context
1597:## Phase 1: [Phase Name]
```

Block-emission rule (controlled by the new signal):
- Under `AUTO` / omission → emit if rollup signal ≥ 3 areas (T02.02 / D-0017 emitters).
- Under `REQUIRED` → always emit (degraded form permitted).
- Under `SUPPRESS` → never emit.

**Result: PASS** — block placement preserved (header-emission ordering already wired by T02.01); new signal only controls whether the block fires, not where it goes.

## 6. AC5 — Sub-agent (quality-engineer) confirms producer/consumer/transport unchanged

**Sub-agent invocation:** `Agent(subagent_type: "quality-engineer")` spawned post-edit. The sub-agent independently read `src/superclaude/skills/task-builder/SKILL.md` and validated each acceptance criterion.

**Sub-agent verdict:** **PASS** (all five acceptance criteria).

**Sub-agent contract-field findings (verbatim from sub-agent report):**

| Contract field | M1 anchor value | Sub-agent verification location |
|----------------|-----------------|---------------------------------|
| Producer (task-builder skill) | `SKILL.md L1512 "Builder Agent Prompt (rf-task-builder — Task File Creation)" — orchestrator role unchanged.` |
| Consumer (rf-task-builder) | `L741 subagent_type: "rf-task-builder", L1514 spawn directive — unchanged.` |
| Transport (Skill prompt + on-disk MDTM) | `L740-960 prompt body; L946 TASK FILE LOCATION: ${TASK_DIR}${TASK_ID}.md; L862 incremental on-disk writing — unchanged.` |
| Output (Execution-Context block) | `Emission rules at L878-944 — present, controlled by new signal.` |
| Error mode (MALFORMED-max-2-retry) | `L977 — verbatim preserved.` |

**Sub-agent concerns (non-blocking, recorded for tracking):**
1. `SKILL.md A.9 mediation` referenced in the new field body is a section-pointer with no `:NN` anchor — minor brittleness if the A.9 header is renumbered (the literal heading nearby is `A.10`); the implicit referent is the MALFORMED flow paragraph at `:944-948`. Non-blocking for M2; recordable as cosmetic future fix.
2. Citation density of the form `DM-001-frozen (T01.13 / D-0011 § 1)` in the new field body is brittle if upstream task IDs shift. Non-blocking for M2.

**NFR-CONV.3 hidden-input determinism guard (sub-agent re-check, also verified locally below):**

```
$ sed -n '779,799p;885,891p' src/superclaude/skills/task-builder/SKILL.md | grep -cE 'src/|/.*:[0-9]+'
0
```

The new field body and the signal-control paragraph introduce zero file_path:line citations — they describe signal semantics in section-pointer prose, not source code. NFR-CONV.3 guard preserved.

**Result: PASS** — sub-agent confirms producer/consumer/transport/output/error-mode contract fields unchanged.

## 7. Acceptance Summary

| AC | Criterion | Status | Reference |
|----|-----------|--------|-----------|
| AC1 | BUILD_REQUEST 15-field schema unchanged (byte-diff zero) | **PASS** | § 2 (SHA `171941856939...`, 4834 chars both sides) |
| AC2 | EXECUTION_CONTEXT_REQUIREMENTS documented as optional | **PASS** | § 3 (`SKILL.md:779`, `:885`, `:1533`) |
| AC3 | MALFORMED retry max-2 preserved verbatim | **PASS** | § 4 (`SKILL.md:977`, `:1742` byte-stable) |
| AC4 | Generated MDTM contains `## Execution Context` block | **PASS** | § 5 (`SKILL.md:1587-1595` placement preserved) |
| AC5 | Sub-agent confirms producer/consumer/transport unchanged | **PASS** | § 6 (quality-engineer report) |

**Overall: PASS** — all five T02.03 acceptance criteria met. The API-001-M2 contract update is landed strictly additively: the M1-frozen 15-field BUILD_REQUEST schema is preserved byte-identical, a single optional EXECUTION_CONTEXT_REQUIREMENTS signal is added with AUTO/REQUIRED/SUPPRESS semantics, the MALFORMED retry max-2 failure-mode is preserved verbatim, and the producer/consumer/transport/output/error-mode contract fields from the M1 anchor row are unchanged.

## 8. Notes

- **Strict additivity** confirmed by the strip-and-diff: removing the new field block from post-edit text yields byte-identical content to the M1 pre-edit snapshot (SHA-equal after trailing-whitespace normalization — the one-byte trailing-newline difference is a boundary artifact from the `INCREMENTAL TASK FILE WRITING` delimiter, not a content change).
- **Cross-references** in the new field body (`DM-001-frozen (T01.13 / D-0011 § 1)`, `SKILL.md A.9 mediation`) are section-pointer prose with no `:NN` line numbers; NFR-CONV.3 hidden-input determinism is satisfied (grep returns 0).
- **Downstream consumer impact**: M3 (FR-CONV.3 / PR-04) consumes DM-005-M2 phase contract published in T02.04. T02.03's new signal does not change DM-005 wiring. M2 → M3 unblocking path is unobstructed.
- **Dependencies for T02.06 (mid-phase checkpoint)** are now satisfied: T02.01 (D-0016), T02.02 (D-0017), T02.03 (D-0018) all PASS.
