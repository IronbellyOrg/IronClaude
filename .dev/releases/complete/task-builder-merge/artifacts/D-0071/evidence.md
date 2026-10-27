# D-0071 — T06.04 Evidence: Implement DM-003.affected_range + DM-003.evidence emitters

**Date:** 2026-05-18
**Task:** T06.04 — Implement DM-003.affected_range + DM-003.evidence emitters
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-115 (DM-003.affected_range verbatim assigned_files slice), R-116 (DM-003.evidence spawn-log path or absence-stub — never blank)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + structural inspection)
**Status:** PASS

---

## 1. Summary

T06.04 binds **explicit emitter-level rejection semantics** to the two dynamic-value DM-003 fields (`affected_range` and `evidence`) that T06.02 (D-0069) enumerated as bullets in the 7-field contract and T06.03 (D-0070) deliberately left content-rule-free (T06.03 covered the fixed-value fields `severity` and `source` only). Before T06.04 the wrapper said `affected_range: <assigned_files slice verbatim>` and `evidence: <spawn log path or evidence-absence stub — never blank>`, but did not name (a) which transformations are forbidden on the slice copy, (b) the canonical wire form of the spawn-log path, (c) the canonical shape of the absence stub, or (d) the rejection symbol. After T06.04 each of the four wrapper sites (`SKILL.md`, `rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`) carries an additional clause/paragraph stating:

1. `affected_range` MUST be the partition's spawn-prompt `assigned_files` (or `assigned_files` / `assigned_phases` for rf-qa-qualitative) slice copied **byte-for-byte**, with no normalization, canonicalization, ordering changes, or whitespace edits.
2. `evidence` MUST never be blank: the canonical wire value is the spawn-log path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`; when that log is unavailable the emitter MUST substitute the stub `<!-- evidence-absence: no-spawn-log: <reason> -->` explicitly citing the absence (e.g., `no-spawn-log: tmpfs-cleared`, `no-spawn-log: orchestrator-write-failed`).
3. The emitter MUST reject any synthetic-dnsp emission whose `affected_range` does not byte-match the spawn-prompt assigned slice OR whose `evidence` field is empty/whitespace-only/missing the absence stub. Such rejections surface as the named error `DM-003-dynamic-field-invariant-violation`.

The rationale (verbatim `affected_range` enables deterministic re-spawn + grep-replay; never-blank `evidence` with canonical path template makes missing-log case grep-detectable; explicit absence stub closes the audit gap between "log missing" and "field omitted") is recorded inline in SKILL.md so downstream emitter-implementation work in T06.07 (API-003 emission code) has an unambiguous contract to bind to. The `rf-team-lead.md:417` all-agents-fail backstop is byte-stable end-to-end (§5).

## 2. Planning Inputs

- **Dependency closure.** T06.03 (D-0070) PASS — DM-003-M6 fixed-field rejection contract (`severity` + `source`) bound at all 4 wrapper sites with the error symbol `DM-003-fixed-field-invariant-violation` (D-0070 §4 grep evidence; D-0070 §7 AC coverage all PASS).
- **R-115 spec (roadmap.md L366).** `DM-003.affected_range` — Verbatim copy of partition's file list as received in spawn prompt. AC: `exhausted-partition-fixture:affected_range-matches-spawn-prompt-assigned_files-byte-for-byte`.
- **R-116 spec (roadmap.md L367).** `DM-003.evidence` — Never blank — if log missing, stub explicitly cites absence (`no-spawn-log: <reason>`). AC: `evidence-field:never-empty; canonical-path-${TASK_DIR}qa/spawn-log-agent_role-partition_id.txt`.
- **M1 contract-freeze reference.** roadmap.md L109 enumerated `affected_range-verbatim-assigned-files-slice; evidence-never-blank-spawn-log-or-stub`. Per the Phase 1 schema-registry pattern (consistent with D-0069 §2 and D-0070 §2), the roadmap row IS the contract-freeze; T06.04 does not re-pin the values, it binds the rejection semantics + the canonical wire shapes (path template + absence-stub form) to them.
- **Parallel pattern (T06.03 / D-0070).** Insert a single new bold-prefixed clause after the existing fixed-field clause at each agent site (extending the bullet at rf-analyst.md L70, rf-qa.md L78, rf-qa-qualitative.md L79); insert a sibling paragraph in SKILL.md immediately after the existing T06.03 paragraph (between L668 and the "Then the orchestrator merges" paragraph). Strictly additive — no existing text is replaced.

## 3. Execution — Acceptance-criterion grep evidence

### 3.1 New error symbol present at all 4 wrapper sites

```text
$ grep -c "DM-003-dynamic-field-invariant-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All 4 wrapper sites carry the named rejection error symbol → spec-level rejection contract landed.

