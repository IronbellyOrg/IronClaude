# D-0058 — T05.05 Spec: F-set + 4-step Ordering Precedence Rule

**Task:** T05.05 (Phase 5 — M5 Retry Monotonicity + Regression Halts)
**Roadmap items:** R-094 (F-set definition — set with dedup-key identity; cardinality post-dedup), R-095 (Ordering precedence rule — regression > monotonicity > hard-cap > proceed)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STRICT
**Confidence:** [█████████-] 90%
**Verification method:** Sub-agent (quality-engineer) — read-only ratification of existing M5 protocol text
**Sub-Agent Delegation:** Required (executed)

---

## 1. Scope

T05.05 is the **ratification** task for the F-set identity definition
(R-094) and the 4-step ordering precedence rule (R-095). It is the
sub-agent-gated capstone of the M5 protocol layer that T05.01 (FR-CONV.5
wrapper, D-0054), T05.02 (API-004-M5 wire ABI contract, D-0055), T05.03
(monotonicity emitter, D-0056), and T05.04 (regression emitter, D-0057)
collectively landed in `src/superclaude/skills/task-builder/SKILL.md`.

By the time T05.05 runs, the SKILL.md text already contains:

- The F-set definition with dedup-key identity (SKILL.md L1042-1048;
  landed by T05.02 / D-0055).
- The 4-step ordering rule (SKILL.md L1050-1059; landed by T05.02 /
  D-0055).
- The INV-012 composition note tying synthetic-dnsp findings into
  `|F_n|` while excluding identical-dedup-key cross-cycle persistence
  from regression (SKILL.md L1025; landed by T05.01 / D-0054 and
  ratified by T05.02 / D-0055).
- The wrapper-level precedence statement "regression always exits
  BEFORE monotonicity" (SKILL.md L1018, L1021, L1059).
- The hard-cap fallback reference to `rf-team-lead.md:417` (SKILL.md
  L1016 and L1056).

