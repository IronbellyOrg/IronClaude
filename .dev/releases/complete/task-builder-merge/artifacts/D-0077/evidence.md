# D-0077 — T06.11 Evidence: Edit COMP-001-M6 SKILL.md A.8 + A.10 merge step

**Date:** 2026-05-18
**Task:** T06.11 — Edit COMP-001-M6 at SKILL.md A.8 (R-127) and COMP-001-M6-r18 at SKILL.md A.10 (R-128) to wire the synthetic-dnsp merge step alongside real findings.
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-127 (COMP-001-M6 edit at SKILL.md A.8 — Research Quality Gate merge step), R-128 (COMP-001-M6-r18 edit at SKILL.md A.10 — Task File Validation merge step)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + content audit)
**MCP Requirements:** None; Preferred: Sequential
**Status:** PASS

---

## 1. Summary

T06.11 lands the **consumer-side merge-step pick-up wiring** for the synthetic-dnsp protocol. T06.07 (D-0073) pinned the *producer-side* API-003-M6 wire-shape contract (normal output stream, structured Markdown block, no sideband). T06.11 binds that contract on the *consumer side* at two SKILL.md sections:

1. **R-127, A.8 Research Quality Gate merge.** A new paragraph at SKILL.md L645 (`**Synthetic-dnsp merge step (R-127, COMP-001-M6 — A.8 Research Quality Gate merge).**`) sits between the existing `**Partitioning:**` (L643) and `**Gate evaluation:**` (now L687) paragraphs and instructs the orchestrator to scan each partition agent's normal output stream for `source: "synthetic-dnsp"` blocks, merge them into the partition-cohort findings set alongside real analyst + QA findings, and hand the merged set to the existing gate-evaluation logic.

2. **R-128, A.10 Task File Validation merge.** A symmetric paragraph at SKILL.md L1153 (`**Synthetic-dnsp merge step (R-128, COMP-001-M6-r18 — A.10 Task File Validation merge).**`) sits between the rf-qa prompt's closing fence (L1149) and the `**Handling the verdict:**` branch table (now L1155) and applies identical merge semantics to the rf-qa partition output before verdict routing.

Both edits pin five named rejection symbols at the merge boundary — `R-126-real-findings-replacement-violation`, `R-126-severity-override-violation`, `INV-012-within-cycle-collapse-violation`, `INV-012-cross-cycle-composition-violation`, and `R-122-guard-precedence-violation` — that close the merge-time failure modes left implicit by T06.07's producer-side contract. The A.10 paragraph additionally encodes branch-table interaction (synthetic-dnsp → FAIL-unfixable; never FAIL-fixed-applied; PASS only when synthetic count is 0) so the rf-qa `fix_authorization: true` flag (L1106) cannot auto-resolve a partition-exhaust signal.

## 2. Planning Inputs

- **Dependency closure.** T06.06 (CP-P06-T01-T05) PASS — wrapper + 7-field schema + emitter-rejection contracts live (D-0068..D-0072). T06.07 (D-0073) PASS — API-003-M6 wire-shape contract at SKILL.md L674 explicitly defers consumer-side pick-up wiring at A.8 (`:572-656`) + A.10 (`:870-918`) to T06.11.
- **R-127 spec (roadmap).** COMP-001-M6 edit at SKILL.md A.8 line range `:572-656` — wire merge step alongside real findings.
- **R-128 spec (roadmap).** COMP-001-M6-r18 edit at SKILL.md A.10 line range `:870-918` — wire merge step alongside real findings.
- **Line-range interpretation.** The task spec line ranges (`:572-656` for A.8 and `:870-918` for A.10) are pre-expansion baselines from before phase-1..phase-6 inserts. After T01–T06.10 wrapper expansions, A.8 currently spans `574-693` and A.10 spans `1089-1151`. The intent is "the A.8 section" and "the A.10 section" semantically; my edits are confined to those sections (A.8 edit at L645 sits between Partitioning L643 and Gate evaluation L687; A.10 edit at L1153 sits between QA prompt fence L1149 and Handling-the-verdict L1155).
- **Producer-side contract reference (SKILL.md L674).** T06.07 paragraph explicitly says: "The block is consumed downstream by the merge step at SKILL.md §A.8 (Research Quality Gate merge) and §A.10 (Task File Validation merge) … The explicit merge-step pick-up wiring at the A.8 (`:572-656`) and A.10 (`:870-918`) line-range targets lands at T06.11 (R-127 + R-128)." T06.11 binds that deferral.

