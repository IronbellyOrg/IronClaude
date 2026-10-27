# D-0033 — T03.09 Spec: COMP-001-M3 SKILL.md A.10.5 Spawn Injection

**Task:** T03.09 (Phase 3)
**Roadmap items:** R-061
**Date:** 2026-05-17
**Edit-site component:** COMP-001-M3

---

## 1. Scope

T03.09 lands the `## Inherited Structural Verdict` block inside the
rf-qa-qualitative spawn-prompt template in `SKILL.md §A.10.5`. The block
header MUST sit **after** TARGET FILES + PROJECT CONVENTIONS and
**before** ADVERSARIAL STANCE + INSTRUCTIONS (R-061 placement
constraint, mirroring API-002 wire-contract from D-0028).

Phase-3-tasklist.md L406-453 cites the target line range as
`[923, 1000]` (with `~:966` as the nominal insertion line). That range
was authored against an earlier SKILL.md state. The file has since
grown to 2054 lines (MIG-002 Execution Context header landed at commit
`2648be8` added ~150 lines around L744-960). The structural intent of
R-061 — block-in-A.10.5, after TARGET FILES, before INSTRUCTIONS — is
the binding constraint; the literal `[923, 1000]` byte-offsets are
documentation-only drift (see D-0026 §4 for the precedent).

## 2. Landed state

| Item | Current line | Range claim in phase file | Drift? |
|---|---|---|---|
| Directive paragraph (`**Inherited Structural Verdict (PR-04 ...)**`) | 1101 | 923-1000 | yes (drift, +178 / +101) |
| Heading (`## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)`) | 1128 | 923-1000 (target ~966) | yes (drift, +162) |
| TARGET FILES (verify ALL ...) | 1112 | n/a | n/a |
| PROJECT CONVENTIONS: | 1115 | n/a | n/a |
| INSTRUCTIONS: | 1153 | n/a | n/a |

Ordering inside the spawn-prompt template:

```
1112  TARGET FILES (verify ALL — no spot-checking):
1115  PROJECT CONVENTIONS:
1128  ## Inherited Structural Verdict (rf-qa A.10 output — DO NOT re-verify)
1150  **ADVERSARIAL STANCE:** ...
1153  INSTRUCTIONS:
```

`1112 < 1115 < 1128 < 1150 < 1153` → the structural intent
("after TARGET FILES, before INSTRUCTIONS") is satisfied.

## 3. Implementation provenance

The block was originally inserted by:

- **Commit `3a57a0d`** — `feat(task-builder): PR-04 gate-results
  passthrough (inherited structural verdict)` (T03.01 / D-0026 wrapper
  landing).
- **T03.03 / D-0028** validated the splice position against the API-002
  wire contract.

T03.09 is the COMP-001-M3 edit-site verification — it confirms the
block is structurally where it must be inside A.10.5 and that the
[923, 1000] phase-file range is documentation drift, not an
implementation gap. No new edits to SKILL.md are required: the
landed-and-verified block from `3a57a0d` already satisfies R-061's
structural constraint.

## 4. Rollback

Same rollback path as FR-CONV.3 (R-061 inherits parent rollback):
disable passthrough flag and fall back to standalone rf-qa-qualitative.
The single commit `3a57a0d` plus the relocation hunks from T03.03 can
be `git revert`ed in order if the M3 wrapper is rolled back wholesale.

## 5. Phase-file housekeeping recommendation

A follow-up cosmetic edit to `phase-3-tasklist.md` could refresh the
`[923, 1000]` line citation to `[1090, 1200]` (covering A.10.5 in the
current file). This is documentation hygiene only and does not block
T03.09 acceptance — the structural intent is the binding constraint.
