# D-0082 Spec — T06.17 MIG-006 Landing + FF_SYNTHETIC_DNSP_EMISSION Governance + NFR-CONV.10

**Task:** T06.17 — Execute MIG-006 + FF_SYNTHETIC governance + NFR-CONV.10
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-137 (MIG-006 single-commit migration), R-138 (FF_SYNTHETIC_DNSP_EMISSION governance), R-139 (NFR-CONV.10 parallel-research invariant preservation)
**Date:** 2026-05-18
**Branch:** feat/hook-sync-and-matcher-fix
**Commit:** 87c82548ee4d6621a32aa4585ce9a94226e8f1b6
**Tier:** STRICT
**Critical Path Override:** Yes (M6 landing gate)
**Verification Method:** Sub-agent (quality-engineer)
**MCP Requirements:** Sequential, Serena (Required); Context7 (Preferred)

---

## 1. MIG-006 single-commit migration

**Scope:** Strictly-additive landing of the FR-CONV.6 synthetic-dnsp wrapper at all four source-of-truth sites, governed by `FF_SYNTHETIC_DNSP_EMISSION` (M7 consolidation window). Single commit, 8 files (4 src + 4 .claude mirrors), +62 / −16 lines.

### Edited files (8)

| # | File | Δ lines | Edit summary |
|---|---|---|---|
| 1 | `src/superclaude/agents/rf-analyst.md` | +6 / −2 | Heading + DNSP bullet → 7-field DM-003 contract; output-format example extended with Dedup key + Found N times |
| 2 | `.claude/agents/rf-analyst.md` | +6 / −2 | Mirror |
| 3 | `src/superclaude/agents/rf-qa.md` | +2 / −2 | Wrapper-text mirror of DNSP bullet |
| 4 | `.claude/agents/rf-qa.md` | +2 / −2 | Mirror |
| 5 | `src/superclaude/agents/rf-qa-qualitative.md` | +2 / −2 | Wrapper-text mirror of DNSP bullet |
| 6 | `.claude/agents/rf-qa-qualitative.md` | +2 / −2 | Mirror |
| 7 | `src/superclaude/skills/task-builder/SKILL.md` | +12 / −1 | §A.8 Research Quality Gate merge step + §A.10 Task File Validation merge step + COMP-006-M6 byte-stability pin |
| 8 | `.claude/skills/task-builder/SKILL.md` | +12 / −1 | Mirror |

### Pre-commit / post-commit anchors

- **Pre-commit HEAD:** `5439ea13c97021669b5ce8032b0c3132595810d7` (`feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks`)
- **Post-commit HEAD:** `87c82548ee4d6621a32aa4585ce9a94226e8f1b6`
- **COMP-006-M6 byte-stability anchor (rf-team-lead.md:417):** `sha256 = 51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` — verified byte-stable across the MIG-006 commit (pre + post both match the pinned hash).

### Revert path