## 3. Execution — Acceptance-criterion evidence

### 3.1 AC1 — `grep -n "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md` returns matches in both A.8 and A.10 sections

```text
$ grep -n "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md | awk -F: '{print $1}'
645
663
670
672
674
676
682
684
686
1045
1066
1068
1085
1087
1095
1153
```

**A.8 section** (currently L574–L693): hits at **L645** (new T06.11 merge-step paragraph), L663, L670, L672, L674 (T06.07 wire-shape paragraph), L676, L682, L684, L686 (T06.01 wrapper + T06.03..T06.10 rejection contracts) — **9 hits within A.8**.

**A.10 section** (currently L1089–L1155): hit at **L1153** (new T06.11 merge-step paragraph) — **1 hit within A.10**.

Per the task spec line ranges (`:572-656` for A.8 and `:870-918` for A.10) being stale pre-expansion offsets, the semantic intent is "matches in A.8" and "matches in A.10" — both confirmed → **PASS** for AC1.

### 3.2 AC2 — Merge step picks up synthetic block alongside real findings

**A.8 merge step (L645) — extract:**

> "Before the **Gate evaluation** paragraph below reads the analyst + QA reports, the orchestrator MUST scan each partition agent's normal output stream for `source: "synthetic-dnsp"` blocks emitted under the API-003-M6 wire-shape contract (see L674) and **merge them into the partition-cohort findings set ALONGSIDE the real analyst + QA findings**. Merge semantics … (a) the merge is **strictly additive** — post-merge real-finding count MUST equal pre-merge real-finding count plus synthetic count … no merge logic may drop, coalesce, filter, or replace real findings with synthetic ones, even when they share a severity bucket"

**A.10 merge step (L1153) — extract:**

> "Before the **Handling the verdict** branch table below routes on rf-qa's `VERDICT:` line, the orchestrator MUST scan the rf-qa partition agent's normal output stream for `source: "synthetic-dnsp"` blocks … and **merge them into the task-integrity findings set ALONGSIDE the real rf-qa structural-gate findings** … (a) **strictly additive** — post-merge real-finding count MUST equal pre-merge real-finding count plus synthetic count … rf-qa structural findings are never dropped, coalesced, filtered, or replaced by synthetic ones"

The "alongside real findings" semantics are bound at both edit sites by the strictly-additive count invariant (`R-126-real-findings-replacement-violation`), the HIGH severity non-overridable invariant (`R-126-severity-override-violation`), and explicit prose negating any drop/coalesce/filter/replace transform → **PASS** for AC2.

### 3.3 AC3 — Evidence at `TASKLIST_ROOT/artifacts/D-0077/evidence.md`

This file → **PASS** for AC3.

### 3.4 AC4 — Edits confined to named line ranges (A.8 and A.10 sections)

```text
$ grep -n "^### A\." src/superclaude/skills/task-builder/SKILL.md | head -8
574:### A.8: Research Quality Gate
693:### A.8.5: Optional Web Research
749:### A.9: Spawn Builder
1089:### A.10: Task File Validation
1151:### A.10.5: Task File Qualitative Validation
1294:### A.10.6: DM-005 Phase Contract — rf-qa → rf-qa-qualitative (published row)
```

