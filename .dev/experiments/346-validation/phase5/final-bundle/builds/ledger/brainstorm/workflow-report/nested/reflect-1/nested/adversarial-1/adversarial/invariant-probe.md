# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent opus fault-finder; probed the emerging consensus against the plan, the spec, the repo tests and the S1 briefs. Nothing written, no tests run.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | Verbatim review briefs (plan :22) plus the revert consent (:23) let a reviewer run the ledger | UNADDRESSED | HIGH | T05/T07/T09 say "write ONLY your output file", "no edits to the spec or any other file"; `init`/`find`/`begin`/`verify` write ledger.json, snapshots/, diffs/, inputs/, plan-r<k>.md (plan :37, :61) and `begin --revert-unclaimed` edits the spec; Precedence bullet "a brief may narrow this scope" (source.md:104) lets the brief win, so the replicate fails V1-ledger (source.md:155); the consent decision covers only the revert |
| INV-002 | interaction_effects | One skip predicate (review-1 PASS + document unchanged) fixes C-002 | UNADDRESSED | HIGH | `close` writes `verdict: PASS` right after `find` (plan :44) when the document cannot yet have changed; the T06 reviser always runs after review 1 (plan :171); the report then says PASS while `verdict` would return 12; `sweep --prepare` copies the accepted snapshot r1.md (:91), so edited text is never swept; the fix must say where the predicate is evaluated, what `close` writes and what the sweep copies |
| INV-003 | sufficiency_challenge | Adding banned-phrase and cap checks to the command test is enough for C-004 | UNADDRESSED | MEDIUM | once committed, every tracked-file scan applies (test_review_severity_rule.py:28 `_SCAN_TREES`), incl. site-sweep phrases and F1-F6 fix-loop patterns (:390, :398-405, :448-450) and the zero-tolerance check (:506-508); plan :26 covers only two |
| INV-004 | sufficiency_challenge | The variant changes nothing about the reviser beyond the three recorded differences (source.md:148) | UNADDRESSED | MEDIUM | spec-panel.md:263 Reviser brief restates "add no rule, mechanism or section…", finding-id citation and byte size before/after; the script tail is only "Reviser brief listing only blocking row ids" (plan :44) and source.md:103 drops these rules: a fourth undeclared treatment difference; spec-origin, owner note |
| INV-005 | guard_conditions | The eight bullets keep every applicable guard of the old Review Loop | UNADDRESSED | MEDIUM | spec-panel.md:261 "every run is one review whatever `--iterations` says", "skips the Improve step and writes no revised specification"; Improve step copied (spec-panel.md:35); Usage keeps `--iterations N` (plan :124); Cap bullet carries neither guard |
| INV-006 | guard_conditions | S1's fixed five dispatches still fit an early loop end | UNADDRESSED | MEDIUM | after a review-1/2 PASS or ESCALATE, T06-T09 still dispatch (plan :170-171); later `begin` gets E-TERMINAL and "a refusal stops the run" (source.md:97); INSTALL.md (plan :197-203) gives no skip rule |
| INV-007 | guard_conditions | E-REPORT-EDITED is a safe refusal | UNADDRESSED | MEDIUM | briefs say "stub the output file first and fill it section by section" and T05 "then add a numbered findings list"; tail must be last (source.md:60), `begin` refuses an edited tail (plan :78); no recovery; failure result 5 (source.md:190) |
| INV-008 | count_divergence | A-F10 (U3 double count) was rightly dropped | UNADDRESSED | MEDIUM | literal plan :93 U3 includes deferred, outside and sweep rows; on the :99 fixture U3 = 3 = headline_raw, making "U3 alone is the analogue of Arm B" (source.md:163) meaningless; :163 covers duplicate defects across sets, not one row in several sets; no AC tests U3 |
| INV-009 | count_divergence | Sweep challenges counted once in headline_raw | UNADDRESSED | LOW | plan :93 "plus sweep challenges"; a challenge stored as a sweep row (:95) counts twice; storage undefined |
| INV-010 | state_variables | Every verifier answer maps to a defined status | UNADDRESSED | MEDIUM | plan :77 maps only `resolved` and `open`; `regressed` and `cannot-verify` have no target (source.md:38); `resolved` on an untouched `open` row has no defined refusal |
| INV-011 | state_variables | The reviser can call `answer`/`revert-unclaimed` on hunks | UNADDRESSED | MEDIUM | hunks and the unclaimed set are computed at the next `begin` (plan :61, source.md:25); `answer` (:62) and `--hunk k` (:63) run before it; phase values never listed (:38) |
| INV-012 | state_variables | round, fix_cycles and review counters are consistent | UNADDRESSED | LOW | three counters with no stated relation (plan :38, :46); zero-hunk round "counts as a review" (:68) |
| INV-013 | collection_boundaries | "Enclosing paragraph" and the diff are well defined for the S1 spec | UNADDRESSED | MEDIUM | paragraph undefined (plan :61); a blank-line paragraph makes a whole table one unit (source.md:207, :237); merged-requirements.md:83 (difflib autojunk off) and :478 (`HUNKS_LARGE`) absent from the plan |
| INV-014 | guard_conditions | Pinning spawn + heartbeat fixes C-007 | UNADDRESSED | LOW | sweep takes ~10-15 min (source.md:200); a smoke check finishing under 5 minutes passes trivially (source.md:144) |
| INV-015 | guard_conditions | The sweep context never sees the ledger | UNADDRESSED | LOW | in `--sweep` mode one session runs `--prepare` and `--input` (plan :125, source.md:116) and every call prints counts/next_action (:46); only a cited row id is detected (source.md:155) |
| INV-016 | interaction_effects | Rewriting line 220 (C-001) fits the drift test | ADDRESSED | LOW | fix adds line 220 to the drift exclusions (plan :145, :127; source.md:125); harmless for S1 (spec input, not TDD) |
| INV-017 | interaction_effects | The owner's C-005 fix fits "additive only" | ADDRESSED | LOW | any fix edits a frozen-package test (test_routing_refresh.py:29-33, :647-648) against plan :15 / source.md:79; Constraints must list it; owner routing agreed |
| INV-018 | interaction_effects | The C-002 predicate conflicts with the owner headline decision | ADDRESSED | LOW | no conflict; headline is reporting only (plan :21) |
| INV-019 | collection_boundaries | The fourth-`begin` refusal is deterministic | ADDRESSED | LOW | E-CAP/E-TERMINAL order to be pinned (C-006); Task 3 E-TERMINAL test must use a ledger ended at review 2 |
| INV-020 | collection_boundaries | Appending to the frontmatter description is mechanical | UNADDRESSED | LOW | spec-panel.md:3 description is a quoted YAML string; plan :123 does not say the suffix goes inside the quotes |
| INV-021 | sufficiency_challenge | The kept body text suits the variant | UNADDRESSED | LOW | title `# /sc:spec-panel` (spec-panel.md:10) and examples (:406-436) name the original command and stay byte-identical (plan :127) |

## Summary

- **Total findings**: 21
- **ADDRESSED**: 4
- **UNADDRESSED**: 17
  - HIGH: 2 (INV-001, INV-002)
  - MEDIUM: 9 (INV-003, INV-004, INV-005, INV-006, INV-007, INV-008, INV-010, INV-011, INV-013)
  - LOW: 6 (INV-009, INV-012, INV-014, INV-015, INV-020, INV-021)

Sufficiency challenge (category 6): the consensus fixes alone would not make the plan pass a strict per-task review; INV-001, INV-002, INV-003 and INV-006 each falsify that.

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002
These invariant violations must be resolved before convergence can be declared.
WARNING: 9 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-003, INV-004, INV-005, INV-006, INV-007, INV-008, INV-010, INV-011, INV-013