### 3.2 AC3 — canonical evidence path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`

```text
$ grep -c -F '${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All 4 wrapper sites carry the canonical evidence-path template byte-exact → **PASS** for AC3.

### 3.3 AC2 — never-blank evidence: explicit absence stub form present

```text
$ grep -c -F 'evidence-absence: no-spawn-log' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All 4 wrapper sites carry the canonical absence-stub shape `<!-- evidence-absence: no-spawn-log: <reason> -->` and the named rule "evidence field MUST NEVER be blank" → **PASS** for AC2 (spec-level: the contract forbids blank emission; positive-path verification deferred to T06.15 TEST-018 fixture, per the same staging used in D-0070 §9 for the T06.03 fixed-field rejection contract).

### 3.4 AC1 — verbatim affected_range clause present

```text
$ grep -c -F 'byte-for-byte' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:3
```

All 4 wrapper sites assert byte-for-byte verbatim copy semantics for `affected_range`; SKILL.md has 3 hits because the rationale paragraph re-invokes the term when explaining the deterministic re-spawn property → **PASS** for AC1 (spec-level: the contract pins verbatim semantics; positive-path verification deferred to T06.15 TEST-018 exhausted-partition fixture per its AC `exhausted-partition-fixture:affected_range-matches-spawn-prompt-assigned_files-byte-for-byte`).

### 3.5 Full clause text (rf-analyst.md L70 tail; symmetric at rf-qa.md L78, rf-qa-qualitative.md L79)

> **Dynamic-field emitter rejection (R-115 + R-116).** The `affected_range` field MUST be the partition's spawn-prompt `assigned_files` slice copied verbatim — byte-for-byte, with no normalization, canonicalization, ordering changes, or whitespace edits. The `evidence` field MUST NEVER be blank: the canonical wire value is the spawn-log path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`; when that log is unavailable the emitter MUST substitute the stub `<!-- evidence-absence: no-spawn-log: <reason> -->` explicitly citing the absence (e.g., `no-spawn-log: tmpfs-cleared`). The emitter MUST reject any synthetic emission whose `affected_range` does not byte-match the spawn-prompt `assigned_files` slice OR whose `evidence` field is empty/whitespace-only. Such rejections surface as `DM-003-dynamic-field-invariant-violation` errors and MUST NOT be silently coerced.

rf-qa-qualitative.md L79 differs only by mentioning `assigned_files` / `assigned_phases` (because qualitative-partition spawns can use either dimension); error symbol, canonical path, stub form, rejection rule all identical.

### 3.6 Full paragraph text (SKILL.md L670)