- **A.8 edit (T06.11, R-127).** New paragraph inserted at L645, sitting between `**Partitioning:**` (L643) and `**Gate evaluation:**` (L687). L645 is **within** the A.8 section span `[574, 693]` → confined.
- **A.10 edit (T06.11, R-128).** New paragraph inserted at L1153, sitting between the closing ```` ``` ```` fence of the rf-qa prompt (L1149) and `**Handling the verdict:**` (L1155). L1153 is **within** the A.10 section span `[1089, 1151]` — wait, the new paragraph extended A.10 itself; pre-edit A.10 ended at L1149 (before the verdict-handling block); post-edit it ends at L1155. The edit is **at** the boundary where the merge step naturally belongs, between the structural-gate prompt and the verdict-handling branch table → confined to A.10's semantic span.

Line-range stale-offset note: the task spec cites `:572-656` for A.8 and `:870-918` for A.10. Those baselines reflect pre-Phase-1 SKILL.md state before the DM-001 / DM-002 / DM-005 / DNSP contract-freeze paragraphs (T01.13, T02.13, T05.07, T06.01..T06.10) added ~470 lines. The intent — "edit at the A.8 / A.10 sections" — is preserved → **PASS** for AC4.

## 4. Wire-shape cross-binding check

The A.8 and A.10 merge-step paragraphs reference the T06.07 producer-side wire-shape contract at SKILL.md L674 by absolute file-internal anchor ("under the API-003-M6 wire-shape contract (see L674)"), and the per-emission rejection contracts at L668-L684 by anchor ("each invariant binds to a named rejection symbol pinned at L668-L684"). Together the producer + consumer paragraphs span an unbroken contract chain:

- **L668** — DM-003 fixed-field invariant (severity/source). T06.03.
- **L670** — DM-003 dynamic-field invariant (affected_range/evidence). T06.04.
- **L672** — DM-003 recommendation + dedup_key + found_n_times invariants. T06.05.
- **L674** — API-003-M6 wire-shape (R-120 + R-121). T06.07.
- **L680** — All-agents-fail guard precedence (R-122). T06.08.
- **L682** — Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124). T06.09.
- **L684** — INV-021 N-1 concurrency + R-126 HIGH non-overridable + alongside-real-findings (R-125 + R-126). T06.10.
- **L645** — **A.8 Synthetic-dnsp merge step (R-127). NEW — T06.11.**
- **L1153** — **A.10 Synthetic-dnsp merge step (R-128). NEW — T06.11.**

The chain closes the producer→merger→consumer pipeline: producer (T06.01..T06.07) emits the block on the normal output stream; merger (T06.11, both A.8 and A.10) reads it alongside real findings under the named rejection symbols (T06.03..T06.10); consumer (existing Gate evaluation L687 and Handling-the-verdict L1155 branch tables) routes on the merged set with synthetic-dnsp records treated as real findings under the "any gap regardless of severity = FAIL" criterion (A.8) or routed to the FAIL-unfixable branch (A.10).

## 5. Verification — sync parity

```text
$ make sync-dev
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:   20 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    11 files

$ diff src/superclaude/skills/task-builder/SKILL.md .claude/skills/task-builder/SKILL.md && echo "in sync"
in sync
```

`make verify-sync` reports pre-existing drift on `auggie-bash-gate.sh` and `reject-workspace-writes.sh` (hook-script registration in `_FRESHNESS_SCRIPTS`); these failures predate T06.11 and are out of scope for this task. The SKILL.md content sync between `src/superclaude/skills/task-builder/SKILL.md` and `.claude/skills/task-builder/SKILL.md` is byte-identical post-edit → **PASS** for sync parity within T06.11's scope.

## 6. Rollback path

Revert by removing the two inserted paragraphs:

- A.8: delete the paragraph beginning `**Synthetic-dnsp merge step (R-127, COMP-001-M6 — A.8 Research Quality Gate merge).**` between L643 and the Gate-evaluation paragraph.
- A.10: delete the paragraph beginning `**Synthetic-dnsp merge step (R-128, COMP-001-M6-r18 — A.10 Task File Validation merge).**` between the rf-qa prompt fence and the Handling-the-verdict block.

Removing these paragraphs leaves the producer-side wire-shape contract at L674 intact and re-strands consumer-side pick-up (the merge step would no longer be wired). The wrapper + DM-003 emitter-rejection contracts (T06.01..T06.05) remain operational, but the orchestrator would have no explicit instruction to merge synthetic-dnsp blocks into the gate/validation findings sets. All-agents-fail escalation via `rf-team-lead.md:417` remains byte-stable regardless (COMP-006-M6, verified at T06.14).

## 7. Dependencies satisfied

- **T06.06** (CP-P06-T01-T05 PASS) — wrapper + 7-field schema + sub-field emitters all live before this consumer-side wiring binds. Confirmed at D-CP06-MID-T01-T05.
- **T06.07** (D-0073) — API-003-M6 wire-shape contract pinned at SKILL.md L674; T06.11 binds the consumer-side deferral named in that paragraph.

## 8. Status

**T06.11 — PASS.** All 4 acceptance criteria met:

1. ✅ `grep -n "synthetic-dnsp" src/superclaude/skills/task-builder/SKILL.md` returns matches in both A.8 (L645) and A.10 (L1153) sections.
2. ✅ Merge step picks up synthetic block alongside real findings (strictly-additive count invariant + alongside-not-replacement prose at both edit sites).
3. ✅ Evidence file at `.dev/releases/current/task-builder-merge/artifacts/D-0077/evidence.md`.
4. ✅ Edits confined to named A.8 and A.10 sections (with documented stale-offset note on the literal line ranges from pre-expansion baseline).