T05.05 therefore makes **zero source-file edits**. Its deliverable is the
quality-engineer sub-agent report that ratifies the four acceptance
criteria byte-for-byte against the landed SKILL.md text and the
preserved `rf-team-lead.md:417` and `rf-task-builder.md:354-364` slices.

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| FR-CONV.5 wrapper (T05.01 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L1014-1027 | Houses the precedence rule statement (L1021) cross-referenced by Step 4 of the ratification |
| API-004 contract block (T05.02 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L1029-1059 | Houses the F-set definition (L1042-1048) and 4-step ordering rule (L1050-1059) — the two artifacts that T05.05 ratifies |
| INV-012 composition note (T05.01 baseline) | `src/superclaude/skills/task-builder/SKILL.md` L1025 | Wires synthetic-dnsp findings into `|F_n|` and excludes same-dedup-key cross-cycle persistence from regression |
| 3-cycle hard cap (preserved end-to-end) | `src/superclaude/agents/rf-team-lead.md` L417 | Step 3 of the 4-step rule references this as the global backstop |
| Per-gate counter table (preserved end-to-end) | `src/superclaude/agents/rf-task-builder.md` L354-364 | Step 3 of the 4-step rule references this for gate-specific caps |
| Roadmap items | `.dev/releases/current/task-builder-merge/tasklist-index.md` L170-L171, L315 | R-094, R-095 ID-to-deliverable mapping and STRICT tier |
| T05.04 evidence (immediate predecessor) | `.dev/releases/current/task-builder-merge/artifacts/D-0057/evidence.md` | Section 2 demonstrates "regression always exits BEFORE monotonicity" empirically; T05.05 ratifies it textually |
| T05.03 evidence | `.dev/releases/current/task-builder-merge/artifacts/D-0056/evidence.md` | Demonstrates monotonicity emitter; the same ordering rule governs both halts |

## 3. F-set identity (R-094 — ratified verbatim)

The F-set definition lives at SKILL.md L1042-1048 (quoted verbatim
in `evidence.md` §2). Three properties are pinned:

1. **F_n is a SET, not a multiset.** Two failures sharing a dedup-key
   collapse to one element BEFORE the monotonicity comparison is
   computed. This is the post-dedup cardinality rule that the
   monotonicity step (Step 2) operates on.
2. **Item identity = dedup-key.** Two identity domains are defined:
   - Ordinary checklist items: dedup-key = item ID (e.g., `3.2`).
   - Synthetic-dnsp findings (PR-03): dedup-key =
     `(assigned_files_range, escalation_ladder_exhaust_point)`.
3. **Regression check uses the SAME dedup-key identity.** A synthetic-
   dnsp finding with an identical dedup-key re-emitted on cycle `n+1`
   is NOT a regression (the prior verdict was FAIL, not PASS); it is
   the INV-012 cross-cycle dedup case. T05.07 / D-0059 will operationally
   wire this for synthetic-dnsp finding ingestion.

## 4. 4-step ordering rule (R-095 — ratified verbatim)

The 4-step ordering rule lives at SKILL.md L1050-1059. Strict ordering
applies per cycle transition `n → n+1`; EXIT on the first match:

| Step | SKILL.md line | Check | Emit on HALT |
|------|---------------|-------|--------------|
| 1 | L1054 | Regression: `PASS_n ∩ FAIL_{n+1}` (by dedup-key) non-empty | byte-exact regression halt-message (API-004 L1038) |
| 2 | L1055 | Monotonicity: `|F_n| > 0` AND `|F_{n+1}| >= |F_n|` (post-dedup) | byte-exact `[HALT-MONOTONICITY] |F|=<n>` (API-004 L1037) |
| 3 | L1056 | Hard-cap: per-gate counter reached gate-specific cap (rf-task-builder.md:354-364 table) with global backstop at rf-team-lead.md:417 | HALT per gate escalation path (HALT-and-escalate or Open Questions) |
| 4 | L1057 | Proceed: re-spawn cycle `n+1` | (no halt) |

The strict ordering invariant at SKILL.md L1059 ("regression ALWAYS
exits BEFORE monotonicity; monotonicity ALWAYS exits BEFORE hard-cap;
hard-cap ALWAYS exits BEFORE proceed") binds producers (must not
reorder or skip steps) and consumers (fixture asserts must verify
ordering by emission ordering in the execution log).

## 5. INV-012 composition wiring (textual ratification at L1025)

SKILL.md L1025 states:

- Synthetic-dnsp findings COUNT as failures for the `|F_n|`
  monotonicity comparison — they are real, citable evidence items.
- A synthetic finding with the same `(assigned_files_range,
  escalation_ladder_exhaust_point)` dedup key appearing across
  consecutive cycles is a DEDUP case, NOT a regression — the same
  partition failed the same way twice.
- The regression-detection logic MUST compare by dedup key, not by
  raw finding count, when synthetic-dnsp items are involved.
- Two synthetic findings with identical dedup keys collapse into one
  with a "found N times" note (cf. PR-03 dedup behavior).

T05.05 ratifies this composition rule textually. T05.07 (D-0059) will
wire the runtime composition (cross-cycle dedup-key tracking) and run
the canonical cross-cycle dedup fixture (TEST-022 / D-0065).

## 6. Acceptance criteria coverage

| AC | Statement (verbatim from T05.05) | Where verified |
|----|-----------------------------------|----------------|
| AC1 | Documented precedence text explicitly states the 4-step order `regression → monotonicity → hard-cap → proceed` (regex match on the ordered string in SKILL.md) and sub-agent report confirms "regression always exits BEFORE monotonicity" | Quality-engineer sub-agent report — AC1 + AC1b sections (`evidence.md` §3 + §4); SKILL.md L1021 + L1052 (ordered string regex match); SKILL.md L1018 + L1021 + L1059 ("regression ALWAYS exits BEFORE monotonicity") |
| AC2 | F-set identity (dedup-key) explicitly stated in SKILL.md | Sub-agent AC2 (`evidence.md` §5); SKILL.md L1042-1048 quoted verbatim for both ordinary checklist items and synthetic-dnsp findings |
| AC3 | Existing rf-team-lead.md:417 hard-cap referenced as fallback | Sub-agent AC3 (`evidence.md` §6); SKILL.md L1016 ("the existing 3-cycle hard cap at `rf-team-lead.md:417` is preserved as the fourth-precedence backstop") + L1056 ("with the global 3-cycle backstop at `rf-team-lead.md:417`"); rf-team-lead.md:417 itself byte-identical (sha256 `51725c0f…`) |
| AC4 | Sub-agent quality-engineer report confirms 4-step ordering verbatim | Sub-agent AC4 (`evidence.md` §7); four steps quoted byte-for-byte from SKILL.md L1054, L1055, L1056, L1057, plus L1059 invariant |

All four ACs PASS. Sub-agent overall verdict: PASS.

## 7. Preservation invariants (carried from T05.01..T05.04)

T05.05 makes ZERO edits to any source file. The following hashes
recorded in D-0054 / D-0055 / D-0056 / D-0057 remain unchanged:

| Slice | sha256 |
|---|---|
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — T05.01 baseline) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` |
| `SKILL.md` L1029-1059 (API-004 contract block — T05.02 baseline; includes F-set L1042-1048 and 4-step rule L1050-1059) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` |
| `rf-team-lead.md:417` (3-cycle hard cap — preserved end-to-end) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` |

The four independent retry counters (RESEARCH_NEEDED, MALFORMED,
research-gate gap-fill, per-gate fix cycles) and the global 3-cycle
hard cap at `rf-team-lead.md:417` are PRESERVED end-to-end. `make
verify-sync` PASS.

## 8. Dependencies and cross-references

- **Dependencies:** T05.03 (D-0056, monotonicity emitter) and T05.04
  (D-0057, regression emitter). Both emitters operate against the
  4-step ordering rule that T05.05 ratifies; T05.04 §2 of evidence
  already demonstrated empirically that the regression step exits
  BEFORE the monotonicity step on the PASS@1/FAIL@2 fixture; T05.05
  ratifies the same property textually for the protocol-level rule.
- **Unblocks:** T05.06 (CP-P05-T01-T05 mid-phase checkpoint),
  T05.07 (D-0059, INV-012 cross-cycle dedup composition — uses
  the dedup-key identity ratified here for synthetic-dnsp finding
  bookkeeping).
- **Wire ABI invariant:** The 4-step ordering rule is the consumer-side
  invariant for API-004-M5. Fixture asserts (TEST-015 / TEST-016 at
  T05.13, TEST-022 at T05.14) verify ordering by emission ordering in
  the execution log — exactly as L1059 mandates.

## 9. Rollback

Per roadmap R-094 / R-095 rollback note: the F-set definition and
4-step ordering rule are the protocol-level scaffolding the FR-CONV.5
wrapper depends on. Rollback aligns with the wrapper rollback policy
(T05.01 / D-0054): disable guards individually by removing or
short-circuiting the relevant step(s) in the 4-step rule. The per-gate
caps continue to govern fix-cycle escalation via the preserved
`rf-team-lead.md:417` hard cap and the per-gate counter table at
`rf-task-builder.md:354-364`.