> **Dynamic-field emitter rejection (R-115 + R-116).** The `affected_range` and `evidence` fields are dynamic-value invariants of DM-003 bound by content rules rather than fixed strings. The `affected_range` field MUST be the partition's spawn-prompt `assigned_files` (or `assigned_phases` for rf-qa-qualitative) slice copied verbatim — byte-for-byte, with no normalization, canonicalization, ordering changes, or whitespace edits. The `evidence` field MUST NEVER be blank: the canonical wire value is the spawn-log path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`; when that log is unavailable the emitter MUST substitute the stub `<!-- evidence-absence: no-spawn-log: <reason> -->` explicitly citing the absence (e.g., `no-spawn-log: tmpfs-cleared`, `no-spawn-log: orchestrator-write-failed`). The emitter MUST reject any synthetic-dnsp emission whose `affected_range` does not byte-match the spawn-prompt assigned slice OR whose `evidence` field is empty / whitespace-only / missing the absence stub when the path is unresolvable. Such rejections surface as `DM-003-dynamic-field-invariant-violation` errors and MUST NOT be silently coerced. Rationale: a verbatim `affected_range` ensures the merged report's row indexes back into the exact spawn prompt that produced the failure (the orchestrator can re-spawn that range deterministically, and humans reviewing the gate report can grep the exact file list against the original spawn record); a never-blank `evidence` field with the canonical path template makes the missing-log case grep-detectable in downstream tooling, and the explicit absence stub closes the audit gap where "no path" could otherwise read as either "log missing" or "field omitted" (the stub distinguishes the two).

## 4. Edits applied

| # | File | Region | Change |
|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | New paragraph at L670 (between the T06.03 "Fixed-field emitter rejection" paragraph at L668 and the "Then the orchestrator merges" paragraph) | Inserted "Dynamic-field emitter rejection (R-115 + R-116)" paragraph with rationale. Strictly additive; bullet contract at L660-666 + T06.03 paragraph at L668 preserved byte-identical. |
| 2 | `src/superclaude/agents/rf-analyst.md` | DNSP wrapper bullet L70 tail (after T06.03 fixed-field rejection clause) | Appended dynamic-field rejection clause naming `DM-003-dynamic-field-invariant-violation` error symbol; verbatim discipline stated; canonical path template stated; absence-stub form stated. Preserves the existing 7-field enumeration + INV-012 composition + T06.03 clause byte-identical. |
| 3 | `src/superclaude/agents/rf-qa.md` | DNSP wrapper bullet L78 tail | Symmetric to Edit 2; identical clause text. |
| 4 | `src/superclaude/agents/rf-qa-qualitative.md` | DNSP wrapper bullet L79 tail | Symmetric to Edits 2 + 3; clause mentions `assigned_files` / `assigned_phases` (qualitative-partition dimension parity); rest identical. |

`rf-team-lead.md` was NOT edited (preservation gate — see §5).

## 5. Preservation invariants

| Slice | sha256 (pre-T06.04 = post-T06.03) | sha256 (post-T06.04) |
|---|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap + all-agents-fail escalation backstop — COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

```text
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
```

Both hashes match the values pinned in D-0068 §6, D-0069 §7, and D-0070 §6 → **COMP-006-M6 preservation gate PASS.**

## 6. Acceptance Criteria — Coverage Table

| AC | Description | Status | Evidence |
|---|---|---|---|
| AC1 | Exhausted-partition fixture's `affected_range` field byte-matches the spawn-prompt `assigned_files` slice | **PASS (spec-level)** | §3.4 (verbatim byte-for-byte discipline pinned at all 4 wrapper sites with explicit "no normalization, canonicalization, ordering changes, or whitespace edits" enumeration; positive-path fixture verification deferred to T06.15 TEST-018, per the same spec-first / fixture-later staging used in T06.03 — see D-0070 §9) |
| AC2 | `evidence` field is never empty across the test corpus | **PASS (spec-level)** | §3.3 (canonical absence-stub form `<!-- evidence-absence: no-spawn-log: <reason> -->` pinned at all 4 wrapper sites with the "MUST NEVER be blank" invariant + named `DM-003-dynamic-field-invariant-violation` rejection on empty/whitespace-only emission; positive-path corpus verification deferred to T06.15 TEST-018 + TEST-019 fixtures) |
| AC3 | Canonical evidence path format used: `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt` | **PASS** | §3.2 (literal path template present at all 4 wrapper sites byte-exact) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0071/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 7. Post-edit slice hashes (for downstream tasks)

