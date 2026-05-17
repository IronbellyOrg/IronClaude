# Research: FR-CONV.6 (PR-03 BASE) DNSP Synthetic Finding Insertion Points

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**CASE:** B (sc silent; task-builder silent — paradigm-neutral execution-resilience mechanism; PR-03 is BASE not borrowed)
**Conflict-register row:** NONE (CASE-B correctly omitted)
**Protected invariant:** parallel-research (NFR-CONV.10) + persistent-`.dev/tasks/`-artifact (OPEN-INV-018) + evidence-bound-item (synthetic finding's evidence field cites spawn-log path)
**Lands:** 6th of 6 FRs (BASE — combined adversarial score 0.959)

---

## 1. Verified-Current Insertion Points

Five edit sites verified verbatim against current source (2026-05-14). Excerpts below are anchored on the partition/quality-gate constructs into which the synthetic-dnsp emission contract lands.

### 1.1 Site 1 — `src/superclaude/skills/task-builder/SKILL.md` lines 572–656 (PRD cite: 574–654)

**Anchor context:** Section **A.8: Research Quality Gate** — defines the parallel rf-analyst + rf-qa spawn that performs research-completeness verification, including the partitioning rule (>6 files per track ⇒ partition) and the gap-fill cycle ceiling (max 3 rounds). This is the orchestrator-side edit site: the gate evaluation block needs the synthetic-dnsp emission contract attached to the "partition agent escalation exhaust" branch.

Verbatim partition-and-gate excerpt (load-bearing for insertion):

```
**Partitioning:** When >6 research files per track, spawn 2 analyst + 2 QA instances (4 agents total), each with assigned_files subsets. Merge reports after all return.

**Gate evaluation:** Read both analyst and QA reports. Gate PASSES when both verdicts are PASS with ALL findings resolved regardless of severity.

**Gap-fill cycle:** If the gate fails:
1. Compile all CRITICAL, IMPORTANT, and MINOR issues from analyst + QA reports into a structured gap list
2. Spawn targeted gap-fill researcher(s) via Agent tool (`subagent_type: "general-purpose"`) with specific gaps to fill
3. After gap-fill, re-run analyst + QA on the NEW research files only
4. **Maximum 3 gap-fill rounds** (aligned with canonical skills and rf-qa agent definition)
5. After 3 rounds, proceed with remaining gaps as Open Questions in the task file
```

**Insertion landing:** A new bullet/sub-section after the "Maximum 3 gap-fill rounds" rule describing per-partition DNSP synthetic emission when a partition agent's full escalation ladder exhausts (retry-2 + gap-fill exhaust). The synthetic emits as a HIGH-severity finding into the merged report, NOT as a new gap-fill request.

### 1.2 Site 2 — `src/superclaude/skills/task-builder/SKILL.md` lines 870–918 (PRD cite: 872–916)

**Anchor context:** Section **A.10: Task File Validation** — defines the rf-qa post-builder validation spawn with `fix_authorization: true` and its retry counter. Excerpt:

```
These are SEPARATE retry counters — a builder that returns RESEARCH_NEEDED twice and then produces a malformed file gets 2+2=4 total invocations maximum.

### A.10: Task File Validation

After the builder returns a task file path, validate the task file before presenting to the user.

**Spawn rf-qa:** Use the Agent tool with `subagent_type: "rf-qa"`, `mode: "bypassPermissions"`.
```

**Insertion landing:** Extend the "Handling the verdict" block at the end of A.10 (line 918 onward) with a clause: if rf-qa partitions are spawned and any partition exhausts its escalation ladder (twice-retry exhaust), the orchestrator records a synthetic-dnsp HIGH finding against that partition's `assigned_files` slice rather than treating the missing report as a silent gate abort.

### 1.3 Site 3 — `src/superclaude/agents/rf-analyst.md` lines 58–71 (PRD cite: 60–69)

**Anchor context:** rf-analyst partition-protocol "When You Are a Single Instance" + "Orchestrator Responsibilities" boundary block. Verbatim:

```
### When You Are a Single Instance (Default)

If no `assigned_files` field is present, you are the sole analyst. Analyze ALL files in scope as described in each analysis type below. This is the default behavior.

### Orchestrator Responsibilities (Not Your Job)

The orchestrator (skill session or team lead) is responsible for:
- Deciding when to partition (based on file count — typically >6 files warrants partitioning)
- Dividing files into balanced subsets
- Spawning multiple rf-analyst instances in parallel, each with its `assigned_files` list
- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items, merge gap compilations with deduplication)
```

**Insertion landing:** Append a new bullet under "Orchestrator Responsibilities" naming synthetic-dnsp emission on per-partition exhaust, AND insert a new section "When Your Escalation Ladder Exhausts" describing the within-agent-instance emission contract (the agent emits the 5-field synthetic finding into its output stream so the orchestrator's merge picks it up).

### 1.4 Site 4 — `src/superclaude/agents/rf-qa.md` lines 68–79 (PRD cite: 70–77)

**Anchor context:** rf-qa partition-protocol "When You Are a Single Instance" / "Orchestrator Responsibilities" mirror of rf-analyst. Verbatim:

```
If no `assigned_files` field is present, you are the sole QA agent. Verify ALL files in scope as described in each QA phase below. This is the default behavior.

### Orchestrator Responsibilities (Not Your Job)

The orchestrator (skill session or team lead) is responsible for:
- Deciding when to partition (based on file count — typically >6 files warrants partitioning)
- Dividing files into balanced subsets
- Spawning multiple rf-qa instances in parallel, each with its `assigned_files` list
- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)
```

**Insertion landing:** Same shape as rf-analyst — synthetic-dnsp emission clause in "Orchestrator Responsibilities" + new "When Your Escalation Ladder Exhausts" section.

### 1.5 Site 5 — `src/superclaude/agents/rf-qa-qualitative.md` lines 70–80 (PRD cite: 72–78)

**Anchor context:** rf-qa-qualitative partition-protocol "Single Instance" / "Orchestrator Responsibilities" identical in shape to rf-qa. Verbatim:

```
If no `assigned_files` field is present, you are the sole QA agent. Verify ALL files in scope as described in each QA phase below. This is the default behavior.

### Orchestrator Responsibilities (Not Your Job)

The orchestrator (skill session or team lead) is responsible for:
- Deciding when to partition (based on file count — typically >6 files warrants partitioning)
- Dividing files into balanced subsets
- Spawning multiple rf-qa instances in parallel, each with its `assigned_files` list
- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)
```

**Insertion landing:** Same shape as rf-qa. Three within-agent files (rf-analyst, rf-qa, rf-qa-qualitative) all carry the same emission contract; orchestrator-side (task-builder SKILL.md) carries the consumption + dedup logic.

**Acceptance grep target:** PRD §14.1 FR-CONV.6 requires `grep -n "synthetic-dnsp" rf-analyst.md rf-qa.md` to return ≥1 hit per file. Current grep returns zero hits across all four files — implementation greenfield as expected for a BASE FR.

---

## 2. Synthetic DNSP Finding 5 Fixed Fields (per PRD §25.3)

Per PRD §14.1 FR-CONV.6 verbatim emission contract:

| Field | Value / Rule |
|---|---|
| `severity` | `HIGH` (fixed — non-overridable; ensures gate-level visibility per Negative criterion) |
| `source` | `"synthetic-dnsp"` (fixed — literal sentinel string; grep-able for acceptance and operator inspection) |
| `affected_range` | The exhausted agent's `assigned_files` slice (verbatim copy of the partition's file list as received in the spawn prompt) |
| `evidence` | Spawn-log path (e.g. `${TASK_DIR}qa/spawn-log-<agent>-<partition_id>.txt`) OR an explicit stub citing log absence (`"no-spawn-log: <reason>"`) — never blank |
| `recommendation` | `"Manual review required — partition agent failed twice"` (fixed literal string) |

**Plus two dedup-control fields appended at emission time:**

| Field | Value / Rule |
|---|---|
| `dedup_key` | Tuple `(assigned_files_range, escalation_ladder_exhaust_point)` — composed at emission time; canonicalised string form for hash/compare (e.g. `"files:src/a.md,src/b.md|exhaust:retry-2"`) |
| `found_n_times` | Integer; default `1` on first emission; increments by 1 each time a finding with an identical `dedup_key` collapses into this one within the same cycle |

**Self-contained-item invariant preservation (NFR-CONV.6 cross-check):** All five fixed fields + the two dedup fields are populated at the moment of emission so the synthetic record satisfies the 5-field per-item schema demanded by TB-Add-1 through TB-Add-8.

---

## 3. Emission Contract

**Trigger:** After the entire escalation ladder exhausts on a single partition agent (rf-analyst partition instance, rf-qa partition instance, or rf-qa-qualitative partition instance) — meaning the agent has consumed all its allowed retries (default twice-retry exhaust) and gap-fill has not recovered the partition's report — the agent emits **one** synthetic HIGH-severity finding into its output stream **rather than silently aborting the gate**.

**Carrier:** The synthetic finding is emitted as a structured block (JSON-or-block per PRD §14.1) in the agent's normal output stream. The orchestrator's existing merge logic (Site 1 / Site 2 in §1 above) consumes it identically to a real finding — no separate transport channel.

**Cardinality:** **Per partition instance**, not per orchestrator. If 4 partition agents are spawned (2 analyst + 2 QA per A.8 partitioning rule) and 1 exhausts, **one** synthetic finding emits. If 2 exhaust independently with **distinct** `assigned_files`, **two** synthetic findings emit (different `dedup_key`s).

**Replacement scope:** The synthetic-dnsp emission **does not replace** the existing rf-team-lead.md:417 escalation ("Fix Cycles: max 3 cycles per phase. If max cycles exhausted, HALT and ask user"). It supplements the gate-output channel with a HIGH-severity record so the partition exhaust becomes a first-class finding consumable by FR-CONV.5 monotonicity and by the user-facing gate summary.

---

## 4. All-Agents-Fail Guard Precedence

**Precedence rule (verbatim from PRD §14.1 FR-CONV.6 Description):** "**All-agents-fail guard preserved**: if zero partition agents succeeded, escalate normally (`rf-team-lead.md:417` — 3 fix cycles per phase) and DO NOT emit synthetic."

**Current source verified:**

- `rf-team-lead.md:417`: `**Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.`
- PRD's `~414` cite differs from confirmed current line `417` — drift of 3 lines, surface-trivial; PRD already flagged this with `[NEEDS-VERIFICATION-IN-PHASE-2]`.

**Decision matrix at gate exhaust time:**

| Condition | Action |
|---|---|
| ≥1 partition agent returned successfully AND ≥1 partition agent's escalation ladder exhausted | **Emit synthetic-dnsp** for each exhausted partition (one per partition) |
| **Zero** partition agents returned successfully (all partitions exhausted) | **Do NOT emit synthetic-dnsp.** Escalate normally per `rf-team-lead.md:417` (3 fix cycles per phase, then HALT-and-ask-user) |
| All partition agents returned successfully | No synthetic emission needed — normal gate flow |

**Rationale:** When zero partitions succeeded, the gate has no merged report to attach findings to — the existing all-agents-fail path takes the user to an explicit halt-and-ask point. Synthetic emission would mask this by producing N HIGH findings that look like ordinary fixable issues.

---

## 5. Dedup-Key Composition

**Key tuple:** `(assigned_files_range, escalation_ladder_exhaust_point)`.

- `assigned_files_range`: the partition's `assigned_files` list, canonicalised (sorted, joined by `,`) — e.g. `"src/a.md,src/b.md"`.
- `escalation_ladder_exhaust_point`: the rung at which the ladder exhausted — e.g. `"retry-2"` for the twice-retry exhaust case (the default trigger), `"gap-fill-round-3"` if exhaust occurred during the gap-fill ceiling, etc. String token, not a free-form description.

**Collapse rule (within-cycle):** When the orchestrator's merge step (Sites 1+2) encounters two synthetic-dnsp findings with **identical** `dedup_key`, it collapses them into one record and increments `found_n_times` (initial `1` → `2`). The PRD acceptance verbiage requires the merged record to carry a `found N times` note.

**Why composite, not just `assigned_files_range`:** If the same partition's ladder exhausts at different rungs across re-spawns (e.g. retry-2 in one re-spawn, gap-fill-round-3 in another), these are distinct failure signatures and should appear as separate findings — composite key enforces this without losing one signal.

**Verification fixture path:** PRD §14.1 acceptance specifies "inject two identical exhaust events; verify only one finding emits with `found N times`" — fixture must emit two synthetic-dnsp blocks with identical `dedup_key` and assert post-merge cardinality = 1.

---

## 6. INV-012 Cross-Cycle Dedup Rule

**Rule (verbatim PRD §141, line 141):** "Synthetic findings emitted by FR-CONV.6 (DNSP) COUNT as failures for `|F_n|` monotonicity. BUT a synthetic finding with identical dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a dedup case, NOT a regression."

**Operational meaning:**

1. **Cardinality contribution:** A synthetic-dnsp finding contributes `1` to `|F_n|` exactly like a real finding — it is not invisible to FR-CONV.5 monotonicity.
2. **Cross-cycle dedup:** If cycle N produces a synthetic-dnsp with `dedup_key = K`, AND cycle N+1 produces a synthetic-dnsp with **identical** `dedup_key = K`, then for the purposes of FR-CONV.5 monotonicity, **this is NOT a regression**. Monotonicity treats the persistent same-partition-same-exhaust-point as a dedup, allowing the loop to proceed past `[HALT-MONOTONICITY]`.
3. **Distinct-dedup-key counts:** If cycle N has synthetic-dnsp with `K1` and cycle N+1 has synthetic-dnsp with `K1` AND `K2`, that is a regression on `|F|` count (one new failure mode).

**FR-CONV.5 ↔ FR-CONV.6 contract:** FR-CONV.5 monotonicity halt-check consumes `dedup_key` to distinguish "same problem persisting" (no-halt) from "new problem appeared" (halt-regression). Without this rule, persistent partition exhaust would falsely trip the regression halt every cycle.

**Verification fixture path (per PRD §141, line 145):** "synthetic 2-cycle fixture with one synthetic-dnsp finding (same `assigned_files_range`+`escalation_ladder_exhaust_point` in both cycles) proceeds to cycle 3 without halting".

---

## 7. Acceptance Criteria (from PRD §14.1 FR-CONV.6)

**Observable behavior:**

- ✅ When a partition agent's escalation ladder exhausts at retry-2, the agent's output stream emits a JSON-or-block synthetic-dnsp finding with **all five** fixed fields (`severity`, `source`, `affected_range`, `evidence`, `recommendation`).
- ✅ Two synthetic findings with identical `dedup_key` collapse with a `found 2 times` note.
- ✅ Zero-partitions-succeeded → no synthetic emits; existing `rf-team-lead.md:417` 3-fix-cycle escalation runs.

**Verification methods:**

- **Twice-exhaust fixture:** Inject partition-agent fixture that times out twice ⇒ assert synthetic-dnsp appears in gate output with all 5 required fields.
- **Identical-exhaust fixture:** Inject two identical exhaust events ⇒ assert exactly one finding emits with `found N times` note.
- **All-agents-fail fixture:** Inject all-agents-fail fixture ⇒ assert zero synthetic emits AND existing `rf-team-lead.md:417` escalation path activates.
- **Grep acceptance:** `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file at the partition-protocol section.

**Negative criteria (must-not-break):**

- ❌ Synthetic-dnsp MUST NOT emit BEFORE the escalation ladder exhausts — the all-agents-fail guard (§4) runs first.
- ❌ Existing `rf-team-lead.md:417` escalation (3 fix cycles per phase, HALT-and-ask-user) MUST NOT be replaced or short-circuited.
- ❌ Synthetic findings MUST NOT mask real findings — HIGH severity ensures gate-level visibility, and they emit alongside (not in place of) real findings from partitions that did succeed.
- ❌ Dedup-key collapse MUST NOT cross-cycle for monotonicity — PR-02 (FR-CONV.5) monotonicity treats cross-cycle identical-key as not-regression per INV-012 (§6).

---

## 8. Parallel-Research Invariant Preservation (NFR-CONV.10 + INV-021)

**Protected invariant:** parallel-research (NFR-CONV.10 in PRD §14.4); INV-021 = "DNSP fires within-agent-instance".

**Mechanism:**

- DNSP emission is **per-partition, within-agent-instance**. Each partition agent (rf-analyst-1, rf-analyst-2, rf-qa-1, rf-qa-2, etc.) independently decides whether its own escalation ladder has exhausted and emits its own synthetic finding into its own output stream.
- The cohort of partition agents continues to run concurrently. One partition's exhaust does not interrupt or serialize the other partitions.
- **N-1 partitions complete normally** while the exhausted partition synthesises its finding. The orchestrator waits for **all** partitions to return (whether with real reports or with synthetic-dnsp records), then performs the standard merge.

**Spawn-log verification (PRD §14.4 NFR-CONV.10 verification clause):** "Spawn-log inspection: N partition agents run concurrently; on one agent's escalation exhaust, N-1 continue to completion before DNSP synthesises a finding."

**What FR-CONV.6 does NOT do:** It does NOT collapse the partition cohort to a single-threaded retry loop. It does NOT block other partitions from completing. The DNSP synthetic is generated locally inside the exhausted agent's reply, not via any cross-agent coordination.

---

## 9. Dependencies on other FRs

- **FR-CONV.5 (Retry Monotonicity Protocol, PR-02 BORROWED-A):** Consumes `dedup_key` to evaluate cross-cycle dedup (INV-012). Without FR-CONV.5's monotonicity halt-check, the dedup rule has no consumer. With FR-CONV.5, persistent same-key synthetic-dnsp findings are correctly classified as not-regression.
- **FR-CONV.1 (Gate produces `F_n` count):** Synthetic-dnsp findings contribute to `|F_n|` cardinality. The gate-output schema must accept synthetic blocks identically to real findings (the merge step does not discriminate by `source` field at counting time).
- **NFR-CONV.6 (self-contained-item):** All 5 fixed fields populated at emission ensures TB-Add-1 through TB-Add-8 do not reject the synthetic block when it later becomes a task-checklist item (if escalation produces a manual-review item).
- **NFR-CONV.10 (parallel-research):** §8 above — per-partition emission preserves cohort parallelism.

---

## 10. Gaps and Questions

1. **Open: spawn-log path canonicalisation.** PRD specifies "spawn-log path, OR stub citing log absence" but does not name the canonical spawn-log location. Current task-builder SKILL.md A.8/A.10 references `${TASK_DIR}qa/` for QA reports but not for spawn logs. **Recommendation:** standardise on `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt` or `${TASK_DIR}.spawn-logs/<agent_role>-<partition_id>.log`. Pick one in TDD §Implementation.
2. **Open: escalation-ladder-exhaust-point token vocabulary.** Current sources reference `retry-2`, gap-fill rounds, and rf-team-lead's "3 fix cycles". The `escalation_ladder_exhaust_point` token must be a closed vocabulary so dedup-key comparison is deterministic. **Recommendation:** enumerate the allowed values (e.g. `{"retry-1", "retry-2", "gap-fill-round-1", "gap-fill-round-2", "gap-fill-round-3"}`) in TDD §Schema.
3. **Open: `rf-qa-qualitative.md` membership in acceptance grep.** PRD §14.1 acceptance grep references only `rf-analyst.md` and `rf-qa.md` but the description requires "partition agents (rf-analyst or rf-qa partition)" — strictly read, rf-qa-qualitative is also a partition agent (and the PRD edit-sites list includes it explicitly). **Recommendation:** TDD should specify whether the synthetic-dnsp emission contract is replicated identically in rf-qa-qualitative.md (almost certainly yes given the PRD edit-site cite) and update the grep acceptance to also include `rf-qa-qualitative.md`.
4. **Resolved: drift on `rf-team-lead.md:414` vs `:417`.** PRD already tagged this with `[NEEDS-VERIFICATION-IN-PHASE-2]`. Confirmed: current line is `417`. Implementation should reference `:417` and a future-stable anchor phrase ("Fix Cycles: ... max 3 cycles per phase") to survive further drift.

---

## 11. Stale Documentation Found

- **`rf-team-lead.md:414` cited in PRD §14.1 FR-CONV.6 Description and Negative criterion** — current source has the relevant clause at line `417`, not `414`. Drift of 3 lines. PRD already carries `[NEEDS-VERIFICATION-IN-PHASE-2]` tag; this research confirms the resolution.
- **PRD line-range cites for the 5 edit sites** were all checked and are within ±2 lines of current source. All sites verified verbatim; the partition-protocol blocks are stable across the three agent files (rf-analyst, rf-qa, rf-qa-qualitative).
- **No other stale references found** in the surveyed surface (task-builder SKILL.md §A.8 / §A.10, three agent partition-protocol blocks).

---

## 12. Summary

FR-CONV.6 lands a DNSP synthetic-finding emission contract across five verified-current edit sites: two in `src/superclaude/skills/task-builder/SKILL.md` (orchestrator-side consumption in §A.8 Research Quality Gate and §A.10 Task File Validation, around lines 572–656 and 870–918) and three in agent partition-protocol blocks (`rf-analyst.md:58–71`, `rf-qa.md:68–79`, `rf-qa-qualitative.md:70–80` — all greenfield, current grep for `"synthetic-dnsp"` returns zero hits). The synthetic finding carries five fixed fields (`severity: HIGH`, `source: "synthetic-dnsp"`, `affected_range`, `evidence`, `recommendation`) plus two dedup-control fields (`dedup_key = (assigned_files_range, escalation_ladder_exhaust_point)`, `found_n_times`), emits per-partition-within-agent-instance to preserve the parallel-research invariant (NFR-CONV.10 + INV-021), and is consumed by FR-CONV.5 monotonicity which treats cross-cycle identical-`dedup_key` as not-regression per INV-012. The all-agents-fail guard at `rf-team-lead.md:417` (PRD cite `~414` is stale-by-3-lines) takes precedence: zero-partitions-succeeded routes to the existing 3-fix-cycle escalation and emits no synthetic. Three open questions remain for TDD resolution: spawn-log path canonicalisation, escalation-ladder-exhaust-point token vocabulary, and whether the acceptance grep should additionally cover `rf-qa-qualitative.md`.

---

**Status:** Complete