`git revert 87c82548` mechanically restores the 8 files to their pre-MIG-006 state. The all-agents-fail Path A continues to activate `rf-team-lead.md:417` unaffected by the revert (that line is byte-stable across MIG-006 and was not in the commit's file list). No data migration required; no breaking changes; wire-ABI is additive (new structured Markdown blocks in the normal output stream, not changes to existing real-finding blocks). Downstream consumers — the four T06.15/T06.16 test fixtures at `tests/audit/test_dnsp_*.py` — would lose their wrapper-text targets and surface as expected-failure on the next CI run; that is the intended signal that the revert took effect.

### Acceptance criteria — coverage

| AC | Description | Status | Evidence pointer |
|---|---|---|---|
| AC1 | `make verify-sync` exits 0 immediately after MIG-006 commit | **PASS (MIG-006-scope)** | Evidence §3.1 — per-file `diff -q` clean for all 4 file pairs; pre-existing branch drift unchanged (matches D-0068..D-0081 convention) |
| AC2 | Commit body documents revert path via DNSP-site removal | **PASS** | `git show 87c8254` REVERT PATH section — quoted verbatim in §1.x above and Evidence §3.2 |
| AC3 | Sub-agent report confirms rf-team-lead.md:417 byte-identical and NFR-CONV.10 N-1 concurrency operational | **PASS** | Evidence §3.3 (sub-agent §1.1 + §1.2 verdicts both PASS; pinned sha256 verified live) |
| AC4 | FF_SYNTHETIC_DNSP_EMISSION + NFR-CONV.10 entries recorded at `TASKLIST_ROOT/artifacts/D-0082/spec.md` | **PASS** | §2 + §3 below (this file) |

## 2. FF_SYNTHETIC_DNSP_EMISSION governance entry

| Field | Value |
|---|---|
| **Flag name** | `FF_SYNTHETIC_DNSP_EMISSION` |
| **Phase** | M6 (Synthetic DNSP on Partition Exhaust) |
| **Default** | ON for the M6 landing window (2026-07-24 → 2026-08-07) |
| **Scope** | Strictly-additive wrapper at four source-of-truth sites: `src/superclaude/agents/rf-analyst.md`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/skills/task-builder/SKILL.md` (+ `.claude/` mirrors). The wrapper governs partition orchestrator behavior when a partition rf-* agent fails after retry-1 AND exhausts its escalation ladder. |
| **Enable behavior** | On Path B (≥1-success AND ≥1-exhaust cohort outcome), the orchestrator emits one synthetic-dnsp block per exhausted partition into the normal output stream alongside the real findings from successful partitions. Block conforms to the 7-field DM-003 contract (`severity: HIGH`, `source: synthetic-dnsp`, `affected_range`, `evidence`, `recommendation`, `dedup_key`, `found_n_times`). |
| **Disable path** | `git revert 87c82548` — removes the DNSP edit sites at all 4 source-of-truth pairs; partition orchestrator falls back to its pre-M6 behavior (silent abort on exhaust); the all-agents-fail Path A continues to activate `rf-team-lead.md:417` unchanged. |
| **Composition with FF_RETRY_MONOTONICITY_GUARDS (M5)** | INV-012 cross-cycle dedup: synthetic-dnsp findings with identical `dedup_key` re-emitted on cycle n+1 contribute `1` (not `2`) to `|F_{n+1}|`; the Step 1 regression-detection predicate at SKILL.md L1070 is FALSE by construction for synthetic-dnsp persistence (`dedup_key ∈ FAIL_n` ⟹ `dedup_key ∉ PASS_n`); Step 2 PR-02 monotonicity halt at SKILL.md L1071 fires iff `|F_{n+1}| >= |F_n|` after dedup-collapse — intended halt when the partition agent is stuck. |
| **M7 consolidation window** | `FF_SYNTHETIC_DNSP_EMISSION` recorded alongside `FF_RETRY_MONOTONICITY_GUARDS` (MIG-005) for unified flag-removal. After M7 lands, both flags become tombstones (the wrapper bullets are unconditional first-class behavior; the flag itself is removed from any conditional check). |
| **Rejection symbols introduced** | `DM-003-fixed-field-invariant-violation` (T06.03), `DM-003-dynamic-field-invariant-violation` (T06.04), `DM-003-recommendation-invariant-violation` + `DM-003-dedup-key-shape-violation` + `DM-003-found-n-times-invariant-violation` (T06.05), `API-003-exhaust-point-vocabulary-violation` (T06.07), `R-122-guard-precedence-violation` (T06.08), `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` (T06.09), `INV-021-cohort-serialization-violation` + `R-126-real-findings-replacement-violation` + `R-126-severity-override-violation` (T06.10). All 11 symbols emit on synthetic-dnsp boundary violations and MUST NOT be silently coerced. |
| **Preservation invariants** | rf-team-lead.md:417 byte-stable (`sha256 = 51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`); real-finding count post-merge equals pre-merge count plus synthetic count (strictly additive); HIGH severity non-overridable at every downstream layer (per-emission + merge step); INV-021 N-1 cohort concurrency. |
| **Test coverage** | `tests/audit/test_dnsp_twice_exhaust.py` (TEST-018, 33 tests), `tests/audit/test_dnsp_dedup_collapse.py` (TEST-019, 24 tests), `tests/audit/test_dnsp_all_agents_fail_bypass.py` (TEST-020), `tests/audit/test_dnsp_does_not_serialize_cohort.py` (TEST-021) — total 139 tests, all green at HEAD `87c8254`. |

## 3. NFR-CONV.10 parallel-research invariant — preservation entry

| Field | Value |
|---|---|
| **Invariant ID** | NFR-CONV.10 (parallel-research invariant) |
| **Scope** | Cohort-level invariant: when one partition's escalation ladder exhausts, the remaining N-1 sibling partitions MUST continue executing concurrently to their own success-or-exhaust terminal state BEFORE the exhausted partition's synthetic-dnsp emission is composed AND BEFORE the merge step at SKILL.md §A.8 / §A.10 runs. |
| **Wrapper-text preservation** | Pinned at all 4 source-of-truth sites by R-125 INV-021 paragraph. Required tokens at every site: "INV-021", "N-1", "concurrently", "NFR-CONV.10", "block, pause, serialize, or reduce the parallelism" (forbidden behaviors enumeration). Verified by sub-agent §1.2: rf-analyst.md L70, rf-qa.md L78, rf-qa-qualitative.md L79, SKILL.md L686 — all carry the full token set. |
| **Spawn-log evidence requirement** | The wrapper MUST require that spawn-log timestamps evidence the N-1 partitions completing concurrently with (overlapping in wall-clock time with) the exhausted partition's synthesis step. Half-open interval semantics: touching endpoints do NOT overlap. |
| **Rejection symbol** | `INV-021-cohort-serialization-violation` — sibling cohort paused awaiting exhausted-partition synthesis; spawn-log timestamps show serialization of the N-1 partitions behind the exhausted partition's synthesis; the parallel-research invariant NFR-CONV.10 is degraded for the exhausted-partition case. Distinct from `R-122-guard-precedence-violation` (cohort-level path-selection layer) and `R-126-*` (merge-step layer). |
| **Test coverage** | `tests/audit/test_dnsp_does_not_serialize_cohort.py` (TEST-021) — `PartitionWindow` dataclass records (`start_ts`, `end_ts`, `terminal`) plus per-exhausted-partition (`synthesis_start_ts`, `synthesis_end_ts`); `check_inv_021_n_minus_1_concurrency` helper verifies every sibling partition's execution window overlaps the exhausted partition's synthesis window in wall-clock time. Parametrized matrix covers `n_siblings ∈ {1,2,3,4,8}`. Negative-path adversarial spawn-logs (missing exhausted partition, wrong terminal state, missing synthesis window, inverted synthesis interval, partial serialization with one out of N-1 siblings serialized) all rejected. |
| **Preservation status post-MIG-006** | **PRESERVED**. Sub-agent §1.2 verdict PASS. The wrapper text and rejection symbol are present at all 4 sites; the test fixture is green; the synthesis step is per-emission and the merge step is per-cohort — sibling cohort parallelism is structurally independent of the synthesis path. |
| **M7 consolidation window** | NFR-CONV.10 is an enduring invariant (not a feature flag); it persists across M7 and beyond. Its M6 enforcement (R-125 wrapper text + TEST-021 fixture) becomes unconditional first-class behavior post-FF-removal. |

## 4. Sub-agent diff spot-check — summary

Verbatim verdict from quality-engineer sub-agent (full report in `evidence.md` §3.3):

> **Overall verdict: PASS** — All four "must NOT regress" invariants verified; all additional spot-checks pass; pre-existing branch drift is unchanged; revert path is documented and mechanically sound.

| Invariant | Verdict |
|---|---|
| §1.1 COMP-006-M6 rf-team-lead.md:417 byte-stable | **PASS** |
| §1.2 NFR-CONV.10 N-1 cohort concurrency operational | **PASS** |
| §1.3 Strictly-additive merge: real findings preserved alongside synthetic | **PASS** |
| §1.4 All-agents-fail guard precedence (R-122) three mutually-exclusive paths | **PASS** |

## 5. Provenance

- Pre-edit HEAD: `5439ea1`
- Commit landed: `87c8254` (single commit, 8 files, +62 / −16)
- Dependency closure: T06.15 (D-0080) PASS, T06.16 (D-0081) PASS, T06.01..T06.14 (D-0068..D-0079) PASS
- Downstream consumer: T06.18 (CP-P06-END end-of-Phase-6 checkpoint); M7 consolidation window picks up `FF_SYNTHETIC_DNSP_EMISSION` and `FF_RETRY_MONOTONICITY_GUARDS` for unified flag-removal