| Slice | sha256 (post-edit) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `c759aba5d6d40d410777d64265c6aa4aec157ef6dfad4726aafc26a8315d5e69` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `1d26642786bd532c2d89df4d062c34e331f67ecaad9d76e0d8b6de3f84a0c07a` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `36583e28c9ee839dabc9cf0a99ac3e5dc87bf1345382b2a53afce9b18ad5a10d` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `29bbbec03dbcfb36e17f8013d8cd4a5ca6e63f0a559c07d9df891fd08ac215cf` |

`make sync-dev` ran clean for the four touched files. Skills/agents/commands cross-check confirms `src/` and `.claude/` agree for the FR-CONV.6 wrapper edit set byte-identically (sha256 of `src/` and `.claude/` copies of all four files are pairwise equal — see the parity output in this session's verification step).

## 8. Observations (Non-Blocking)

- **`make verify-sync` reports pre-existing drift on `auggie-bash-gate.sh` (not distributable) + `reject-workspace-writes.sh` installer registration.** Same pre-existing drift documented in D-0068 §6, D-0069 §9, D-0070 §9 — belongs to the in-flight `feat/hook-sync-and-matcher-fix` branch, unrelated to T06.04 / FR-CONV.6 / R-115 / R-116. The skills/agents/commands cross-checks all PASS for the four T06.04-touched files.
- **Negative-path programmatic verification.** AC1 + AC2 are pinned as spec-level invariants at all four wrapper sites with explicit error symbol `DM-003-dynamic-field-invariant-violation` so the programmatic emission code landing in T06.07 (D-0073, API-003-M6 emission) can bind to them. The end-to-end positive path (an exhausted-partition emitter producing `affected_range` byte-matching the spawn prompt + non-blank `evidence`) becomes fixture-verifiable when T06.15's TEST-018 lands (D-0080), and the end-to-end negative path (an emitter producing a normalized/reordered `affected_range` or a blank `evidence` being rejected) becomes programmatically exercisable when T06.07's emission code lands. This sequencing is by-design per the Phase 6 task graph (T06.04 spec → T06.07 emission code → T06.15 positive fixture → T06.10 / T06.18 cross-cutting ratification), identical to T06.03's staging (D-0070 §9).
- **Bullet renumbering avoided.** The dynamic-field clause extends the existing T06.03 fixed-field clause within the same bullet at each agent site rather than introducing a new bullet, preserving the 6-bullet "Orchestrator Responsibilities" list count and the rf-team-lead.md:417 byte-stability invariant downstream sub-agent verification keys on.

## 9. Provenance

- Pre-edit HEAD: `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry` (same baseline as T06.01, T06.02, T06.03 — no commits yet for the M6 wrapper landing series).
- M1 contract-freeze reference: `roadmap.md` L109 + L366-367 (DM-003 row + R-115/R-116 rows).
- T06.01 closure (FR-CONV.6 wrapper landed): D-0068 (Overall PASS, 2026-05-18).
- T06.02 closure (DM-003-M6 7-field schema): D-0069 (Overall PASS, 2026-05-18; sub-agent verification 6/6 PASS).
- T06.03 closure (severity + source fixed-field rejection): D-0070 (Overall PASS, 2026-05-18).
- R-115 (DM-003.affected_range verbatim assigned_files slice): wrapper-level rejection contract landed by T06.04; programmatic emission code lands in T06.07; positive-path fixture lands in T06.15 (TEST-018).
- R-116 (DM-003.evidence never-blank + canonical path + absence stub): wrapper-level rejection contract landed by T06.04; programmatic emission code lands in T06.07.
- T06.05 will follow with the remaining 3 emitters (recommendation + dedup_key + found_n_times) per the Phase 6 task graph; T06.06 mid-phase checkpoint then gates T06.01–T06.05 collectively.
